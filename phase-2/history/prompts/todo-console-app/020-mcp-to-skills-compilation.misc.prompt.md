---
id: "020"
title: "MCP to skills compilation pattern"
stage: "misc"
date: "2025-12-29"
surface: "agent"
model: "sonnet-4-5-20250929"
feature: "001-todo-console-app"
branch: "001-todo-console-app"
user: "aqsagulllinux"
command: "Implement MCP to skills compilation pattern from reference architecture"
labels: ["mcp", "skills", "compilation", "token-reduction", "architecture"]
links:
  spec: "null"
  plan: "null"
  ticket: "null"
  adr: "null"
  pr: "null"
files:
  - "/home/aqsagulllinux/Todo-app/.claude/skills/mcp-client/SKILL.md"
  - "/home/aqsagulllinux/Todo-app/.claude/skills/mcp-client/scripts/mcp-client.py"
  - "/home/aqsagulllinux/Todo-app/.claude/skills/mcp-client/scripts/start-context7.sh"
  - "/home/aqsagulllinux/Todo-app/.claude/skills/mcp-client/scripts/start-better-auth.sh"
  - "/home/aqsagulllinux/Todo-app/.claude/skills/mcp-client/scripts/start-neon.sh"
  - "/home/aqsagulllinux/Todo-app/.claude/skills/mcp-client/scripts/start-playwright.sh"
tests:
  - "Universal MCP client created"
  - "Start scripts created for all 4 MCP servers"
  - "SKILL.md under 200 tokens"
  - "Scripts executable"
---

## Prompt

User provided reference architecture for MCP-to-skills compilation to reduce token usage:

**Pattern:**
- SKILL.md provides high-level procedures (~150 tokens, loaded once)
- Claude executes bash commands calling mcp-client.py (runs locally, outside context)
- mcp-client.py connects to MCP server via HTTP transport
- Only filtered results returned to conversation

**Token Comparison:**
| Method | Tokens × 3 Calls | Total |
|--------|-----------------|-------|
| Direct MCP | ~5,000-8,000 × 3 | ~15,000-24,000 |
| Compiled Skill | ~150 × 1 | ~150 |
| **Savings** | | **~98-99%** |

**Architecture Reference:**
```
.claude/skills/browsing-with-playwright/
├── SKILL.md                    # High-level procedures (~150 tokens)
├── references/                 # Cached tool documentation
└── scripts/
    ├── mcp-client.py          # Universal MCP client
    ├── start-server.sh        # Starts MCP on localhost
    └── stop-server.sh         # Stops server gracefully
```

## Response snapshot

Implemented MCP-to-skills compilation pattern for Phase II:

### File Structure

```
.claude/skills/mcp-client/
├── SKILL.md                    # This file (~150 tokens)
├── scripts/
│   ├── mcp-client.py          # Universal MCP client (Python)
│   ├── start-context7.sh      # Start Context7 server (port 3001)
│   ├── start-better-auth.sh   # Start Better Auth server (port 3002)
│   ├── start-neon.sh          # Start Neon server (port 3003)
│   └── start-playwright.sh    # Start Playwright server (port 8808)
```

### mcp-client.py Features

| Feature | Implementation |
|---------|---------------|
| HTTP transport | urllib for HTTP requests |
| Multi-server support | context7, better-auth, neon, playwright |
| Argument parsing | argparse for CLI interface |
| Result filtering | Auto-truncates large responses |
| Error handling | Comprehensive exception handling |

### Server Configuration

| Server | Default Port | Purpose |
|--------|-------------|---------|
| context7 | 3001 | Next.js, FastAPI, SQLModel, Tailwind docs |
| better-auth | 3002 | Better Auth, JWT, OAuth docs |
| neon | 3003 | PostgreSQL, database operations |
| playwright | 8808 | Browser automation |

### Usage Examples

```bash
# Get Next.js docs via compiled script
python scripts/mcp-client.py --server context7 --tool get-library-docs \
  --args '{"context7CompatibleLibraryID": "nextjs", "topic": "app-router"}'

# Search Better Auth docs
python scripts/mcp-client.py --server better-auth --tool search \
  --args '{"query": "jwt plugin"}'

# Run Neon SQL query
python scripts/mcp-client.py --server neon --tool run_sql \
  --args '{"sql": "SELECT * FROM tasks LIMIT 5"}'
```

### Token Savings Calculation

| Metric | Direct MCP | Compiled Skill | Savings |
|--------|-----------|----------------|---------|
| SKILL.md tokens | ~5,000-8,000 | ~150 | 97-99% |
| Per 3 calls | ~15,000-24,000 | ~150 | 99% |
| Context overhead | High | None | - |
| Runtime | In-context | Local script | - |

## Implementation Details

### SKILL.md Structure

1. **Header** (~50 tokens) - Name, description, purpose
2. **Usage** (~50 tokens) - Quick reference patterns
3. **Server Config** (~30 tokens) - Port mappings
4. **Examples** (~20 tokens) - Common calls

### mcp-client.py Features

1. **Universal client**: Works with any HTTP-based MCP server
2. **Result filtering**: Truncates large responses to reduce tokens
3. **Error handling**: Returns structured error responses
4. **Environment override**: MCP_*_URL env vars for customization

### Scripts

1. **Start scripts**: Check if running, start server, wait for ready
2. **Port management**: Each server on unique port
3. **Error handling**: Graceful failure with helpful messages

## Outcome

- ✅ Impact: MCP-to-skills compilation pattern implemented
- 🧪 Tests: Scripts created, chmod +x applied
- 📁 Files: 6 files (1 skill + 5 scripts)
- 🔁 Next prompts: Update Phase II agents to use compiled MCP
- 🧠 Reflection: ~98-99% token savings for documentation queries

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): All files created - PASS
- Prompt variant (if applicable): Based on reference architecture
- Next experiment (smallest change to try): Add result caching to references/ folder
