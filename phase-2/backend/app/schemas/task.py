from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field

from app.models.task import TaskPriority, RecurrencePattern


class TaskBase(BaseModel):
    """Base properties for Task resource."""
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = False
    priority: TaskPriority = Field(default=TaskPriority.medium)
    due_date: Optional[datetime] = None
    due_date_tz: Optional[str] = "UTC"
    reminder: Optional[datetime] = None
    reminder_time: Optional[str] = None
    recurrence_pattern: Optional[RecurrencePattern] = None


class TaskCreate(TaskBase):
    """Properties to receive on item creation."""
    tags: Optional[List[str]] = None


class TaskUpdate(BaseModel):
    """Properties to receive on item update."""
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None
    due_date_tz: Optional[str] = None
    reminder: Optional[datetime] = None
    recurrence_pattern: Optional[RecurrencePattern] = None
    tags: Optional[List[str]] = None


class TaskRead(TaskBase):
    """Properties to return to client."""
    id: int
    user_id: str
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None
    tags: List[str] = []

    class Config:
        from_attributes = True
