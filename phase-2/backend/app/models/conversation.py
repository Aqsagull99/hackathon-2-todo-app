"""Conversation model for Phase III AI Chatbot."""

from datetime import datetime
from typing import TYPE_CHECKING, List
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.message import Message


class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"

    conversation_id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: str = Field(foreign_key="users.id", nullable=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    messages: List["Message"] = Relationship(
        back_populates="conversation",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    user: "User" = Relationship(back_populates="conversations")