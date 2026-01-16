"""User model for Phase III AI Chatbot."""

from datetime import datetime
from typing import TYPE_CHECKING, List
from uuid import UUID

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.conversation import Conversation


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: UUID = Field(default=None, primary_key=True)
    email: str = Field(unique=True, nullable=False)
    name: str = Field(max_length=100, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    conversations: List["Conversation"] = Relationship(
        back_populates="user"
    )