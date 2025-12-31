---
id: "023"
title: "Phase II full-stack web application spec"
stage: "spec"
date: "2025-12-29"
surface: "agent"
model: "sonnet-4-5-20250929"
feature: "002-phase2-fullstack"
branch: "001-todo-console-app"
user: "aqsagulllinux"
command: "/sp.specify"
labels: ["spec", "phase2", "fullstack", "nextjs", "fastapi", "monorepo"]
links:
  spec: "specs/002-phase2-fullstack/"
  plan: "null"
  ticket: "null"
  adr: "null"
  pr: "null"
files:
  - "/home/aqsagulllinux/Todo-app/specs/002-phase2-fullstack/overview.md"
  - "/home/aqsagulllinux/Todo-app/specs/002-phase2-fullstack/architecture.md"
  - "/home/aqsagulllinux/Todo-app/specs/002-phase2-fullstack/features/task-crud.md"
  - "/home/aqsagulllinux/Todo-app/specs/002-phase2-fullstack/features/authentication.md"
  - "/home/aqsagulllinux/Todo-app/specs/002-phase2-fullstack/api/rest-endpoints.md"
  - "/home/aqsagulllinux/Todo-app/specs/002-phase2-fullstack/database/schema.md"
  - "/home/aqsagulllinux/Todo-app/specs/002-phase2-fullstack/ui/components.md"
  - "/home/aqsagulllinux/Todo-app/specs/002-phase2-fullstack/ui/pages.md"
  - "/home/aqsagulllinux/Todo-app/frontend/CLAUDE.md"
  - "/home/aqsagulllinux/Todo-app/backend/CLAUDE.md"
tests:
  - "All 8 spec files created"
  - "Monorepo structure defined"
  - "CLAUDE.md files for frontend/backend created"
  - "All tech stack documented"
---

## Prompt

/sp.specify Project: Todo Full-Stack Web Application – Phase II

Objective:
Transform the Phase I console app into a multi-user web application with persistent storage using Claude Code + Spec-Kit Plus. Follow the Agentic Dev Stack workflow: write spec → generate plan → break into tasks → implement via Claude Code (no manual coding).

Target Audience:
- Hackathon evaluators
- Full-stack developers using spec-driven workflows

Success Criteria:
- All 5 basic Todo features fully functional
- RESTful API endpoints implemented
- Responsive frontend interface built
- Data stored in Neon Serverless PostgreSQL
- Authentication via Better Auth with JWT enforced
- API endpoints filter tasks by authenticated user
- All implementation done via Claude Code using structured specs

Functional Requirements:
- Frontend: Next.js 16+ (App Router), responsive UI
- Backend: Python FastAPI, SQLModel ORM
- Authentication: Better Auth with JWT plugin
- REST API Endpoints (6 endpoints)
- API Behavior: JWT auth, user isolation

Constraints:
- No manual coding outside Claude Code workflow
- Persistent storage only in Neon PostgreSQL
- Monorepo structure recommended

Reference Monorepo Structure provided.

## Response snapshot

### Specs Created (8 files)

| Spec File | Purpose | Lines |
|-----------|---------|-------|
| `overview.md` | Project summary, tech stack, success criteria | ~150 |
| `architecture.md` | System design, data flow diagrams | ~350 |
| `features/task-crud.md` | 6 CRUD operations with test cases | ~400 |
| `features/authentication.md` | Auth flow, JWT verification | ~350 |
| `api/rest-endpoints.md` | REST API contract, curl examples | ~350 |
| `database/schema.md` | SQLModel, migrations, queries | ~300 |
| `ui/components.md` | React components, props, styling | ~400 |
| `ui/pages.md` | Page layouts, routing, middleware | ~450 |

### Spec Structure

```
specs/002-phase2-fullstack/
├── overview.md              # Project overview
├── architecture.md          # System architecture
├── features/
│   ├── task-crud.md        # CRUD operations
│   └── authentication.md    # Auth flow
├── api/
│   └── rest-endpoints.md    # API contract
├── database/
│   └── schema.md            # Database design
└── ui/
    ├── components.md        # UI components
    └── pages.md             # Page layouts
```

### CLAUDE.md Files

| File | Purpose |
|------|---------|
| `frontend/CLAUDE.md` | Next.js specific instructions |
| `backend/CLAUDE.md` | FastAPI specific instructions |

### Key Specifications

**API Endpoints:**
- GET/POST `/api/{user_id}/tasks`
- GET/PUT/DELETE `/api/{user_id}/tasks/{id}`
- PATCH `/api/{user_id}/tasks/{id}/complete`
- GET `/health`

**Pages:**
- `/` - Landing page
- `/login` - Login page
- `/register` - Register page
- `/dashboard` - Main task interface (protected)

**Components:**
- Auth: LoginForm, RegisterForm, LogoutButton
- Tasks: TaskList, TaskItem, TaskForm, TaskActions, EmptyState
- UI: Button, Input, Modal, LoadingSpinner, Alert
- Layout: Header, Footer, Container

**Database Schema:**
- `tasks` table with user_id index
- Better Auth tables (user, session, account, verification)

## Outcome

- ✅ Impact: Complete Phase II specification created
- 🧪 Tests: All 8 spec files verified
- 📁 Files: 10 files (8 specs + 2 CLAUDE.md)
- 🔁 Next prompts: `/sp.plan` to create implementation plan
- 🧠 Reflection: Comprehensive specs cover all Phase II requirements

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): All specs complete - PASS
- Prompt variant (if applicable): /sp.specify with monorepo reference
- Next experiment (smallest change to try): Add OpenAPI schema generation
