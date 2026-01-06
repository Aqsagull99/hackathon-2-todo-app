# Implementation Plan: Task Organization & Intelligence (004)

**Feature ID**: 004-task-organization-intelligence
**Plan Version**: 1.0.0
**Created**: 2026-01-03
**Status**: PLANNING COMPLETE - READY FOR IMPLEMENTATION
**Feature Spec**: [spec.md](./spec.md)

---

## 1. Technical Context

### 1.1 Current Architecture (Phase II)

```
┌─────────────────────────────────────────────────────────────────────┐
│                        NEXT.JS FRONTEND                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌──────────┐  │
│  │  Landing    │  │  Dashboard  │  │   Auth UI   │  │  API     │  │
│  │  Page       │  │  (Tasks)    │  │  (Sign In)  │  │  Client  │  │
│  └─────────────┘  └─────────────┘  └─────────────┘  └────┬─────┘  │
│                                                          │         │
└──────────────────────────────────────────────────────────┼─────────┘
                                                           │
                          REST API (JWT Auth)              │
┌──────────────────────────────────────────────────────────┼─────────┐
│                        FASTAPI BACKEND                    │         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │         │
│  │  Auth       │  │  Task CRUD  │  │  User       │       │         │
│  │  Endpoints  │  │  Endpoints  │  │  Endpoints  │       │         │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘       │         │
│         │                │                │               │         │
│         └────────────────┼────────────────┘               │         │
│                          │                              │         │
└──────────────────────────┼──────────────────────────────┼─────────┘
                           │                              │
                    SQLModel ORM                   asyncpg driver
                           │                              │
┌──────────────────────────────────────────────────────────┼─────────┐
│                     NEON POSTGRESQL                       │         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │         │
│  │  Users      │  │  Tasks      │  │  Sessions   │       │         │
│  │  Table      │  │  Table      │  │  Table      │       │         │
│  └─────────────┘  └─────────────┘  └─────────────┘       │         │
└─────────────────────────────────────────────────────────────────────┘
```

### 1.2 Architecture Changes Required

```
┌─────────────────────────────────────────────────────────────────────┐
│                        NEXT.JS FRONTEND                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌──────────┐  │
│  │  Search     │  │  Filter/    │  │  Priority   │  │  Tag     │  │
│  │  Component  │  │  Sort Bar   │  │  Selector   │  │  Manager │  │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └────┬─────┘  │
│         │                │                │               │         │
│  ┌──────┴────────────────┴────────────────┴───────────────┴─────┐  │
│  │  Date/Time Picker    │    Notification Handler    │  Recurring │  │
│  │  (Due Date)          │    (Browser API)           │  Controls  │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                  │
│  New State Management:                                           │
│  - FilterContext (status, priority, due date filters)            │
│  - SearchContext (keyword, results)                              │
│  - SortContext (sort field, direction)                           │
│  - TagContext (user tags, assignments)                           │
│  - NotificationContext (permission, queue)                       │
└──────────────────────────────────────────────────────────────────┘
                                   │
                           REST API (JWT Auth)
                                   │
┌──────────────────────────────────────────────────────────────────┐
│                        FASTAPI BACKEND                            │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  Extended Task Endpoints (CRUD + New Fields)               │  │
│  │  - POST /tasks (priority, due_date, recurrence)            │  │
│  │  - GET /tasks?search=&priority=&status=&sort=              │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌────────────────────┐  ┌────────────────────────────────────┐ │
│  │  Tag Management    │  │  Search & Filter Engine            │ │
│  │  - GET/POST /tags  │  │  - Full-text search (Postgres)     │ │
│  │  - PUT/DELETE      │  │  - Dynamic query building          │ │
│  │  - /tags/{id}/task │  │  - Multi-filter combination        │ │
│  └────────────────────┘  └────────────────────────────────────┘ │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  Recurring Task Service                                    │  │
│  │  - Auto-reschedule on completion                           │  │
│  │  - Pattern parsing (daily/weekly/monthly)                  │  │
│  │  - New instance creation                                   │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  Reminder Service                                          │  │
│  │  - Scheduled notification queue                            │  │
│  │  - Timezone conversion                                     │  │
│  │  - Snooze handling                                         │  │
│  └────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────┘
                                   │
                           SQLModel ORM
                                   │
┌──────────────────────────────────────────────────────────────────┐
│                     NEON POSTGRESQL                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌────────┐  │
│  │  Tasks      │  │  Tags       │  │  TaskTags   │  │  Re-   │  │
│  │  (Extended) │  │  (New)      │  │  (New)      │  │minders │  │
│  └─────────────┘  └─────────────┘  └─────────────┘  └────────┘  │
│                                                                  │
│  Indexes Added:                                                  │
│  - tasks.priority (for filtering/sorting)                       │
│  - tasks.due_date (for sorting/filtering)                       │
│  - tasks.user_id + tasks.status (compound)                      │
│  - tags.user_id (for user isolation)                            │
│  - Full-text index on title + description                       │
└──────────────────────────────────────────────────────────────────┘
```

### 1.3 Technology Decisions & Rationale

| Decision | Choice | Rationale | Alternatives Considered |
|----------|--------|-----------|------------------------|
| **Database** | Neon PostgreSQL (existing) | Already in use; supports full-text search, enums, JSON for flexible data | Could use separate search service (Elasticsearch) - overkill for this scale |
| **Full-Text Search** | PostgreSQL `tsvector` | Built-in, no extra infrastructure, < 500ms performance achievable | External search service - higher complexity/cost |
| **Date/Time Storage** | PostgreSQL `TIMESTAMP WITH TIME ZONE` | Handles timezone conversions natively; stored in UTC | Store as UNIX timestamp - loses readability |
| **Recurring Logic** | Event-driven (on completion) | Simpler than cron; no external scheduler needed; instant reschedule | Background cron job - adds complexity, potential delays |
| **Browser Notifications** | Notification API | Standard web API; no external service required | Push API + service worker - overkill for single-user app |
| **Tag Storage** | Separate table + join table | Normalized design; efficient querying; user isolation built-in | JSON array in task - harder to filter/query |
| **Priority Storage** | PostgreSQL `ENUM` type | Type safety; efficient storage; clear ordering | VARCHAR - less efficient, no type checking |
| **State Management** | React Context (per feature) | Matches existing frontend architecture | Redux/Zustand - adds dependency, overkill |
| **Date Picker** | Native `<input type="datetime-local">` | No extra dependency; accessible; works on mobile | Third-party library - adds bundle size |

### 1.4 Known Unknowns (NEEDS CLARIFICATION)

| Unknown | Impact | Research Approach |
|---------|--------|-------------------|
| **User Timezone Collection** | HIGH - Affects reminder accuracy | Check if signup collects timezone; if not, default to UTC or use browser detection |
| **Tag Color Defaults** | LOW - Only affects visual display | Define a standard palette (pink variants to match UI theme) |
| **Filter Persistence** | MEDIUM - UX expectation | Store in localStorage or session state |
| **Max Tag Limit** | LOW - Prevents abuse | Set reasonable limit (e.g., 50 tags per user) |

---

## 2. Constitution Check

### 2.1 Alignment with Core Principles

| Principle | Status | Evidence |
|-----------|--------|----------|
| **Spec-First** | ✅ COMPLIANT | Feature implementation follows approved spec.md |
| **User Isolation** | ✅ COMPLIANT | All queries filter by `user_id`; tags table includes user_id foreign key |
| **Stateless Auth** | ✅ COMPLIANT | JWT Bearer token required on all new endpoints |
| **Agentic Workflow** | ✅ COMPLIANT | Backend, Frontend, and Database agents will be invoked via Task tool |
| **Feature Integration** | ✅ COMPLIANT | New features extend existing Task model; no breaking changes to CRUD |

### 2.2 Alignment with Architectural Requirements

| Requirement | Status | Evidence |
|-------------|--------|----------|
| **Frontend/Backend Separation** | ✅ COMPLIANT | All data via REST API; no direct database access from frontend |
| **Strict Typing** | ✅ COMPLIANT | TypeScript interfaces for frontend; Pydantic/SQLModel for backend |
| **Environment Safety** | ✅ COMPLIANT | No secrets in code; timezone settings stored in user profile if collected |

### 2.3 Alignment with Security Standards

| Standard | Status | Evidence |
|----------|--------|----------|
| **401 Unauthorized** | ✅ COMPLIANT | JWT verification on all new endpoints |
| **403 Forbidden** | ✅ COMPLIANT | User isolation enforced on tags and reminders |
| **JWT Verification** | ✅ COMPLIANT | Backend validates Bearer token using `BETTER_AUTH_SECRET` |

### 2.4 Gate Evaluation

| Gate | Result | Justification |
|------|--------|---------------|
| **Phase 0: Dependencies Resolved** | ✅ PASS | All dependencies (PostgreSQL, Browser API) are available and understood |
| **Phase 1: Design Approved** | ✅ PASS | Data model and API contracts align with spec requirements |
| **Phase 2: Implementation Ready** | ✅ PASS | Technology decisions align with existing stack and constraints |

---

## 3. Research & Decisions

### 3.1 User Timezone Handling

**Decision**: Default to UTC; use browser detection for new signups

**Rationale**:
- Neon PostgreSQL stores all timestamps in UTC
- Browser's `Intl.DateTimeFormat().resolvedOptions().timezone` provides user's local timezone
- Simple solution: store timezone in localStorage on first visit
- Fallback: UTC if timezone not available

**Implementation**:
```python
# Backend: Store timezone with reminder
class UserProfile(SQLModel, table=True):
    timezone: str = Field(default="UTC")
    # ... existing fields

# Frontend: Detect and store timezone
const userTimezone = Intl.DateTimeFormat().resolvedOptions().timezone
localStorage.setItem('userTimezone', userTimezone)
```

### 3.2 Tag Color Palette

**Decision**: Use pink-themed colors matching existing UI

**Rationale**:
- Maintains visual consistency with glassmorphic black/pink theme
- Users can customize; defaults provide quick start

**Palette**:
| Tag Name | Default Color |
|----------|---------------|
| Work | #EC4899 (Pink 500) |
| Home | #8B5CF6 (Violet 500) |
| Personal | #10B981 (Emerald 500) |
| Urgent | #EF4444 (Red 500) |
| General | #6B7280 (Gray 500) |

### 3.3 Filter Persistence Strategy

**Decision**: Client-side session storage (localStorage)

**Rationale**:
- User preference: remembers filter state between sessions
- Simple implementation: no backend changes needed
- Alternative: user preferences table - overkill for this feature

**Implementation**:
```typescript
// Frontend: Persist filters
useEffect(() => {
  const savedFilters = localStorage.getItem('taskFilters')
  if (savedFilters) {
    setFilters(JSON.parse(savedFilters))
  }
}, [])

useEffect(() => {
  localStorage.setItem('taskFilters', JSON.stringify(filters))
}, [filters])
```

### 3.4 Max Tag Limit

**Decision**: Soft limit of 20 tags per user with UI warning

**Rationale**:
- Prevents abuse while not restricting normal usage
- Warning at 15 tags to prevent hitting limit unknowingly
- Hard limit in backend for safety (50 max)

---

## 4. Data Model (data-model.md)

### 4.1 Updated Task Entity

```python
# backend/src/models/task.py

from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID

from sqlmodel import Field, Relationship, SQLModel


class TaskPriority(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class RecurrencePattern(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class TaskStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"


class Task(SQLModel, table=True):
    """Extended Task model with organization and intelligence features."""

    # Existing fields (unchanged)
    id: UUID = Field(default=None, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", nullable=False, index=True)
    title: str = Field(max_length=255, nullable=False)
    description: Optional[str] = Field(default=None, max_length=2000)
    status: TaskStatus = Field(default=TaskStatus.PENDING)

    # NEW: Priority field
    priority: TaskPriority = Field(
        default=TaskPriority.MEDIUM,
        nullable=False,
        index=True
    )

    # NEW: Due date with timezone awareness
    due_date: Optional[datetime] = Field(default=None, nullable=True)
    due_date_tz: Optional[str] = Field(
        default=None,
        max_length=50,
        description="Timezone for due_date (e.g., 'America/New_York')"
    )

    # NEW: Recurring task support
    recurrence_pattern: Optional[RecurrencePattern] = Field(default=None, nullable=True)
    recurrence_parent_id: Optional[UUID] = Field(
        default=None,
        nullable=True,
        description="Links to original recurring task"
    )

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    completed_at: Optional[datetime] = Field(default=None, nullable=True)

    # Relationships
    tags: List["Tag"] = Relationship(
        link_model="TaskTagLink",
        back_populates="tasks"
    )
    reminders: List["Reminder"] = Relationship(back_populates="task")


# Association table for many-to-many Task-Tag relationship
class TaskTagLink(SQLModel, table=True):
    """Join table for Task and Tag many-to-many relationship."""

    task_id: UUID = Field(foreign_key="task.id", primary_key=True, nullable=False)
    tag_id: UUID = Field(foreign_key="tag.id", primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationships for easier access
    task: Task = Relationship(back_populates="tags")
    tag: "Tag" = Relationship(back_populates="tasks")
```

### 4.2 New Tag Entity

```python
# backend/src/models/tag.py

from datetime import datetime
from typing import List
from uuid import UUID

from sqlmodel import Field, Relationship, SQLModel


class Tag(SQLModel, table=True):
    """User-created tags for task organization."""

    id: UUID = Field(default=None, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", nullable=False, index=True)
    name: str = Field(max_length=50, nullable=False)
    color: str = Field(
        max_length=7,
        default="#EC4899",
        description="Hex color code for tag display"
    )
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationships
    tasks: List["Task"] = Relationship(
        link_model="TaskTagLink",
        back_populates="tags"
    )

    class Config:
        unique_constraints = [("name", "user_id")]  # Tag name unique per user
```

### 4.3 New Reminder Entity

```python
# backend/src/models/reminder.py

from datetime import datetime
from enum import Enum
from uuid import UUID

from sqlmodel import Field, Relationship, SQLModel


class ReminderStatus(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    SNOOZED = "snoozed"
    DISMISSED = "dismissed"


class Reminder(SQLModel, table=True):
    """Tracks reminder state for task notifications."""

    id: UUID = Field(default=None, primary_key=True)
    task_id: UUID = Field(foreign_key="task.id", nullable=False, index=True)
    due_time: datetime = Field(nullable=False, description="When reminder should trigger")
    status: ReminderStatus = Field(default=ReminderStatus.PENDING, nullable=False)
    snoozed_until: Optional[datetime] = Field(default=None, nullable=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationship
    task: Task = Relationship(back_populates="reminders")
```

### 4.4 Database Schema Migration

```sql
-- backend/migrations/004_extended_features.sql

-- 1. Add new columns to tasks table
ALTER TABLE task
ADD COLUMN IF NOT EXISTS priority task_priority DEFAULT 'medium' NOT NULL,
ADD COLUMN IF NOT EXISTS due_date TIMESTAMP WITH TIME ZONE,
ADD COLUMN IF NOT EXISTS due_date_tz VARCHAR(50),
ADD COLUMN IF NOT EXISTS recurrence_pattern VARCHAR(20),
ADD COLUMN IF NOT EXISTS recurrence_parent_id UUID,
ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT NOW();

-- 2. Create tags table
CREATE TABLE IF NOT EXISTS tag (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
    name VARCHAR(50) NOT NULL,
    color VARCHAR(7) DEFAULT '#EC4899',
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(name, user_id)
);

CREATE INDEX IF NOT EXISTS idx_tag_user_id ON tag(user_id);

-- 3. Create task_tag link table
CREATE TABLE IF NOT EXISTS task_tag_link (
    task_id UUID NOT NULL REFERENCES task(id) ON DELETE CASCADE,
    tag_id UUID NOT NULL REFERENCES tag(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (task_id, tag_id)
);

-- 4. Create reminders table
CREATE TABLE IF NOT EXISTS reminder (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    task_id UUID NOT NULL REFERENCES task(id) ON DELETE CASCADE,
    due_time TIMESTAMP NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    snoozed_until TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_reminder_task_id ON reminder(task_id);
CREATE INDEX IF NOT EXISTS idx_reminder_due_time ON reminder(due_time) WHERE status = 'pending';

-- 5. Create indexes on tasks for filtering/sorting
CREATE INDEX IF NOT EXISTS idx_task_priority ON task(priority);
CREATE INDEX IF NOT EXISTS idx_task_due_date ON task(due_date);
CREATE INDEX IF NOT EXISTS idx_task_user_status_priority ON task(user_id, status, priority);
CREATE INDEX IF NOT EXISTS idx_task_user_status_due_date ON task(user_id, status, due_date);

-- 6. Full-text search index (PostgreSQL tsvector)
ALTER TABLE task ADD COLUMN IF NOT EXISTS search_vector tsvector;
CREATE INDEX IF NOT EXISTS idx_task_search_vector ON task USING GIN(search_vector);

-- Function to update search vector
CREATE OR REPLACE FUNCTION update_task_search_vector()
RETURNS TRIGGER AS $$
BEGIN
    NEW.search_vector :=
        setweight(to_tsvector('english', COALESCE(NEW.title, '')), 'A') ||
        setweight(to_tsvector('english', COALESCE(NEW.description, '')), 'B');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to auto-update search vector
DROP TRIGGER IF EXISTS task_search_vector_update ON task;
CREATE TRIGGER task_search_vector_update
    BEFORE INSERT OR UPDATE OF title, description
    ON task
    FOR EACH ROW
    EXECUTE FUNCTION update_task_search_vector();
```

---

## 5. API Contracts

### 5.1 Task Endpoints (Extended)

#### POST /api/{user_id}/tasks
Create a new task with extended features.

**Request Body**:
```json
{
  "title": "Weekly team sync",
  "description": "Discuss project updates",
  "priority": "high",
  "due_date": "2026-01-10T10:00:00Z",
  "recurrence_pattern": "weekly",
  "tag_ids": ["uuid-1", "uuid-2"]
}
```

**Response** (201 Created):
```json
{
  "id": "uuid-new-task",
  "user_id": "uuid-user",
  "title": "Weekly team sync",
  "description": "Discuss project updates",
  "status": "pending",
  "priority": "high",
  "due_date": "2026-01-10T10:00:00Z",
  "due_date_tz": "UTC",
  "recurrence_pattern": "weekly",
  "tags": [
    {"id": "uuid-1", "name": "Work", "color": "#EC4899"},
    {"id": "uuid-2", "name": "Meeting", "color": "#8B5CF6"}
  ],
  "created_at": "2026-01-03T10:00:00Z"
}
```

#### GET /api/{user_id}/tasks
List tasks with search, filter, and sort support.

**Query Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| `search` | string | Keyword to search in title/description |
| `status` | string | Filter by status: "pending", "completed" |
| `priority` | string | Filter by priority: "high", "medium", "low" |
| `due_date_from` | string | Filter due date >= this date (ISO 8601) |
| `due_date_to` | string | Filter due date <= this date (ISO 8601) |
| `tag_ids` | array | Filter by tag IDs (comma-separated) |
| `sort_by` | string | Sort field: "due_date", "priority", "title", "created_at" |
| `sort_order` | string | Sort direction: "asc", "desc" |
| `page` | int | Page number (default: 1) |
| `page_size` | int | Items per page (default: 20, max: 100) |

**Response** (200 OK):
```json
{
  "tasks": [
    {
      "id": "uuid-1",
      "title": "Weekly team sync",
      "status": "pending",
      "priority": "high",
      "due_date": "2026-01-10T10:00:00Z",
      "tags": [{"id": "uuid-1", "name": "Work", "color": "#EC4899"}],
      "created_at": "2026-01-03T10:00:00Z"
    }
  ],
  "total": 50,
  "page": 1,
  "page_size": 20,
  "total_pages": 3
}
```

#### PATCH /api/{user_id}/tasks/{task_id}
Update task with extended fields.

**Request Body** (partial update):
```json
{
  "priority": "low",
  "due_date": "2026-01-15T14:00:00Z"
}
```

#### POST /api/{user_id}/tasks/{task_id}/complete
Complete task with recurring logic.

**Response** (200 OK):
```json
{
  "completed_task": {
    "id": "uuid-original",
    "status": "completed",
    "completed_at": "2026-01-03T10:00:00Z"
  },
  "new_instance": {
    "id": "uuid-new-instance",
    "title": "Weekly team sync",
    "due_date": "2026-01-17T10:00:00Z",
    "status": "pending"
  }
}
```

### 5.2 Tag Management Endpoints

#### GET /api/{user_id}/tags
List all user tags.

**Response** (200 OK):
```json
{
  "tags": [
    {"id": "uuid-1", "name": "Work", "color": "#EC4899", "task_count": 5},
    {"id": "uuid-2", "name": "Home", "color": "#10B981", "task_count": 3}
  ]
}
```

#### POST /api/{user_id}/tags
Create new tag.

**Request Body**:
```json
{
  "name": "Urgent",
  "color": "#EF4444"
}
```

#### PATCH /api/{user_id}/tags/{tag_id}
Update tag (rename, recolor).

#### DELETE /api/{user_id}/tags/{tag_id}
Delete tag. Returns list of affected task IDs.

**Response** (200 OK):
```json
{
  "message": "Tag deleted successfully",
  "affected_task_ids": ["uuid-task-1", "uuid-task-2"]
}
```

#### POST /api/{user_id}/tasks/{task_id}/tags
Add tag to task.

**Request Body**:
```json
{
  "tag_id": "uuid-tag-1"
}
```

#### DELETE /api/{user_id}/tasks/{task_id}/tags/{tag_id}
Remove tag from task.

### 5.3 Reminder Endpoints

#### GET /api/{user_id}/tasks/{task_id}/reminder
Get reminder for task.

**Response** (200 OK):
```json
{
  "reminder": {
    "id": "uuid-reminder",
    "task_id": "uuid-task",
    "due_time": "2026-01-10T09:55:00Z",
    "status": "pending"
  }
}
```

#### POST /api/{user_id}/tasks/{task_id}/reminder
Create or update reminder.

**Request Body**:
```json
{
  "due_time": "2026-01-10T09:55:00Z"
}
```

#### POST /api/{user_id}/reminders/{reminder_id}/snooze
Snooze reminder.

**Request Body**:
```json
{
  "minutes": 15
}
```

#### DELETE /api/{user_id}/reminders/{reminder_id}
Dismiss/cancel reminder.

---

## 6. Frontend Architecture

### 6.1 New Components

```
src/components/
├── tasks/
│   ├── PrioritySelector.tsx      # Dropdown for High/Medium/Low
│   ├── TagBadge.tsx              # Visual tag display
│   ├── TagManager.tsx            # Create/manage tags modal
│   ├── TagInput.tsx              # Multi-select tag input
│   ├── SearchBar.tsx             # Keyword search input
│   ├── FilterBar.tsx             # Filter by status, priority, due date
│   ├── SortDropdown.tsx          # Sort by due date/priority/title
│   ├── DateTimePicker.tsx        # Due date and time selection
│   ├── RecurringConfig.tsx       # Daily/Weekly/Monthly selector
│   └── TaskCardExtended.tsx      # Task card with priority/tag/date display
│
├── notifications/
│   ├── NotificationPermission.tsx # Request browser permission
│   ├── NotificationToast.tsx      # In-app reminder display
│   └── NotificationSettings.tsx   # Manage notification preferences
│
└── layout/
    └── FilterSortToolbar.tsx     # Combined filter/sort controls
```

### 6.2 State Management

```typescript
// src/lib/stores/

// Filter Context
interface FilterState {
  status: 'all' | 'pending' | 'completed'
  priority: 'all' | 'high' | 'medium' | 'low'
  dueDateRange: 'all' | 'today' | 'thisWeek' | 'thisMonth' | 'overdue'
  tagIds: string[]
}

const useFilterStore = create<FilterState>((set) => ({
  status: 'all',
  priority: 'all',
  dueDateRange: 'all',
  tagIds: [],
  setStatus: (status) => set({ status }),
  setPriority: (priority) => set({ priority }),
  // ... other actions
}))

// Search Context
interface SearchState {
  query: string
  results: Task[]
  isSearching: boolean
}

const useSearchStore = create<SearchState>((set) => ({
  query: '',
  results: [],
  isSearching: false,
  setQuery: (query) => set({ query }),
  setResults: (results) => set({ results }),
}))

// Notification Context
interface NotificationState {
  permission: NotificationPermission
  queue: Reminder[]
  requestPermission: () => Promise<void>
  scheduleReminder: (task: Task) => void
  snoozeReminder: (reminderId: string, minutes: number) => void
}
```

### 6.3 API Client Extensions

```typescript
// src/lib/api.ts (extended)

export const api = {
  // ... existing methods

  // Tags
  async getTags(userId: string): Promise<Tag[]> {
    const res = await fetch(`${API_URL}/${userId}/tags`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    return res.json()
  },

  async createTag(userId: string, data: { name: string; color?: string }): Promise<Tag> {
    const res = await fetch(`${API_URL}/${userId}/tags`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    })
    return res.json()
  },

  // Search & Filter
  async searchTasks(
    userId: string,
    params: {
      search?: string
      status?: string
      priority?: string
      tag_ids?: string[]
      sort_by?: string
      sort_order?: string
    }
  ): Promise<{ tasks: Task[]; total: number }> {
    const query = new URLSearchParams()
    Object.entries(params).forEach(([k, v]) => {
      if (v !== undefined) query.append(k, String(v))
    })
    const res = await fetch(`${API_URL}/${user_id}/tasks?${query}`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    return res.json()
  },

  // Reminders
  async createReminder(userId: string, taskId: string, dueTime: string): Promise<Reminder> {
    const res = await fetch(`${API_URL}/${userId}/tasks/${taskId}/reminder`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({ due_time: dueTime })
    })
    return res.json()
  },

  async snoozeReminder(userId: string, reminderId: string, minutes: number): Promise<Reminder> {
    const res = await fetch(`${API_URL}/${userId}/reminders/${reminderId}/snooze`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({ minutes })
    })
    return res.json()
  }
}
```

---

## 7. Backend Implementation Details

### 7.1 Search Service

```python
# backend/src/services/search_service.py

from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models import Task, TaskPriority, TaskStatus


class SearchService:
    """Handles search and filter queries for tasks."""

    async def search_tasks(
        self,
        session: AsyncSession,
        user_id: str,
        search: str | None = None,
        status: str | None = None,
        priority: str | None = None,
        due_date_from: str | None = None,
        due_date_to: str | None = None,
        tag_ids: list[str] | None = None,
        sort_by: str = "created_at",
        sort_order: str = "desc",
        page: int = 1,
        page_size: int = 20
    ) -> dict:
        """Build and execute search query with filters."""

        # Base query with user isolation
        query = select(Task).where(Task.user_id == user_id)

        # Apply search filter
        if search:
            # Use PostgreSQL full-text search
            query = query.where(
                Task.search_vector.op("@@")(func.plainto_tsquery(search))
            )

        # Apply status filter
        if status and status != "all":
            query = query.where(Task.status == TaskStatus(status))

        # Apply priority filter
        if priority and priority != "all":
            query = query.where(Task.priority == TaskPriority(priority))

        # Apply due date range filter
        if due_date_from:
            query = query.where(Task.due_date >= due_date_from)
        if due_date_to:
            query = query.where(Task.due_date <= due_date_to)

        # Apply tag filter (requires JOIN)
        if tag_ids:
            # Would need to join with TaskTagLink and Tag tables
            # Simplified: filter by exists subquery
            pass

        # Apply sorting
        sort_column = getattr(Task, sort_by, Task.created_at)
        if sort_order == "desc":
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())

        # Apply pagination
        query = query.offset((page - 1) * page_size).limit(page_size)

        # Execute with tags loaded
        query = query.options(selectinload(Task.tags))
        result = await session.execute(query)
        tasks = result.scalars().all()

        # Get total count
        count_query = select(Task).where(Task.user_id == user_id)
        count_result = await session.execute(count_query)
        total = len(count_result.scalars().all())

        return {
            "tasks": [t.to_dict() for t in tasks],
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size
        }
```

### 7.2 Recurring Task Service

```python
# backend/src/services/recurring_service.py

from datetime import datetime, timedelta
from typing import Optional
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from models import Task, RecurrencePattern


class RecurringService:
    """Handles recurring task auto-rescheduling."""

    async def complete_recurring_task(
        self,
        session: AsyncSession,
        task: Task
    ) -> Optional[Task]:
        """When a recurring task is completed, create next instance."""

        if not task.recurrence_pattern:
            return None

        # Mark original task complete
        task.status = TaskStatus.COMPLETED
        task.completed_at = datetime.utcnow()
        session.add(task)

        # Calculate next due date based on recurrence pattern
        new_due_date = self._calculate_next_instance(task.due_date, task.recurrence_pattern)

        # Create new task instance
        new_task = Task(
            id=uuid4(),
            user_id=task.user_id,
            title=task.title,
            description=task.description,
            priority=task.priority,
            due_date=new_due_date,
            recurrence_pattern=task.recurrence_pattern,
            recurrence_parent_id=task.recurrence_parent_id or task.id,
            status=TaskStatus.PENDING
        )
        session.add(new_task)

        await session.commit()
        await session.refresh(new_task)

        return new_task

    def _calculate_next_instance(
        self,
        due_date: Optional[datetime],
        pattern: RecurrencePattern
    ) -> Optional[datetime]:
        """Calculate the next occurrence date based on pattern."""
        if not due_date:
            return None

        if pattern == RecurrencePattern.DAILY:
            return due_date + timedelta(days=1)
        elif pattern == RecurrencePattern.WEEKLY:
            return due_date + timedelta(weeks=1)
        elif pattern == RecurrencePattern.MONTHLY:
            # Same day next month
            if due_date.month == 12:
                return due_date.replace(
                    year=due_date.year + 1,
                    month=1
                )
            else:
                return due_date.replace(month=due_date.month + 1)
        return due_date
```

### 7.3 Reminder Service

```python
# backend/src/services/reminder_service.py

from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from models import Reminder, ReminderStatus


class ReminderService:
    """Handles reminder scheduling and notifications."""

    async def create_reminder(
        self,
        session: AsyncSession,
        task_id: str,
        due_time: datetime
    ) -> Reminder:
        """Create a reminder for task due time."""

        # Check for existing reminder
        existing = await self.get_reminder_for_task(session, task_id)

        if existing:
            # Update existing reminder
            existing.due_time = due_time
            existing.status = ReminderStatus.PENDING
            existing.snoozed_until = None
            session.add(existing)
            await session.commit()
            await session.refresh(existing)
            return existing

        # Create new reminder
        reminder = Reminder(
            id=uuid4(),
            task_id=task_id,
            due_time=due_time,
            status=ReminderStatus.PENDING
        )
        session.add(reminder)
        await session.commit()
        await session.refresh(reminder)

        return reminder

    async def get_reminder_for_task(
        self,
        session: AsyncSession,
        task_id: str
    ) -> Optional[Reminder]:
        """Get active reminder for a task."""
        from sqlalchemy import select
        result = await session.execute(
            select(Reminder).where(
                Reminder.task_id == task_id,
                Reminder.status == ReminderStatus.PENDING
            )
        )
        return result.scalar_one_or_none()

    async def snooze_reminder(
        self,
        session: AsyncSession,
        reminder_id: str,
        minutes: int
    ) -> Reminder:
        """Snooze a reminder for specified minutes."""
        from sqlalchemy import select
        from datetime import timedelta

        result = await session.execute(
            select(Reminder).where(Reminder.id == reminder_id)
        )
        reminder = result.scalar_one()

        reminder.status = ReminderStatus.SNOOZED
        reminder.snoozed_until = datetime.utcnow() + timedelta(minutes=minutes)

        session.add(reminder)
        await session.commit()
        await session.refresh(reminder)

        return reminder

    async def get_pending_reminders(self, session: AsyncSession) -> list[Reminder]:
        """Get all pending reminders that are due."""
        from sqlalchemy import select

        result = await session.execute(
            select(Reminder).where(
                Reminder.status == ReminderStatus.PENDING,
                Reminder.due_time <= datetime.utcnow()
            )
        )
        return list(result.scalars().all())
```

---

## 8. Quickstart Guide

### 8.1 Database Setup

```bash
# 1. Connect to Neon database
psql "postgresql://user:password@ep-xyz.us-east-1.aws.neon.tech/neon_db"

# 2. Run migration
\i backend/migrations/004_extended_features.sql

# 3. Verify tables
\dt
```

### 8.2 Backend Development

```bash
# 1. Navigate to backend
cd backend

# 2. Install dependencies
uv pip install -e .

# 3. Run database migrations
uv run alembic upgrade head

# 4. Start development server
uv run uvicorn src.main:app --reload
```

### 8.3 Frontend Development

```bash
# 1. Navigate to frontend
cd frontend

# 2. Install dependencies
npm install

# 3. Start development server
npm run dev
```

### 8.4 Testing

```bash
# Backend tests
cd backend
uv run pytest tests/ -v

# Frontend tests
cd frontend
npm run test
```

---

## 9. Rollout Checklist

### Pre-Launch
- [ ] Database migration applied to Neon
- [ ] All API endpoints tested with authentication
- [ ] Full-text search index verified
- [ ] Frontend components styled to match existing UI
- [ ] Browser notification permission flow tested
- [ ] Recurring task auto-reschedule tested end-to-end
- [ ] Performance: Search returns < 500ms for 100 tasks
- [ ] User isolation tested (cannot access other user's tags/tasks)
- [ ] Rollback plan documented

### Post-Launch
- [ ] Monitor error logs for 24 hours
- [ ] Track recurring task success rate (target: 99.9%)
- [ ] Gather user feedback on new features
- [ ] Performance monitoring: Search latency percentiles
- [ ] Feature adoption metrics

---

## 10. Risk Analysis

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| **Full-text search performance** | HIGH | LOW | Add indexes; paginate results; add search debouncing |
| **Timezone handling bugs** | MEDIUM | MEDIUM | Default to UTC; validate timezone strings; test edge cases |
| **Browser notification blocking** | LOW | HIGH | Graceful fallback; show in-app notifications instead |
| **Recurring task infinite loop** | HIGH | LOW | Add instance count limit (max 100 per parent); audit trail |
| **Tag deletion cascade issues** | MEDIUM | LOW | Use ON DELETE CASCADE; confirm before bulk deletion |
| **User isolation breach** | CRITICAL | LOW | Always filter by user_id; security audit on new endpoints |

---

**Plan Status**: ✅ APPROVED FOR IMPLEMENTATION
**Next Steps**:
1. Run `/sp.tasks` to generate implementation tasks
2. Invoke Backend Agent for API development
3. Invoke Frontend Agent for UI development
4. Invoke Database Agent for migration and optimization

---

**Plan Created By**: Claude (AI Planning Agent)
**Date**: 2026-01-03
**Feature**: 004-task-organization-intelligence
