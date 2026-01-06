"""Recurring task service for auto-rescheduling."""

from datetime import datetime, timedelta
from typing import Optional
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task, RecurrencePattern


async def complete_recurring_task(
    db: AsyncSession,
    task: Task,
) -> Optional[Task]:
    """When a recurring task is completed, create next instance.

    Args:
        db: Database session
        task: Recurring task being completed

    Returns:
        New instance task if recurring, None otherwise
    """
    if not task.recurrence_pattern:
        return None

    # Mark original task complete
    from datetime import datetime as dt
    task.completed = True
    task.completed_at = dt.utcnow()
    task.updated_at = dt.utcnow()
    db.add(task)

    # Calculate next due date based on recurrence pattern
    new_due_date = calculate_next_instance(task.due_date, task.recurrence_pattern)

    # Create new task instance
    new_task = Task(
        user_id=task.user_id,
        title=task.title,
        description=task.description,
        priority=task.priority,
        due_date=new_due_date,
        due_date_tz=task.due_date_tz,
        recurrence_pattern=task.recurrence_pattern,
        recurrence_parent_id=task.recurrence_parent_id or task.id,
        completed=False,
    )
    db.add(new_task)

    await db.commit()
    await db.refresh(new_task)

    return new_task


def calculate_next_instance(
    due_date: Optional[datetime],
    pattern: RecurrencePattern,
) -> Optional[datetime]:
    """Calculate next occurrence date based on pattern.

    Args:
        due_date: Original task's due date
        pattern: Recurrence pattern (daily, weekly, monthly)

    Returns:
        Next due date, or None if no due_date
    """
    if not due_date:
        return None

    if pattern == RecurrencePattern.DAILY:
        return due_date + timedelta(days=1)

    elif pattern == RecurrencePattern.WEEKLY:
        return due_date + timedelta(weeks=1)

    elif pattern == RecurrencePattern.MONTHLY:
        # Same day next month
        if due_date.month == 12:
            # December -> January next year
            try:
                return due_date.replace(
                    year=due_date.year + 1,
                    month=1,
                )
            except ValueError:
                # Handle Feb 29 case
                return due_date.replace(
                    year=due_date.year + 1,
                    month=1,
                    day=28,
                )
        else:
            try:
                return due_date.replace(month=due_date.month + 1)
            except ValueError:
                # Handle cases like Jan 31 -> Feb
                next_month = due_date.month + 1
                return due_date.replace(month=next_month, day=28)

    return due_date


async def skip_task_instance(
    db: AsyncSession,
    task: Task,
) -> Optional[Task]:
    """Skip a recurring task instance and create next one.

    Args:
        db: Database session
        task: Task instance to skip

    Returns:
        New instance task if recurring, None otherwise
    """
    if not task.recurrence_pattern:
        return None

    # Mark skipped as complete
    task.completed = True
    task.completed_at = datetime.utcnow()
    task.updated_at = datetime.utcnow()
    db.add(task)

    # Create next instance
    new_due_date = calculate_next_instance(task.due_date, task.recurrence_pattern)

    new_task = Task(
        user_id=task.user_id,
        title=task.title,
        description=task.description,
        priority=task.priority,
        due_date=new_due_date,
        due_date_tz=task.due_date_tz,
        recurrence_pattern=task.recurrence_pattern,
        recurrence_parent_id=task.recurrence_parent_id or task.id,
        completed=False,
    )
    db.add(new_task)

    await db.commit()
    await db.refresh(new_task)

    return new_task


async def cancel_recurrence(
    db: AsyncSession,
    task: Task,
) -> Task:
    """Cancel recurrence pattern on a task.

    Args:
        db: Database session
        task: Task to cancel recurrence for

    Returns:
        Updated task
    """
    task.recurrence_pattern = None
    task.recurrence_parent_id = None
    task.updated_at = datetime.utcnow()

    await db.commit()
    await db.refresh(task)

    return task


async def get_recurring_instances(
    db: AsyncSession,
    user_id: str,
    parent_id: int,
) -> list[Task]:
    """Get all instances of a recurring task.

    Args:
        db: Database session
        user_id: Owner's user ID
        parent_id: Original recurring task ID

    Returns:
        List of recurring instances
    """
    result = await db.execute(
        select(Task)
        .where(Task.user_id == user_id)
        .where(Task.recurrence_parent_id == parent_id)
        .order_by(Task.due_date.desc())
    )
    return list(result.scalars().all())
