# Todo Console Application

A simple, user-friendly command-line todo list application built with Python 3.13+.

## Features

- ✅ Add new tasks
- 📋 View all tasks
- ✓ Mark tasks as complete
- ✏️ Edit task titles
- 🗑️ Delete tasks
- 🎯 Arrow key navigation
- 💬 Clear user feedback

## Quick Start

### Requirements

- Python 3.13 or higher
- UV (Python package manager)

### Installation

```bash
# Install with UV
uv pip install -e .
```

### Run the App

```bash
uv run todo
```

Or if using virtual environment:

```bash
# Activate virtual environment
. .venv/bin/activate

# Run the app
python -m todo_app.main
```

## How to Use

### Main Menu

```
┌────────────────────────────────────────────────┐
│                TODO APPLICATION                │
├────────────────────────────────────────────────┤
│ ▶ 1. Add New Task      - Create a new todo item │
│    2. View Tasks       - See all your tasks    │
│    3. Exit Application - Close the app         │
├────────────────────────────────────────────────┤
│ Use ↑/↓ arrows to select, Enter to choose      │
└────────────────────────────────────────────────┘
```

### Controls

| Key | Action |
|-----|--------|
| ↑/↓ | Navigate menu |
| Enter | Select option |
| c | Mark task complete |
| d | Delete task |
| e | Edit task |
| q | Go back |

### Adding Tasks

1. Select "Add New Task"
2. Enter task description
3. Press Enter to confirm
4. Add another task or press 'n' to return to menu

### Viewing Tasks

1. Select "View Tasks"
2. Use ↑/↓ to navigate
3. Press Enter to see task details
4. Choose action: complete, edit, or delete

## Project Structure

```
Todo-app/
├── src/todo_app/
│   ├── __init__.py       # Package init
│   ├── models.py         # Task dataclass
│   ├── storage.py        # TaskList storage
│   ├── cli.py            # Command parser
│   ├── ui.py             # User interface
│   └── main.py           # Entry point
├── specs/
│   └── 001-todo-console-app/
│       ├── spec.md       # Feature specification
│       ├── plan.md       # Implementation plan
│       └── tasks.md      # Task breakdown
├── pyproject.toml        # Package config
└── README.md             # This file
```

## Development

### Run Tests

```bash
uv run python -m pytest
```

### Reinstall Package

```bash
uv pip install -e .
```

## License

MIT
