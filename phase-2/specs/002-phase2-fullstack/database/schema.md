# Database Specification: Schema Design

**Spec ID**: 002-phase2-fullstack/database/schema
**Version**: 1.0.0
**Status**: Draft
**Created**: 2025-12-29

---

## Database Provider

| Property | Value |
|----------|-------|
| Provider | Neon Serverless PostgreSQL |
| Version | PostgreSQL 16 |
| Region | US East (Ohio) |
| Project ID | `round-frog-47707317` |
| Project Name | `todo-app` |

## Connection Configuration

### Connection Strings

**Backend (asyncpg driver):**
```
postgresql+asyncpg://neondb_owner:***@ep-delicate-thunder-ahwhfweh-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require
```

**Frontend (Better Auth - pg driver):**
```
postgresql://neondb_owner:***@ep-delicate-thunder-ahwhfweh-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require
```

### Connection Pool Settings

| Setting | Value |
|---------|-------|
| Pool Size | 5 (min) - 20 (max) |
| Connection Timeout | 30 seconds |
| Idle Timeout | 300 seconds |
| SSL Mode | require |

---

## Schema Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      neondb (database)                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                    public schema                     │    │
│  │                                                      │    │
│  │  ┌──────────────────────────────────────────────┐   │    │
│  │  │                   tasks                       │   │    │
│  │  │  - id (PK)                                    │   │    │
│  │  │  - user_id (indexed)                          │   │    │
│  │  │  - title                                      │   │    │
│  │  │  - description                                │   │    │
│  │  │  - completed                                  │   │    │
│  │  │  - created_at                                 │   │    │
│  │  │  - updated_at                                 │   │    │
│  │  └──────────────────────────────────────────────┘   │    │
│  │                                                      │    │
│  │  ┌──────────────────────────────────────────────┐   │    │
│  │  │           Better Auth Tables                  │   │    │
│  │  │  - user                                       │   │    │
│  │  │  - session                                    │   │    │
│  │  │  - account                                    │   │    │
│  │  │  - verification                               │   │    │
│  │  └──────────────────────────────────────────────┘   │    │
│  │                                                      │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Table: tasks

### Schema Definition

```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    completed BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Index for user_id queries (essential for user isolation)
CREATE INDEX idx_tasks_user_id ON tasks(user_id);

-- Index for filtering by completion status
CREATE INDEX idx_tasks_user_completed ON tasks(user_id, completed);

-- Index for sorting by created_at
CREATE INDEX idx_tasks_user_created ON tasks(user_id, created_at DESC);
```

### Column Details

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| `id` | SERIAL | No | auto | Primary key, auto-increment |
| `user_id` | VARCHAR(255) | No | - | User identifier from JWT |
| `title` | VARCHAR(255) | No | - | Task title (1-255 chars) |
| `description` | TEXT | Yes | NULL | Optional description |
| `completed` | BOOLEAN | No | false | Completion status |
| `created_at` | TIMESTAMPTZ | No | NOW() | Creation timestamp |
| `updated_at` | TIMESTAMPTZ | No | NOW() | Last update timestamp |

### Constraints

| Constraint | Type | Description |
|------------|------|-------------|
| `tasks_pkey` | PRIMARY KEY | Unique task identifier |
| `tasks_title_check` | CHECK | `LENGTH(title) > 0` |
| `tasks_user_id_check` | CHECK | `LENGTH(user_id) > 0` |

### Indexes

| Index | Columns | Type | Purpose |
|-------|---------|------|---------|
| `tasks_pkey` | id | B-tree | Primary key lookup |
| `idx_tasks_user_id` | user_id | B-tree | User isolation queries |
| `idx_tasks_user_completed` | user_id, completed | B-tree | Filter by status |
| `idx_tasks_user_created` | user_id, created_at DESC | B-tree | Sort by date |

---

## SQLModel Definition

```python
# models/task.py
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field

class TaskBase(SQLModel):
    """Base task fields for create/update operations."""
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)

class TaskCreate(TaskBase):
    """Schema for creating a new task."""
    pass

class TaskUpdate(SQLModel):
    """Schema for updating a task (all fields optional)."""
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)

class Task(TaskBase, table=True):
    """Task database model."""
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, min_length=1, max_length=255)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class TaskResponse(TaskBase):
    """Schema for task API responses."""
    id: int
    user_id: str
    completed: bool
    created_at: datetime
    updated_at: datetime
```

---

## Better Auth Tables

Better Auth automatically creates and manages these tables:

### user

```sql
CREATE TABLE "user" (
    id VARCHAR(255) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    email_verified BOOLEAN DEFAULT false,
    name VARCHAR(255),
    image VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### session

```sql
CREATE TABLE session (
    id VARCHAR(255) PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    ip_address VARCHAR(255),
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### account

```sql
CREATE TABLE account (
    id VARCHAR(255) PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
    account_id VARCHAR(255) NOT NULL,
    provider_id VARCHAR(255) NOT NULL,
    access_token TEXT,
    refresh_token TEXT,
    access_token_expires_at TIMESTAMP WITH TIME ZONE,
    refresh_token_expires_at TIMESTAMP WITH TIME ZONE,
    scope TEXT,
    password TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### verification

```sql
CREATE TABLE verification (
    id VARCHAR(255) PRIMARY KEY,
    identifier VARCHAR(255) NOT NULL,
    value VARCHAR(255) NOT NULL,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

---

## Migration Scripts

### Initial Migration

```sql
-- migrations/001_create_tasks.sql
-- Create tasks table for Phase II Todo app

BEGIN;

CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    completed BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),

    CONSTRAINT tasks_title_check CHECK (LENGTH(title) > 0),
    CONSTRAINT tasks_user_id_check CHECK (LENGTH(user_id) > 0)
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_tasks_user_id
    ON tasks(user_id);

CREATE INDEX IF NOT EXISTS idx_tasks_user_completed
    ON tasks(user_id, completed);

CREATE INDEX IF NOT EXISTS idx_tasks_user_created
    ON tasks(user_id, created_at DESC);

COMMIT;
```

### Rollback Migration

```sql
-- migrations/001_create_tasks_rollback.sql
-- Rollback tasks table creation

BEGIN;

DROP INDEX IF EXISTS idx_tasks_user_created;
DROP INDEX IF EXISTS idx_tasks_user_completed;
DROP INDEX IF EXISTS idx_tasks_user_id;
DROP TABLE IF EXISTS tasks;

COMMIT;
```

---

## Database Operations

### Create Task

```sql
INSERT INTO tasks (user_id, title, description, completed, created_at, updated_at)
VALUES ($1, $2, $3, false, NOW(), NOW())
RETURNING id, user_id, title, description, completed, created_at, updated_at;
```

### List Tasks by User

```sql
SELECT id, user_id, title, description, completed, created_at, updated_at
FROM tasks
WHERE user_id = $1
ORDER BY created_at DESC;
```

### Get Task by ID

```sql
SELECT id, user_id, title, description, completed, created_at, updated_at
FROM tasks
WHERE id = $1 AND user_id = $2;
```

### Update Task

```sql
UPDATE tasks
SET title = COALESCE($3, title),
    description = COALESCE($4, description),
    updated_at = NOW()
WHERE id = $1 AND user_id = $2
RETURNING id, user_id, title, description, completed, created_at, updated_at;
```

### Toggle Completion

```sql
UPDATE tasks
SET completed = NOT completed,
    updated_at = NOW()
WHERE id = $1 AND user_id = $2
RETURNING id, user_id, title, description, completed, created_at, updated_at;
```

### Delete Task

```sql
DELETE FROM tasks
WHERE id = $1 AND user_id = $2;
```

---

## Database Connection (Python)

```python
# core/database.py
from sqlmodel import SQLModel, create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from .config import settings

# Async engine for FastAPI
async_engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=300
)

# Async session factory
async_session_maker = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_session() -> AsyncSession:
    """Dependency for getting database session."""
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()

async def init_db():
    """Initialize database tables."""
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
```

---

## Performance Considerations

### Query Optimization

1. **User Isolation**: Always include `user_id` in WHERE clause
2. **Index Usage**: Use indexed columns for filtering/sorting
3. **Pagination**: Implement limit/offset for large datasets
4. **Connection Pooling**: Use Neon's pooler endpoint

### Example Optimized Query

```sql
-- Paginated list with filter
SELECT id, user_id, title, description, completed, created_at, updated_at
FROM tasks
WHERE user_id = $1
  AND ($2::boolean IS NULL OR completed = $2)
ORDER BY created_at DESC
LIMIT $3 OFFSET $4;
```

---

**Previous**: [../api/rest-endpoints.md](../api/rest-endpoints.md)
**Next**: [../ui/components.md](../ui/components.md)
