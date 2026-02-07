"""
Sorting Service - Phase V
Provides sorting functionality for task lists.

[Task]: T014
[From]: phase-5/specs/007-phase-v-cloud-deployment/plan.md §3.1
"""

from typing import List
from datetime import datetime
from app.models.task import Task, TaskPriority
from typing import List, Dict, Any, Optional


def sort_tasks(tasks: List[Task], sort_by: str = "created_at", ascending: bool = False) -> List[Task]:
    """
    Sort tasks by specified field.

    Args:
        tasks: List of tasks to sort
        sort_by: Field to sort by (due_date, priority, title, created_at, updated_at)
        ascending: Sort order (False = descending/newest first)

    Returns:
        Sorted task list

    Supported sort fields:
    - due_date: Sort by due date (nulls last)
    - priority: Sort high → medium → low
    - title: Alphabetical
    - created_at: Newest first (default)
    - updated_at: Recently updated first
    """
    if sort_by == "due_date":
        return sort_by_due_date(tasks, ascending)
    elif sort_by == "priority":
        return sort_by_priority(tasks, ascending)
    elif sort_by == "title":
        return sort_by_title(tasks, ascending)
    elif sort_by == "updated_at":
        return sort_by_updated_at(tasks, ascending)
    else:  # Default: created_at
        return sort_by_created_at(tasks, ascending)


def sort_by_due_date(tasks: List[Task], ascending: bool = False) -> List[Task]:
    """
    Sort tasks by due date.
    Tasks without due dates appear last.

    Args:
        tasks: List of tasks
        ascending: If True, earliest due dates first

    Returns:
        Sorted tasks
    """
    # Separate tasks with and without due dates
    tasks_with_due = [t for t in tasks if t.due_date]
    tasks_without_due = [t for t in tasks if not t.due_date]

    # Sort tasks with due dates
    tasks_with_due.sort(key=lambda t: t.due_date, reverse=not ascending)

    # Combine: due dates first, then no due dates
    return tasks_with_due + tasks_without_due


def sort_by_priority(tasks: List[Task], ascending: bool = False) -> List[Task]:
    """
    Sort tasks by priority level.
    High → Medium → Low (or reverse if ascending).

    Args:
        tasks: List of tasks
        ascending: If True, low priority first

    Returns:
        Sorted tasks
    """
    priority_order = {
        TaskPriority.high: 0,
        TaskPriority.medium: 1,
        TaskPriority.low: 2
    }

    # Sort by priority order
    sorted_tasks = sorted(
        tasks,
        key=lambda t: priority_order.get(t.priority, 1)
    )

    if ascending:
        sorted_tasks.reverse()

    return sorted_tasks


def sort_by_title(tasks: List[Task], ascending: bool = True) -> List[Task]:
    """
    Sort tasks alphabetically by title.

    Args:
        tasks: List of tasks
        ascending: If True, A-Z; if False, Z-A

    Returns:
        Sorted tasks
    """
    return sorted(
        tasks,
        key=lambda t: t.title.lower(),
        reverse=not ascending
    )


def sort_by_created_at(tasks: List[Task], ascending: bool = False) -> List[Task]:
    """
    Sort tasks by creation date.
    Default: Newest first (descending).

    Args:
        tasks: List of tasks
        ascending: If True, oldest first

    Returns:
        Sorted tasks
    """
    return sorted(
        tasks,
        key=lambda t: t.created_at,
        reverse=not ascending
    )


def sort_by_updated_at(tasks: List[Task], ascending: bool = False) -> List[Task]:
    """
    Sort tasks by last update date.
    Default: Recently updated first (descending).

    Args:
        tasks: List of tasks
        ascending: If True, least recently updated first

    Returns:
        Sorted tasks
    """
    return sorted(
        tasks,
        key=lambda t: t.updated_at,
        reverse=not ascending
    )


def multi_sort(
    tasks: List[Task],
    primary_sort: str = "priority",
    secondary_sort: str = "due_date"
) -> List[Task]:
    """
    Sort by multiple fields (primary, then secondary).

    Args:
        tasks: List of tasks
        primary_sort: Primary sort field
        secondary_sort: Secondary sort field (for ties)

    Returns:
        Multi-level sorted tasks

    Example:
        Sort by priority (high first), then by due date within each priority
    """
    # First sort by secondary field
    result = sort_tasks(tasks, secondary_sort)

    # Then sort by primary field (stable sort preserves secondary order)
    result = sort_tasks(result, primary_sort)

    return result


def get_sort_statistics(tasks: List[Task]) -> Dict[str, int]:
    """
    Get statistics about task distribution.

    Args:
        tasks: List of tasks

    Returns:
        Dictionary with counts by priority, status, etc.
    """
    stats = {
        "total": len(tasks),
        "completed": len([t for t in tasks if t.completed]),
        "pending": len([t for t in tasks if not t.completed]),
        "high_priority": len([t for t in tasks if t.priority == TaskPriority.high]),
        "medium_priority": len([t for t in tasks if t.priority == TaskPriority.medium]),
        "low_priority": len([t for t in tasks if t.priority == TaskPriority.low]),
        "with_due_date": len([t for t in tasks if t.due_date]),
        "overdue": len(filter_overdue_tasks(tasks)),
        "recurring": len([t for t in tasks if t.recurrence_pattern]),
    }

    return stats
