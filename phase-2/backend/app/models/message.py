"""Message model for Phase III AI Chatbot."""

from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID, uuid4

from sqlalchemy import Column, Enum as SQLAlchemyEnum, JSON
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.conversation import Conversation


class Message(SQLModel, table=True):
    __tablename__ = "messages"

    message_id: UUID = Field(default_factory=uuid4, primary_key=True)
    conversation_id: UUID = Field(
        foreign_key="conversations.conversation_id", nullable=False, index=True
    )
    role: str = Field(
        sa_column=Column(
            SQLAlchemyEnum("user", "assistant", name="message_role"), nullable=False
        )
    )
    content: str = Field(nullable=False, max_length=10000)
    tool_calls: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)

    # Relationships
    conversation: "Conversation" = Relationship(back_populates="messages")