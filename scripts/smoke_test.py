"""Launch each packed MCP server through dnx and check it completes the stdio handshake.

Usage: python scripts/smoke_test.py <feed-dir>
"""

import json
import os
import subprocess
import sys
import tempfile

SERVERS = {
    "Ibhatt089.McpSamples.AwesomeCopilot": ("search_instructions", {"keywords": "csharp"}),
    "Ibhatt089.McpSamples.MarkdownToHtml": ("convert_markdown_to_html", {"markdown": "# Hi"}),
    "Ibhatt089.McpSamples.OutlookEmail": None,
    "Ibhatt089.McpSamples.TodoList": ("add_todo_item", {"todoItemText": "smoke"}),
}


def check(package: str, call, feed: str, cache: str) -> None:
    env = dict(os.environ, NUGET_PACKAGES=cache)
    proc = subprocess.Popen(
        ["dnx", package, "--yes", "--add-source", feed],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True, env=env, shell=(os.name == "nt"),
    )

    def send(message):
        proc.stdin.write(json.dumps(message) + "\n")
        proc.stdin.flush()

    def receive(want_id):
        while True:
            line = proc.stdout.readline()
            if not line:
                raise RuntimeError(f"{package}: server exited. stderr:\n{proc.stderr.read()[-4000:]}")
            try:
                message = json.loads(line)
            except json.JSONDecodeError:
                # dnx prints this for unsigned local packages before the server starts.
                if "signature verification" in line:
                    continue
                raise RuntimeError(f"{package}: non-JSON on stdout: {line.rstrip()}")
            if message.get("id") == want_id:
                return message

    try:
        send({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
            "protocolVersion": "2025-06-18", "capabilities": {},
            "clientInfo": {"name": "smoke-test", "version": "1"}}})
        receive(1)
        send({"jsonrpc": "2.0", "method": "notifications/initialized"})
        send({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
        tools = [t["name"] for t in receive(2)["result"]["tools"]]
        if not tools:
            raise RuntimeError(f"{package}: no tools listed")
        if call:
            send({"jsonrpc": "2.0", "id": 3, "method": "tools/call",
                  "params": {"name": call[0], "arguments": call[1]}})
            result = receive(3)["result"]
            if result.get("isError"):
                raise RuntimeError(f"{package}: {call[0]} failed: {result}")
        print(f"ok  {package}  tools={tools}")
    finally:
        proc.kill()


def main() -> int:
    feed = os.path.abspath(sys.argv[1])
    with tempfile.TemporaryDirectory() as cache:
        for package, call in SERVERS.items():
            check(package, call, feed, cache)
    return 0


if __name__ == "__main__":
    sys.exit(main())
