"""Pydantic schemas for extended task features (priority, tags, reminders)."""

from datetime import datetime
from typing import Optional, List
from enum import Enum

from pydantic import BaseModel, Field, field_validator


class TaskPriority(str, Enum):
    """Task priority levels."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class RecurrencePattern(str, Enum):
    """Recurrence pattern for repeating tasks."""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class ReminderStatus(str, Enum):
    """Reminder notification status."""
    PENDING = "PENDING"
    SENT = "SENT"
    SNOOZED = "SNOOZED"
    DISMISSED = "DISMISSED"


# ============================================================================
# Tag Schemas
# ============================================================================

class TagBase(BaseModel):
    """Base schema for tag data."""
    name: str = Field(..., min_length=1, max_length=50)
    color: str = Field(default="#EC4899", pattern="^#[0-9A-Fa-f]{6}$")


class TagCreate(TagBase):
    """Schema for creating a new tag."""
    pass


class TagUpdate(BaseModel):
    """Schema for updating a tag."""
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    color: Optional[str] = Field(None, pattern="^#[0-9A-Fa-f]{6}$")


class TagResponse(TagBase):
    """Schema for tag API responses."""
    id: int
    user_id: str
    created_at: datetime

    model_config = {"from_attributes": True}


class TagWithTaskCount(TagResponse):
    """Tag response with task count."""
    task_count: int = 0


# ============================================================================
# Reminder Schemas
# ============================================================================

class ReminderBase(BaseModel):
    """Base schema for reminder data."""
    due_time: datetime


class ReminderCreate(ReminderBase):
    """Schema for creating a reminder."""

    @field_validator('due_time')
    @classmethod
    def strip_timezone_from_due_time(cls, v):
        """Strip timezone info from due_time since DB uses TIMESTAMP WITHOUT TIME ZONE."""
        if v is not None and isinstance(v, datetime) and v.tzinfo is not None:
            return v.replace(tzinfo=None)
        return v


class ReminderUpdate(BaseModel):
    """Schema for updating a reminder."""
    status: Optional[ReminderStatus] = None
    snoozed_minutes: Optional[int] = Field(None, ge=1, le=1440)


class ReminderResponse(BaseModel):
    """Schema for reminder API responses."""
    id: int
    task_id: int
    due_time: datetime
    status: ReminderStatus
    snoozed_until: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ============================================================================
# Extended Task Schemas
# ============================================================================

class TaskCreateExtended(BaseModel):
    """Schema for creating a task with extended features."""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM)
    due_date: Optional[datetime] = None
    due_date_tz: Optional[str] = Field(default="UTC", max_length=50)
    recurrence_pattern: Optional[RecurrencePattern] = None
    tag_ids: Optional[List[int]] = None

    @field_validator('due_date')
    @classmethod
    def strip_timezone_from_due_date(cls, v):
        """Strip timezone info from due_date since DB uses TIMESTAMP WITHOUT TIME ZONE."""
        if v is not None and isinstance(v, datetime) and v.tzinfo is not None:
            return v.replace(tzinfo=None)
        return v


class TaskUpdateExtended(BaseModel):
    """Schema for updating a task with extended features."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    completed: Optional[bool] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None
    due_date_tz: Optional[str] = Field(None, max_length=50)
    recurrence_pattern: Optional[RecurrencePattern] = None

    @field_validator('due_date')
    @classmethod
    def strip_timezone_from_due_date(cls, v):
        """Strip timezone info from due_date since DB uses TIMESTAMP WITHOUT TIME ZONE."""
        if v is not None and isinstance(v, datetime) and v.tzinfo is not None:
            return v.replace(tzinfo=None)
        return v


class TaskResponseExtended(BaseModel):
    """Schema for extended task API responses."""
    id: int
    user_id: str
    title: str
    description: Optional[str]
    completed: bool
    priority: TaskPriority
    due_date: Optional[datetime]
    due_date_tz: Optional[str]
    recurrence_pattern: Optional[RecurrencePattern]
    recurrence_parent_id: Optional[int]
    tags: List[TagResponse] = []
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class TaskListResponseExtended(BaseModel):
    """Schema for paginated extended task list response."""
    tasks: List[TaskResponseExtended]
    total: int
    page: int
    page_size: int
    total_pages: int


# ============================================================================
# Search & Filter Schemas
# ============================================================================

class TaskSearchParams(BaseModel):
    """Query parameters for searching and filtering tasks."""
    search: Optional[str] = None
    status: Optional[str] = Field(None, pattern="^(pending|completed|all)$")
    priority: Optional[TaskPriority] = None
    due_date_from: Optional[datetime] = None
    due_date_to: Optional[datetime] = None
    tag_ids: Optional[List[int]] = None
    sort_by: str = Field(default="created_at", pattern="^(created_at|due_date|priority|title)$")
    sort_order: str = Field(default="desc", pattern="^(asc|desc)$")
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)


# ============================================================================
# Recurring Task Schemas
# ============================================================================

class RecurringCompleteResponse(BaseModel):
    """Response when completing a recurring task."""
    completed_task: TaskResponseExtended
    new_instance: Optional[TaskResponseExtended] = None


class RecurringSkipResponse(BaseModel):
    """Response when skipping a recurring instance."""
    skipped_task: TaskResponseExtended
    new_instance: Optional[TaskResponseExtended] = None
