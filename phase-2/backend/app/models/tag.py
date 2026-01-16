"""Tag model for task organization."""

from datetime import datetime
from typing import List, TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

from app.models.task_tag_link import TaskTagLink

if TYPE_CHECKING:
    from app.models.task import Task


class Tag(SQLModel, table=True):
    """User-created tags for task organization."""

    __tablename__ = "tags"

    id: int = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, nullable=False)
    name: str = Field(max_length=50, nullable=False)
    color: str = Field(
        max_length=7,
        default="#EC4899",
        description="Hex color code for tag display"
    )
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationships
    tasks: List["Task"] = Relationship(
        back_populates="tags",
        link_model=TaskTagLink
    )
