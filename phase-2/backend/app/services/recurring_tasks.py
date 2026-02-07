"""
Recurring Task Service - Phase V
Handles spawning next occurrences of recurring tasks.

[Task]: T010
[From]: phase-5/specs/007-phase-v-cloud-deployment/plan.md §3.1
"""

from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from croniter import croniter

from app.models.task import Task, RecurrencePattern


async def spawn_next_occurrence(session: AsyncSession, task_id: int) -> Optional[Task]:
    """
    Create the next occurrence of a recurring task when current one is completed.

    Args:
        session: Database session
        task_id: ID of the completed recurring task

    Returns:
        The newly created task, or None if not recurring

    Process:
    1. Load completed task
    2. Check if has recurrence_pattern
    3. Calculate next due_date based on pattern
    4. Create new task with same properties
    5. Link to original via recurrence_parent_id
    """
    # Load the original task
    statement = select(Task).where(Task.id == task_id)
    result = await session.execute(statement)
    original_task = result.scalar_one_or_none()

    if not original_task or not original_task.recurrence_pattern:
        return None

    # Calculate next due date
    next_due = calculate_next_due_date(
        original_task.due_date or datetime.utcnow(),
        original_task.recurrence_pattern
    )

    # Create next occurrence
    next_task = Task(
        user_id=original_task.user_id,
        title=original_task.title,
        description=original_task.description,
        priority=original_task.priority,
        due_date=next_due,
        due_date_tz=original_task.due_date_tz,
        reminder=calculate_reminder_time(next_due),
        recurrence_pattern=original_task.recurrence_pattern,
        recurrence_parent_id=original_task.id,  # Link to parent
        completed=False,
    )

    session.add(next_task)
    await session.commit()
    await session.refresh(next_task)

    # Copy tags from original task
    if original_task.tags:
        next_task.tags = original_task.tags
        await session.commit()

    return next_task


def calculate_next_due_date(current_due: datetime, pattern: RecurrencePattern) -> datetime:
    """
    Calculate the next due date based on recurrence pattern.

    Args:
        current_due: Current due date
        pattern: Recurrence pattern (daily, weekly, monthly)

    Returns:
        Next due date
    """
    if pattern == RecurrencePattern.daily:
        return current_due + timedelta(days=1)
    elif pattern == RecurrencePattern.weekly:
        return current_due + timedelta(weeks=1)
    elif pattern == RecurrencePattern.monthly:
        # Add approximately 30 days, adjust for month boundaries
        next_month = current_due.replace(day=1) + timedelta(days=32)
        return next_month.replace(day=min(current_due.day, 28))
    else:
        return current_due + timedelta(days=1)  # Default to daily


def calculate_reminder_time(due_date: datetime) -> Optional[datetime]:
    """
    Calculate reminder time (1 hour before due date).

    Args:
        due_date: Task due date

    Returns:
        Reminder datetime or None
    """
    if not due_date:
        return None

    # Set reminder 1 hour before due date
    return due_date - timedelta(hours=1)


async def get_recurring_tasks(session: AsyncSession, user_id: str) -> list[Task]:
    """
    Get all recurring tasks for a user.

    Args:
        session: Database session
        user_id: User identifier

    Returns:
        List of recurring tasks
    """
    statement = select(Task).where(
        Task.user_id == user_id,
        Task.recurrence_pattern.is_not(None)
    )
    result = await session.execute(statement)
    return result.scalars().all()
