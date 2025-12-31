"""Task model for SQLModel ORM."""

from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


class Task(SQLModel, table=True):
    """Task model representing a todo item in the database."""

    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, nullable=False)
    title: str = Field(max_length=200, nullable=False)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def mark_updated(self) -> None:
        """Update the updated_at timestamp."""
        self.updated_at = datetime.utcnow()
