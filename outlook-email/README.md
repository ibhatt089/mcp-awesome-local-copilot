# MCP Server: Outlook Email

This MCP server sends email through Outlook using Microsoft Graph.

It runs locally over stdio through [`dnx`](https://learn.microsoft.com/dotnet/core/tools/dotnet-tool-exec), which downloads the `Ibhatt089.McpSamples.OutlookEmail` package from nuget.org on first run. Docker is not required.

## Prerequisites

- [.NET 10 SDK](https://dotnet.microsoft.com/download/dotnet/10.0) (provides `dnx`). No admin rights needed: see the repo README for a per-user install.

## Install

[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect?url=vscode%3Amcp%2Finstall%3F%7B%22name%22%3A%22outlook-email%22%2C%22gallery%22%3Afalse%2C%22command%22%3A%22dnx%22%2C%22args%22%3A%5B%22Ibhatt089.McpSamples.OutlookEmail%22%2C%22--yes%22%5D%7D) [![Install in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect?url=vscode-insiders%3Amcp%2Finstall%3F%7B%22name%22%3A%22outlook-email%22%2C%22gallery%22%3Afalse%2C%22command%22%3A%22dnx%22%2C%22args%22%3A%5B%22Ibhatt089.McpSamples.OutlookEmail%22%2C%22--yes%22%5D%7D)

Or add this to your MCP client config (Cursor `~/.cursor/mcp.json`, Claude Code `.mcp.json`):

```json
{
  "mcpServers": {
    "outlook-email": {
      "command": "dnx",
      "args": [
        "Ibhatt089.McpSamples.OutlookEmail",
        "--yes"
      ]
    }
  }
}
```

To get all four servers at once, install the [plugin](https://github.com/ibhatt089/mcp-awesome-local-copilot#install).

## What's included

| Building Block | Name         | Description                   |
|----------------|--------------|-------------------------------|
| Tools          | `send_email` | Sends an email to recipients. |

## Security considerations

> [!WARNING]
> `register-app.sh` and `Register-App.ps1` request the Microsoft Graph `Mail.Send` **application** permission and try to grant tenant-wide admin consent. That permission lets the app send mail as any mailbox in the tenant. Review it with your tenant admin and apply mailbox-level restrictions where your policy requires them. Treat the generated client secret as a credential: never commit it or put it in logs.

## Credentials

The server reads three environment variables:

| Variable                | Value                              |
|-------------------------|------------------------------------|
| `EntraId__TenantId`     | Entra ID tenant ID                 |
| `EntraId__ClientId`     | Application (client) ID            |
| `EntraId__ClientSecret` | Client secret                      |

To create an app registration (requires the Azure CLI and admin consent rights):

```bash
./register-app.sh            # bash/zsh
./Register-App.ps1           # PowerShell
```

- **VS Code** prompts for all three values when the server first starts (see `.vscode/mcp.json` at the repo root).
- **Cursor and Claude Code** pass your environment to the server. Export the three variables in your shell profile before starting the editor, or add an `env` block to the server entry in your own MCP config.

## Run from source

```bash
dotnet run --project ./src/McpSamples.OutlookEmail.HybridApp            # stdio
dotnet run --project ./src/McpSamples.OutlookEmail.HybridApp -- --http  # streamable HTTP
```

`.vscode/mcp.stdio.local.json` and `.vscode/mcp.http.local.json` in this folder connect VS Code to a server run from source.
