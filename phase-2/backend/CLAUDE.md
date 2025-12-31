# Claude Code Rules - Backend

This file provides Claude Code instructions for the FastAPI backend application.

## Project Overview

**Project**: Todo App Backend (Phase II)
**Framework**: Python FastAPI
**ORM**: SQLModel
**Database**: Neon PostgreSQL
**Authentication**: JWT verification

## How to Run

```bash
cd ~/Todo-app/backend
uv venv
source .venv/bin/activate
uv pip install -e .
uvicorn app.main:app --reload --port 8000
```

Server runs at: http://localhost:8000
API docs at: http://localhost:8000/docs

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   └── tasks.py     # Task CRUD endpoints
│   │   └── deps.py          # Dependencies
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py          # SQLModel models
│   ├── services/
│   │   ├── __init__.py
│   │   └── task_service.py  # Business logic
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py        # Settings
│   │   ├── security.py      # JWT verification
│   │   └── database.py      # DB connection
│   └── schemas/
│       ├── __init__.py
│       └── task.py          # Pydantic schemas
├── .env                     # Environment variables
├── .env.example             # Template
└── pyproject.toml           # Package config
```

## Key Files

| File | Purpose |
|------|---------|
| `app/main.py` | FastAPI app setup |
| `app/api/routes/tasks.py` | Task CRUD endpoints |
| `app/core/security.py` | JWT verification |
| `app/core/database.py` | Neon connection |
| `app/models/task.py` | SQLModel Task model |

## Environment Variables

```bash
# .env
DATABASE_URL="postgresql+asyncpg://..."
NEON_PROJECT_ID="your-project-id"
JWT_SECRET="same-as-frontend"
JWT_ALGORITHM="HS256"
BACKEND_PORT=8000
FRONTEND_URL="http://localhost:3000"
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/{user_id}/tasks` | List tasks |
| POST | `/api/{user_id}/tasks` | Create task |
| GET | `/api/{user_id}/tasks/{id}` | Get task |
| PUT | `/api/{user_id}/tasks/{id}` | Update task |
| DELETE | `/api/{user_id}/tasks/{id}` | Delete task |
| PATCH | `/api/{user_id}/tasks/{id}/complete` | Toggle completion |
| GET | `/health` | Health check |

## Specifications

Read these specs before implementing:
- `specs/002-phase2-fullstack/api/rest-endpoints.md` - API contract
- `specs/002-phase2-fullstack/database/schema.md` - Database schema
- `specs/002-phase2-fullstack/features/task-crud.md` - CRUD operations
- `specs/002-phase2-fullstack/features/authentication.md` - JWT verification

## MCP Servers

Use these MCP servers for documentation:
- **context7**: FastAPI, SQLModel, Pydantic docs
- **neon**: Database operations, schema management

## Coding Standards

- Use type hints for all functions
- Use async/await for database operations
- Implement proper error handling
- Follow SQLModel patterns for models
- Use Pydantic for request/response schemas
- Add docstrings for public APIs

## Common Patterns

### Route with JWT Auth
```python
@router.get("/{user_id}/tasks")
async def list_tasks(
    user_id: str,
    current_user_id: str = Depends(verify_user_access),
    session: AsyncSession = Depends(get_session)
):
    tasks = await task_service.get_user_tasks(session, user_id)
    return tasks
```

### SQLModel Query
```python
async def get_user_tasks(session: AsyncSession, user_id: str):
    statement = select(Task).where(Task.user_id == user_id)
    result = await session.execute(statement)
    return result.scalars().all()
```

### JWT Verification
```python
async def verify_jwt(credentials: HTTPAuthorizationCredentials):
    token = credentials.credentials
    payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    return payload
```

## Testing

```bash
# Run tests
pytest

# Type check
mypy app/

# Lint
ruff check app/
```

## Database Migrations

```bash
# Create migration
alembic revision --autogenerate -m "description"

# Run migrations
alembic upgrade head
```
