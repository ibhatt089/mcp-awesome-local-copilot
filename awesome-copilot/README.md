# MCP Server: Awesome Copilot

This MCP server retrieves GitHub Copilot customizations from the [awesome-copilot](https://github.com/github/awesome-copilot) repository.

It runs locally over stdio through [`dnx`](https://learn.microsoft.com/dotnet/core/tools/dotnet-tool-exec), which downloads the `Ibhatt089.McpSamples.AwesomeCopilot` package from nuget.org on first run. Docker is not required.

## Prerequisites

- [.NET 10 SDK](https://dotnet.microsoft.com/download/dotnet/10.0) (provides `dnx`). No admin rights needed: see the repo README for a per-user install.

## Install

[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect?url=vscode%3Amcp%2Finstall%3F%7B%22name%22%3A%22awesome-copilot%22%2C%22gallery%22%3Afalse%2C%22command%22%3A%22dnx%22%2C%22args%22%3A%5B%22Ibhatt089.McpSamples.AwesomeCopilot%22%2C%22--yes%22%5D%7D) [![Install in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect?url=vscode-insiders%3Amcp%2Finstall%3F%7B%22name%22%3A%22awesome-copilot%22%2C%22gallery%22%3Afalse%2C%22command%22%3A%22dnx%22%2C%22args%22%3A%5B%22Ibhatt089.McpSamples.AwesomeCopilot%22%2C%22--yes%22%5D%7D)

Or add this to your MCP client config (Cursor `~/.cursor/mcp.json`, Claude Code `.mcp.json`):

```json
{
  "mcpServers": {
    "awesome-copilot": {
      "command": "dnx",
      "args": [
        "Ibhatt089.McpSamples.AwesomeCopilot",
        "--yes"
      ]
    }
  }
}
```

To get all four servers at once, install the [plugin](https://github.com/ibhatt089/mcp-awesome-local-copilot#install).

## What's included

| Building Block | Name                  | Description                                                                                                             |
|----------------|-----------------------|-------------------------------------------------------------------------------------------------------------------------|
| Tools          | `search_instructions` | Searches agents, hooks, instructions, prompts, skills, and workflows by keywords in their names and descriptions.        |
| Tools          | `load_instruction`    | Loads a custom instruction, agent, hook, prompt, skill, or workflow from the repository.                                |
| Prompts        | `get_search_prompt`   | Gets a prompt for searching Copilot instructions.                                                                       |

## Refreshing the search index

The search index is `src/McpSamples.AwesomeCopilot.HybridApp/metadata.json` and ships inside the package. To rebuild it from a local checkout of awesome-copilot:

```bash
cd awesome-copilot
git clone --depth 1 https://github.com/github/awesome-copilot src/awesome-copilot
dotnet run ./update-metadata.cs
```

## Run from source

```bash
dotnet run --project ./src/McpSamples.AwesomeCopilot.HybridApp            # stdio
dotnet run --project ./src/McpSamples.AwesomeCopilot.HybridApp -- --http  # streamable HTTP
```

`.vscode/mcp.stdio.local.json` and `.vscode/mcp.http.local.json` in this folder connect VS Code to a server run from source.
