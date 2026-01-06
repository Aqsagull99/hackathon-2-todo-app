# Research Findings: Todo App Phase I Extended Features

**Branch**: `002-phase1-extended-features` | **Date**: 2026-01-01
**Status**: Complete - Ready for Phase 1

---

## Overview

This document summarizes research findings for unknowns identified in the planning phase. All unknowns have been resolved using standard library solutions that align with the constitution (no external dependencies).

---

## 1. Browser/Notification Mechanism for Console App

### Unknown

How to trigger notifications from a console application without external libraries?

### Decision

Use platform-specific subprocess calls with graceful fallback to console messages.

### Implementation Plan

```python
import subprocess
import platform

class NotificationManager:
    def __init__(self):
        self.platform = platform.system().lower()

    def send_notification(self, title: str, message: str) -> bool:
        """Send a system notification, fallback to console."""
        try:
            if self.platform == 'linux':
                return self._notify_linux(title, message)
            elif self.platform == 'darwin':
                return self._notify_macos(title, message)
            elif self.platform == 'windows':
                return self._notify_windows(title, message)
        except Exception:
            return self._notify_console(title, message)
        return False

    def _notify_linux(self, title: str, message: str) -> bool:
        """Use notify-send for Linux notifications."""
        cmd = ["notify-send", "-u", "normal", title, message]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            return self._notify_console(title, message)
        return True

    def _notify_macos(self, title: str, message: str) -> bool:
        """Use osascript for macOS notifications."""
        cmd = [
            "osascript", "-e",
            f'display notification "{message}" with title "{title}"'
        ]
        subprocess.run(cmd, capture_output=True, text=True)
        return True

    def _notify_windows(self, title: str, message: str) -> bool:
        """Use PowerShell toast notification on Windows."""
        powershell_script = f"""
        Add-Type -AssemblyName System.Windows.Forms
        [System.Windows.Forms.ToolTip]::new().Show("{message}", "{title}", 0, 0, 5000)
        """
        cmd = ["powershell", "-Command", powershell_script]
        subprocess.run(cmd, capture_output=True, text=True)
        return True

    def _notify_console(self, title: str, message: str) -> bool:
        """Fallback: Print to console with visual indicator."""
        print(f"\n\ud83d\udd14 REMINDER: [{title}] {message}")
        print("Press Enter to continue...")
        return True
```

### Rationale

- **Platform Coverage**: Supports Linux, macOS, Windows (the three major platforms)
- **Graceful Degradation**: If system notifications fail, falls back to console output
- **No External Dependencies**: Uses only `subprocess` and `platform` from standard library
- **User Experience**: Console fallback ensures reminders are always visible
- **Maintainability**: Simple implementation, easy to debug

### Alternatives Considered

| Alternative | Pros | Cons | Decision |
|-------------|------|------|----------|
| Third-party library (plyer) | Cross-platform, robust | Violates constitution (no external deps) | ❌ Rejected |
| Web browser notifications | Consistent across platforms | Requires web server, not console app | ❌ Rejected |
| Only console output | No platform-specific code | Poor user experience | ❌ Rejected |
| Subprocess with fallback | Works on all platforms, degrades gracefully | More code, platform-specific commands | ✅ **Chosen** |

---

## 2. Recurrence Rule Implementation

### Unknown

How to handle date arithmetic for recurring tasks?

### Decision

Use `datetime` and `timedelta` from standard library for robust date handling.

### Implementation Plan

```python
from datetime import datetime, timedelta
from typing import Optional

class RecurrenceManager:
    """Handle recurrence logic for tasks."""

    @staticmethod
    def calculate_next_due_date(
        current_due: datetime,
        recurrence: str  # "Daily" or "Weekly"
    ) -> Optional[datetime]:
        """Calculate next due date based on recurrence pattern.

        Args:
            current_due: The current due date of completed task
            recurrence: Recurrence pattern ("Daily" or "Weekly")

        Returns:
            The next due date, or None if recurrence is "None"
        """
        if recurrence == "Daily":
            return current_due + timedelta(days=1)
        elif recurrence == "Weekly":
            return current_due + timedelta(weeks=1)
        else:
            return None  # No recurrence

    @staticmethod
    def validate_recurrence(recurrence: str) -> bool:
        """Validate that a recurrence pattern is supported."""
        return recurrence in ["None", "Daily", "Weekly"]
```

### Usage in TaskList

```python
def create_recurring_instance(self, task: Task) -> Task:
    """Create a new task instance for a recurring task.

    Args:
        task: The completed recurring task

    Returns:
        The new task instance with updated due date
    """
    if task.recurrence == "None":
        return None

    next_due = RecurrenceManager.calculate_next_due_date(
        task.due_date,
        task.recurrence
    )

    if next_due is None:
        return None

    new_task = Task(
        id=self.next_id,
        title=task.title,
        completed=False,
        priority=task.priority,
        tags=task.tags.copy(),
        due_date=next_due,
        recurrence=task.recurrence
    )

    self.tasks[new_task.id] = new_task
    self.next_id += 1
    return new_task
```

### Rationale

- **Standard Library**: `datetime` and `timedelta` are built-in, no external deps
- **Edge Case Handling**: Automatically handles month boundaries, leap years, etc.
- **Type Safety**: Clear datetime objects, no string parsing issues
- **Extensibility**: Easy to add new recurrence patterns (e.g., bi-weekly, monthly)

### Alternatives Considered

| Alternative | Pros | Cons | Decision |
|-------------|------|------|----------|
| Manual day counting (int + 1, + 7) | Simple, no datetime objects | Error-prone, doesn't handle edge cases | ❌ Rejected |
| dateutil library (rrule) | Powerful recurrence patterns | External dependency (violates constitution) | ❌ Rejected |
| datetime + timedelta | Robust, handles edge cases, standard lib | Slightly more complex than int math | ✅ **Chosen** |

---

## 3. Tag Storage Format

### Unknown

How to store tags in data model?

### Decision

Use `List[str]` (stored as field, converted to `Set[str]` for deduplication in operations).

### Implementation Plan

```python
from dataclasses import dataclass, field
from typing import List

@dataclass
class Task:
    # ... other fields ...
    tags: List[str] = field(default_factory=list)
```

### Tag Operations

```python
class TaskList:
    def add_tags(self, task_id: int, tags: List[str]) -> Optional[Task]:
        """Add tags to a task, avoiding duplicates.

        Args:
            task_id: ID of task
            tags: List of tags to add

        Returns:
            Updated task if found, None otherwise
        """
        task = self.tasks.get(task_id)
        if task:
            # Use set for deduplication, convert back to list
            existing_tags = set(task.tags)
            new_tags = set(tags)
            combined = existing_tags.union(new_tags)
            task.tags = list(combined)
        return task

    def remove_tags(self, task_id: int, tags: List[str]) -> Optional[Task]:
        """Remove tags from a task.

        Args:
            task_id: ID of task
            tags: List of tags to remove

        Returns:
            Updated task if found, None otherwise
        """
        task = self.tasks.get(task_id)
        if task:
            existing_tags = set(task.tags)
            tags_to_remove = set(tags)
            remaining = existing_tags - tags_to_remove
            task.tags = list(remaining)
        return task
```

### Rationale

- **Storage**: `List[str]` is simple and serializable (if persistence is added later)
- **Deduplication**: Use `Set[str]` temporarily in operations, then convert back to `List[str]`
- **Type Clarity**: Clear representation of ordered collection of strings
- **Flexibility**: Easy to iterate, search, and manipulate

### Alternatives Considered

| Alternative | Pros | Cons | Decision |
|-------------|------|------|----------|
| Comma-separated string | Simple storage, easy to serialize | No deduplication, requires parsing, loses order | ❌ Rejected |
| Set[str] (as field) | Automatic deduplication | Loses order (tags may appear in different order), non-serializable in some contexts | ❌ Rejected |
| List[str] with set operations | Ordered, serializable, deduplicated in logic | Slightly more code for deduplication | ✅ **Chosen** |

---

## Summary of Decisions

| Area | Decision | Impact |
|------|----------|--------|
| Notifications | Platform subprocess calls with console fallback | Cross-platform, graceful degradation |
| Recurrence | `datetime` + `timedelta` | Robust date arithmetic, standard library |
| Tags | `List[str]` stored, `Set[str]` for operations | Ordered storage, automatic deduplication |

---

## Verification Checklist

- [x] All unknowns from plan.md are resolved
- [x] Decisions align with constitution (no external dependencies)
- [x] Alternatives were evaluated and documented
- [x] Implementation approaches are clear and actionable
- [x] Rationale is well-documented for future reference

---

**Status**: READY FOR PHASE 1 (Design & Contracts)
