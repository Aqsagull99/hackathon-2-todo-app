# Implementation Plan: In-Memory Todo Console Application

**Branch**: `001-todo-console-app` | **Date**: 2025-12-28 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `specs/001-todo-console-app/spec.md`

## Summary

Build a user-friendly Python console application for managing todo tasks in memory. The application supports 5 basic operations: Add, View, Update, Delete, and Mark Complete. Following spec-driven development principles, all implementation decisions are derived from the approved feature specification. The architecture prioritizes simplicity, readability, and excellent user experience for beginner developers.

## Working Console Demo Requirements

The application must demonstrate these 5 core features:

| # | Feature | Description |
|---|---------|-------------|
| 1 | **Adding Tasks** | Users can add tasks with title and description, with clear input guidance and examples |
| 2 | **Listing Tasks** | Display all tasks in a formatted table with `[  TODO ]` or `[✓ DONE]` status indicators |
| 3 | **Updating Tasks** | Edit task titles with before/after comparison and confirmation |
| 4 | **Deleting Tasks** | Remove tasks by ID with y/n confirmation dialog |
| 5 | **Marking Complete** | Toggle task status between pending and complete with visual feedback |

### UX Requirements

| Requirement | Implementation |
|-------------|----------------|
| Clear screen titles | Every screen shows: ADD NEW TASK, VIEW TASKS, etc. |
| Input guidance | Show examples: "Examples: 'Buy groceries', 'Call mom'" |
| Status indicators | `[  TODO ]` for pending, `[✓ DONE]` for completed |
| User feedback | `✓` success, `✗` error, `ℹ` information icons |
| Arrow navigation | `▶` indicates selection, `↑/↓` for navigation |
| Confirmation dialogs | Delete requires explicit y/n confirmation |
| Error recovery | "Press Enter to continue" after errors/actions |

## Technical Context

**Language/Version**: Python 3.13+ (standard library only)
**Primary Dependencies**: None (standard library only)
**Storage**: In-memory dictionary (no persistence)
**Testing**: Manual CLI testing only (no automated tests for Phase I)
**Target Platform**: Console/Terminal (cross-platform: Linux, macOS, Windows)
**Project Type**: Single console application
**Performance Goals**: Not applicable (single-user, small dataset)
**Constraints**: No persistence, no external libraries, no GUI/web
**Scale/Scope**: Single-user, local session only

## Constitution Check

*GATE: Must pass before implementation*

| Principle | Compliance | Evidence |
|-----------|------------|----------|
| I. Spec-Driven Development | ✅ PASS | All features defined in spec.md, no deviation |
| II. Simplicity | ✅ PASS | Standard library only, simple data structures |
| III. Correctness | ✅ PASS | Acceptance scenarios define expected behavior |
| IV. Maintainability | ✅ PASS | Clear module separation planned |
| V. Determinism | ✅ PASS | In-memory only, no external state |

## Project Structure

### Documentation (this feature)

```text
specs/001-todo-console-app/
├── plan.md              # This file
├── spec.md              # Feature specification
├── research.md          # Phase 0 output (not needed - no unknowns)
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # CLI commands interface
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code (repository root)

```text
src/
├── todo_app/
│   ├── __init__.py
│   ├── models.py        # Task dataclass
│   ├── storage.py       # In-memory TaskList
│   ├── cli.py           # Command interface
│   └── main.py          # Entry point
tests/                   # Not required for Phase I
```

**Structure Decision**: Using single project structure under `src/todo_app/` as specified in the constitution. Simple console app requires minimal structure.

## Data Model

### Task Entity

```python
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Task:
    id: int
    title: str
    completed: bool = False
    created_at: datetime = None  # Optional timestamp
```

### TaskList Storage

```python
class TaskList:
    def __init__(self):
        self.tasks: dict[int, Task] = {}
        self.next_id: int = 1

    def add(self, title: str) -> Task
    def get_all(self) -> list[Task]
    def get_by_id(self, task_id: int) -> Task | None
    def update_title(self, task_id: int, title: str) -> Task | None
    def delete(self, task_id: int) -> bool
    def toggle_complete(self, task_id: int) -> Task | None
```

## CLI Commands

| Command | Format | Description |
|---------|--------|-------------|
| add | `add "title"` | Create new task |
| list | `list` | Show all tasks |
| view | `view <id>` | Show task details |
| complete | `complete <id>` | Mark task complete |
| update | `update <id> "new title"` | Update task title |
| delete | `delete <id>` | Delete task |
| help | `help` | Show commands |
| exit | `exit` | Quit application |

## Complexity Tracking

No constitution violations. Simple in-memory console app requires no complex patterns or justifications.

## Key Decisions

| Decision | Rationale |
|----------|-----------|
| Dictionary for storage | O(1) lookup by ID, simple implementation |
| Auto-increment IDs | Predictable, matches spec requirement |
| Dataclass for Task | Pythonic, clean representation |
| Simple CLI loop | Standard pattern for console apps |
| No external dependencies | Constitutional requirement |
