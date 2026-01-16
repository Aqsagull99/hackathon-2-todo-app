"""Pydantic schemas module."""

from app.schemas.task import TaskCreate, TaskUpdate, TaskRead
from app.schemas.extended import (
    TaskPriority,
    RecurrencePattern,
    ReminderStatus,
    TagCreate,
    TagUpdate,
    TagResponse,
    TagWithTaskCount,
    ReminderCreate,
    ReminderUpdate,
    ReminderResponse,
    TaskCreateExtended,
    TaskUpdateExtended,
    TaskResponseExtended,
    TaskListResponseExtended,
    TaskSearchParams,
    RecurringCompleteResponse,
    RecurringSkipResponse,
)

__all__ = [
    # Task schemas
    "TaskCreate",
    "TaskUpdate",
    "TaskRead",
    # Extended schemas
    "TaskPriority",
    "RecurrencePattern",
    "ReminderStatus",
    "TagCreate",
    "TagUpdate",
    "TagResponse",
    "TagWithTaskCount",
    "ReminderCreate",
    "ReminderUpdate",
    "ReminderResponse",
    "TaskCreateExtended",
    "TaskUpdateExtended",
    "TaskResponseExtended",
    "TaskListResponseExtended",
    "TaskSearchParams",
    "RecurringCompleteResponse",
    "RecurringSkipResponse",
]
