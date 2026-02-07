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
    """
    Filter tasks by priority level.

    Args:
        tasks: List of tasks to filter
        priority: Priority level to filter by

    Returns:
        Filtered list of tasks
    """
    return [t for t in tasks if t.priority == priority]


def filter_by_tags(tasks: List[Task], tag_names: List[str]) -> List[Task]:
    """
    Filter tasks that have any of the specified tags.

    Args:
        tasks: List of tasks to filter
        tag_names: List of tag names to search for

    Returns:
        Tasks that have at least one matching tag
    """
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
    """
    Filter tasks by completion status.

    Args:
        tasks: List of tasks to filter
        status: Status filter ("all", "pending", "completed")

    Returns:
        Filtered list of tasks
    """
    if status == "completed":
        return [t for t in tasks if t.completed]
    elif status == "pending":
        return [t for t in tasks if not t.completed]
    else:  # "all"
        return tasks


def filter_by_due_date_range(
    tasks: List[Task],
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> List[Task]:
    """
    Filter tasks by due date range.

    Args:
        tasks: List of tasks to filter
        start_date: Start of date range (inclusive)
        end_date: End of date range (inclusive)

    Returns:
        Tasks with due dates in the specified range
    """
    from datetime import datetime

    filtered = tasks

    if start_date:
        filtered = [t for t in filtered if t.due_date and t.due_date >= start_date]

    if end_date:
        filtered = [t for t in filtered if t.due_date and t.due_date <= end_date]

    return filtered


def filter_overdue_tasks(tasks: List[Task]) -> List[Task]:
    """
    Filter tasks that are overdue (past due date and not completed).

    Args:
        tasks: List of tasks to filter

    Returns:
        Overdue tasks
    """
    from datetime import datetime

    now = datetime.utcnow()
    return [
        t for t in tasks
        if t.due_date and t.due_date < now and not t.completed
    ]


def get_today_tasks(tasks: List[Task]) -> List[Task]:
    """
    Get tasks due today.

    Args:
        tasks: List of tasks to filter

    Returns:
        Tasks due today
    """
    from datetime import datetime, date

    today = date.today()

    return [
        t for t in tasks
        if t.due_date and t.due_date.date() == today and not t.completed
    ]


def get_upcoming_tasks(tasks: List[Task], days: int = 7) -> List[Task]:
    """
    Get tasks due in the next N days.

    Args:
        tasks: List of tasks to filter
        days: Number of days to look ahead

    Returns:
        Tasks due in the next N days
    """
    from datetime import datetime, timedelta

    now = datetime.utcnow()
    future = now + timedelta(days=days)

    return [
        t for t in tasks
        if t.due_date and now <= t.due_date <= future and not t.completed
    ]


def apply_multiple_filters(
    tasks: List[Task],
    priority: Optional[TaskPriority] = None,
    tags: Optional[List[str]] = None,
    status: Optional[str] = "all",
    overdue_only: bool = False,
    today_only: bool = False
) -> List[Task]:
    """
    Apply multiple filters to task list.

    Args:
        tasks: List of tasks to filter
        priority: Filter by priority
        tags: Filter by tags
        status: Filter by status
        overdue_only: Show only overdue tasks
        today_only: Show only today's tasks

    Returns:
        Filtered task list
    """
    result = tasks

    # Apply status filter
    result = filter_by_status(result, status)

    # Apply priority filter
    if priority:
        result = filter_by_priority(result, priority)

    # Apply tags filter
    if tags:
        result = filter_by_tags(result, tags)

    # Apply date filters
    if overdue_only:
        result = filter_overdue_tasks(result)
    elif today_only:
        result = get_today_tasks(result)

    return result
