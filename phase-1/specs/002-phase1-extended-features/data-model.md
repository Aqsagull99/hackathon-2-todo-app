# Data Model: Todo App Phase I Extended Features

**Branch**: `002-phase1-extended-features` | **Date**: 2026-01-01
**Status**: Phase 1 Design Complete

---

## Entity: Task (Extended)

### Overview

The Task entity represents a single todo item with extended attributes for organization, categorization, and intelligent scheduling. All extended fields are optional with sensible defaults to maintain backward compatibility with Phase I.

### Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|----------|-------------|
| `id` | `int` | Yes | Assigned by TaskList | Unique identifier for the task |
| `title` | `str` | Yes | N/A | Short description of the task |
| `completed` | `bool` | No | `False` | Whether the task has been completed |
| `created_at` | `Optional[datetime]` | No | `datetime.now()` | Timestamp when the task was created |
| `priority` | `Priority` (enum) | No | `Priority.MEDIUM` | Task priority level |
| `tags` | `List[str]` | No | `[]` | List of string labels for categorization |
| `due_date` | `Optional[datetime]` | No | `None` | Optional deadline for task |
| `recurrence` | `Recurrence` (enum) | No | `Recurrence.NONE` | Recurrence pattern for task |

### Enum: Priority

```python
class Priority(str, Enum):
    """Priority levels for tasks."""
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
```

**Values**:
- `High`: Urgent tasks that should be done soon
- `Medium`: Normal priority tasks (default)
- `Low`: Tasks that can be deferred

**Validation**:
- Must be one of three defined values
- Case-sensitive (matches enum values exactly)

### Enum: Recurrence

```python
class Recurrence(str, Enum):
    """Recurrence patterns for tasks."""
    NONE = "None"
    DAILY = "Daily"
    WEEKLY = "Weekly"
```

**Values**:
- `None`: Task does not repeat (default)
- `Daily`: Task repeats every 24 hours from completion
- `Weekly`: Task repeats every 7 days from completion

**Validation**:
- Must be one of three defined values
- Case-sensitive (matches enum values exactly)

### Field Validation Rules

| Field | Rule |
|-------|------|
| `title` | Non-empty string |
| `id` | Positive integer, unique within TaskList |
| `tags` | List of non-empty strings (duplicates allowed in storage, deduplicated in operations) |
| `due_date` | Must be a valid `datetime` object or `None` |
| `priority` | Must be a valid `Priority` enum value |
| `recurrence` | Must be a valid `Recurrence` enum value |

### State Transitions

#### Completion State

```
pending (completed=False)  →  completed (completed=True)
        ↻  (toggle_complete)
           completed=True  →  completed=False (if recurrence=NONE)
```

**Special Case - Recurring Tasks**:
When a recurring task (recurrence != NONE) is marked complete:
1. Current task remains completed
2. New task instance is created with:
   - Same title, priority, tags, recurrence
   - `completed = False`
   - `due_date` = previous due_date + interval (1 day for Daily, 7 days for Weekly)

#### Priority State

```
Priority can be set at any time:
HIGH  ↔  MEDIUM  ↔  LOW
      (update_priority)
```

#### Tags State

```
Tags can be added, removed, or modified at any time:
[] → [Work] → [Work, Home] → [Work] (remove Home)
  (add_tags)    (add_tags)     (remove_tags)
```

#### Due Date State

```
None → datetime (set_due_date)
datetime → different datetime (set_due_date)
```

#### Recurrence State

```
NONE → DAILY/WEEKLY (set_recurrence)
DAILY/WEEKLY → NONE (set_recurrence)
```

### Relationships

The Task entity has **no explicit relationships** to other entities (in-memory, single-session architecture).

However, it has **implicit relationships**:

| Relationship | Type | Description |
|--------------|------|-------------|
| TaskList | Collection | Multiple Task objects are managed by a single TaskList |
| Recurring Instance | Self-reference | A completed recurring task can spawn a new Task instance |

### Constraints

| Constraint | Description |
|------------|-------------|
| Unique ID | No two tasks can have same ID within a TaskList |
| Valid Enum Values | Priority and Recurrence must be valid enum values |
| Non-empty Tags | Each tag must be a non-empty string |
| Optional Extended Fields | All new fields (priority, tags, due_date, recurrence) are optional |

### Data Consistency Rules

1. **Tag Deduplication**: When adding tags, duplicates are automatically removed
   - Example: Adding `[Work, Work, Urgent]` results in `[Work, Urgent]`

2. **Recurring Task Creation**: When a recurring task is completed, a new instance is created only if `due_date` is set

3. **Search Indexing**: Keywords for search are derived from `title` and `tags` fields only

---

## Entity: TaskList (Extended)

### Overview

The TaskList entity manages in-memory storage of Task objects, providing CRUD operations and extended functionality for search, filter, and sort.

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `tasks` | `Dict[int, Task]` | Dictionary mapping task IDs to Task objects |
| `next_id` | `int` | Auto-incrementing counter for assigning new task IDs |

### Methods

#### Base CRUD Methods (from Phase I)

```python
def add(self, title: str) -> Task
def get_all(self) -> List[Task]
def get_by_id(self, task_id: int) -> Optional[Task]
def update_title(self, task_id: int, title: str) -> Optional[Task]
def delete(self, task_id: int) -> bool
def toggle_complete(self, task_id: int) -> Optional[Task]
```

#### Extended Methods

**Priority Management**:

```python
def update_priority(self, task_id: int, priority: Priority) -> Optional[Task]:
    """Set or update priority of a task."""
```

**Tag Management**:

```python
def add_tags(self, task_id: int, tags: List[str]) -> Optional[Task]:
    """Add tags to a task (duplicates removed automatically)."""

def remove_tags(self, task_id: int, tags: List[str]) -> Optional[Task]:
    """Remove tags from a task."""
```

**Due Date Management**:

```python
def set_due_date(self, task_id: int, due_date: datetime) -> Optional[Task]:
    """Set due date and time for a task."""
```

**Recurrence Management**:

```python
def set_recurrence(self, task_id: int, recurrence: Recurrence) -> Optional[Task]:
    """Set or update recurrence pattern for a task."""
```

**Search**:

```python
def search(self, keyword: str) -> List[Task]:
    """Search for tasks by keyword in title or tags.
    Returns tasks where keyword appears in title or any tag."""
```

**Filter**:

```python
def filter_by_status(self, status: bool) -> List[Task]:
    """Filter tasks by completion status (True=completed, False=pending)."""

def filter_by_priority(self, priority: Priority) -> List[Task]:
    """Filter tasks by priority level."""

def filter_by_due_date(self, start: Optional[datetime], end: Optional[datetime]) -> List[Task]:
    """Filter tasks by due date range.
    start: inclusive start date (None = no lower bound)
    end: inclusive end date (None = no upper bound)"""
```

**Sort**:

```python
def sort_by_date(self, descending: bool = False) -> List[Task]:
    """Sort tasks by due date (tasks without due_date last).
    descending: if True, highest dates first."""

def sort_by_priority(self, descending: bool = False) -> List[Task]:
    """Sort tasks by priority (High > Medium > Low).
    descending: if True, lowest priorities first."""

def sort_by_name(self, descending: bool = False) -> List[Task]:
    """Sort tasks alphabetically by title.
    descending: if True, Z to A."""
```

**Recurring Task Handling**:

```python
def create_recurring_instance(self, task: Task) -> Optional[Task]:
    """Create a new task instance for a completed recurring task.
    Returns new task, or None if task is not recurring."""
```

**Reminder Management**:

```python
def check_reminders(self, current_time: datetime) -> List[Task]:
    """Check for tasks with due dates that have been reached or passed.
    Returns list of tasks needing reminders."""
```

### Method Signatures and Return Types

All extended methods return either:
- `Optional[Task]`: Single task operations (update, delete)
- `List[Task]`: Query operations (search, filter, sort)
- `bool`: Status operations (delete)

---

## Entity: NotificationManager

### Overview

The NotificationManager entity handles sending system notifications for task reminders, with platform-specific implementations and graceful fallback to console output.

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `platform` | `str` | Detected platform name (e.g., 'linux', 'darwin', 'win32') |

### Methods

```python
def send_notification(self, title: str, message: str) -> bool:
    """Send a system notification if available, fallback to console.

    Args:
        title: Notification title (e.g., task name)
        message: Notification message (e.g., due time)

    Returns:
        True if notification was sent (system or console), False on error
    """

def _notify_linux(self, title: str, message: str) -> bool:
    """Send notification on Linux using notify-send."""

def _notify_macos(self, title: str, message: str) -> bool:
    """Send notification on macOS using osascript."""

def _notify_windows(self, title: str, message: str) -> bool:
    """Send notification on Windows using PowerShell."""

def _notify_console(self, title: str, message: str) -> bool:
    """Fallback: Print reminder to console with visual indicator."""
```

### Platform Detection

```python
import platform
platform_name = platform.system().lower()
# 'linux', 'darwin', 'windows', etc.
```

---

## Entity: RecurrenceManager

### Overview

The RecurrenceManager entity handles date arithmetic for recurring tasks, calculating next due dates based on recurrence patterns.

### Methods

```python
@staticmethod
def calculate_next_due_date(
    current_due: datetime,
    recurrence: str  # "Daily" or "Weekly"
) -> Optional[datetime]:
    """Calculate next due date based on recurrence pattern.

    Args:
        current_due: The current due date of the completed task
        recurrence: Recurrence pattern ("Daily" or "Weekly")

    Returns:
        The next due date, or None if recurrence is "None"
    """

@staticmethod
def validate_recurrence(recurrence: str) -> bool:
    """Validate that a recurrence pattern is supported.
    Returns True if valid, False otherwise."""
```

---

## Data Flow Examples

### Example 1: Adding a Task with Extended Fields

```
Input: add "Buy groceries" priority=High tags=[Shopping] due_date=2026-01-02T10:00

1. TaskList.add() creates Task with:
   id=1, title="Buy groceries", completed=False, created_at=<now>
   priority=Priority.HIGH, tags=[Shopping], due_date=<datetime>, recurrence=Recurrence.NONE

2. Task stored in TaskList.tasks[1]

3. Return Task object to caller
```

### Example 2: Searching for Tasks

```
Input: search "grocery"

1. TaskList.search("grocery") iterates through all tasks
2. For each task, checks if "grocery" is in:
   - task.title (case-insensitive)
   - any tag in task.tags (case-insensitive)
3. Returns list of matching tasks
```

### Example 3: Completing a Recurring Task

```
Initial State: Task(id=1, title="Drink water", due_date=2026-01-01T08:00, recurrence=Weekly, completed=False)

Input: toggle_complete(1)

1. TaskList.toggle_complete(1) marks task.completed=True
2. If task.recurrence != Recurrence.NONE:
   - Calls RecurrenceManager.calculate_next_due_date(2026-01-01T08:00, "Weekly")
     Returns 2026-01-08T08:00
   - Creates new Task with same attributes, new due_date, completed=False
   - Adds to TaskList with id=2

3. Returns completed task (original)

Final State:
- Task(1, "Drink water", completed=True, due_date=2026-01-01T08:00, recurrence=Weekly)
- Task(2, "Drink water", completed=False, due_date=2026-01-08T08:00, recurrence=Weekly)
```

### Example 4: Filtering and Sorting

```
Input: filter_by_priority(Priority.HIGH) → sort_by_date(descending=False)

1. TaskList.filter_by_priority(Priority.HIGH) returns all High priority tasks
2. Result is passed to sort_by_date()
3. sort_by_date() sorts by due_date ascending
   - Tasks with due_date first (oldest first)
   - Tasks without due_date last
4. Returns sorted list
```

---

## Backward Compatibility

### Phase I Compatibility

All extended fields are **optional** with sensible defaults:

| Field | Default Value | Phase I Behavior |
|-------|---------------|------------------|
| `priority` | `Priority.MEDIUM` | N/A (not used) |
| `tags` | `[]` | N/A (not used) |
| `due_date` | `None` | N/A (not used) |
| `recurrence` | `Recurrence.NONE` | N/A (not used) |

### Phase I Operations Remain Unchanged

| Phase I Method | Behavior with Extended Model |
|----------------|-----------------------------|
| `add(title)` | Creates task with defaults for extended fields |
| `get_all()` | Returns all tasks (extended fields present but unused) |
| `get_by_id(id)` | Returns task (extended fields present but unused) |
| `update_title(id, title)` | Updates title only (extended fields unchanged) |
| `delete(id)` | Deletes task (extended fields not relevant) |
| `toggle_complete(id)` | Toggles completion (extended fields unchanged) |

---

## Serialization Notes

While Phase I is in-memory only, the data model is designed to support future persistence:

### JSON-Friendly Types

- `Priority` and `Recurrence` are `str` enums → serialize as strings
- `datetime` → serialize as ISO 8601 strings (e.g., "2026-01-01T08:00:00")
- `List[str]` → serialize as JSON array
- `Optional[datetime]` → serialize as string or null

### Example JSON Representation

```json
{
  "id": 1,
  "title": "Buy groceries",
  "completed": false,
  "created_at": "2026-01-01T09:00:00",
  "priority": "High",
  "tags": ["Shopping", "Urgent"],
  "due_date": "2026-01-02T10:00:00",
  "recurrence": "None"
}
```

---

**Version**: 1.0.0 | **Status**: READY FOR IMPLEMENTATION
