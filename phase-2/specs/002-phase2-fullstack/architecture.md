# Phase II: System Architecture

**Spec ID**: 002-phase2-fullstack/architecture
**Version**: 1.0.0
**Status**: Draft
**Created**: 2025-12-29

---

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                            │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Next.js 16+ (App Router)                    │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────────────────┐   │   │
│  │  │  Pages   │  │Components│  │   Better Auth Client │   │   │
│  │  └────┬─────┘  └────┬─────┘  └──────────┬───────────┘   │   │
│  │       │              │                   │               │   │
│  │       └──────────────┴───────────────────┘               │   │
│  │                      │                                    │   │
│  │              ┌───────▼───────┐                           │   │
│  │              │  API Client   │                           │   │
│  │              │ (fetch + JWT) │                           │   │
│  │              └───────┬───────┘                           │   │
│  └──────────────────────┼───────────────────────────────────┘   │
│                         │ HTTP + JWT Bearer Token               │
└─────────────────────────┼───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                         API LAYER                               │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  FastAPI Backend                         │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │   │
│  │  │ JWT Verify   │  │   Routes     │  │  Services    │   │   │
│  │  │ Middleware   │──│ /api/tasks   │──│ Task CRUD    │   │   │
│  │  └──────────────┘  └──────────────┘  └──────┬───────┘   │   │
│  │                                              │           │   │
│  │                                     ┌────────▼────────┐  │   │
│  │                                     │ SQLModel ORM    │  │   │
│  │                                     └────────┬────────┘  │   │
│  └──────────────────────────────────────────────┼───────────┘   │
│                                                 │               │
└─────────────────────────────────────────────────┼───────────────┘
                                                  │
                                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                       DATA LAYER                                │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Neon Serverless PostgreSQL                  │   │
│  │  ┌──────────────────────────────────────────────────┐   │   │
│  │  │                    tasks                          │   │   │
│  │  │  id | user_id | title | completed | timestamps   │   │   │
│  │  └──────────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Frontend (Next.js 16+)

| Component | Technology | Responsibility |
|-----------|------------|----------------|
| App Router | Next.js 16 | Page routing, SSR/RSC |
| Components | React + TypeScript | Reusable UI elements |
| Auth Client | Better Auth | Login/Register/Session |
| API Client | fetch | HTTP requests with JWT |
| Styling | Tailwind CSS | Responsive design |

**Key Files:**
```
frontend/src/
├── app/
│   ├── layout.tsx          # Root layout with auth provider
│   ├── page.tsx            # Landing/redirect page
│   ├── login/page.tsx      # Login page
│   ├── register/page.tsx   # Register page
│   └── dashboard/
│       └── page.tsx        # Main todo interface
├── components/
│   ├── auth/
│   │   ├── LoginForm.tsx
│   │   └── RegisterForm.tsx
│   ├── tasks/
│   │   ├── TaskList.tsx
│   │   ├── TaskItem.tsx
│   │   ├── TaskForm.tsx
│   │   └── TaskActions.tsx
│   └── ui/
│       ├── Button.tsx
│       ├── Input.tsx
│       └── Modal.tsx
└── lib/
    ├── auth.ts             # Better Auth config
    ├── api.ts              # API client with JWT
    └── types.ts            # TypeScript interfaces
```

### 2. Backend (FastAPI)

| Component | Technology | Responsibility |
|-----------|------------|----------------|
| Framework | FastAPI | REST API, async support |
| ORM | SQLModel | Database models, queries |
| Auth | python-jose | JWT verification |
| Database | asyncpg | Async PostgreSQL driver |
| Config | pydantic-settings | Environment management |

**Key Files:**
```
backend/app/
├── main.py                 # FastAPI app entry
├── api/
│   ├── __init__.py
│   ├── routes/
│   │   ├── __init__.py
│   │   └── tasks.py        # Task CRUD endpoints
│   └── deps.py             # Dependencies (auth, db)
├── models/
│   ├── __init__.py
│   └── task.py             # SQLModel Task model
├── services/
│   ├── __init__.py
│   └── task_service.py     # Business logic
├── core/
│   ├── __init__.py
│   ├── config.py           # Settings from env
│   ├── security.py         # JWT verification
│   └── database.py         # DB connection
└── schemas/
    ├── __init__.py
    └── task.py             # Pydantic schemas
```

### 3. Database (Neon PostgreSQL)

| Table | Purpose |
|-------|---------|
| tasks | Store user tasks with completion status |

**Connection:**
- Pooled connection via Neon pooler endpoint
- Async driver (asyncpg) for non-blocking I/O
- Connection string from `DATABASE_URL` env var

## Authentication Flow

```
┌────────┐     ┌─────────────┐     ┌─────────┐     ┌──────────┐
│ User   │     │  Frontend   │     │ Backend │     │  Neon DB │
└───┬────┘     └──────┬──────┘     └────┬────┘     └────┬─────┘
    │                 │                 │               │
    │ 1. Login/Register                 │               │
    │────────────────>│                 │               │
    │                 │                 │               │
    │                 │ 2. Better Auth  │               │
    │                 │    handles auth │               │
    │                 │                 │               │
    │ 3. JWT Token    │                 │               │
    │<────────────────│                 │               │
    │                 │                 │               │
    │ 4. Request + JWT│                 │               │
    │────────────────>│                 │               │
    │                 │ 5. API Call     │               │
    │                 │   + JWT Header  │               │
    │                 │────────────────>│               │
    │                 │                 │               │
    │                 │                 │ 6. Verify JWT │
    │                 │                 │    Extract    │
    │                 │                 │    user_id    │
    │                 │                 │               │
    │                 │                 │ 7. Query DB   │
    │                 │                 │   WHERE       │
    │                 │                 │   user_id=X   │
    │                 │                 │──────────────>│
    │                 │                 │               │
    │                 │                 │ 8. Results    │
    │                 │                 │<──────────────│
    │                 │                 │               │
    │                 │ 9. Response     │               │
    │                 │<────────────────│               │
    │                 │                 │               │
    │ 10. Display     │                 │               │
    │<────────────────│                 │               │
    │                 │                 │               │
```

## Security Architecture

### JWT Token Structure

```json
{
  "header": {
    "alg": "HS256",
    "typ": "JWT"
  },
  "payload": {
    "sub": "user_id_here",
    "email": "user@example.com",
    "iat": 1735488000,
    "exp": 1735491600
  },
  "signature": "HMACSHA256(header + payload, BETTER_AUTH_SECRET)"
}
```

### Security Measures

| Layer | Protection |
|-------|------------|
| Frontend | JWT stored in httpOnly cookie or memory |
| API | JWT verification on every request |
| Database | User isolation via `user_id` filtering |
| Network | HTTPS in production |
| Secrets | Environment variables, never in code |

### Error Responses

| Status | Condition | Response |
|--------|-----------|----------|
| 401 | No token provided | `{"detail": "Not authenticated"}` |
| 401 | Invalid/expired token | `{"detail": "Invalid token"}` |
| 403 | Wrong user_id | `{"detail": "Access denied"}` |
| 404 | Task not found | `{"detail": "Task not found"}` |

## Data Flow Examples

### Create Task

```
Frontend                    Backend                     Database
   │                           │                           │
   │ POST /api/{user_id}/tasks │                           │
   │ Authorization: Bearer JWT │                           │
   │ Body: {title, description}│                           │
   │──────────────────────────>│                           │
   │                           │                           │
   │                           │ 1. Verify JWT             │
   │                           │ 2. Check user_id match    │
   │                           │ 3. Validate request body  │
   │                           │                           │
   │                           │ INSERT INTO tasks         │
   │                           │──────────────────────────>│
   │                           │                           │
   │                           │ Return new task           │
   │                           │<──────────────────────────│
   │                           │                           │
   │ 201 Created               │                           │
   │ Body: {id, title, ...}    │                           │
   │<──────────────────────────│                           │
```

### List Tasks

```
Frontend                    Backend                     Database
   │                           │                           │
   │ GET /api/{user_id}/tasks  │                           │
   │ Authorization: Bearer JWT │                           │
   │──────────────────────────>│                           │
   │                           │                           │
   │                           │ 1. Verify JWT             │
   │                           │ 2. Check user_id match    │
   │                           │                           │
   │                           │ SELECT * FROM tasks       │
   │                           │ WHERE user_id = ?         │
   │                           │──────────────────────────>│
   │                           │                           │
   │                           │ Return tasks array        │
   │                           │<──────────────────────────│
   │                           │                           │
   │ 200 OK                    │                           │
   │ Body: [{task1}, {task2}]  │                           │
   │<──────────────────────────│                           │
```

## Environment Configuration

### Backend (.env)

```bash
# Database
DATABASE_URL="postgresql+asyncpg://user:pass@host/db?sslmode=require"
NEON_PROJECT_ID="project-id"

# JWT
JWT_SECRET="shared-secret-with-frontend"
JWT_ALGORITHM="HS256"
JWT_EXPIRATION_MINUTES=30

# Server
BACKEND_HOST="0.0.0.0"
BACKEND_PORT=8000
DEBUG=true

# CORS
FRONTEND_URL="http://localhost:3000"
```

### Frontend (.env.local)

```bash
# Better Auth
BETTER_AUTH_SECRET="shared-secret-with-backend"
BETTER_AUTH_URL="http://localhost:3000"

# API
NEXT_PUBLIC_API_URL="http://localhost:8000"

# Database (for Better Auth)
DATABASE_URL="postgresql://user:pass@host/db?sslmode=require"
```

## Deployment Topology

### Development

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ Next.js Dev     │     │ FastAPI Dev     │     │ Neon Cloud      │
│ localhost:3000  │────>│ localhost:8000  │────>│ (Remote)        │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

### Production (Future)

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ Vercel          │     │ Railway/Render  │     │ Neon Cloud      │
│ (Frontend)      │────>│ (Backend)       │────>│ (Database)      │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

---

**Previous**: [overview.md](./overview.md)
**Next**: [features/task-crud.md](./features/task-crud.md)
