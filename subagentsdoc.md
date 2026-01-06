# Claude Code Subagents Documentation

## Overview
Subagents are specialized AI assistants in Claude Code that handle specific types of tasks with their own context windows, custom system prompts, and tool access. They enable more efficient problem-solving by providing task-specific configurations.

## Key Benefits
- **Context preservation**: Each subagent operates in its own context, preventing pollution of the main conversation
- **Specialized expertise**: Fine-tuned with detailed instructions for specific domains
- **Reusability**: Can be used across different projects and shared with teams
- **Flexible permissions**: Different tool access levels per subagent

## Quick Start
1. **Open the subagents interface**:
   ```
   /agents
   ```

2. **Select 'Create New Agent'** and choose project-level or user-level

3. **Define the subagent** with description, tools, and system prompt

4. **Save and use** - Claude uses it automatically or can be invoked explicitly:
   ```
   > Use the code-reviewer subagent to check my recent changes
   ```

## Configuration

### File Locations
| Type | Location | Scope | Priority |
|------|----------|-------|----------|
| Project subagents | `.claude/agents/` | Current project | Highest |
| User subagents | `~/.claude/agents/` | All projects | Lower |

### File Format
```markdown
---
name: your-sub-agent-name
description: Description of when this subagent should be invoked
tools: tool1, tool2, tool3  # Optional - inherits all tools if omitted
model: sonnet  # Optional - specify model alias or 'inherit'
permissionMode: default  # Optional
skills: skill1, skill2  # Optional
---

Your subagent's system prompt goes here. This can be multiple paragraphs
and should clearly define the subagent's role, capabilities, and approach
to solving problems.
```

### Configuration Fields
- `name`: Unique identifier using lowercase letters and hyphens
- `description`: Natural language description of the subagent's purpose
- `tools`: Comma-separated list of specific tools (inherits all if omitted)
- `model`: Model alias (`sonnet`, `opus`, `haiku`) or `'inherit'`
- `permissionMode`: Controls permission handling (`default`, `acceptEdits`, `bypassPermissions`, `plan`, `ignore`)
- `skills`: Comma-separated list of skills to auto-load

### CLI Configuration
```bash
claude --agents '{
  "code-reviewer": {
    "description": "Expert code reviewer. Use proactively after code changes.",
    "prompt": "You are a senior code reviewer. Focus on code quality, security, and best practices.",
    "tools": ["Read", "Grep", "Glob", "Bash"],
    "model": "sonnet"
  }
}'
```

## Built-in Subagents

### General-purpose Subagent
- Uses Sonnet model
- Access to all tools
- Handles complex, multi-step tasks requiring both exploration and action

### Plan Subagent
- Used during plan mode for research
- Sonnet model with Read, Glob, Grep, Bash tools
- Prevents infinite nesting of agents

### Explore Subagent
- Uses Haiku for fast searches
- Strictly read-only mode
- Optimized for codebase exploration

## Example Subagents

### Code Reviewer
```markdown
---
name: code-reviewer
description: Expert code review specialist. Proactively reviews code for quality, security, and maintainability. Use immediately after writing or modifying code.
tools: Read, Grep, Glob, Bash
model: inherit
---

You are a senior code reviewer ensuring high standards of code quality and security.

When invoked:
1. Run git diff to see recent changes
2. Focus on modified files
3. Begin review immediately

Review checklist:
- Code is clear and readable
- Functions and variables are well-named
- No duplicated code
- Proper error handling
- No exposed secrets or API keys
- Input validation implemented
- Good test coverage
- Performance considerations addressed
```

### Debugger
```markdown
---
name: debugger
description: Debugging specialist for errors, test failures, and unexpected behavior. Use proactively when encountering any issues.
tools: Read, Edit, Bash, Grep, Glob
---

You are an expert debugger specializing in root cause analysis.

When invoked:
1. Capture error message and stack trace
2. Identify reproduction steps
3. Isolate the failure location
4. Implement minimal fix
5. Verify solution works

Debugging process:
- Analyze error messages and logs
- Check recent code changes
- Form and test hypotheses
- Add strategic debug logging
- Inspect variable states
```

## Usage Methods

### Automatic Delegation
Claude Code proactively delegates based on task descriptions and context. Include "use PROACTIVELY" or "MUST BE USED" in descriptions to encourage usage.

### Explicit Invocation
```
> Use the test-runner subagent to fix failing tests
> Have the code-reviewer subagent look at my recent changes
> Ask the debugger subagent to investigate this error
```

## Advanced Features

### Resumable Subagents
Subagents can be resumed to continue previous conversations:
```
> Resume agent abc123 and now analyze the authorization logic as well
```

### Chaining Subagents
```
> First use the code-analyzer subagent to find performance issues, then use the optimizer subagent to fix them
```

## Best Practices
- Start with Claude-generated agents and iterate
- Create focused subagents with single responsibilities
- Include clear usage instructions with "Use this agent when you need:" to specify when the agent should be invoked
- Write detailed system prompts with specific instructions
- Limit tool access to necessary tools only
- Version control project subagents for team collaboration