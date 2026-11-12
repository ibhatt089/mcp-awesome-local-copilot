# MCP Server: Markdown to HTML

This MCP server converts Markdown text to HTML.

It runs locally over stdio through [`dnx`](https://learn.microsoft.com/dotnet/core/tools/dotnet-tool-exec), which downloads the `Ibhatt089.McpSamples.MarkdownToHtml` package from nuget.org on first run. Docker is not required.

## Prerequisites

- [.NET 10 SDK](https://dotnet.microsoft.com/download/dotnet/10.0) (provides `dnx`). No admin rights needed: see the repo README for a per-user install.

## Install

[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect?url=vscode%3Amcp%2Finstall%3F%7B%22name%22%3A%22markdown-to-html%22%2C%22gallery%22%3Afalse%2C%22command%22%3A%22dnx%22%2C%22args%22%3A%5B%22Ibhatt089.McpSamples.MarkdownToHtml%22%2C%22--yes%22%5D%7D) [![Install in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect?url=vscode-insiders%3Amcp%2Finstall%3F%7B%22name%22%3A%22markdown-to-html%22%2C%22gallery%22%3Afalse%2C%22command%22%3A%22dnx%22%2C%22args%22%3A%5B%22Ibhatt089.McpSamples.MarkdownToHtml%22%2C%22--yes%22%5D%7D)

Or add this to your MCP client config (Cursor `~/.cursor/mcp.json`, Claude Code `.mcp.json`):

```json
{
  "mcpServers": {
    "markdown-to-html": {
      "command": "dnx",
      "args": [
        "Ibhatt089.McpSamples.MarkdownToHtml",
        "--yes"
      ]
    }
  }
}
```

To get all four servers at once, install the [plugin](https://github.com/ibhatt089/mcp-awesome-local-copilot#install).

## What's included

| Building Block | Name                       | Description                         |
|----------------|----------------------------|-------------------------------------|
| Tools          | `convert_markdown_to_html` | Converts a Markdown document to HTML. |

## Options

Pass these after `--` in `args`, for example `["Ibhatt089.McpSamples.MarkdownToHtml", "--yes", "--", "-tc", "-p", "--tags", "p,h1,h2,h3,ol,ul"]`:

- `--tech-community` / `-tc`: produce HTML for Microsoft Tech Community.
- `--extra-paragraph` / `-p`: add an extra paragraph between the elements listed in `--tags`.
- `--tags`: comma-delimited tags that get the extra paragraph. Tech Community formatting is only applied when this is set.

## Run from source

```bash
dotnet run --project ./src/McpSamples.MarkdownToHtml.HybridApp            # stdio
dotnet run --project ./src/McpSamples.MarkdownToHtml.HybridApp -- --http  # streamable HTTP
```

`.vscode/mcp.stdio.local.json` and `.vscode/mcp.http.local.json` in this folder connect VS Code to a server run from source.
