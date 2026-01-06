"""TaskTagLink model for many-to-many relationship between Task and Tag."""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import SQLModel, Field

if TYPE_CHECKING:
    from app.models.task import Task
    from app.models.tag import Tag


class TaskTagLink(SQLModel, table=True):
    """Join table for Task and Tag many-to-many relationship."""

    __tablename__ = "task_tag_link"

    task_id: int = Field(foreign_key="tasks.id", primary_key=True, nullable=False)
    tag_id: int = Field(foreign_key="tags.id", primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # This link model is referenced via link_model on Task.tags / Tag.tasks
    # so we intentionally do not declare Relationship fields here to avoid
    # circular configuration issues.
