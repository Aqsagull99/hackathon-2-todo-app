# Data Model: In-Memory Todo Console Application

**Feature**: 001-todo-console-app
**Created**: 2025-12-28

## Entities

### Task

Represents a single todo item.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | int | Yes | Unique identifier, auto-incremented starting from 1 |
| title | str | Yes | Task description, 1-200 characters |
| completed | bool | No | Completion status, default False |

### TaskList

Manages collection of tasks in memory.

| Field | Type | Description |
|-------|------|-------------|
| tasks | dict[int, Task] | Task storage keyed by ID |
| next_id | int | Counter for generating unique IDs |

## Validation Rules

- Title must be 1-200 characters
- Title cannot be empty or whitespace-only
- Task ID must exist in TaskList to perform operations
- Operations on non-existent IDs return None/False with error message

## State Transitions

```
Task Creation
    Empty → Task(id=N, title="...", completed=False)

Toggle Complete
    completed=False → completed=True
    completed=True → completed=True (idempotent)

Update Title
    Any state → Updated title (same ID)

Delete
    Existing → Removed from TaskList
```

## Example Data

```python
# Initial state
task_list = TaskList()

# After adding tasks
task_list.add("Buy groceries")
task_list.add("Call mom")

# State representation:
{
    1: Task(id=1, title="Buy groceries", completed=False),
    2: Task(id=2, title="Call mom", completed=False)
}

# After marking task 1 complete
task_list.toggle_complete(1)

# State representation:
{
    1: Task(id=1, title="Buy groceries", completed=True),
    2: Task(id=2, title="Call mom", completed=False)
}
```
