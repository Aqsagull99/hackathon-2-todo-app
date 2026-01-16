"""Task model for SQLModel ORM with extended features."""

from datetime import datetime
from enum import Enum
from typing import Optional, List, TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, Text, Enum as SAEnum
from sqlalchemy.dialects.postgresql import TSVECTOR

from app.models.task_tag_link import TaskTagLink

if TYPE_CHECKING:
    from app.models.tag import Tag


class TaskPriority(str, Enum):
    """Task priority levels."""
    high = "high"
    medium = "medium"
    low = "low"


class RecurrencePattern(str, Enum):
    """Recurring task patterns."""
    daily = "daily"
    weekly = "weekly"
    monthly = "monthly"


class Task(SQLModel, table=True):
    """Task model representing a todo item in the database with extended features."""

    __tablename__ = "tasks"
    model_config = {
        "arbitrary_types_allowed": True,
    }

    # Existing fields
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, nullable=False)
    title: str = Field(max_length=200, nullable=False)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)

    # NEW: Extended fields
    priority: TaskPriority = Field(
        sa_column=Column(
            SAEnum(TaskPriority, name="task_priority", values_callable=lambda x: [e.value for e in x]),
            default=TaskPriority.medium,
            nullable=False,
            index=True
        )
    )
    due_date: Optional[datetime] = Field(default=None, nullable=True, index=True)
    due_date_tz: Optional[str] = Field(
        default="UTC",
        max_length=50,
        description="Timezone for due_date (e.g., 'America/New_York')"
    )
    reminder: Optional[datetime] = Field(default=None, nullable=True)
    reminder_time: Optional[str] = Field(
        default=None,
        max_length=50,
        nullable=True,
        description="Reminder time as string (e.g., '7am', '3:30pm')"
    )
    recurrence_pattern: Optional[RecurrencePattern] = Field(
        sa_column=Column(
            SAEnum(RecurrencePattern, name="recurrence_pattern", values_callable=lambda x: [e.value for e in x]),
            nullable=True
        )
    )
    recurrence_parent_id: Optional[int] = Field(
        default=None,
        nullable=True,
        foreign_key="tasks.id",
        description="Links to original recurring task"
    )

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    completed_at: Optional[datetime] = Field(default=None, nullable=True)

    # Full-text search vector (PostgreSQL TSVECTOR)
    search_vector: TSVECTOR = Field(
        sa_column=Column("search_vector", TSVECTOR),
        default=None,
        exclude=True
    )

    # Relationships (defined but not loaded by default)
    tags: List["Tag"] = Relationship(
        back_populates="tasks",
        link_model=TaskTagLink
    )

    def mark_updated(self) -> None:
        """Update the updated_at timestamp."""
        self.updated_at = datetime.utcnow()
