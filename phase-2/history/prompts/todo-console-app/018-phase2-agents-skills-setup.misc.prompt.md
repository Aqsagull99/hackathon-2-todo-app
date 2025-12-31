---
id: "018"
title: "Phase II agents and skills setup"
stage: "misc"
date: "2025-12-29"
surface: "agent"
model: "sonnet-4-5-20250929"
feature: "001-todo-console-app"
branch: "001-todo-console-app"
user: "aqsagulllinux"
command: "Create Phase II agents and skills with MCP server integration"
labels: ["phase2", "agents", "skills", "mcp", "nextjs", "fastapi", "better-auth", "neon"]
links:
  spec: "/home/aqsagulllinux/Todo-app/specs/001-todo-console-app/spec.md"
  plan: "null"
  ticket: "null"
  adr: "null"
  pr: "null"
files:
  - "/home/aqsagulllinux/Todo-app/.claude/agents/todo-main-agent-phase2.md"
  - "/home/aqsagulllinux/Todo-app/.claude/subagents/backend-dev.md"
  - "/home/aqsagulllinux/Todo-app/.claude/subagents/auth-specialist.md"
  - "/home/aqsagulllinux/Todo-app/.claude/subagents/frontend-dev.md"
  - "/home/aqsagulllinux/Todo-app/.claude/subagents/ui-ux-designer.md"
  - "/home/aqsagulllinux/Todo-app/.claude/skills/nextjs-skill/SKILL.md"
  - "/home/aqsagulllinux/Todo-app/.claude/skills/fastapi-skill/SKILL.md"
  - "/home/aqsagulllinux/Todo-app/.claude/skills/sqlmodel-skill/SKILL.md"
  - "/home/aqsagulllinux/Todo-app/.claude/skills/neon-db-skill/SKILL.md"
  - "/home/aqsagulllinux/Todo-app/.claude/skills/better-auth-skill/SKILL.md"
  - "/home/aqsagulllinux/Todo-app/.claude/skills/rest-api-skill/SKILL.md"
tests:
  - "Main agent created with MCP references"
  - "4 subagents created (backend-dev, auth-specialist, frontend-dev, ui-ux-designer)"
  - "6 skills created (nextjs, fastapi, sqlmodel, neon-db, better-auth, rest-api)"
  - "All agents reference relevant MCP servers"
---

## Prompt

User requested to create Phase II agents and skills structure for Hackathon II Phase 2 (Full-Stack Web Application).

User specified requirements:
1. Use MCP servers for documentation:
   - `context7` - Next.js, FastAPI, SQLModel docs
   - `better-auth` - Better Auth docs
   - `neon` - Neon PostgreSQL docs

2. Create structure with:
   - Main agent (coordinator)
   - Backend subagents (FastAPI, Auth)
   - Frontend subagents (Next.js, UI/UX Designer)
   - Reusable skills for each technology

3. Monorepo structure with Better Auth (not Neon Auth)

## Response snapshot

Created comprehensive Phase II agent/skill structure:

### Main Agent
| File | Purpose |
|------|---------|
| `todo-main-agent-phase2.md` | Main coordinator with MCP references |

### Backend Subagents (2)
| Subagent | Purpose | MCP Servers |
|----------|---------|-------------|
| `backend-dev.md` | FastAPI routes, SQLModel models | context7, neon |
| `auth-specialist.md` | JWT verification, Better Auth | better-auth, context7 |

### Frontend Subagents (2)
| Subagent | Purpose | MCP Servers |
|----------|---------|-------------|
| `frontend-dev.md` | Next.js pages, components | context7 |
| `ui-ux-designer.md` | UI/UX with Tailwind | context7 |

### Backend Skills (4)
| Skill | Purpose |
|-------|---------|
| `fastapi-skill/SKILL.md` | REST endpoints, Pydantic, dependencies |
| `sqlmodel-skill/SKILL.md` | ORM models, relationships, sessions |
| `neon-db-skill/SKILL.md` | Neon PostgreSQL, async connections |
| `better-auth-skill/SKILL.md` | JWT plugin, OAuth, sessions |
| `rest-api-skill/SKILL.md` | HTTP methods, status codes, patterns |

### Frontend Skill (1)
| Skill | Purpose |
|-------|---------|
| `nextjs-skill/SKILL.md` | App Router, Server/Client Components |

### MCP Integration Pattern
All agents reference MCP servers with usage examples:
```yaml
mcp_servers:
  - context7
  - better-auth
  - neon
```

Fetching docs: `@context7:get-library-docs`, `@better-auth:search`, `@neon:run-sql`

## Phase II Tech Stack
| Layer | Technology |
|-------|------------|
| Frontend | Next.js 16+ (App Router) |
| Backend | Python FastAPI |
| ORM | SQLModel |
| Database | Neon Serverless PostgreSQL |
| Auth | Better Auth with JWT |

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/{user_id}/tasks` | List all tasks |
| `POST` | `/api/{user_id}/tasks` | Create new task |
| `GET` | `/api/{user_id}/tasks/{id}` | Get task details |
| `PUT` | `/api/{user_id}/tasks/{id}` | Update task |
| `DELETE` | `/api/{user_id}/tasks/{id}` | Delete task |
| `PATCH` | `/api/{user_id}/tasks/{id}/complete` | Toggle completion |

## Monorepo Structure
```
Todo-app/
├── frontend/           # Next.js 16+
├── backend/            # FastAPI
├── specs/
│   └── phase2/         # Phase II specs
└── CLAUDE.md
```

## Outcome

- ✅ Impact: Phase II agents and skills ready for implementation
- 🧪 Tests: 10 files created, all syntax validated
- 📁 Files: 1 main agent + 4 subagents + 6 skills = 11 files
- 🔁 Next prompts: Create Phase II spec.md, plan.md, tasks.md
- 🧠 Reflection: All agents/skills include MCP server references for docs

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): All files created - PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Add MCP fetch examples to each skill
