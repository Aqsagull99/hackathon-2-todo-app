# Phase II: Task Breakdown

**Tasks ID**: 002-phase2-fullstack/tasks
**Version**: 1.0.0
**Status**: Active
**Created**: 2025-12-29
**Plan Reference**: `specs/002-phase2-fullstack/plan.md`

---

## Task Summary

| Phase | Tasks | Status |
|-------|-------|--------|
| Phase 1: Environment Setup | 8 | 5 Done, 3 Pending |
| Phase 2: Backend | 25 | Pending |
| Phase 3: Frontend | 28 | Pending |
| Phase 4: Integration | 12 | Pending |
| **Total** | **73** | **5 Done, 68 Pending** |

---

## Phase 1: Environment Setup

### 1.1 Project Initialization (5/8 Done)

| # | Task | Status | Test |
|---|------|--------|------|
| 1.1.1 | Create `frontend/` directory | ✅ Done | Directory exists |
| 1.1.2 | Create `backend/` directory | ✅ Done | Directory exists |
| 1.1.3 | Create `backend/.env` with Neon credentials | ✅ Done | Contains DATABASE_URL |
| 1.1.4 | Create `frontend/.env.local` with Better Auth | ✅ Done | Contains BETTER_AUTH_SECRET |
| 1.1.5 | Create `.gitignore` for env files | ✅ Done | .env files ignored |
| 1.1.6 | Initialize Next.js project | ⏳ Pending | `package.json` exists |
| 1.1.7 | Initialize FastAPI project | ⏳ Pending | `pyproject.toml` exists |
| 1.1.8 | Verify both servers start | ⏳ Pending | No startup errors |

### 1.1.6 Initialize Next.js

```bash
cd ~/Todo-app/frontend
npx create-next-app@latest . --typescript --tailwind --eslint --app --src-dir --no-git
npm install better-auth @better-auth/react
```

**Acceptance Criteria:**
- [ ] `package.json` created with dependencies
- [ ] `src/app/` directory exists
- [ ] `tailwind.config.ts` exists
- [ ] `npm run dev` starts server on port 3000

### 1.1.7 Initialize FastAPI

```bash
cd ~/Todo-app/backend
uv init --name todo-backend
uv add fastapi "uvicorn[standard]" sqlmodel asyncpg python-jose "pydantic-settings"
```

**Acceptance Criteria:**
- [ ] `pyproject.toml` created with dependencies
- [ ] Virtual environment created
- [ ] `uvicorn app.main:app --reload` starts (after main.py)

### 1.1.8 Verify Environment

**Acceptance Criteria:**
- [ ] `python --version` shows 3.13+
- [ ] `node --version` shows 18+
- [ ] Neon database connection works
- [ ] Environment variables load correctly

---

## Phase 2: Backend Implementation

### 2.1 Core Setup (5 Tasks)

| # | Task | Priority | Spec Reference |
|---|------|----------|----------------|
| 2.1.1 | Create `app/__init__.py` | High | - |
| 2.1.2 | Create `app/core/config.py` | High | - |
| 2.1.3 | Create `app/core/database.py` | High | `database/schema.md` |
| 2.1.4 | Create `app/core/security.py` | High | `features/authentication.md` |
| 2.1.5 | Create `app/core/__init__.py` | High | - |

#### 2.1.2 Create config.py

```python
# app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    FRONTEND_URL: str = "http://localhost:3000"

    class Config:
        env_file = ".env"

settings = Settings()
```

**Test:**
```python
from app.core.config import settings
assert settings.DATABASE_URL is not None
assert settings.JWT_SECRET is not None
```

#### 2.1.3 Create database.py

```python
# app/core/database.py
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from .config import settings

async_engine = create_async_engine(settings.DATABASE_URL, echo=True)
async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

async def get_session():
    async with async_session() as session:
        yield session

async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
```

**Test:**
```python
# Connection to Neon works
async with async_engine.connect() as conn:
    result = await conn.execute(text("SELECT 1"))
    assert result.scalar() == 1
```

#### 2.1.4 Create security.py

```python
# app/core/security.py
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from .config import settings

security = HTTPBearer()

async def verify_jwt(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

async def get_current_user_id(payload: dict = Depends(verify_jwt)):
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    return user_id

async def verify_user_access(user_id: str, current_user_id: str = Depends(get_current_user_id)):
    if user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    return current_user_id
```

**Test:**
```python
# Valid JWT passes
# Invalid JWT returns 401
# Wrong user_id returns 403
```

---

### 2.2 Models & Schemas (4 Tasks)

| # | Task | Priority | Spec Reference |
|---|------|----------|----------------|
| 2.2.1 | Create `app/models/__init__.py` | High | - |
| 2.2.2 | Create `app/models/task.py` | High | `database/schema.md` |
| 2.2.3 | Create `app/schemas/__init__.py` | High | - |
| 2.2.4 | Create `app/schemas/task.py` | High | `api/rest-endpoints.md` |

#### 2.2.2 Create models/task.py

```python
# app/models/task.py
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    title: str = Field(max_length=255)
    description: Optional[str] = None
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

**Test:**
```python
task = Task(user_id="user123", title="Test")
assert task.completed == False
assert task.user_id == "user123"
```

#### 2.2.4 Create schemas/task.py

```python
# app/schemas/task.py
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)

class TaskResponse(BaseModel):
    id: int
    user_id: str
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```

---

### 2.3 Services (7 Tasks)

| # | Task | Priority | Spec Reference |
|---|------|----------|----------------|
| 2.3.1 | Create `app/services/__init__.py` | High | - |
| 2.3.2 | Create `app/services/task_service.py` | High | `features/task-crud.md` |
| 2.3.3 | Implement `create_task()` | High | `features/task-crud.md` |
| 2.3.4 | Implement `get_tasks()` | High | `features/task-crud.md` |
| 2.3.5 | Implement `get_task()` | High | `features/task-crud.md` |
| 2.3.6 | Implement `update_task()` | High | `features/task-crud.md` |
| 2.3.7 | Implement `delete_task()` | High | `features/task-crud.md` |

#### 2.3.2 Create task_service.py

```python
# app/services/task_service.py
from datetime import datetime
from typing import Optional, List
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate

async def create_task(session: AsyncSession, user_id: str, data: TaskCreate) -> Task:
    task = Task(user_id=user_id, **data.model_dump())
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task

async def get_tasks(session: AsyncSession, user_id: str) -> List[Task]:
    statement = select(Task).where(Task.user_id == user_id).order_by(Task.created_at.desc())
    result = await session.execute(statement)
    return result.scalars().all()

async def get_task(session: AsyncSession, user_id: str, task_id: int) -> Optional[Task]:
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    result = await session.execute(statement)
    return result.scalar_one_or_none()

async def update_task(session: AsyncSession, task: Task, data: TaskUpdate) -> Task:
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(task, key, value)
    task.updated_at = datetime.utcnow()
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task

async def delete_task(session: AsyncSession, task: Task) -> None:
    await session.delete(task)
    await session.commit()

async def toggle_complete(session: AsyncSession, task: Task) -> Task:
    task.completed = not task.completed
    task.updated_at = datetime.utcnow()
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task
```

**Tests:**
```gherkin
Given a user "user123"
When I create task with title "Buy groceries"
Then task is saved with user_id "user123"
And completed is False

Given task with id 1 exists for "user123"
When I get tasks for "user123"
Then I receive list containing task with id 1

Given task with id 1 exists for "user123"
When I update task 1 with title "New title"
Then task.title is "New title"
And task.updated_at is updated
```

---

### 2.4 API Routes (8 Tasks)

| # | Task | Priority | Spec Reference |
|---|------|----------|----------------|
| 2.4.1 | Create `app/api/__init__.py` | High | - |
| 2.4.2 | Create `app/api/deps.py` | High | - |
| 2.4.3 | Create `app/api/routes/__init__.py` | High | - |
| 2.4.4 | Create `app/api/routes/tasks.py` | High | `api/rest-endpoints.md` |
| 2.4.5 | Implement GET `/api/{user_id}/tasks` | High | `api/rest-endpoints.md` |
| 2.4.6 | Implement POST `/api/{user_id}/tasks` | High | `api/rest-endpoints.md` |
| 2.4.7 | Implement GET/PUT/DELETE `/api/{user_id}/tasks/{id}` | High | `api/rest-endpoints.md` |
| 2.4.8 | Implement PATCH `/api/{user_id}/tasks/{id}/complete` | High | `api/rest-endpoints.md` |

#### 2.4.4 Create routes/tasks.py

```python
# app/api/routes/tasks.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.core.security import verify_user_access
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.services import task_service

router = APIRouter(prefix="/api", tags=["tasks"])

@router.get("/{user_id}/tasks", response_model=List[TaskResponse])
async def list_tasks(
    user_id: str,
    current_user: str = Depends(verify_user_access),
    session: AsyncSession = Depends(get_session)
):
    return await task_service.get_tasks(session, user_id)

@router.post("/{user_id}/tasks", response_model=TaskResponse, status_code=201)
async def create_task(
    user_id: str,
    data: TaskCreate,
    current_user: str = Depends(verify_user_access),
    session: AsyncSession = Depends(get_session)
):
    return await task_service.create_task(session, user_id, data)

@router.get("/{user_id}/tasks/{task_id}", response_model=TaskResponse)
async def get_task(
    user_id: str,
    task_id: int,
    current_user: str = Depends(verify_user_access),
    session: AsyncSession = Depends(get_session)
):
    task = await task_service.get_task(session, user_id, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{user_id}/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    user_id: str,
    task_id: int,
    data: TaskUpdate,
    current_user: str = Depends(verify_user_access),
    session: AsyncSession = Depends(get_session)
):
    task = await task_service.get_task(session, user_id, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return await task_service.update_task(session, task, data)

@router.delete("/{user_id}/tasks/{task_id}", status_code=204)
async def delete_task(
    user_id: str,
    task_id: int,
    current_user: str = Depends(verify_user_access),
    session: AsyncSession = Depends(get_session)
):
    task = await task_service.get_task(session, user_id, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    await task_service.delete_task(session, task)

@router.patch("/{user_id}/tasks/{task_id}/complete", response_model=TaskResponse)
async def toggle_complete(
    user_id: str,
    task_id: int,
    current_user: str = Depends(verify_user_access),
    session: AsyncSession = Depends(get_session)
):
    task = await task_service.get_task(session, user_id, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return await task_service.toggle_complete(session, task)
```

**Tests:**
```bash
# List tasks
curl -X GET "http://localhost:8000/api/user123/tasks" -H "Authorization: Bearer <token>"

# Create task
curl -X POST "http://localhost:8000/api/user123/tasks" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"title": "Test task"}'

# Toggle complete
curl -X PATCH "http://localhost:8000/api/user123/tasks/1/complete" \
  -H "Authorization: Bearer <token>"
```

---

### 2.5 Main App (1 Task)

| # | Task | Priority | Spec Reference |
|---|------|----------|----------------|
| 2.5.1 | Create `app/main.py` | High | - |

#### 2.5.1 Create main.py

```python
# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import init_db
from app.api.routes import tasks

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(title="Todo API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tasks.router)

@app.get("/health")
async def health():
    return {"status": "healthy"}
```

**Test:**
```bash
uvicorn app.main:app --reload --port 8000
curl http://localhost:8000/health
# {"status": "healthy"}
```

---

## Phase 3: Frontend Implementation

### 3.1 Auth Setup (5 Tasks)

| # | Task | Priority | Spec Reference |
|---|------|----------|----------------|
| 3.1.1 | Create `src/lib/auth.ts` | High | `features/authentication.md` |
| 3.1.2 | Create `src/lib/auth-client.ts` | High | `features/authentication.md` |
| 3.1.3 | Create `src/app/api/auth/[...all]/route.ts` | High | `features/authentication.md` |
| 3.1.4 | Create `src/middleware.ts` | High | `ui/pages.md` |
| 3.1.5 | Create `src/types/index.ts` | High | - |

### 3.2 UI Components (8 Tasks)

| # | Task | Priority | Spec Reference |
|---|------|----------|----------------|
| 3.2.1 | Create `components/ui/Button.tsx` | High | `ui/components.md` |
| 3.2.2 | Create `components/ui/Input.tsx` | High | `ui/components.md` |
| 3.2.3 | Create `components/ui/Modal.tsx` | High | `ui/components.md` |
| 3.2.4 | Create `components/ui/LoadingSpinner.tsx` | Medium | `ui/components.md` |
| 3.2.5 | Create `components/ui/Alert.tsx` | Medium | `ui/components.md` |
| 3.2.6 | Create `components/layout/Header.tsx` | High | `ui/components.md` |
| 3.2.7 | Create `components/layout/Container.tsx` | High | `ui/components.md` |
| 3.2.8 | Create `components/ui/index.ts` (exports) | High | - |

### 3.3 Auth Components (3 Tasks)

| # | Task | Priority | Spec Reference |
|---|------|----------|----------------|
| 3.3.1 | Create `components/auth/LoginForm.tsx` | High | `ui/components.md` |
| 3.3.2 | Create `components/auth/RegisterForm.tsx` | High | `ui/components.md` |
| 3.3.3 | Create `components/auth/LogoutButton.tsx` | High | `ui/components.md` |

### 3.4 Task Components (5 Tasks)

| # | Task | Priority | Spec Reference |
|---|------|----------|----------------|
| 3.4.1 | Create `components/tasks/TaskList.tsx` | High | `ui/components.md` |
| 3.4.2 | Create `components/tasks/TaskItem.tsx` | High | `ui/components.md` |
| 3.4.3 | Create `components/tasks/TaskForm.tsx` | High | `ui/components.md` |
| 3.4.4 | Create `components/tasks/TaskActions.tsx` | Medium | `ui/components.md` |
| 3.4.5 | Create `components/tasks/EmptyState.tsx` | Medium | `ui/components.md` |

### 3.5 Pages (5 Tasks)

| # | Task | Priority | Spec Reference |
|---|------|----------|----------------|
| 3.5.1 | Create `app/layout.tsx` | High | `ui/pages.md` |
| 3.5.2 | Create `app/page.tsx` (Landing) | High | `ui/pages.md` |
| 3.5.3 | Create `app/login/page.tsx` | High | `ui/pages.md` |
| 3.5.4 | Create `app/register/page.tsx` | High | `ui/pages.md` |
| 3.5.5 | Create `app/dashboard/page.tsx` | High | `ui/pages.md` |

### 3.6 API Client (2 Tasks)

| # | Task | Priority | Spec Reference |
|---|------|----------|----------------|
| 3.6.1 | Create `src/lib/api.ts` | High | `api/rest-endpoints.md` |
| 3.6.2 | Implement all API methods | High | `api/rest-endpoints.md` |

---

## Phase 4: Integration & Testing

### 4.1 Integration Tests (8 Tasks)

| # | Task | Priority | Test |
|---|------|----------|------|
| 4.1.1 | Test user registration | High | New user created in DB |
| 4.1.2 | Test user login | High | JWT token received |
| 4.1.3 | Test create task | High | Task saved to Neon |
| 4.1.4 | Test list tasks | High | User's tasks returned |
| 4.1.5 | Test update task | High | Task modified in DB |
| 4.1.6 | Test delete task | High | Task removed from DB |
| 4.1.7 | Test toggle complete | High | Completion toggled |
| 4.1.8 | Test logout | High | Session cleared |

### 4.2 Security Tests (3 Tasks)

| # | Task | Priority | Test |
|---|------|----------|------|
| 4.2.1 | Test 401 without JWT | High | API returns 401 |
| 4.2.2 | Test 403 wrong user | High | API returns 403 |
| 4.2.3 | Test user isolation | High | Can't see others' tasks |

### 4.3 Documentation (1 Task)

| # | Task | Priority | Deliverable |
|---|------|----------|-------------|
| 4.3.1 | Update README.md | High | Setup instructions |

---

## Task Checklist Summary

### Phase 1: Environment Setup
- [x] 1.1.1 Create frontend/ directory
- [x] 1.1.2 Create backend/ directory
- [x] 1.1.3 Create backend/.env
- [x] 1.1.4 Create frontend/.env.local
- [x] 1.1.5 Create .gitignore
- [ ] 1.1.6 Initialize Next.js project
- [ ] 1.1.7 Initialize FastAPI project
- [ ] 1.1.8 Verify environment

### Phase 2: Backend (25 Tasks)
- [ ] 2.1.1-2.1.5 Core setup (5 tasks)
- [ ] 2.2.1-2.2.4 Models & schemas (4 tasks)
- [ ] 2.3.1-2.3.7 Services (7 tasks)
- [ ] 2.4.1-2.4.8 API routes (8 tasks)
- [ ] 2.5.1 Main app (1 task)

### Phase 3: Frontend (28 Tasks)
- [ ] 3.1.1-3.1.5 Auth setup (5 tasks)
- [ ] 3.2.1-3.2.8 UI components (8 tasks)
- [ ] 3.3.1-3.3.3 Auth components (3 tasks)
- [ ] 3.4.1-3.4.5 Task components (5 tasks)
- [ ] 3.5.1-3.5.5 Pages (5 tasks)
- [ ] 3.6.1-3.6.2 API client (2 tasks)

### Phase 4: Integration (12 Tasks)
- [ ] 4.1.1-4.1.8 Integration tests (8 tasks)
- [ ] 4.2.1-4.2.3 Security tests (3 tasks)
- [ ] 4.3.1 Documentation (1 task)

---

## Definition of Done

- [ ] All 73 tasks completed
- [ ] Frontend runs on localhost:3000
- [ ] Backend runs on localhost:8000
- [ ] All 5 Todo features functional
- [ ] JWT authentication working
- [ ] User isolation enforced
- [ ] Data persists in Neon DB
- [ ] All tests pass
- [ ] Ready for hackathon submission

---

**Previous**: [plan.md](./plan.md)
**Next**: `/sp.implement` to start implementation
