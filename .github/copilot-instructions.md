# Copilot Instructions (Concise) – MCP Awesome Local Copilot

Purpose: Make agents instantly productive. Follow ONLY patterns proven in this repo; don’t invent abstractions.

## Architecture & Runtime
- Mono-repo of independent Hybrid MCP servers: `awesome-copilot/`, `markdown-to-html/`, `todo-list/`, `outlook-email/` + shared lib `shared/McpSamples.Shared/`.
- Hybrid pattern: same `Program.cs` can run STDIO (default) or stateless HTTP when `-- http` (or env `UseHttp=true`). Selection via `AppSettings.UseStreamableHttp(...)`; final wiring through `BuildApp(useStreamableHttp)`.
- Discovery: Tools / Prompts / Resources auto-registered by assembly scan (`With*FromAssembly`). New public attributed types in the entry assembly just work—avoid manual registration.
- HTTP mode: single POST `/mcp`; some samples add dual OpenAPI docs (swagger 2.0 + openapi 3.0) via `McpDocumentTransformer<T>`.

## Sample-Specific Nuance
- awesome-copilot: Large `metadata.json`; reuse `IMetadataService` (don’t repeatedly load whole file). Tools: search & load instructions.
- markdown-to-html: Extra switches `-tc`, `-p`, `--tags` only parsed AFTER `--` delimiter.
- todo-list: In‑memory SQLite kept alive by one singleton `SqliteConnection`; use EF Core set-based ops (`ExecuteUpdateAsync/ExecuteDeleteAsync`).
- outlook-email: Supports auth parameters (`--tenant-id/-t`, `--client-id/-c`, `--client-secret/-s`) or `EntraId__TenantId` / `EntraId__ClientId` / `EntraId__ClientSecret` env vars (preferred for plugins). Only add auth handling inside this sample—do not leak to shared.

## Core Conventions
- Target: .NET 10; nullable + implicit usings enabled globally.
- Entry project path pattern: `./<sample>/src/<PascalName>.HybridApp/`.
- Always preserve argument delimiter: `dotnet run … -- --http <other-switches>`.
- JSON camelCase & case-insensitive (match existing config); prefer `System.Text.Json`.
- No Docker or Azure deployment. Distribution is NuGet + `dnx`. In stdio mode only JSON-RPC may go to stdout. Local HTTP dev ports: ac=5250, todo=5240, html=5280, outlook=5260.

## Adding / Modifying Tools
- Create public class or method with `[McpServerTool]` (and `[Description]` for method + parameters). Return lightweight DTO / primitives; let host format.
- For prompts use `[McpServerPrompt]`. No manual DI registration unless you need extra services—then add via `builder.Services` before `BuildApp`.

## Safe Editing Rules
- Don’t change signatures of shared extension methods (`AddAppSettings<T>`, `BuildApp`) unless updating EVERY sample in one PR.
- Don’t introduce persistence in other samples without isolating it; never move sample-only concerns into `shared` casually.
- When touching `awesome-copilot` metadata handling, avoid O(n) reload loops—stream or cache.

## Frequent Pitfalls (avoid silently breaking)
- Missing `--` causes custom flags ignored.
- Forgetting singleton SQLite => empty todo DB each request.
- Adding OpenAPI without mapping json endpoints or `AddHttpContextAccessor()` => docs missing.
- Wrong `mcp.*.json` copied (name/port mismatch) => VS Code cannot start server.
- Re-loading `metadata.json` repeatedly => performance hit.

## Minimal Workflows
- Run STDIO: `dotnet run --project ./markdown-to-html/src/McpSamples.MarkdownToHtml.HybridApp`
- Run HTTP: append `-- --http` (plus sample switches after that).
- Pack: `dotnet pack ./todo-list/src/McpSamples.TodoList.HybridApp -c Release -o ./artifacts`.
- Run packed: `dnx Ibhatt089.McpSamples.TodoList --yes --add-source ./artifacts`; verify all with `python scripts/smoke_test.py ./artifacts`.

## Adding a New Sample (Checklist)
1. Copy structure from an existing sample; reference `McpSamples.Shared`.
2. Implement `Program.cs` with same pattern (parse settings -> add services -> `BuildApp`).
3. Add NuGet tool properties to the csproj, a `.mcp/server.json`, and `.vscode/mcp.*.local.json`.
4. Register it in `.mcp.json`, `.vscode/mcp.json`, `scripts/smoke_test.py`, and the root README table.

## PR Expectations (Essentials)
- Build passes (.NET 10). Tools/prompts discoverable. No hardcoded secrets. Sample-specific behavior isolated. Conventional commits.

Questions / unclear? Compare with the most similar existing sample before inventing new structure.

Feedback welcome: open a docs PR if a recurring pattern isn’t captured here.