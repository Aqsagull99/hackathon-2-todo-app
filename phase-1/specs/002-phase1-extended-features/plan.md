# Implementation Plan: Todo App Phase I Extended Features

**Branch**: `002-phase1-extended-features` | **Date**: 2026-01-01 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification for intermediate (organization) and advanced (intelligent) features

## Summary

Extend the existing in-memory Python console Todo app with organization, usability, and intelligent features while maintaining simplicity and backward compatibility with basic CRUD operations. This implementation adds task priorities, tags, search, filtering, sorting, recurring tasks, and due date reminders without modifying the existing UI flow or breaking existing functionality. All changes must be incremental and optional.

## Technical Context

**Language/Version**: Python 3.13+ (standard library only)
**Primary Dependencies**: None (standard library only)
**Storage**: In-memory dictionary (no persistence)
**Testing**: Manual CLI testing
**Target Platform**: Console/Terminal (cross-platform)
**Project Type**: Single console application (extending existing Phase I)
**Performance Goals**:
- Filter operations on 50 tasks must complete within 2 seconds
- Recurring task rescheduling must complete within 1 second
- Reminder notifications must trigger within ±5 seconds of set time
**Constraints**:
- No persistence (in-memory)
- No external libraries
- No UI/UX redesign (reuse existing screens and layouts)
- All new features must be optional and non-intrusive
- Must maintain backward compatibility with existing CRUD operations
- Browser/system notifications (may use platform-specific calls)
**Scale/Scope**: Single-user, local session only
**Unknowns to Resolve**: NEEDS CLARIFICATION - Browser notification mechanism for console app

## Constitution Check

*GATE: Must pass before implementation*

| Principle | Compliance | Evidence |
|-----------|------------|----------|
| I. Spec-Driven Development | ✅ PASS | All features defined in spec.md |
| II. Usability | ✅ PASS | Features enhance usability without complexity |
| III. Clarity | ✅ PASS | Simple, readable data model extensions planned |
| IV. Incremental Enhancement | ✅ PASS | All new features extend existing model |
| V. Backward Compatibility | ✅ PASS | New fields optional; existing CRUD unchanged |

## Phase 0: Research & Clarifications

### Research Tasks

**Task 1**: Browser/notification mechanism for console app
- **Unknown**: How to trigger notifications from a console application without external libraries?
- **Options**:
  1. Use `platform` module to call system notifications (terminal-specific)
  2. Use `subprocess` to call native notification commands (e.g., `notify-send` on Linux)
  3. Fallback to console beeps or on-screen messages
- **Decision**: Use platform-specific subprocess calls with graceful fallback to console messages
- **Rationale**: Provides notification capability when available, degrades gracefully otherwise

**Task 2**: Recurrence rule implementation
- **Unknown**: How to handle date arithmetic for recurring tasks?
- **Options**:
  1. Use `datetime` and `timedelta` from standard library
  2. Implement simple day counting
- **Decision**: Use `datetime` and `timedelta` for robust date handling
- **Rationale**: Standard library, handles edge cases (month boundaries, leap years)

**Task 3**: Tag storage format
- **Unknown**: How to store tags in the data model?
- **Options**:
  1. Comma-separated string
  2. List[str]
  3. Set[str] (deduplicated)
- **Decision**: List[str] (stored as field, converted to Set for deduplication in operations)
- **Rationale**: Simple representation, allows duplicate prevention in logic

## Phase 1: Design & Contracts

### Data Model Extensions

#### Updated Task Entity

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
from enum import Enum

class Priority(str, Enum):
    """Priority levels for tasks."""
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"

class Recurrence(str, Enum):
    """Recurrence patterns for tasks."""
    NONE = "None"
    DAILY = "Daily"
    WEEKLY = "Weekly"

@dataclass
class Task:
    """Represents a single todo task with extended attributes.

    Attributes:
        id: Unique identifier for the task (assigned by TaskList)
        title: Short description of the task
        completed: Whether the task has been completed
        created_at: Timestamp when the task was created
        priority: Task priority (High/Medium/Low)
        tags: List of string labels for categorization
        due_date: Optional datetime for task deadline
        recurrence: Recurrence pattern (None/Daily/Weekly)
    """
    id: int
    title: str
    completed: bool = False
    created_at: Optional[datetime] = field(default_factory=datetime.now)
    priority: Priority = Priority.MEDIUM  # Default
    tags: List[str] = field(default_factory=list)  # Default empty
    due_date: Optional[datetime] = None
    recurrence: Recurrence = Recurrence.NONE  # Default
```

#### Extended TaskList Operations

```python
class TaskList:
    # ... existing CRUD methods ...

    # New methods for extended features
    def update_priority(self, task_id: int, priority: Priority) -> Optional[Task]
    def add_tags(self, task_id: int, tags: List[str]) -> Optional[Task]
    def remove_tags(self, task_id: int, tags: List[str]) -> Optional[Task]
    def set_due_date(self, task_id: int, due_date: datetime) -> Optional[Task]
    def set_recurrence(self, task_id: int, recurrence: Recurrence) -> Optional[Task]

    # Search and filter methods
    def search(self, keyword: str) -> List[Task]
    def filter_by_status(self, status: bool) -> List[Task]
    def filter_by_priority(self, priority: Priority) -> List[Task]
    def filter_by_due_date(self, start: Optional[datetime], end: Optional[datetime]) -> List[Task]

    # Sorting methods
    def sort_by_date(self, descending: bool = False) -> List[Task]
    def sort_by_priority(self, descending: bool = False) -> List[Task]
    def sort_by_name(self, descending: bool = False) -> List[Task]

    # Recurring task handling
    def create_recurring_instance(self, task: Task) -> Task

    # Notification methods
    def check_reminders(self) -> List[Task]
```

### CLI Command Extensions

| Command | Format | Description |
|---------|--------|-------------|
| add | `add "title" [options]` | Create new task with optional priority, tags, due date |
| priority | `priority <id> <High|Medium|Low>` | Set task priority |
| tag | `tag <id> <tag1,tag2,...>` | Add tags to task |
| untag | `untag <id> <tag1,tag2,...>` | Remove tags from task |
| due | `due <id> "YYYY-MM-DD HH:MM"` | Set due date/time for task |
| recurring | `recurring <id> <None|Daily|Weekly>` | Set recurrence pattern |
| search | `search "<keyword>"` | Search tasks by keyword |
| filter | `filter --status <pending|completed> --priority <High|Medium|Low>` | Filter tasks |
| sort | `sort --by <date|priority|name> --order <asc|desc>` | Sort tasks |
| check-reminders | `check-reminders` | Check for due tasks (manual trigger for console) |

### Notification Mechanism

```python
# Platform-specific notification handler
class NotificationManager:
    def send_notification(self, title: str, message: str) -> bool:
        """Send system notification if available, fallback to console."""
        # Linux: notify-send
        # macOS: osascript -e 'display notification'
        # Windows: toast notification (powershell)
        # Fallback: Print to console with visual indicator
```

## Phase 2: Implementation Tasks (Generated by /sp.tasks)

To be generated after plan approval.

## Project Structure

### Documentation (this feature)

```text
specs/002-phase1-extended-features/
├── plan.md              # This file
├── spec.md              # Feature specification
├── research.md          # Phase 0 output (see above section)
├── data-model.md        # Phase 1 output (detailed entity definitions)
├── quickstart.md        # Phase 1 output (usage guide)
├── contracts/           # CLI interface documentation
│   └── commands.md      # Extended CLI commands
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code Modifications

```text
src/todo_app/
├── models.py            # Extended with Priority, Recurrence enums, Task fields
├── storage.py           # Extended with search, filter, sort methods
├── cli.py               # Extended with new command handlers
├── ui.py                # Extended with new UI screens (optional)
├── notifications.py     # NEW: Notification manager
└── main.py              # Unchanged (or minor adjustments)
```

## Key Decisions

| Decision | Rationale |
|----------|-----------|
| Dataclass extensions | Clean, backward-compatible field additions |
| Optional fields with defaults | Maintains backward compatibility with existing code |
| Enum for Priority/Recurrence | Type safety, prevents invalid values |
| List[str] for tags | Simple, supports multiple tags per task |
| subprocess for notifications | No external dependencies, platform-agnostic |
| Separate search/filter/sort methods | Clear separation of concerns |
| Manual reminder check command | Console-app limitation (no event loop for timers) |
| create_recurring_instance method | Encapsulates recurrence logic |

## Complexity Tracking

No constitution violations. All features are extensions to existing model, maintaining simplicity and backward compatibility.

## Integration Points

- **Existing TaskList**: Extend with new methods (no breaking changes)
- **Existing UI**: Reuse existing screens, add new menu options
- **Existing CLI**: Add new commands, preserve existing command interface
- **Data migration**: Not needed (in-memory, fresh start on app restart)

## Testing Strategy

1. **Unit-level**: Manual CLI testing of each new command
2. **Integration**: Test search/filter/sort combinations
3. **Regression**: Verify existing CRUD operations still work
4. **Edge cases**:
   - Empty task list
   - Tasks with all optional fields
   - Tasks with no optional fields
   - Recurring task boundary cases (month end, leap year)
   - Notification on different platforms (or graceful failure)

## Definition of Done

- [ ] All extended features implemented per spec
- [ ] Existing CRUD operations remain functional
- [ ] User can add tasks with priorities, tags, due dates, recurrence
- [ ] Search, filter, and sort work on task list
- [ ] Recurring tasks auto-create new instances on completion
- [ ] Notifications trigger (or fallback gracefully)
- [ ] No UI/UX redesign (reuse existing screens)
- [ ] Code remains readable and maintainable
- [ ] Ready for Phase II (full-stack web app migration)

---

**Version**: 1.0.0 | **Status**: DRAFT | **Phase**: I (Extended)
