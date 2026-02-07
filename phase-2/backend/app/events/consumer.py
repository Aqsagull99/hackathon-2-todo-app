"""Event Consumer for Dapr callbacks."""
from fastapi import APIRouter, Request
from app.events.handlers import on_task_completed, on_task_due_soon

router = APIRouter(prefix="/events")

@router.get("/dapr/subscribe")
async def subscribe():
    """Dapr subscription endpoint."""
    return [
        {"pubsubname": "pubsub", "topic": "task-events", "route": "/events/task/completed"},
        {"pubsubname": "pubsub", "topic": "task-reminders", "route": "/events/task/due-soon"},
    ]

@router.post("/task/completed")
async def task_completed_handler(request: Request):
    """Handle task completed events."""
    data = await request.json()
    # Dapr sends the raw event data, not wrapped in a "data" field
    await on_task_completed(data)
    return {"status": "SUCCESS"}

@router.post("/task/due-soon")
async def task_due_soon_handler(request: Request):
    """Handle task due soon events."""
    data = await request.json()
    # Dapr sends the raw event data, not wrapped in a "data" field
    await on_task_due_soon(data)
    return {"status": "SUCCESS"}

@router.post("/cron/reminder-check")
async def cron_reminder_check(request: Request):
    """Cron-triggered reminder check."""
    from app.core.database import async_session_maker
    from app.services.reminders import check_due_reminders
    async with async_session_maker() as session:
        reminders = await check_due_reminders(session)
        for reminder in reminders:
            # Pass the full reminder object with user_id
            await on_task_due_soon({
                "task_data": {
                    "id": reminder.task_id,
                    "user_id": reminder.user_id
                }
            })
        await session.commit()  # Ensure all changes are committed
    return {"status": "SUCCESS", "reminders_sent": len(reminders)}
