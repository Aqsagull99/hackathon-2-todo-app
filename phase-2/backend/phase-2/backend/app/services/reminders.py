"""
Reminder Service - Phase V
Handles checking and sending reminders for tasks with due dates.

[Task]: T011
[From]: phase-5/specs/007-phase-v-cloud-deployment/plan.md §3.1
"""

from datetime import datetime, timedelta
from typing import List
from sqlmodel import Session, select

from app.models.task import Task
from app.models.reminder import Reminder


async def check_due_reminders(session: Session, look_ahead_minutes: int = 60) -> List[Reminder]:
    """Scan for tasks with upcoming due dates that need reminders."""
    now = datetime.utcnow()
    look_ahead = now + timedelta(minutes=look_ahead_minutes)

    statement = select(Task).where(
        Task.reminder.is_not(None),
        Task.reminder <= look_ahead,
        Task.reminder >= now,
        Task.completed == False
    )

    result = await session.execute(statement)
    tasks = result.scalars().all()

    reminders_to_send = []

    for task in tasks:
        reminder_statement = select(Reminder).where(
            Reminder.task_id == task.id,
            Reminder.sent == False
        )
        reminder_result = await session.execute(reminder_statement)
        existing_reminder = reminder_result.scalar_one_or_none()

        if existing_reminder:
            reminders_to_send.append(existing_reminder)
        else:
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


async def send_reminder_notification(session: Session, task_id: int, user_id: str) -> bool:
    """Send reminder notification for a task."""
    statement = select(Task).where(Task.id == task_id)
    result = await session.execute(statement)
    task = result.scalar_one_or_none()

    if not task:
        return False

    notification_message = format_reminder_message(task)
    print(f"📬 REMINDER for {user_id}: {notification_message}")

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
    """Format a friendly reminder message."""
    priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}
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
