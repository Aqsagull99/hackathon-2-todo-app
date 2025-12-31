# Todo Web Application Constitution (Phase II)
<!-- Official Governance for Phase II Full-Stack Implementation -->

## 1. Project Vision
**Objective**: Build a modern, multi-user Todo Web Application with a split architecture (Next.js Frontend / FastAPI Backend) and persistent storage (Neon PostgreSQL).

## 2. Technology Stack (Strict)
- **Frontend**: Next.js 16 (App Router), TypeScript, Tailwind CSS, Better Auth Client.
- **Backend**: Python 3.13+, FastAPI, SQLModel (ORM), JWT Security.
- **Database**: Neon Serverless PostgreSQL (Async via asyncpg).
- **Tooling**: UV (Python package manager), Claude Code (AI Implementation).

## 3. Core Development Principles
1. **Spec-First**: No code is written until a specification (`specs/`) is approved.
2. **User Isolation**: Users must ONLY see their own tasks. Filter by `user_id` on every query.
3. **Stateless Auth**: Every API request must be authenticated via a Bearer JWT token.
4. **Agentic Workflow**: Use specialized agents (Backend, Frontend, Database) via Claude Code Task tool.

## 4. Architectural Requirements
- **Frontend/Backend Separation**: The frontend communicates with the backend only via REST API.
- **Strict Typing**: Use TypeScript interfaces on frontend and Pydantic/SQLModel models on backend.
- **Environment Safety**: Secrets (DB keys, Auth secrets) must stay in `.env` and never be committed.

## 5. Security Standards
- **401 Unauthorized**: Missing or invalid token.
- **403 Forbidden**: Trying to access another user's task ID.
- **JWT Verification**: Backend must verify JWT signature using `BETTER_AUTH_SECRET`.

## 6. Project Structure
```
/Todo-app/
├── frontend/         # Next.js workspace
├── backend/          # FastAPI workspace
├── specs/            # Phase 2 Specifications (002, 003)
├── history/          # Phase 2 Prompt History (018+)
├── .specify/         # Phase 2 Constitution & Memory
└── CLAUDE.md         # Phase 2 Claude Code Instructions
```

## 7. Success Criteria
- [ ] End-to-end user authentication (Sign up / Login).
- [ ] Persistent CRUD (tasks saved in Postgres cloud).
- [ ] Responsive UI (Desktop and Mobile).
- [ ] Fully documented spec-to-task traceability.

---
**Version**: 2.2.0 | **Status**: ACTIVE | **Phase**: II
