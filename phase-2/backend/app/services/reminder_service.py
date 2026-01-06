"""Reminder service for task due date notifications."""

from datetime import datetime, timedelta
from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.reminder import Reminder, ReminderStatus


async def create_reminder(
    db: AsyncSession,
    task_id: int,
    due_time: datetime,
) -> Reminder:
    """Create a reminder for task due time.

    Args:
        db: Database session
        task_id: Task ID
        due_time: When reminder should trigger

    Returns:
        Created reminder
    """
    # Check for existing reminder
    existing = await get_reminder_for_task(db, task_id)

    if existing:
        # Update existing reminder
        existing.due_time = due_time
        existing.status = ReminderStatus.PENDING
        existing.snoozed_until = None
        existing.updated_at = datetime.utcnow()
        db.add(existing)
        await db.commit()
        await db.refresh(existing)
        return existing

    # Create new reminder
    reminder = Reminder(
        task_id=task_id,
        due_time=due_time,
        status=ReminderStatus.PENDING,
    )
    db.add(reminder)
    await db.commit()
    await db.refresh(reminder)

    return reminder


async def get_reminder_for_task(
    db: AsyncSession,
    task_id: int,
) -> Optional[Reminder]:
    """Get active reminder for a task.

    Args:
        db: Database session
        task_id: Task ID

    Returns:
        Reminder if found, None otherwise
    """
    result = await db.execute(
        select(Reminder).where(
            Reminder.task_id == task_id,
            Reminder.status == ReminderStatus.PENDING,
        )
    )
    return result.scalar_one_or_none()


async def get_reminder(
    db: AsyncSession,
    reminder_id: int,
) -> Optional[Reminder]:
    """Get a specific reminder by ID.

    Args:
        db: Database session
        reminder_id: Reminder ID

    Returns:
        Reminder if found, None otherwise
    """
    result = await db.execute(
        select(Reminder).where(Reminder.id == reminder_id)
    )
    return result.scalar_one_or_none()


async def snooze_reminder(
    db: AsyncSession,
    reminder_id: int,
    minutes: int,
) -> Reminder:
    """Snooze a reminder for specified minutes.

    Args:
        db: Database session
        reminder_id: Reminder ID
        minutes: Minutes to snooze

    Returns:
        Updated reminder
    """
    result = await db.execute(
        select(Reminder).where(Reminder.id == reminder_id)
    )
    reminder = result.scalar_one_or_none()

    if not reminder:
        raise ValueError(f"Reminder {reminder_id} not found")

    reminder.status = ReminderStatus.SNOOZED
    reminder.snoozed_until = datetime.utcnow() + timedelta(minutes=minutes)
    reminder.updated_at = datetime.utcnow()

    db.add(reminder)
    await db.commit()
    await db.refresh(reminder)

    return reminder


async def dismiss_reminder(
    db: AsyncSession,
    reminder_id: int,
) -> Reminder:
    """Dismiss/cancel a reminder.

    Args:
        db: Database session
        reminder_id: Reminder ID

    Returns:
        Updated reminder
    """
    result = await db.execute(
        select(Reminder).where(Reminder.id == reminder_id)
    )
    reminder = result.scalar_one_or_none()

    if not reminder:
        raise ValueError(f"Reminder {reminder_id} not found")

    reminder.status = ReminderStatus.DISMISSED
    reminder.updated_at = datetime.utcnow()

    db.add(reminder)
    await db.commit()
    await db.refresh(reminder)

    return reminder


async def mark_reminder_sent(
    db: AsyncSession,
    reminder_id: int,
) -> Reminder:
    """Mark a reminder as sent.

    Args:
        db: Database session
        reminder_id: Reminder ID

    Returns:
        Updated reminder
    """
    result = await db.execute(
        select(Reminder).where(Reminder.id == reminder_id)
    )
    reminder = result.scalar_one_or_none()

    if not reminder:
        raise ValueError(f"Reminder {reminder_id} not found")

    reminder.status = ReminderStatus.SENT
    reminder.updated_at = datetime.utcnow()

    db.add(reminder)
    await db.commit()
    await db.refresh(reminder)

    return reminder


async def get_pending_reminders(
    db: AsyncSession,
) -> List[Reminder]:
    """Get all pending reminders that are due.

    Args:
        db: Database session

    Returns:
        List of due pending reminders
    """
    now = datetime.utcnow()

    result = await db.execute(
        select(Reminder).where(
            Reminder.status == ReminderStatus.PENDING,
            Reminder.due_time <= now,
        )
        .order_by(Reminder.due_time.asc())
    )
    return list(result.scalars().all())


async def delete_reminder(
    db: AsyncSession,
    reminder_id: int,
) -> bool:
    """Delete a reminder.

    Args:
        db: Database session
        reminder_id: Reminder ID

    Returns:
        True if deleted
    """
    reminder = await get_reminder(db, reminder_id)
    if not reminder:
        return False

    await db.delete(reminder)
    await db.commit()
    return True
