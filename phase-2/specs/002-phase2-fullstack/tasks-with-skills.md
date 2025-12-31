# Phase II: Tasks with Agents & Skills Assignment

**Purpose**: Map each task to the appropriate subagent and skill for implementation.

---

## Quick Reference

| Subagent | Skills | MCP Servers |
|----------|--------|-------------|
| `backend-dev` | fastapi-skill, sqlmodel-skill, neon-db-skill, rest-api-skill | context7, neon |
| `auth-specialist` | better-auth-skill | better-auth, context7 |
| `frontend-dev` | nextjs-skill | context7 |
| `ui-ux-designer` | tailwind-skill | context7 |
| `tailwind-dev` | tailwind-skill | context7 |

---

## Phase 1: Environment Setup

### Task 1.1.6: Initialize Next.js Project

**Subagent**: `frontend-dev`
**Skill**: `nextjs-skill`
**MCP**: `context7` (Next.js docs)

```bash
# Invoke skill for documentation
/nextjs-skill

# Or use MCP directly
mcp__context7__get-library-docs --context7CompatibleLibraryID "/vercel/next.js" --topic "installation"
```

**Commands**:
```bash
cd ~/Todo-app/frontend
npx create-next-app@latest . --typescript --tailwind --eslint --app --src-dir --no-git
npm install better-auth @better-auth/react
```

---

### Task 1.1.7: Initialize FastAPI Project

**Subagent**: `backend-dev`
**Skill**: `fastapi-skill`
**MCP**: `context7` (FastAPI docs)

```bash
# Invoke skill for documentation
/fastapi-skill

# Or use MCP directly
mcp__context7__get-library-docs --context7CompatibleLibraryID "/fastapi/fastapi" --topic "installation"
```

**Commands**:
```bash
cd ~/Todo-app/backend
uv init --name todo-backend
uv add fastapi "uvicorn[standard]" sqlmodel asyncpg python-jose "pydantic-settings"
```

---

## Phase 2: Backend Implementation

### Task 2.1.2: Create config.py

**Subagent**: `backend-dev`
**Skill**: `fastapi-skill`
**MCP**: `context7`

```bash
# Get pydantic-settings docs
mcp__context7__get-library-docs --context7CompatibleLibraryID "/pydantic/pydantic" --topic "settings"
```

---

### Task 2.1.3: Create database.py

**Subagent**: `backend-dev`
**Skill**: `sqlmodel-skill`, `neon-db-skill`
**MCP**: `context7`, `neon`

```bash
# Get SQLModel async session docs
mcp__context7__get-library-docs --context7CompatibleLibraryID "/sqlmodel/sqlmodel" --topic "async-session"

# Get Neon connection string format
mcp__neon__get_connection_string --projectId "round-frog-47707317"
```

---

### Task 2.1.4: Create security.py (JWT)

**Subagent**: `auth-specialist`
**Skill**: `better-auth-skill`
**MCP**: `better-auth`

```bash
# Get Better Auth JWT docs
mcp__better-auth__search --query "JWT verification Python backend"

# Or chat for detailed guidance
mcp__better-auth__chat --messages '[{"role":"user","content":"How to verify Better Auth JWT in FastAPI?"}]'
```

---

### Task 2.2.2: Create Task Model

**Subagent**: `backend-dev`
**Skill**: `sqlmodel-skill`
**MCP**: `context7`

```bash
# Get SQLModel table definition docs
mcp__context7__get-library-docs --context7CompatibleLibraryID "/sqlmodel/sqlmodel" --topic "table-models"
```

---

### Task 2.3.2-2.3.7: Create Task Service (CRUD)

**Subagent**: `backend-dev`
**Skill**: `task-crud-skill`, `sqlmodel-skill`
**MCP**: `context7`, `neon`

```bash
# Get SQLModel CRUD patterns
mcp__context7__get-library-docs --context7CompatibleLibraryID "/sqlmodel/sqlmodel" --topic "crud"

# Test SQL on Neon
mcp__neon__run_sql --projectId "round-frog-47707317" --sql "SELECT * FROM tasks LIMIT 5"
```

---

### Task 2.4.4-2.4.8: Create API Routes

**Subagent**: `backend-dev`
**Skill**: `rest-api-skill`, `fastapi-skill`
**MCP**: `context7`

```bash
# Get FastAPI routing docs
mcp__context7__get-library-docs --context7CompatibleLibraryID "/fastapi/fastapi" --topic "routing"

# Get FastAPI dependency injection docs
mcp__context7__get-library-docs --context7CompatibleLibraryID "/fastapi/fastapi" --topic "dependencies"
```

---

## Phase 3: Frontend Implementation

### Task 3.1.1-3.1.2: Better Auth Setup

**Subagent**: `auth-specialist`
**Skill**: `better-auth-skill`
**MCP**: `better-auth`

```bash
# Get Better Auth Next.js setup
mcp__better-auth__search --query "Next.js App Router setup"

# Get detailed config
mcp__better-auth__chat --messages '[{"role":"user","content":"How to setup Better Auth in Next.js 16 App Router?"}]'
```

---

### Task 3.2.1-3.2.8: UI Components

**Subagent**: `ui-ux-designer`, `tailwind-dev`
**Skill**: `tailwind-skill`
**MCP**: `context7`

```bash
# Get Tailwind component patterns
mcp__context7__get-library-docs --context7CompatibleLibraryID "/tailwindlabs/tailwindcss" --topic "components"

# Get Tailwind forms styling
mcp__context7__get-library-docs --context7CompatibleLibraryID "/tailwindlabs/tailwindcss" --topic "forms"
```

---

### Task 3.5.1-3.5.5: Pages

**Subagent**: `frontend-dev`
**Skill**: `nextjs-skill`
**MCP**: `context7`

```bash
# Get Next.js App Router pages
mcp__context7__get-library-docs --context7CompatibleLibraryID "/vercel/next.js" --topic "app-router"

# Get Next.js middleware
mcp__context7__get-library-docs --context7CompatibleLibraryID "/vercel/next.js" --topic "middleware"
```

---

### Task 3.6.1: API Client

**Subagent**: `frontend-dev`
**Skill**: `rest-api-skill`
**MCP**: `context7`

```bash
# Get Next.js fetch patterns
mcp__context7__get-library-docs --context7CompatibleLibraryID "/vercel/next.js" --topic "data-fetching"
```

---

## Implementation Workflow

### Step 1: Start Implementation

```bash
# User command
/sp.implement

# Claude reads task, identifies subagent and skill
# Example: Task 2.1.3 (database.py)
# → Subagent: backend-dev
# → Skills: sqlmodel-skill, neon-db-skill
# → MCP: context7, neon
```

### Step 2: Invoke Skill for Documentation

```bash
# Option A: Use skill directly
/sqlmodel-skill

# Option B: Use MCP tool
mcp__context7__get-library-docs --context7CompatibleLibraryID "/sqlmodel/sqlmodel" --topic "async-engine"
```

### Step 3: Implement Based on Skill + MCP Docs

```python
# Claude implements using skill patterns + MCP documentation
# Example: database.py from sqlmodel-skill + neon-db-skill
```

### Step 4: Verify with MCP

```bash
# Test database connection
mcp__neon__run_sql --projectId "round-frog-47707317" --sql "SELECT 1"
```

---

## Skill Invocation Summary

| Task Category | Skill to Invoke | MCP to Use |
|---------------|-----------------|------------|
| FastAPI setup | `/fastapi-skill` | context7 |
| SQLModel models | `/sqlmodel-skill` | context7 |
| Neon database | `/neon-db-skill` | neon |
| JWT auth | `/better-auth-skill` | better-auth |
| Next.js pages | `/nextjs-skill` | context7 |
| Tailwind CSS | `/tailwind-skill` | context7 |
| REST API design | `/rest-api-skill` | context7 |
| Task CRUD logic | `/task-crud-skill` | - |

---

## Example: Complete Task Implementation

### Task 2.1.3: Create database.py

**1. Read skill documentation**:
```bash
/sqlmodel-skill
/neon-db-skill
```

**2. Fetch MCP docs**:
```bash
mcp__context7__get-library-docs --context7CompatibleLibraryID "/sqlmodel/sqlmodel" --topic "async"
```

**3. Implement**:
```python
# backend/app/core/database.py
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from .config import settings

async_engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_size=5,
    max_overflow=10
)

async_session = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)

async def get_session():
    async with async_session() as session:
        yield session

async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
```

**4. Verify with MCP**:
```bash
mcp__neon__run_sql --projectId "round-frog-47707317" --sql "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
```

---

## Ready to Implement?

Run `/sp.implement` and I will:
1. Pick the next task
2. Identify the subagent and skill
3. Invoke MCP for latest documentation
4. Implement based on skill patterns
5. Verify with MCP tools
6. Create PHR record
