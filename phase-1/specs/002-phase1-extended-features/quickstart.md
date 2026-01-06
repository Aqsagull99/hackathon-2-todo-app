# Quick Start Guide: Todo App Phase I Extended Features

**Branch**: `002-phase1-extended-features` | **Date**: 2026-01-01

---

## Overview

This guide helps you quickly get started with the extended features of the Todo console application. Extended features include task priorities, tags, search, filtering, sorting, recurring tasks, and due date reminders.

---

## Installation

No installation required. The app is an in-memory Python console application using only the standard library.

### Running the App

```bash
cd ~/Todo-app/Phase-one
uv run todo
```

Or with Python directly:

```bash
cd ~/Todo-app/Phase-one
python -m todo_app
```

---

## Quick Tutorial

### 1. Basic Workflow (Phase I Compatible)

Create, view, and complete tasks:

```bash
# Add a simple task
> add "Buy groceries"

# View all tasks
> list

# Mark a task complete
> complete 1

# View tasks again (shows completed status)
> list
```

### 2. Add Task with Priority

```bash
# Add high-priority task
> add "Submit project report" --priority High

# View task details
> view 1
# Output: ID: 1, Title: Submit project report, Priority: High, Completed: No
```

### 3. Add Tags to Tasks

```bash
# Add tags to an existing task
> tag 1 Work,Urgent

# Add another tag
> tag 1 Important

# Remove a tag
> untag 1 Urgent
```

### 4. Set Due Date and Recurrence

```bash
# Set a due date for a task
> due 1 "2026-01-05 17:00"

# Make it a weekly recurring task
> recurring 1 Weekly

# View the task
> view 1
# Shows: Due: 2026-01-05 17:00, Recurrence: Weekly
```

### 5. Search for Tasks

```bash
# Search by keyword
> search "project"

# Output shows all tasks with "project" in title or tags
```

### 6. Filter Tasks

```bash
# Filter by priority
> filter --priority High

# Filter by status
> filter --status pending

# Filter by date range
> filter --start-date "2026-01-01" --end-date "2026-01-31"

# Combine filters
> filter --status pending --priority High
```

### 7. Sort Tasks

```bash
# Sort by due date (oldest first)
> sort --by date

# Sort by priority (high to low)
> sort --by priority

# Sort by name (A to Z)
> sort --by name

# Sort descending
> sort --by date --order desc
```

### 8. Check Reminders

```bash
# Check for overdue tasks
> check-reminders

# Shows overdue tasks and triggers system notifications (or console alerts)
```

---

## Common Use Cases

### Use Case 1: Work Task Management

```bash
# Add multiple work tasks
> add "Finish quarterly report" --priority High --tags Work,Important --due "2026-01-10 17:00"
> add "Team standup meeting" --priority Medium --tags Work --due "2026-01-03 09:00" --recurring Weekly
> add "Review pull requests" --priority Medium --tags Work

# View only work tasks
> filter --tags Work

# View only high-priority work tasks
> filter --priority High
```

### Use Case 2: Personal Task Management

```bash
# Add personal tasks
> add "Grocery shopping" --priority Low --tags Home,Shopping
> add "Call dentist" --priority Medium --tags Home,Health --due "2026-01-05 10:00"
> add "Daily exercise" --priority Medium --tags Health --due "2026-01-01 07:00" --recurring Daily

# Search for health-related tasks
> search "health"

# Sort personal tasks by priority
> sort --by priority
```

### Use Case 3: Managing Recurring Tasks

```bash
# Create daily recurring task
> add "Morning meditation" --priority Medium --tags Health --due "2026-01-01 07:00" --recurring Daily

# Create weekly recurring task
> add "Weekly team sync" --priority High --tags Work --due "2026-01-03 14:00" --recurring Weekly

# Complete the task (creates new instance automatically)
> complete 1

# List tasks again (new recurring instance appears)
> list
```

---

## Priority Levels

| Priority | Color/Indicator | When to Use |
|----------|-----------------|--------------|
| High | 🔴 Red | Urgent, deadline-driven tasks |
| Medium | 🟡 Yellow | Normal priority tasks (default) |
| Low | 🟢 Green | Tasks that can be deferred |

---

## Tagging Best Practices

1. **Keep tags short**: 1-2 words per tag (e.g., "Work", "Shopping", "Important")
2. **Use consistent tags**: "Work" vs "Office" - pick one and stick to it
3. **Limit tags per task**: 3-5 tags max for readability
4. **Use categories**: Common categories include:
   - Context: Work, Home, Personal
   - Project: Website, App, Report
   - Priority: Urgent, Important, Normal
   - Type: Meeting, Task, Call, Email

---

## Date Format

All due dates use **ISO 8601 format**: `YYYY-MM-DD HH:MM`

| Format | Example | Meaning |
|---------|----------|----------|
| `YYYY-MM-DD` | `2026-01-05` | January 5, 2026 at midnight (00:00) |
| `YYYY-MM-DD HH:MM` | `2026-01-05 14:30` | January 5, 2026 at 2:30 PM |

**Tips**:
- Time is optional (defaults to 00:00)
- Use 24-hour format (14:30 = 2:30 PM)
- Dates are inclusive for filtering

---

## Recurrence Patterns

| Pattern | Behavior | Example |
|----------|----------|----------|
| None | Task does not repeat | Default for all tasks |
| Daily | Repeats every 24 hours from completion | "Drink water" → new task daily |
| Weekly | Repeats every 7 days from completion | "Team meeting" → new task weekly |

**Important**: Recurring tasks require a due date to work correctly.

---

## Search, Filter, Sort Cheatsheet

### Search
```bash
search "keyword"           # Search title and tags (case-insensitive)
```

### Filter
```bash
filter --status pending                # Show pending tasks only
filter --priority High                # Show high-priority tasks only
filter --start-date "2026-01-01"    # Show tasks due after Jan 1
filter --end-date "2026-01-31"      # Show tasks due before Jan 31
filter --status pending --priority High  # Combine filters (AND logic)
```

### Sort
```bash
sort --by date                    # Sort by due date (earliest first)
sort --by date --order desc        # Sort by due date (latest first)
sort --by priority                 # Sort by priority (high to low)
sort --by priority --order desc     # Sort by priority (low to high)
sort --by name                    # Sort alphabetically (A to Z)
sort --by name --order desc        # Sort alphabetically (Z to A)
```

---

## Keyboard Shortcuts

| Command | Shortcut (if available) |
|---------|----------------------|
| `help` | `?` |
| `exit` | `quit`, `q` |
| `list` | `ls` |
| `search "<kw>"` | `s "<kw>"` |

---

## Troubleshooting

### Issue: Command not recognized

**Solution**: Check command spelling and arguments. Run `help` to see all commands.

### Issue: Date format error

**Solution**: Use `YYYY-MM-DD` or `YYYY-MM-DD HH:MM` format with 24-hour time.

### Issue: Task ID not found

**Solution**: Run `list` to see all task IDs. Make sure you're using the correct ID.

### Issue: Notification not appearing

**Solution**: On Linux, install `notify-send` (`sudo apt-get install libnotify-bin`). On Windows/macOS, notifications may require permissions. If system notifications fail, the app falls back to console alerts.

---

## Next Steps

- Review [spec.md](spec.md) for detailed requirements
- Review [plan.md](plan.md) for implementation details
- Review [data-model.md](data-model.md) for entity definitions
- Review [contracts/commands.md](contracts/commands.md) for CLI reference

---

**Version**: 1.0.0 | **Status**: READY FOR USE
