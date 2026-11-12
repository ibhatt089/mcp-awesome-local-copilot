# AGENTS.md - MCP Awesome Local Copilot

## Project Overview

Four .NET 10 MCP servers, packaged as .NET tools on nuget.org and run locally over stdio with `dnx`. The repository is also a Cursor plugin, a Claude Code plugin and marketplace, and a VS Code MCP workspace. Docker and Azure deployment are intentionally not supported.

## Project Structure and Architecture

### Repository Organization

```
mcp-awesome-local-copilot/
├── .cursor-plugin/plugin.json   # Cursor plugin manifest
├── .claude-plugin/              # Claude Code plugin + marketplace manifests
├── .mcp.json                    # MCP servers (dnx) for the Cursor and Claude Code plugins
├── .vscode/mcp.json             # MCP servers (dnx) for VS Code
├── .github/workflows/           # ci.yaml (pack + dnx smoke test), publish.yaml (NuGet on v* tags)
├── scripts/smoke_test.py        # stdio handshake test for all packed servers
├── shared/McpSamples.Shared/    # Shared MCP host code
├── awesome-copilot/ | markdown-to-html/ | outlook-email/ | todo-list/
│   ├── src/McpSamples.<Name>.HybridApp/
│   │   └── .mcp/server.json     # MCP registry metadata packed into the NuGet package
│   └── .vscode/                 # mcp.stdio.local.json / mcp.http.local.json for running from source
├── Directory.Build.props        # Shared MSBuild + NuGet package properties
└── global.json                  # .NET SDK configuration
```

### Sample Components

#### 1. Awesome Copilot Sample
- **Purpose**: Integrates with GitHub's awesome-copilot repository to provide Copilot customizations
- **Key Features**: 
  - Search and retrieve GitHub Copilot instructions
  - File metadata processing
  - JSON-based configuration management
- **Technologies**: File I/O, HTTP clients, JSON processing

#### 2. Markdown to HTML Sample  
- **Purpose**: Converts Markdown content to HTML with customizable options
- **Key Features**:
  - Markdown parsing and HTML generation
  - Configurable HTML output options
- **Technologies**: Markdown processing, HTML generation, web services

#### 3. Outlook Email Sample
- **Purpose**: Sends emails through Outlook
- **Key Features**:
  - Email sending capabilities via Microsoft Graph API
  - Entra ID client-secret credentials from `EntraId__*` environment variables
- **Technologies**: Microsoft Graph, Azure.Identity

#### 4. Todo List Sample
- **Purpose**: Manages todo items with full CRUD operations
- **Key Features**:
  - Create, read, update, delete operations
  - Data persistence
  - RESTful API patterns
- **Technologies**: Data management, API development, persistence

## Coding Conventions and Standards

### C# and .NET Standards

#### Language and Framework
- **Target Framework**: .NET 10.0 (as specified in Directory.Build.props)
- **Language Version**: Latest C# features enabled
- **Nullable Reference Types**: Enabled for all projects
- **Implicit Global Usings**: Enabled to reduce boilerplate

#### Code Organization
```csharp
// Namespace structure
namespace McpSamples.{SampleName}.{ComponentType};

// Class organization
public class ExampleMcpServer : IMcpServer
{
    // Private readonly fields first
    private readonly ILogger<ExampleMcpServer> _logger;
    
    // Constructor
    public ExampleMcpServer(ILogger<ExampleMcpServer> logger)
    {
        _logger = logger;
    }
    
    // Public methods
    [McpServerTool(Name = "example_tool")]
    [Description("Example tool implementation")]
    public async Task<string> ExampleToolAsync(
        [Description("Input parameter")] string input)
    {
        // Implementation
    }
}
```

#### Naming Conventions
- **Classes**: PascalCase with descriptive names
- **Methods**: PascalCase with verb-noun pattern
- **Properties**: PascalCase
- **Private Fields**: _camelCase with underscore prefix
- **Parameters**: camelCase
- **Constants**: UPPER_SNAKE_CASE

### MCP Server Development Standards

#### Server Registration
- Use dependency injection for all services
- Implement proper lifetime management
- Follow the MCP protocol specifications

#### Tool Implementation
```csharp
[McpServerTool(Name = "tool_name")]
[Description("Clear description of what the tool does")]
public async Task<ToolResult> ToolNameAsync(
    [Description("Parameter description")] string parameter)
{
    // Validate input
    if (string.IsNullOrWhiteSpace(parameter))
        throw new ArgumentException("Parameter cannot be null or empty");
    
    // Implement functionality
    var result = await ProcessAsync(parameter);
    
    // Return structured result
    return new ToolResult { Content = result };
}
```

#### Prompt Implementation
```csharp
[McpServerPrompt(Name = "prompt_name", Title = "Human-readable title")]
[Description("Description of the prompt's purpose")]
public string GetPrompt([Description("Context parameter")] string context)
{
    return $"Structured prompt template with {context}";
}
```

### Packaging Standards

- Every server is a .NET tool with `PackageType` `McpServer` and a `.mcp/server.json`
- In stdio mode nothing but MCP JSON-RPC may be written to stdout; logs go to stderr
- Keep `.mcp.json`, `.vscode/mcp.json` and each README install snippet in sync with package IDs

## Testing Protocols and Guidelines

### Unit Testing Framework
- **Framework**: MSTest or xUnit (depending on sample requirements)
- **Mocking**: Moq for dependency mocking
- **Coverage**: Minimum 80% code coverage for business logic

### Test Structure
```csharp
[TestClass]
public class ExampleMcpServerTests
{
    private readonly Mock<ILogger<ExampleMcpServer>> _mockLogger;
    private readonly ExampleMcpServer _server;
    
    public ExampleMcpServerTests()
    {
        _mockLogger = new Mock<ILogger<ExampleMcpServer>>();
        _server = new ExampleMcpServer(_mockLogger.Object);
    }
    
    [TestMethod]
    public async Task ExampleTool_WithValidInput_ReturnsExpectedResult()
    {
        // Arrange
        var input = "test input";
        var expectedOutput = "expected result";
        
        // Act
        var result = await _server.ExampleToolAsync(input);
        
        // Assert
        Assert.AreEqual(expectedOutput, result.Content);
    }
}
```

### Integration Testing
- Test MCP server initialization and registration
- Verify tool and prompt functionality end-to-end
- Test error handling and edge cases
- Run `scripts/smoke_test.py` against packed packages to verify the `dnx` stdio handshake

### Running Tests
```bash
# Run all tests
dotnet test

# Run with coverage
dotnet test --collect:"XPlat Code Coverage"

# Run specific test project
dotnet test ./tests/McpSamples.{Sample}.Tests/
```

## Pull Request Guidelines and Workflow

### Branch Naming Convention
- `feature/description-of-feature`
- `bugfix/description-of-fix`
- `docs/description-of-documentation-change`

### PR Requirements Checklist
- [ ] **Code Quality**: Follows established coding standards
- [ ] **Tests**: Includes appropriate unit and integration tests
- [ ] **Documentation**: Updates relevant documentation
- [ ] **Build**: Successfully builds with .NET 10
- [ ] **Smoke test**: `python scripts/smoke_test.py ./artifacts` passes
- [ ] **Security**: No hardcoded secrets or vulnerabilities
- [ ] **Performance**: No significant performance regressions
- [ ] **MCP Compliance**: Follows MCP protocol specifications

### PR Description Template
```markdown
## Summary
Brief description of the changes made.

## Changes Made
- List specific changes
- Include any new features or modifications
- Mention any removed functionality

## Testing Performed
- Unit tests: [Pass/Fail]
- Integration tests: [Pass/Fail]
- Manual testing: [Description]

## Breaking Changes
List any breaking changes or migration requirements.

## Screenshots
Include screenshots for UI changes (if applicable).

## Additional Notes
Any additional context or considerations for reviewers.
```

### Commit Message Format
Follow conventional commit format:
```
type(scope): description

feat(awesome-copilot): add search functionality for instructions
fix(shared): resolve MCP server initialization issue  
docs(readme): update installation instructions
refactor(todo-list): optimize data access patterns
test(markdown): add unit tests for HTML conversion
```

## Development Environment Setup

### Prerequisites
- .NET 10 SDK (provides `dnx`)
- Python 3 (smoke test only)

### Local Development Workflow
1. **Clone Repository**: `git clone <repository-url>`
2. **Install Dependencies**: `dotnet restore`
3. **Build Solution**: `dotnet build`
4. **Run Tests**: `dotnet test`
5. **Configure MCP**: Copy appropriate `.vscode/mcp.json` configuration
6. **Start Development**: Use VS Code with MCP integration

### Editor Configuration
- `.vscode/mcp.json` (repo root) - all four servers via `dnx`
- `<sample>/.vscode/mcp.stdio.local.json` - run one server from source over stdio
- `<sample>/.vscode/mcp.http.local.json` - run one server from source over streamable HTTP

## Release

- Add the `NUGET_API_KEY` repository secret
- Bump plugin manifest versions, then push a `v*` tag; `publish.yaml` packs, smoke-tests and pushes to nuget.org

This document serves as the primary reference for development practices and standards within the MCP .NET Samples repository. All contributors should familiarize themselves with these guidelines to ensure consistency and quality across the codebase.