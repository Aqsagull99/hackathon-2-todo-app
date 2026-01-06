"""Reminder model for task due date notifications."""

from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, Enum as SAEnum

if TYPE_CHECKING:
    from app.models.task import Task


class ReminderStatus(str, Enum):
    """Reminder status states."""
    PENDING = "pending"
    SENT = "sent"
    SNOOZED = "snoozed"
    DISMISSED = "dismissed"


class Reminder(SQLModel, table=True):
    """Tracks reminder state for task notifications."""

    __tablename__ = "reminders"

    id: int = Field(default=None, primary_key=True)
    task_id: int = Field(foreign_key="tasks.id", nullable=False, index=True)
    due_time: datetime = Field(nullable=False, description="When reminder should trigger")
    status: ReminderStatus = Field(
        sa_column=Column(
            SAEnum(ReminderStatus, name="reminder_status", values_callable=lambda x: [e.value for e in x]),
            default=ReminderStatus.PENDING,
            nullable=False
        )
    )
    snoozed_until: datetime | None = Field(default=None, nullable=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationship
    task: "Task" = Relationship()
