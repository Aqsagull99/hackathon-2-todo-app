"""Task data model for the todo console application."""
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional, List
from enum import Enum


class Priority(str, Enum):
    """Priority levels for tasks."""
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class Recurrence(str, Enum):
    """Recurrence patterns for tasks."""
    NONE = "None"
    DAILY = "Daily"
    WEEKLY = "Weekly"
    MONTHLY = "Monthly"


class RecurrenceManager:
    """Handle recurrence logic for tasks."""

    @staticmethod
    def calculate_next_due_date(
        current_due: datetime,
        recurrence: str  # "Daily", "Weekly", or "Monthly"
    ) -> Optional[datetime]:
        """Calculate next due date based on recurrence pattern.

        Args:
            current_due: The current due date of completed task
            recurrence: Recurrence pattern ("Daily", "Weekly", or "Monthly")

        Returns:
            The next due date, or None if recurrence is "None"
        """
        if recurrence == "Daily":
            return current_due + timedelta(days=1)
        elif recurrence == "Weekly":
            return current_due + timedelta(weeks=1)
        elif recurrence == "Monthly":
            # Handle monthly recurrence by adding approximately 30 days
            # then adjusting to the same day of next month
            year = current_due.year
            month = current_due.month + 1
            day = current_due.day

            # Handle year rollover
            if month > 12:
                month = 1
                year += 1

            # Handle day overflow (e.g., Jan 31 -> Feb 28/29)
            # Find last day of target month
            if month == 12:
                next_month_first = datetime(year + 1, 1, 1)
            else:
                next_month_first = datetime(year, month + 1, 1)
            last_day_of_month = (next_month_first - timedelta(days=1)).day

            if day > last_day_of_month:
                day = last_day_of_month

            return datetime(year, month, day, current_due.hour, current_due.minute, current_due.second)
        else:
            return None  # No recurrence

    @staticmethod
    def validate_recurrence(recurrence: str) -> bool:
        """Validate that a recurrence pattern is supported.
        Returns True if valid, False otherwise."""
        return recurrence in ["None", "Daily", "Weekly", "Monthly"]


@dataclass
class Task:
    """Represents a single todo task.

    Attributes:
        id: Unique identifier for the task (assigned by TaskList)
        title: Short description of the task
        completed: Whether the task has been completed
        created_at: Timestamp when the task was created
        priority: Task priority (High/Medium/Low)
        tags: List of string labels for categorization
        due_date: Optional datetime for task deadline
        recurrence: Recurrence pattern for task
    """
    id: int
    title: str
    completed: bool = False
    created_at: Optional[datetime] = field(default_factory=datetime.now)
    priority: Priority = Priority.MEDIUM  # Default
    tags: List[str] = field(default_factory=list)  # Default empty
    due_date: Optional[datetime] = None
    recurrence: Recurrence = Recurrence.NONE  # Default
