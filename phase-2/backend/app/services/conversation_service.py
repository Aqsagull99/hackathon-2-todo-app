"""Conversation service for managing chat conversations and messages."""

from datetime import datetime
from typing import List, Optional
pass

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from uuid import UUID

from app.models.conversation import Conversation
from app.models.message import Message


async def create_conversation(user_id: str) -> str:
    """Create a new conversation for a user, creating the user if they don't exist."""
    from app.core.database import async_session_maker
    from app.models.user import User
    from sqlmodel import select

    async with async_session_maker() as session:
        # Check if user exists, create if not
        statement = select(User).where(User.id == user_id)
        result = await session.execute(statement)
        user = result.scalar_one_or_none()

        if not user:
            # Create a default user
            user = User(
                id=user_id,
                email=f"{user_id}@default.com",  # Generate a default email
                name="Default User"  # Default name
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)

        conversation = Conversation(user_id=user_id)
        session.add(conversation)
        await session.commit()
        await session.refresh(conversation)
        return str(conversation.conversation_id)


async def get_conversation_history(
    conversation_id: str,
    limit: int = 10
) -> List[dict]:
    """Get conversation history with last N messages."""
    from app.core.database import async_session_maker

    async with async_session_maker() as session:
        statement = (
            select(Message)
            .where(Message.conversation_id == UUID(conversation_id))
            .order_by(Message.created_at.desc())
            .limit(limit)
        )
        result = await session.execute(statement)
        messages = result.scalars().all()

        # Return in chronological order (oldest first)
        return [
            {
                "role": msg.role,
                "content": msg.content,
                "tool_calls": msg.tool_calls,
                "created_at": msg.created_at
            }
            for msg in reversed(messages)
        ]


async def add_message(
    conversation_id: str,
    role: str,
    content: str,
    tool_calls: Optional[dict] = None
) -> None:
    """Add a message to a conversation."""
    from app.core.database import async_session_maker
    import html
    import re

    # Input sanitization: max 10,000 chars and strip HTML tags
    if len(content) > 10000:
        content = content[:10000]

    # Strip HTML tags using regex
    clean_content = re.sub(r'<[^>]+>', '', content)

    # Additionally, escape any HTML entities for safety
    clean_content = html.escape(clean_content, quote=True)

    async with async_session_maker() as session:
        message = Message(
            conversation_id=UUID(conversation_id),
            role=role,
            content=clean_content,
            tool_calls=tool_calls
        )
        session.add(message)

        # Update conversation.updated_at
        conversation = await session.get(Conversation, UUID(conversation_id))
        if conversation:
            conversation.updated_at = datetime.utcnow()

        await session.commit()


async def list_user_conversations(user_id: str) -> List[Conversation]:
    """List all conversations for a user."""
    from app.core.database import async_session_maker

    async with async_session_maker() as session:
        statement = (
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .order_by(Conversation.updated_at.desc())
        )
        result = await session.execute(statement)
        return result.scalars().all()