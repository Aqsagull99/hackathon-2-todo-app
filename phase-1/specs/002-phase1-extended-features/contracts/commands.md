# CLI Commands: Todo App Phase I Extended Features

**Branch**: `002-phase1-extended-features` | **Date**: 2026-01-01

---

## Command Overview

All commands are executed in the CLI interface. Extended commands for Phase I maintain the same pattern as Phase I commands (verb followed by arguments).

---

## Extended Commands

### 1. Set Priority

**Command**: `priority <id> <High|Medium|Low>`

**Description**: Set or update the priority level of a task.

**Arguments**:
- `<id>`: Task ID (integer)
- `<priority>`: One of "High", "Medium", "Low"

**Examples**:
```
priority 1 High
priority 2 Medium
priority 3 Low
```

**Errors**:
- Invalid task ID: "Task not found."
- Invalid priority: "Invalid priority. Use High, Medium, or Low."

---

### 2. Add Tags

**Command**: `tag <id> <tag1,tag2,...>`

**Description**: Add one or more tags to a task. Duplicate tags are automatically removed.

**Arguments**:
- `<id>`: Task ID (integer)
- `<tags>`: Comma-separated list of tags (no spaces in tag names)

**Examples**:
```
tag 1 Work
tag 2 Home,Urgent,Shopping
tag 3 Project,Important
```

**Errors**:
- Invalid task ID: "Task not found."
- Empty tag: "Tags cannot be empty."

---

### 3. Remove Tags

**Command**: `untag <id> <tag1,tag2,...>`

**Description**: Remove one or more tags from a task.

**Arguments**:
- `<id>`: Task ID (integer)
- `<tags>`: Comma-separated list of tags to remove

**Examples**:
```
untag 1 Work
untag 2 Home,Urgent
untag 3 AllTags
```

**Errors**:
- Invalid task ID: "Task not found."

---

### 4. Set Due Date

**Command**: `due <id> "YYYY-MM-DD HH:MM"`

**Description**: Set a due date and time for a task. Time is optional (defaults to 00:00).

**Arguments**:
- `<id>`: Task ID (integer)
- `<datetime>`: Due date and time in ISO 8601 format

**Examples**:
```
due 1 "2026-01-02"
due 2 "2026-01-03 14:30"
due 3 "2026-01-04 09:00"
```

**Errors**:
- Invalid task ID: "Task not found."
- Invalid date format: "Invalid date format. Use YYYY-MM-DD HH:MM"
- Past date (optional validation): "Due date cannot be in the past."

---

### 5. Set Recurrence

**Command**: `recurring <id> <None|Daily|Weekly>`

**Description**: Set or update the recurrence pattern for a task.

**Arguments**:
- `<id>`: Task ID (integer)
- `<recurrence>`: One of "None", "Daily", "Weekly"

**Examples**:
```
recurring 1 Daily
recurring 2 Weekly
recurring 3 None
```

**Errors**:
- Invalid task ID: "Task not found."
- Invalid recurrence: "Invalid recurrence. Use None, Daily, or Weekly."

---

### 6. Search Tasks

**Command**: `search "<keyword>"`

**Description**: Search for tasks by keyword. Matches against task title and all tags.

**Arguments**:
- `<keyword>`: Search string (case-insensitive)

**Examples**:
```
search "grocery"
search "work"
search "urgent"
```

**Behavior**:
- Searches all tasks (completed and pending)
- Returns list of matching tasks
- Shows "No matching tasks found." if no results

---

### 7. Filter Tasks

**Command**: `filter [options]`

**Description**: Filter tasks by status, priority, or due date range.

**Options**:
- `--status <pending|completed>`: Filter by completion status
- `--priority <High|Medium|Low>`: Filter by priority level
- `--start-date "YYYY-MM-DD"`: Filter tasks due after this date
- `--end-date "YYYY-MM-DD"`: Filter tasks due before this date

**Examples**:
```
filter --status pending
filter --priority High
filter --start-date "2026-01-01" --end-date "2026-01-31"
filter --status pending --priority High
```

**Behavior**:
- Filters can be combined (AND logic)
- Shows all matching tasks in a list
- Shows "No matching tasks found." if no results

---

### 8. Sort Tasks

**Command**: `sort --by <date|priority|name> [--order <asc|desc>]`

**Description**: Sort tasks by date, priority, or name.

**Options**:
- `--by <date|priority|name>`: Sort criteria (required)
- `--order <asc|desc>`: Sort order (optional, default: asc)

**Examples**:
```
sort --by date
sort --by priority --order desc
sort --by name
sort --by date --order desc
```

**Behavior**:
- **Sort by date**: Tasks with due dates first (oldest first), tasks without due dates last
- **Sort by priority**: High > Medium > Low
- **Sort by name**: Alphabetical (A-Z by default)
- Displays sorted list of all tasks

---

### 9. Check Reminders

**Command**: `check-reminders`

**Description**: Manually check for tasks with due dates that have been reached or passed. Triggers notifications for overdue tasks.

**Arguments**: None

**Behavior**:
- Checks all pending tasks
- Triggers system notification (or console fallback) for each overdue task
- Displays list of overdue tasks
- Shows "No overdue tasks." if none found

**Note**: In a console app, reminders require manual triggering. This is a limitation of the in-memory, event-loop-less architecture.

---

## Extended Add Command

**Command**: `add "<title>" [--priority <High|Medium|Low>] [--tags <tag1,tag2,...>] [--due "YYYY-MM-DD HH:MM"] [--recurrence <None|Daily|Weekly>]`

**Description**: Create a new task with optional extended attributes.

**Arguments**:
- `<title>`: Task description (required)
- `--priority`: Priority level (optional, default: Medium)
- `--tags`: Comma-separated tags (optional)
- `--due`: Due date and time (optional)
- `--recurrence`: Recurrence pattern (optional, default: None)

**Examples**:
```
add "Buy groceries"
add "Submit report" --priority High --tags Work,Urgent
add "Team meeting" --priority Medium --tags Work --due "2026-01-05 14:00" --recurrence Weekly
add "Exercise" --tags Health --due "2026-01-03 07:00" --recurrence Daily
```

**Behavior**:
- Creates a new task with ID auto-incremented
- All optional fields use defaults if not specified
- Returns confirmation with task details

---

## Command Reference Summary

| Command | Purpose | Required Args | Optional Args |
|----------|-----------|----------------|---------------|
| `priority` | Set task priority | id, priority | none |
| `tag` | Add tags to task | id, tags | none |
| `untag` | Remove tags from task | id, tags | none |
| `due` | Set due date | id, datetime | none |
| `recurring` | Set recurrence pattern | id, recurrence | none |
| `search` | Search by keyword | keyword | none |
| `filter` | Filter tasks | filter criteria | additional filters |
| `sort` | Sort tasks | sort criteria | order |
| `check-reminders` | Check overdue tasks | none | none |
| `add` (extended) | Create task with attributes | title | priority, tags, due, recurrence |

---

## Phase I Commands (Unchanged)

The following Phase I commands remain unchanged and fully compatible:

- `add "<title>"` (basic version)
- `list`
- `view <id>`
- `complete <id>`
- `update <id> "new title"`
- `delete <id>`
- `help`
- `exit`

---

**Version**: 1.0.0 | **Status**: READY FOR IMPLEMENTATION
