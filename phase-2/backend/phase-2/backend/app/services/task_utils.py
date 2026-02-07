"""
Task Utility Service - Phase V
Provides filtering and utility functions for task management.

[Task]: T012
[From]: phase-5/specs/007-phase-v-cloud-deployment/plan.md §3.1
"""

from typing import List, Optional
from datetime import datetime
from app.models.task import Task, TaskPriority


def filter_by_priority(tasks: List[Task], priority: TaskPriority) -> List[Task]:
    """Filter tasks by priority level."""
    return [t for t in tasks if t.priority == priority]


def filter_by_tags(tasks: List[Task], tag_names: List[str]) -> List[Task]:
    """Filter tasks that have any of the specified tags."""
    if not tag_names:
        return tasks

    filtered_tasks = []
    for task in tasks:
        if task.tags:
            task_tag_names = [tag.name.lower() for tag in task.tags]
            if any(tag.lower() in task_tag_names for tag in tag_names):
                filtered_tasks.append(task)

    return filtered_tasks


def filter_by_status(tasks: List[Task], status: str) -> List[Task]:
    """Filter tasks by completion status."""
    if status == "completed":
        return [t for t in tasks if t.completed]
    elif status == "pending":
        return [t for t in tasks if not t.completed]
    else:
        return tasks


def filter_overdue_tasks(tasks: List[Task]) -> List[Task]:
    """Filter tasks that are overdue."""
    now = datetime.utcnow()
    return [
        t for t in tasks
        if t.due_date and t.due_date < now and not t.completed
    ]


def get_today_tasks(tasks: List[Task]) -> List[Task]:
    """Get tasks due today."""
    from datetime import date
    today = date.today()
    return [
        t for t in tasks
        if t.due_date and t.due_date.date() == today and not t.completed
    ]
