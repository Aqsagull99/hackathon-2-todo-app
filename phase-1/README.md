# Todo Console Application (Hackathon 2 Phase 1)

Professional in-memory console-based Todo application built using **Spec-Driven Development** (SDD) and **Claude Code**.

## 🚀 Features

- **Interactive UI**: Rich terminal interface with box borders and arrow key navigation.
- **Dynamic Highlights**: Colorful selection markers and status indicators (PENDING/DONE).
- **Comprehensive Task Management**:
  - Add new tasks with description validation.
  - View tasks in a formatted table with timestamps.
  - Update task titles.
  - Mark tasks as complete/incomplete.
  - Delete tasks by ID.
- **Robust Navigation**: Takeover screen buffer for a clean, stationary UI experience (no scrolling artifact).

## 🛠️ Technology Stack

- **Language**: Python 3.13+
- **Library**: [Rich](https://github.com/Textualize/rich) for terminal UI formatting.
- **Environment**: Managed with [UV](https://github.com/astral-sh/uv).
- **Methodology**: Spec-Driven Development using Spec-Kit Plus.

## 📦 Installation & Setup

1. **Ensure UV is installed**:
   ```bash
   curl -LsSf https://astral-sh/uv/install.sh | sh
   ```

2. **Run the Application**:
   ```bash
   uv run todo
   ```

3. **Install as Editable Package** (Optional):
   ```bash
   uv pip install -e .
   ```

## 📂 Project Structure

```
phase-1/
├── src/todo_app/
│   ├── models.py     # Data structures
│   ├── storage.py    # Memory-based task storage
│   ├── ui.py         # Advanced Interactive UI
│   ├── cli.py        # Command-line parser
│   └── main.py       # Application entry point
├── specs/            # SDD Documentation (Spec, Plan, Tasks)
├── history/          # PHR (Prompt History Records)
└── pyproject.toml    # Project configuration
```

## 🧠 Development Methodology

This project was built entirely using **Spec-Driven Development**.
- **Specifications**: Defined in `specs/001-todo-console-app/spec.md`.
- **Implementation**: Executed by Claude Code based on approved plans and task lists.
- **Traceability**: All prompt history is preserved in `history/prompts/`.

---
🤖 Generated with [Claude Code](https://claude.com/claude-code)
