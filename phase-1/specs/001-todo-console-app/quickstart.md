# Quickstart: Todo Console Application

**Phase**: Hackathon 2 - Phase I
**Created**: 2025-12-28

## Prerequisites

- Python 3.13+
- UV package manager

## Setup

```bash
# Initialize UV project
uv init todo-app --python 3.13
cd todo-app

# Create source structure
mkdir -p src/todo_app
touch src/todo_app/__init__.py
touch src/todo_app/models.py
touch src/todo_app/storage.py
touch src/todo_app/cli.py
touch src/todo_app/main.py
```

## Run the Application

```bash
# Activate environment and run
uv run python src/todo_app/main.py
```

## Usage Workflow

### 1. Add a Task
```
> add "Buy groceries"
Created task 1: "Buy groceries"
```

### 2. View All Tasks
```
> list
[ ] 1. Buy groceries
```

### 3. Mark Complete
```
> complete 1
Task 1 marked as complete
```

### 4. Update Title
```
> update 1 "Buy groceries and fruits"
Task 1 updated to: "Buy groceries and fruits"
```

### 5. Delete Task
```
> delete 1
Task 1 deleted
```

## Full Command List

| Command | Example |
|---------|---------|
| `add "title"` | `add "Buy groceries"` |
| `list` | `list` |
| `view <id>` | `view 1` |
| `complete <id>` | `complete 1` |
| `update <id> "title"` | `update 1 "New title"` |
| `delete <id>` | `delete 1` |
| `help` | `help` |
| `exit` | `exit` |

## Verification Checklist

- [ ] App starts successfully
- [ ] Can add tasks
- [ ] Tasks appear in list
- [ ] Can mark tasks complete
- [ ] Can update task titles
- [ ] Can delete tasks
- [ ] Error messages display correctly
- [ ] Help shows all commands

## Next Steps

After verification, proceed to `/sp.tasks` to generate implementation tasks.
