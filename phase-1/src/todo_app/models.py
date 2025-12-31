"""Task data model for the todo console application."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Task:
    """Represents a single todo task.

    Attributes:
        id: Unique identifier for the task (assigned by TaskList)
        title: Short description of the task
        completed: Whether the task has been completed
        created_at: Timestamp when the task was created
    """
    id: int
    title: str
    completed: bool = False
    created_at: Optional[datetime] = field(default_factory=datetime.now)
