"""Reminder API routes."""

from fastapi import APIRouter, HTTPException, Path, status

from app.api.deps import DBSession, VerifiedUserId
from app.schemas.extended import (
    ReminderCreate,
    ReminderResponse,
    ReminderUpdate,
)
from app.services import reminder_service


router = APIRouter(prefix="/api", tags=["reminders"])


@router.get("/{user_id}/tasks/{task_id}/reminder", response_model=ReminderResponse)
async def get_task_reminder(
    user_id: VerifiedUserId,
    task_id: int = Path(..., ge=1, description="Task ID"),
    db: DBSession = None,
) -> ReminderResponse:
    """Get reminder for a task.

    - **user_id**: Owner's user ID
    - **task_id**: Task ID
    """
    reminder = await reminder_service.get_reminder_for_task(db, task_id)

    if not reminder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No reminder found for task {task_id}",
        )

    return ReminderResponse.model_validate(reminder)


@router.post("/{user_id}/tasks/{task_id}/reminder", response_model=ReminderResponse, status_code=status.HTTP_201_CREATED)
async def create_reminder(
    user_id: VerifiedUserId,
    task_id: int = Path(..., ge=1, description="Task ID"),
    reminder_data: ReminderCreate = None,
    db: DBSession = None,
) -> ReminderResponse:
    """Create or update reminder for a task.

    - **user_id**: Owner's user ID
    - **task_id**: Task ID
    - **due_time**: When reminder should trigger
    """
    # Verify task exists and belongs to user
    from app.services import task_service
    task = await task_service.get_task(db, task_id, user_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found",
        )

    reminder = await reminder_service.create_reminder(db, task_id, reminder_data.due_time)
    return ReminderResponse.model_validate(reminder)


@router.post("/{user_id}/reminders/{reminder_id}/snooze", response_model=ReminderResponse)
async def snooze_reminder(
    user_id: VerifiedUserId,
    reminder_id: int = Path(..., ge=1, description="Reminder ID"),
    minutes: int = None,
    db: DBSession = None,
) -> ReminderResponse:
    """Snooze a reminder.

    - **user_id**: Owner's user ID
    - **reminder_id**: Reminder ID
    - **minutes**: Minutes to snooze (5, 15, or 30)
    """
    reminder = await reminder_service.snooze_reminder(db, reminder_id, minutes)
    return ReminderResponse.model_validate(reminder)


@router.delete("/{user_id}/reminders/{reminder_id}", status_code=status.HTTP_204_NO_CONTENT)
async def dismiss_reminder(
    user_id: VerifiedUserId,
    reminder_id: int = Path(..., ge=1, description="Reminder ID"),
    db: DBSession = None,
) -> None:
    """Dismiss/cancel a reminder.

    - **user_id**: Owner's user ID
    - **reminder_id**: Reminder ID
    """
    await reminder_service.dismiss_reminder(db, reminder_id)
