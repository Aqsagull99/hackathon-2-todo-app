# Phase II: Todo Full-Stack Web Application - Overview

**Spec ID**: 002-phase2-fullstack
**Version**: 1.0.0
**Status**: Draft
**Created**: 2025-12-29
**Author**: Claude Code (spec-driven)

---

## Project Summary

Transform the Phase I in-memory console Todo app into a modern, multi-user web application with persistent storage using spec-driven development (Claude Code + Spec-Kit Plus).

## Objective

Build a full-stack Todo application following the Agentic Dev Stack workflow:
```
write spec → generate plan → break into tasks → implement via Claude Code
```

**No manual coding allowed** - all implementation through Claude Code using structured specs.

## Target Audience

- Hackathon evaluators
- Full-stack developers using spec-driven workflows

## Core Features (5 Basic Todo Operations)

| # | Feature | Description |
|---|---------|-------------|
| 1 | **Add Todo** | Create new task with title, persist to database |
| 2 | **View Todos** | Display authenticated user's tasks with status |
| 3 | **Update Todo** | Modify existing task title/description |
| 4 | **Delete Todo** | Remove task from database permanently |
| 5 | **Mark Complete** | Toggle task completion status |

## Technology Stack

### Frontend
| Technology | Purpose |
|------------|---------|
| Next.js 16+ | App Router, React Server Components |
| TypeScript | Type safety |
| Tailwind CSS | Responsive styling |
| Better Auth Client | Authentication UI |

### Backend
| Technology | Purpose |
|------------|---------|
| Python FastAPI | REST API framework |
| SQLModel | ORM with Pydantic validation |
| asyncpg | Async PostgreSQL driver |
| python-jose | JWT verification |

### Database
| Technology | Purpose |
|------------|---------|
| Neon PostgreSQL | Serverless database |
| Connection pooling | Via Neon pooler endpoint |

### Authentication
| Technology | Purpose |
|------------|---------|
| Better Auth | Auth framework with JWT plugin |
| JWT tokens | Stateless authentication |
| Shared secret | `BETTER_AUTH_SECRET` env var |

## Success Criteria

- [ ] All 5 Todo features fully functional as web app
- [ ] RESTful API endpoints implemented and secured
- [ ] Responsive frontend interface built
- [ ] Data persisted in Neon PostgreSQL
- [ ] Better Auth + JWT authentication enforced
- [ ] API endpoints filter tasks by authenticated user
- [ ] All implementation via Claude Code using specs
- [ ] Complete spec traceability maintained

## Project Structure (Monorepo)

```
Todo-app/
├── specs/002-phase2-fullstack/    # This specification
│   ├── overview.md                # Project overview (this file)
│   ├── architecture.md            # System architecture
│   ├── features/
│   │   ├── task-crud.md          # CRUD operations spec
│   │   └── authentication.md      # Auth flow spec
│   ├── api/
│   │   └── rest-endpoints.md      # API contract
│   ├── database/
│   │   └── schema.md              # Database schema
│   └── ui/
│       ├── components.md          # UI components
│       └── pages.md               # Page layouts
│
├── frontend/                       # Next.js application
│   ├── src/
│   │   ├── app/                   # App Router pages
│   │   ├── components/            # React components
│   │   ├── lib/                   # Utilities, auth
│   │   └── types/                 # TypeScript types
│   ├── CLAUDE.md                  # Frontend instructions
│   └── .env.local                 # Frontend secrets
│
├── backend/                        # FastAPI application
│   ├── app/
│   │   ├── api/                   # Route handlers
│   │   ├── models/                # SQLModel models
│   │   ├── services/              # Business logic
│   │   └── core/                  # Config, security
│   ├── CLAUDE.md                  # Backend instructions
│   └── .env                       # Backend secrets
│
├── src/todo_app/                  # Phase I console app (preserved)
├── CLAUDE.md                      # Root instructions
├── docker-compose.yml             # Local development
└── README.md                      # Setup guide
```

## Constraints

| Constraint | Requirement |
|------------|-------------|
| No manual coding | All code via Claude Code workflow |
| Persistent storage | Neon PostgreSQL only |
| Authentication | Stateless JWT, no server sessions |
| Secrets | Never committed to git |
| Scope | Phase II only (no Phase III features) |

## Related Specifications

| Spec | Description |
|------|-------------|
| [architecture.md](./architecture.md) | System design and data flow |
| [features/task-crud.md](./features/task-crud.md) | CRUD operations |
| [features/authentication.md](./features/authentication.md) | Auth flow |
| [api/rest-endpoints.md](./api/rest-endpoints.md) | API contract |
| [database/schema.md](./database/schema.md) | Database design |
| [ui/components.md](./ui/components.md) | UI components |
| [ui/pages.md](./ui/pages.md) | Page layouts |

## Development Workflow

```
/sp.specify → /sp.plan → /sp.tasks → /sp.implement → /sp.checklist
```

1. **Specify**: Create detailed specs for each component
2. **Plan**: Generate implementation plan from specs
3. **Tasks**: Break plan into testable tasks
4. **Implement**: Execute via Claude Code
5. **Checklist**: Verify against requirements

---

**Next**: See [architecture.md](./architecture.md) for system design.
