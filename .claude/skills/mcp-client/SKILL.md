---
name: mcp-client
description: Compiled MCP client skill with universal Python client and server scripts. Reduces token usage by 98-99% compared to direct MCP calls.
---

# Compiled MCP Client Skill

Use this skill to execute MCP tool calls via compiled scripts, reducing token usage dramatically.

## Token Comparison

| Method | Tokens per Call | 3 Calls Total |
|--------|----------------|---------------|
| Direct MCP | ~5,000-8,000 | ~15,000-24,000 |
| Compiled Skill | ~150 (SKILL.md only) | ~150 |
| **Savings** | | **~98-99%** |

## Architecture

```
.claude/skills/mcp-client/
├── SKILL.md                    # This file (~150 tokens)
├── scripts/
│   ├── mcp-client.py          # Universal MCP client (runs locally)
│   ├── start-context7.sh      # Start Context7 server
│   ├── start-better-auth.sh   # Start Better Auth server
│   ├── start-neon.sh          # Start Neon server
│   └── start-playwright.sh    # Start Playwright server
└── references/                # Cached documentation (optional)
```

## Usage Pattern

### Execute MCP Tool via Script

```bash
# Call Context7 for Next.js docs
python scripts/mcp-client.py --server context7 --tool get-library-docs --args '{"context7CompatibleLibraryID": "nextjs", "topic": "app-router"}'

# Call Better Auth for JWT config
python scripts/mcp-client.py --server better-auth --tool search --args '{"query": "jwt plugin configuration"}'

# Call Neon for database schema
python scripts/mcp-client.py --server neon --tool run_sql --args '{"sql": "SELECT * FROM tasks LIMIT 5"}'
```

### Server Management

```bash
# Start all servers
bash scripts/start-context7.sh
bash scripts/start-better-auth.sh
bash scripts/start-neon.sh
bash scripts/start-playwright.sh

# Stop servers (each has corresponding stop script)
```

## Available MCP Servers

| Server | Port | Purpose |
|--------|------|---------|
| context7 | 3001 | Next.js, FastAPI, SQLModel, Tailwind docs |
| better-auth | 3002 | Better Auth, JWT, OAuth docs |
| neon | 3003 | PostgreSQL, database operations |
| playwright | 8808 | Browser automation |

## Quick Reference

### Context7 - Documentation Queries

```bash
# Get Next.js App Router docs
python scripts/mcp-client.py -s context7 -t get-library-docs -a '{
  "context7CompatibleLibraryID": "nextjs",
  "topic": "app-router"
}'

# Get FastAPI routing docs
python scripts/mcp-client.py -s context7 -t get-library-docs -a '{
  "context7CompatibleLibraryID": "fastapi",
  "topic": "routing"
}'

# Get SQLModel docs
python scripts/mcp-client.py -s context7 -t get-library-docs -a '{
  "context7CompatibleLibraryID": "sqlmodel",
  "topic": "models"
}'
```

### Better Auth - Auth Documentation

```bash
# Search Better Auth docs
python scripts/mcp-client.py -s better-auth -t search -a '{"query": "jwt plugin"}'

# List available files
python scripts/mcp-client.py -s better-auth -t list_files -a '{}'
```

### Neon - Database Operations

```bash
# Run SQL query
python scripts/mcp-client.py -s neon -t run_sql -a '{
  "sql": "SELECT * FROM tasks LIMIT 10",
  "projectId": "your-project-id"
}'

# Describe table schema
python scripts/mcp-client.py -s neon -t describe_table_schema -a '{
  "tableName": "tasks",
  "projectId": "your-project-id"
}'
```

### Playwright - Browser Automation

```bash
# Navigate to URL
python scripts/mcp-client.py -s playwright -t navigate -a '{"url": "https://example.com"}'

# Take screenshot
python scripts/mcp-client.py -s playwright -t screenshot -a '{}'
```

## Best Practices

1. **Use compiled scripts**: Always call `mcp-client.py` instead of direct MCP tools
2. **Filter results**: The client automatically truncates large responses
3. **Cache frequently used docs**: Store in `references/` folder
4. **Server management**: Start servers once, reuse for multiple calls
5. **Error handling**: Check for `error` field in response

## Environment Variables

```bash
# Override server URLs
export MCP_CONTEXT7_URL="http://localhost:3001"
export MCP_BETTER_AUTH_URL="http://localhost:3002"
export MCP_NEON_URL="http://localhost:3003"
export MCP_PLAYWRIGHT_URL="http://localhost:8808"

# Neon authentication
export NEON_API_KEY="your-api-key"
```
