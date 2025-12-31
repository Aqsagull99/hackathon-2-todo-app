# Claude Code Rules - Phase 1 (Console App)

This file provides Claude Code instructions for the Todo Console Application.

## Project Overview

**Project**: Todo Console Application (Hackathon 2 Phase 1)
**Language**: Python 3.13+
**Type**: In-memory console application
**Features**: Add, View, Complete, Update, Delete tasks

## How to Run the App

```bash
cd ~/Todo-app/Phase-one
uv run todo
```

## Testing the App

```bash
# Run the app interactively
uv run todo

# Quick feature test
echo -e '1\nBuy groceries\nn\n4' | uv run todo
```

## Project Structure

```
Phase-one/
├── src/todo_app/
│   ├── models.py     # Task dataclass
│   ├── storage.py    # TaskList storage
│   ├── cli.py        # Command parser
│   ├── ui.py         # Interactive UI
│   └── main.py       # Entry point
├── specs/001-todo-console-app/
│   ├── spec.md       # Feature spec
│   ├── plan.md       # Implementation plan
│   └── tasks.md      # Task breakdown
└── history/prompts/todo-console-app/  # Prompt History
```

## PHR Records

All work for Phase 1 is recorded in `history/prompts/todo-console-app/` and `history/prompts/phase1-ui-enhancement/` inside this folder.

---

## Core Guarantees

- Record every user input verbatim in a Prompt History Record (PHR).
- PHR routing:
  - Constitution → `history/prompts/constitution/`
  - Feature-specific → `history/prompts/todo-console-app/`
  - General → `history/prompts/general/`

## Development Guidelines

1. **Authoritative Source**: Use MCP tools for verification.
2. **Spec-Driven**: Always update `specs/` before changing code.
3. **Small Diffs**: Prefer smallest viable changes.
