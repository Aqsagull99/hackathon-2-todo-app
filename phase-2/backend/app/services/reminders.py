"""
Reminder Service - Phase V
Handles checking and sending reminders for tasks with due dates.

[Task]: T011
[From]: phase-5/specs/007-phase-v-cloud-deployment/plan.md §3.1
"""

from datetime import datetime, timedelta
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.task import Task
from app.models.reminder import Reminder


async def check_due_reminders(session: AsyncSession, look_ahead_minutes: int = 60) -> List[Reminder]:
    """
    Scan for tasks with upcoming due dates that need reminders.

    Args:
        session: Database session
        look_ahead_minutes: How far ahead to check (default 60 minutes)

    Returns:
        List of reminders to send

    Process:
    1. Query tasks where reminder <= now + look_ahead_minutes
    2. Filter for unsent reminders
    3. Create/update Reminder records
    4. Return reminders ready to send
    """
    now = datetime.utcnow()
    look_ahead = now + timedelta(minutes=look_ahead_minutes)

    # Find tasks with reminders in the window
    statement = select(Task).where(
        Task.reminder.is_not(None),
        Task.reminder <= look_ahead,
        Task.reminder >= now,
        Task.completed == False  # Don't remind for completed tasks
    )

    result = await session.execute(statement)
    tasks = result.scalars().all()

    reminders_to_send = []

    for task in tasks:
        # Check if reminder already sent
        reminder_statement = select(Reminder).where(
            Reminder.task_id == task.id,
            Reminder.sent == False
        )
        reminder_result = await session.execute(reminder_statement)
        existing_reminder = reminder_result.scalar_one_or_none()

        if existing_reminder:
            # Use existing unsent reminder
            reminders_to_send.append(existing_reminder)
        else:
            # Create new reminder record
            new_reminder = Reminder(
                task_id=task.id,
                user_id=task.user_id,
                reminder_time=task.reminder,
                sent=False
            )
            session.add(new_reminder)
            reminders_to_send.append(new_reminder)

    await session.commit()
    return reminders_to_send


async def send_reminder_notification(
    session: AsyncSession,
    task_id: int,
    user_id: str,
    notification_type: str = "email"
) -> bool:
    """
    Send reminder notification for a task.

    Args:
        session: Database session
        task_id: Task to remind about
        user_id: User to notify
        notification_type: Type of notification (email, push, webhook)

    Returns:
        True if notification sent successfully

    Process:
    1. Load task details
    2. Format notification message
    3. Send via notification service (stub for now)
    4. Mark reminder as sent
    """
    # Load task
    statement = select(Task).where(Task.id == task_id)
    result = await session.execute(statement)
    task = result.scalar_one_or_none()

    if not task:
        return False

    # Format notification
    notification_message = format_reminder_message(task)

    # TODO: Integrate with actual notification service
    # For now, just log it
    print(f"📬 REMINDER for {user_id}: {notification_message}")

    # Mark reminder as sent
    reminder_statement = select(Reminder).where(
        Reminder.task_id == task_id,
        Reminder.sent == False
    )
    reminder_result = await session.execute(reminder_statement)
    reminder = reminder_result.scalar_one_or_none()

    if reminder:
        reminder.sent = True
        reminder.updated_at = datetime.utcnow()
        await session.commit()

    return True


def format_reminder_message(task: Task) -> str:
    """
    Format a friendly reminder message.

    Args:
        task: Task to create reminder for

    Returns:
        Formatted message string
    """
    priority_emoji = {
        "high": "🔴",
        "medium": "🟡",
        "low": "🟢"
    }

    emoji = priority_emoji.get(task.priority.value if task.priority else "medium", "📌")

    if task.due_date:
        time_until = task.due_date - datetime.utcnow()
        hours = int(time_until.total_seconds() / 3600)

        if hours < 1:
            urgency = "⚠️ DUE VERY SOON"
        elif hours < 24:
            urgency = f"Due in {hours} hours"
        else:
            days = hours // 24
            urgency = f"Due in {days} days"

        return f"{emoji} {urgency}: {task.title}"
    else:
        return f"{emoji} Reminder: {task.title}"


async def get_upcoming_tasks_with_reminders(
    session: AsyncSession,
    user_id: str,
    days_ahead: int = 7
) -> List[Task]:
    """
    Get all tasks with upcoming reminders for a user.

    Args:
        session: Database session
        user_id: User identifier
        days_ahead: How many days ahead to look

    Returns:
        List of tasks with upcoming reminders
    """
    now = datetime.utcnow()
    future = now + timedelta(days=days_ahead)

    statement = select(Task).where(
        Task.user_id == user_id,
        Task.reminder.is_not(None),
        Task.reminder >= now,
        Task.reminder <= future,
        Task.completed == False
    ).order_by(Task.reminder)

    result = await session.execute(statement)
    return result.scalars().all()
