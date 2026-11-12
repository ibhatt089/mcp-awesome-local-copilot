# MCP Awesome Local Copilot

Four .NET [Model Context Protocol](https://modelcontextprotocol.io/) servers packaged as a plugin for **Cursor**, **Claude Code**, and **VS Code / GitHub Copilot**. Every server runs locally over stdio through `dnx`. **No Docker, no containers, no Azure.**

Based on [microsoft/mcp-dotnet-samples](https://github.com/microsoft/mcp-dotnet-samples) (MIT). The Docker images, Azure Container Apps, Azure Functions, and API Management deployments were removed. Each server is published to nuget.org as a .NET tool instead.

## Servers

| Server | NuGet package | What it does |
|--------|---------------|--------------|
| [Awesome Copilot](./awesome-copilot/) | `Ibhatt089.McpSamples.AwesomeCopilot` | Searches and loads GitHub Copilot customizations from [awesome-copilot](https://github.com/github/awesome-copilot). |
| [Markdown to HTML](./markdown-to-html/) | `Ibhatt089.McpSamples.MarkdownToHtml` | Converts Markdown to HTML. |
| [Outlook Email](./outlook-email/) | `Ibhatt089.McpSamples.OutlookEmail` | Sends email through Microsoft Graph. Needs Entra ID credentials. |
| [Todo List](./todo-list/) | `Ibhatt089.McpSamples.TodoList` | Manages an in-memory todo list. |

## Prerequisite: .NET 10 SDK

`dnx` ships with the .NET 10 SDK. It downloads each server package from nuget.org on first run and caches it, like `npx` does for npm.

If you can't run an installer, install the SDK per-user without admin rights:

```bash
# macOS / Linux
curl -sSL https://dot.net/v1/dotnet-install.sh | bash -s -- --channel 10.0
export PATH="$HOME/.dotnet:$PATH"   # add to your shell profile
```

```powershell
# Windows
& ([scriptblock]::Create((irm https://dot.net/v1/dotnet-install.ps1))) -Channel 10.0
# Adds %LOCALAPPDATA%\Microsoft\dotnet; put it on your user PATH
```

Check with `dnx --help`. If your editor can't find `dnx`, restart it from a shell where `dnx` works, or replace `"command": "dnx"` with its absolute path.

Machines behind a NuGet proxy or private feed: `dnx` honors your `NuGet.config`, so mirror the four packages there.

## Install

### Cursor

```bash
git clone https://github.com/ibhatt089/mcp-awesome-local-copilot ~/.cursor/plugins/local/mcp-awesome-local-copilot
```

Restart Cursor. The four servers appear under **Settings → MCP**.

### Claude Code

```text
/plugin marketplace add ibhatt089/mcp-awesome-local-copilot
/plugin install mcp-awesome-local-copilot@mcp-awesome-local-copilot
```

### VS Code / GitHub Copilot

Clone the repo and open it in VS Code. `.vscode/mcp.json` registers all four servers and prompts for the Outlook credentials. To add a single server to your user profile, use the install buttons in that server's README.

### Any other MCP client

Use `dnx <package> --yes` as the stdio command, for example:

```json
{
  "mcpServers": {
    "todo-list": { "command": "dnx", "args": ["Ibhatt089.McpSamples.TodoList", "--yes"] }
  }
}
```

## Outlook Email credentials

The `outlook-email` server reads `EntraId__TenantId`, `EntraId__ClientId`, and `EntraId__ClientSecret` from its environment. Without them the server starts, but `send_email` fails. If you don't need email, disable that server in your client. See [outlook-email/README.md](./outlook-email/README.md) for setup and security notes.

## Repository layout

```text
.cursor-plugin/plugin.json      Cursor plugin manifest
.claude-plugin/plugin.json      Claude Code plugin manifest
.claude-plugin/marketplace.json Claude Code marketplace (this repo is its own marketplace)
.mcp.json                       MCP servers shared by the Cursor and Claude Code plugins
.vscode/mcp.json                MCP servers for VS Code
shared/                         Shared MCP host code
<sample>/src/                   Server source; <sample>/src/*/.mcp/server.json is the MCP registry metadata
.github/workflows/              Build/test and NuGet publish
```

## Build and test locally

```bash
for p in */src/*/*.HybridApp.csproj; do dotnet pack "$p" -c Release -o ./artifacts; done
dnx Ibhatt089.McpSamples.TodoList --yes --add-source ./artifacts
```

## Publish a release

1. Add a nuget.org API key as the repository secret `NUGET_API_KEY`.
2. Bump `version` in `.cursor-plugin/plugin.json`, `.claude-plugin/plugin.json`, and `.claude-plugin/marketplace.json`.
3. Push a tag such as `v1.0.1`. The `publish` workflow stamps that version into each `.mcp/server.json` and package, runs the smoke test, pushes to nuget.org, and attaches the `.nupkg` files to a GitHub release.

## License

MIT. See [LICENSE](./LICENSE). This project is not affiliated with or endorsed by Microsoft.
