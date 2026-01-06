# Phase II Implementation Plan

**Plan ID**: 002-phase2-fullstack/plan
**Version**: 1.0.0
**Status**: Draft
**Created**: 2025-12-29
**Spec Reference**: `specs/002-phase2-fullstack/`

---

## Plan Overview

Transform the Phase I console Todo app into a full-stack web application with:
- **Frontend**: Next.js 16+ (App Router) + Tailwind CSS
- **Backend**: Python FastAPI + SQLModel
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: Better Auth + JWT

## Implementation Phases

```
┌─────────────────────────────────────────────────────────────────────┐
│                    PHASE II IMPLEMENTATION TIMELINE                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Phase 1: Environment Setup                                         │
│  ══════════════════════════                                         │
│  [████████] Milestone 1                                             │
│                                                                     │
│  Phase 2: Backend Implementation                                    │
│  ═══════════════════════════════                                    │
│  [████████████████] Milestone 2                                     │
│                                                                     │
│  Phase 3: Frontend Implementation                                   │
│  ════════════════════════════════                                   │
│  [████████████████████████] Milestone 3                             │
│                                                                     │
│  Phase 4: Integration & Testing                                     │
│  ══════════════════════════════                                     │
│  [████████████████████████████████] Milestone 4                     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Environment Setup ✓ (Partially Complete)

### Objective
Prepare development environment with all dependencies and configurations.

### Status: In Progress

| Task | Status | Notes |
|------|--------|-------|
| Create `frontend/` directory | ✅ Done | Created |
| Create `backend/` directory | ✅ Done | Created |
| Configure `backend/.env` | ✅ Done | Neon + JWT secrets (Expiry: 30m) |
| Configure `frontend/.env.local` | ✅ Done | Better Auth + API URL (Expiry: 30m) |
| Create `.gitignore` | ✅ Done | Protects secrets |
| Initialize Next.js project | ⏳ Pending | `npx create-next-app` |
| Initialize FastAPI project | ⏳ Pending | `pyproject.toml` |
| Install dependencies | ⏳ Pending | npm/uv |

### Tasks Remaining

#### 1.1 Initialize Frontend (Next.js)
```bash
cd ~/Todo-app/frontend
npx create-next-app@latest . --typescript --tailwind --eslint --app --src-dir
npm install better-auth @better-auth/react
```

#### 1.2 Initialize Backend (FastAPI)
```bash
cd ~/Todo-app/backend
uv init
uv add fastapi uvicorn sqlmodel asyncpg python-jose pydantic-settings
```

#### 1.3 Verify Environment
- [ ] Python 3.13+ available
- [ ] Node.js 18+ available
- [ ] Neon database accessible
- [ ] Environment variables loaded correctly

### Deliverables
- [ ] `frontend/package.json` with dependencies
- [ ] `backend/pyproject.toml` with dependencies
- [ ] Both servers start without errors

---

## Phase 2: Backend Implementation

### Objective
Build FastAPI backend with SQLModel ORM and JWT authentication.

### Architecture

```
backend/app/
├── main.py                 # FastAPI app entry
├── api/
│   ├── routes/
│   │   └── tasks.py       # Task CRUD endpoints
│   └── deps.py            # Auth dependencies
├── models/
│   └── task.py            # SQLModel Task model
├── services/
│   └── task_service.py    # Business logic
├── core/
│   ├── config.py          # Settings from env
│   ├── security.py        # JWT verification
│   └── database.py        # Neon connection
└── schemas/
    └── task.py            # Request/Response schemas
```

### Tasks

#### 2.1 Core Setup
| Task | Priority | Spec Reference |
|------|----------|----------------|
| Create `core/config.py` - Settings | High | - |
| Create `core/database.py` - Neon connection | High | `database/schema.md` |
| Create `core/security.py` - JWT verify | High | `features/authentication.md` |

#### 2.2 Models & Schemas
| Task | Priority | Spec Reference |
|------|----------|----------------|
| Create `models/task.py` - SQLModel | High | `database/schema.md` |
| Create `schemas/task.py` - Pydantic | High | `api/rest-endpoints.md` |

#### 2.3 Services
| Task | Priority | Spec Reference |
|------|----------|----------------|
| Create `task_service.py` - CRUD logic | High | `features/task-crud.md` |
| Implement `create_task()` | High | `features/task-crud.md` |
| Implement `get_tasks()` | High | `features/task-crud.md` |
| Implement `get_task()` | High | `features/task-crud.md` |
| Implement `update_task()` | High | `features/task-crud.md` |
| Implement `delete_task()` | High | `features/task-crud.md` |
| Implement `toggle_complete()` | High | `features/task-crud.md` |

#### 2.4 API Routes
| Task | Priority | Spec Reference |
|------|----------|----------------|
| Create `api/deps.py` - Dependencies | High | `features/authentication.md` |
| Create `api/routes/tasks.py` | High | `api/rest-endpoints.md` |
| GET `/api/{user_id}/tasks` | High | `api/rest-endpoints.md` |
| POST `/api/{user_id}/tasks` | High | `api/rest-endpoints.md` |
| GET `/api/{user_id}/tasks/{id}` | High | `api/rest-endpoints.md` |
| PUT `/api/{user_id}/tasks/{id}` | High | `api/rest-endpoints.md` |
| DELETE `/api/{user_id}/tasks/{id}` | High | `api/rest-endpoints.md` |
| PATCH `/api/{user_id}/tasks/{id}/complete` | High | `api/rest-endpoints.md` |
| GET `/health` | Medium | `api/rest-endpoints.md` |

#### 2.5 Main App
| Task | Priority | Spec Reference |
|------|----------|----------------|
| Create `main.py` - FastAPI app | High | - |
| Configure CORS | High | - |
| Register routes | High | - |
| Add startup event (init DB) | Medium | `database/schema.md` |

### Deliverables
- [ ] FastAPI server runs on port 8000
- [ ] All 6 task endpoints functional
- [ ] JWT verification working
- [ ] Database operations successful
- [ ] Swagger docs at `/docs`

---

## Phase 3: Frontend Implementation

### Objective
Build Next.js frontend with Better Auth and task management UI.

### Architecture

```
frontend/src/
├── app/
│   ├── layout.tsx          # Root layout
│   ├── page.tsx            # Landing (/)
│   ├── login/page.tsx      # Login
│   ├── register/page.tsx   # Register
│   ├── dashboard/page.tsx  # Tasks (protected)
│   └── api/auth/[...all]/route.ts  # Better Auth
├── components/
│   ├── auth/               # Auth components
│   ├── tasks/              # Task components
│   └── ui/                 # UI primitives
├── lib/
│   ├── auth.ts             # Better Auth server
│   ├── auth-client.ts      # Better Auth client
│   └── api.ts              # Backend API client
└── middleware.ts           # Route protection
```

### Tasks

#### 3.1 Auth Setup
| Task | Priority | Spec Reference |
|------|----------|----------------|
| Create `lib/auth.ts` - Better Auth config | High | `features/authentication.md` |
| Create `lib/auth-client.ts` - Client | High | `features/authentication.md` |
| Create `api/auth/[...all]/route.ts` | High | `features/authentication.md` |
| Create `middleware.ts` - Route protection | High | `ui/pages.md` |

#### 3.2 UI Components
| Task | Priority | Spec Reference |
|------|----------|----------------|
| Create `ui/Button.tsx` | High | `ui/components.md` |
| Create `ui/Input.tsx` | High | `ui/components.md` |
| Create `ui/Modal.tsx` | High | `ui/components.md` |
| Create `ui/LoadingSpinner.tsx` | Medium | `ui/components.md` |
| Create `ui/Alert.tsx` | Medium | `ui/components.md` |

#### 3.3 Auth Components
| Task | Priority | Spec Reference |
|------|----------|----------------|
| Create `auth/LoginForm.tsx` | High | `ui/components.md` |
| Create `auth/RegisterForm.tsx` | High | `ui/components.md` |
| Create `auth/LogoutButton.tsx` | High | `ui/components.md` |

#### 3.4 Task Components
| Task | Priority | Spec Reference |
|------|----------|----------------|
| Create `tasks/TaskList.tsx` | High | `ui/components.md` |
| Create `tasks/TaskItem.tsx` | High | `ui/components.md` |
| Create `tasks/TaskForm.tsx` | High | `ui/components.md` |
| Create `tasks/TaskActions.tsx` | Medium | `ui/components.md` |
| Create `tasks/EmptyState.tsx` | Medium | `ui/components.md` |

#### 3.5 Pages
| Task | Priority | Spec Reference |
|------|----------|----------------|
| Create `app/layout.tsx` | High | `ui/pages.md` |
| Create `app/page.tsx` - Landing | High | `ui/pages.md` |
| Create `app/login/page.tsx` | High | `ui/pages.md` |
| Create `app/register/page.tsx` | High | `ui/pages.md` |
| Create `app/dashboard/page.tsx` | High | `ui/pages.md` |

#### 3.6 API Client
| Task | Priority | Spec Reference |
|------|----------|----------------|
| Create `lib/api.ts` - Backend client | High | `api/rest-endpoints.md` |
| Implement `getTasks()` | High | - |
| Implement `createTask()` | High | - |
| Implement `updateTask()` | High | - |
| Implement `deleteTask()` | High | - |
| Implement `toggleComplete()` | High | - |

### Deliverables
- [ ] Next.js server runs on port 3000
- [ ] Landing, Login, Register pages working
- [ ] Dashboard with task CRUD functional
- [ ] Better Auth authentication working
- [ ] Responsive design implemented

---

## Phase 4: Integration & Testing

### Objective
Integrate frontend and backend, test all flows, prepare for submission.

### Tasks

#### 4.1 Integration Testing
| Task | Priority | Notes |
|------|----------|-------|
| Test registration flow | High | End-to-end |
| Test login flow | High | End-to-end |
| Test task creation | High | End-to-end |
| Test task listing | High | End-to-end |
| Test task update | High | End-to-end |
| Test task deletion | High | End-to-end |
| Test task completion toggle | High | End-to-end |
| Test logout flow | High | End-to-end |

#### 4.2 Security Testing
| Task | Priority | Notes |
|------|----------|-------|
| Test 401 without JWT | High | API security |
| Test 403 wrong user_id | High | User isolation |
| Test JWT expiration | Medium | Token lifecycle |

#### 4.3 Database Testing
| Task | Priority | Notes |
|------|----------|-------|
| Verify data persistence | High | Neon DB |
| Test user isolation | High | SQL queries |
| Check indexes performance | Medium | Query optimization |

#### 4.4 UI/UX Testing
| Task | Priority | Notes |
|------|----------|-------|
| Test responsive design | High | Mobile/desktop |
| Test loading states | Medium | User feedback |
| Test error handling | Medium | Error messages |

#### 4.5 Documentation
| Task | Priority | Notes |
|------|----------|-------|
| Update README.md | High | Setup instructions |
| Verify all specs complete | High | Traceability |
| Create demo screenshots | Medium | Hackathon submission |

### Deliverables
- [ ] All user flows working end-to-end
- [ ] No security vulnerabilities
- [ ] Data persists correctly
- [ ] UI responsive and functional
- [ ] Documentation complete

---

## Risk Analysis

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Better Auth config issues | Medium | High | Follow official docs, use MCP |
| Neon connection problems | Low | High | Test connection early |
| JWT secret mismatch | Medium | High | Verify env vars match |
| CORS errors | Medium | Medium | Configure properly in FastAPI |
| Type errors | Medium | Low | Use TypeScript strict mode |

---

## Dependencies

```
Phase 1 (Setup)
    │
    ├──→ Phase 2 (Backend)
    │         │
    │         └──→ Phase 4 (Integration)
    │                    ↑
    └──→ Phase 3 (Frontend)
              │
              └─────────────┘
```

**Critical Path**: Phase 1 → Phase 2 → Phase 4

---

## Success Criteria

### Must Have (P0)
- [ ] User can register and login
- [ ] User can create, view, update, delete tasks
- [ ] User can mark tasks complete/incomplete
- [ ] Tasks persist in Neon PostgreSQL
- [ ] Users can only see their own tasks

### Should Have (P1)
- [ ] Responsive mobile design
- [ ] Loading states and error handling
- [ ] Clean, intuitive UI

### Nice to Have (P2)
- [ ] Task filtering (all/completed/pending)
- [ ] Task sorting (newest/oldest)
- [ ] Animations and transitions

---

## Definition of Done

- [ ] Frontend runs on localhost:3000
- [ ] Backend runs on localhost:8000
- [ ] All 5 Todo features functional
- [ ] JWT authentication working
- [ ] User isolation enforced
- [ ] Data persists in Neon DB
- [ ] Specs maintained and versioned
- [ ] PHR records created
- [ ] Ready for hackathon submission

---

## Next Steps

After plan approval, proceed to `/sp.tasks` to generate detailed task breakdown.

---

**Previous**: [overview.md](./overview.md)
**Next**: [tasks.md](./tasks.md) (to be created)
