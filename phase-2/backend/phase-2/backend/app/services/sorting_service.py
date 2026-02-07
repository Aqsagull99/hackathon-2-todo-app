"""
Sorting Service - Phase V
Provides sorting functionality for task lists.

[Task]: T014
[From]: phase-5/specs/007-phase-v-cloud-deployment/plan.md §3.1
"""

from typing import List
from datetime import datetime
from app.models.task import Task, TaskPriority


def sort_tasks(tasks: List[Task], sort_by: str = "created_at", ascending: bool = False) -> List[Task]:
    """Sort tasks by specified field."""
    if sort_by == "due_date":
        return sort_by_due_date(tasks, ascending)
    elif sort_by == "priority":
        return sort_by_priority(tasks, ascending)
    elif sort_by == "title":
        return sort_by_title(tasks, ascending)
    elif sort_by == "updated_at":
        return sort_by_updated_at(tasks, ascending)
    else:
        return sort_by_created_at(tasks, ascending)


def sort_by_due_date(tasks: List[Task], ascending: bool = False) -> List[Task]:
    """Sort tasks by due date (nulls last)."""
    tasks_with_due = [t for t in tasks if t.due_date]
    tasks_without_due = [t for t in tasks if not t.due_date]
    tasks_with_due.sort(key=lambda t: t.due_date, reverse=not ascending)
    return tasks_with_due + tasks_without_due


def sort_by_priority(tasks: List[Task], ascending: bool = False) -> List[Task]:
    """Sort tasks by priority (high → medium → low)."""
    priority_order = {
        TaskPriority.high: 0,
        TaskPriority.medium: 1,
        TaskPriority.low: 2
    }
    sorted_tasks = sorted(tasks, key=lambda t: priority_order.get(t.priority, 1))
    if ascending:
        sorted_tasks.reverse()
    return sorted_tasks


def sort_by_title(tasks: List[Task], ascending: bool = True) -> List[Task]:
    """Sort tasks alphabetically by title."""
    return sorted(tasks, key=lambda t: t.title.lower(), reverse=not ascending)


def sort_by_created_at(tasks: List[Task], ascending: bool = False) -> List[Task]:
    """Sort tasks by creation date (newest first by default)."""
    return sorted(tasks, key=lambda t: t.created_at, reverse=not ascending)


def sort_by_updated_at(tasks: List[Task], ascending: bool = False) -> List[Task]:
    """Sort tasks by update date (recently updated first)."""
    return sorted(tasks, key=lambda t: t.updated_at, reverse=not ascending)
