"""Event Handlers for business logic."""
from typing import Dict, Any

async def on_task_completed(event_data: Dict[str, Any]):
    """Handle task completed event - spawn next recurring."""
    from app.core.database import async_session_maker
    from app.services.recurring_tasks import spawn_next_occurrence

    task_data = event_data.get("task_data", {})
    task_id = task_data.get("id")
    if task_id:
        async with async_session_maker() as session:
            await spawn_next_occurrence(session, task_id)
            await session.commit()  # Ensure transaction is committed

async def on_task_due_soon(event_data: Dict[str, Any]):
    """Handle task due soon event - send reminder."""
    from app.core.database import async_session_maker
    from app.services.reminders import send_reminder_notification

    # Handle both formats: direct task_data or wrapped in task_data
    task_data = event_data.get("task_data", {})
    task_id = event_data.get("task_id") or task_data.get("id")
    user_id = event_data.get("user_id") or task_data.get("user_id")

    if task_id and user_id:
        async with async_session_maker() as session:
            await send_reminder_notification(session, task_id, user_id)
            await session.commit()  # Ensure transaction is committed
