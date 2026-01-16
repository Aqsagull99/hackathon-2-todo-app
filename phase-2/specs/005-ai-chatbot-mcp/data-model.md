# Phase 1: Data Model Design

**Feature**: 005-ai-chatbot-mcp
**Date**: 2026-01-10
**Prerequisites**: research.md complete

## Overview

Phase III extends Phase II database schema with two new entities: **Conversation** and **Message**. No changes to existing Task, Tag, User schemas.

---

## New Entities

### 1. Conversation

Represents a chat session between user and AI assistant.

**SQLModel Definition**:
```python
# backend/app/models/conversation.py
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
import uuid

class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"

    conversation_id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True
    )
    user_id: uuid.UUID = Field(
        foreign_key="users.id",
        nullable=False,
        index=True
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    messages: list["Message"] = Relationship(
        back_populates="conversation",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    user: "User" = Relationship(back_populates="conversations")
```

**Fields**:
- `conversation_id`: UUID primary key (auto-generated)
- `user_id`: Foreign key to users table (indexed for fast lookups)
- `created_at`: Timestamp of conversation start
- `updated_at`: Timestamp of last message

**Indexes**:
- `idx_conversations_user_id` ON `user_id` (for listing user's conversations)

**Validation**:
- `user_id` must reference existing user
- Conversations cannot exist without an owner (CASCADE DELETE)

---

### 2. Message

Represents a single message within a conversation (user or assistant).

**SQLModel Definition**:
```python
# backend/app/models/message.py
from sqlmodel import SQLModel, Field, Relationship, Column, Enum, JSON
from datetime import datetime
import uuid

class Message(SQLModel, table=True):
    __tablename__ = "messages"

    message_id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True
    )
    conversation_id: uuid.UUID = Field(
        foreign_key="conversations.conversation_id",
        nullable=False,
        index=True
    )
    role: str = Field(
        sa_column=Column(
            Enum("user", "assistant", name="message_role"),
            nullable=False
        )
    )
    content: str = Field(nullable=False, max_length=10000)
    tool_calls: Optional[dict] = Field(
        default=None,
        sa_column=Column(JSON)
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        index=True
    )

    # Relationships
    conversation: Conversation = Relationship(back_populates="messages")
```

**Fields**:
- `message_id`: UUID primary key
- `conversation_id`: Foreign key to conversations (indexed)
- `role`: Enum "user" or "assistant" (enforced at DB level)
- `content`: Message text (max 10,000 characters)
- `tool_calls`: JSONB array of MCP tool invocations (nullable)
- `created_at`: Timestamp (indexed for ordering)

**tool_calls Format**:
```json
[
  {
    "tool": "add_task",
    "parameters": {"title": "Buy groceries", "priority": "high"},
    "result": {"task_id": 42, "status": "created"}
  }
]
```

**Indexes**:
- `idx_messages_conversation_id` ON `conversation_id`
- `idx_messages_created_at` ON `created_at` (for chronological ordering)

**Validation**:
- `role` must be "user" or "assistant"
- `content` must not be empty
- `tool_calls` must be valid JSON if present

---

## Existing Entities (No Changes)

### Task
Remains unchanged from Phase II (spec 004).

### Tag
Remains unchanged from Phase II (spec 004).

### TaskTag
Join table, no changes.

### User
Add new relationship:
```python
conversations: list[Conversation] = Relationship(back_populates="user")
```

---

## Database Migration

**Alembic Migration Script**:
```python
# migrations/versions/xxxx_add_conversation_message.py
from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

revision = 'xxxx'
down_revision = 'previous_revision'

def upgrade():
    # Create conversations table
    op.create_table(
        'conversations',
        sa.Column('conversation_id', postgresql.UUID(), nullable=False),
        sa.Column('user_id', postgresql.UUID(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('conversation_id')
    )
    op.create_index('idx_conversations_user_id', 'conversations', ['user_id'])

    # Create messages table
    op.create_table(
        'messages',
        sa.Column('message_id', postgresql.UUID(), nullable=False),
        sa.Column('conversation_id', postgresql.UUID(), nullable=False),
        sa.Column('role', sa.Enum('user', 'assistant', name='message_role'), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('tool_calls', postgresql.JSONB(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.conversation_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('message_id')
    )
    op.create_index('idx_messages_conversation_id', 'messages', ['conversation_id'])
    op.create_index('idx_messages_created_at', 'messages', ['created_at'])

def downgrade():
    op.drop_table('messages')
    op.drop_table('conversations')
```

**Run Migration**:
```bash
cd backend/
alembic revision --autogenerate -m "Add conversation and message tables"
alembic upgrade head
```

---

## Entity Relationships

```
User (existing)
  └── 1:N → Conversation (new)
                └── 1:N → Message (new)

Task (existing) - No relationship to Conversation
  └── M:N → Tag (existing, via TaskTag)
```

**Key Insight**: Conversations are independent of Tasks. MCP tools create/modify tasks, but tasks don't "know" about conversations.

---

## Query Patterns

### 1. Create New Conversation
```python
async def create_conversation(user_id: uuid.UUID):
    async with get_async_session() as session:
        conversation = Conversation(user_id=user_id)
        session.add(conversation)
        await session.commit()
        return conversation.conversation_id
```

### 2. Add Message
```python
async def add_message(
    conversation_id: uuid.UUID,
    role: str,
    content: str,
    tool_calls: dict | None = None
):
    async with get_async_session() as session:
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
            tool_calls=tool_calls
        )
        session.add(message)

        # Update conversation.updated_at
        conversation = await session.get(Conversation, conversation_id)
        conversation.updated_at = datetime.utcnow()

        await session.commit()
```

### 3. Get Conversation History (Last N Messages)
```python
async def get_conversation_history(
    conversation_id: uuid.UUID,
    limit: int = 10
) -> list[dict]:
    async with get_async_session() as session:
        statement = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.desc())
            .limit(limit)
        )
        result = await session.execute(statement)
        messages = result.scalars().all()

        # Return in chronological order
        return [
            {
                "role": msg.role,
                "content": msg.content,
                "tool_calls": msg.tool_calls,
                "created_at": msg.created_at
            }
            for msg in reversed(messages)
        ]
```

### 4. List User's Conversations
```python
async def list_user_conversations(user_id: uuid.UUID):
    async with get_async_session() as session:
        statement = (
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .order_by(Conversation.updated_at.desc())
        )
        result = await session.execute(statement)
        return result.scalars().all()
```

---

## Data Validation Rules

### Conversation
- `user_id`: Must exist in users table
- `created_at`, `updated_at`: Auto-managed, no manual updates

### Message
- `role`: Must be "user" or "assistant" (DB enum enforced)
- `content`: 1-10,000 characters (validated in Pydantic schema)
- `tool_calls`: If present, must be valid JSON array with structure:
  ```json
  [{"tool": str, "parameters": dict, "result": dict}]
  ```
- `conversation_id`: Must exist in conversations table

---

## Performance Considerations

### Index Strategy
- `idx_conversations_user_id`: Fast user conversation listing
- `idx_messages_conversation_id`: Fast message retrieval for a conversation
- `idx_messages_created_at`: Efficient chronological ordering

### Query Optimization
- Limit conversation history to 10 messages (configurable)
- Use `order_by().desc().limit()` for efficient last-N-messages query
- JSONB field `tool_calls` uses PostgreSQL's native JSON support (fast queries)

### Expected Performance
- Get conversation history (10 messages): <100ms
- Create conversation: <50ms
- Add message: <50ms
- List user conversations: <200ms (assuming <100 conversations per user)

---

## Storage Estimates

### Per Conversation
- Conversation row: ~100 bytes
- Message row: ~500 bytes average (content + metadata)
- Tool calls JSON: ~200 bytes per tool call

### Scaling Assumptions
- 10,000 users
- 5 conversations per user (average)
- 50 messages per conversation (average)

**Total Storage**: 10k × 5 × 50 × 700 bytes ≈ **1.75 GB**

Neon free tier: 10 GB → Sufficient for MVP

---

## Security Considerations

### User Isolation
- **Critical**: Always filter conversations by `user_id`
- Never expose `conversation_id` without verifying ownership

```python
# CORRECT
async def get_conversation(conversation_id: uuid.UUID, user_id: uuid.UUID):
    async with get_async_session() as session:
        statement = (
            select(Conversation)
            .where(
                Conversation.conversation_id == conversation_id,
                Conversation.user_id == user_id  # Ownership check
            )
        )
        result = await session.execute(statement)
        return result.scalar_one_or_none()

# WRONG - Allows cross-user access
async def get_conversation_insecure(conversation_id: uuid.UUID):
    async with get_async_session() as session:
        return await session.get(Conversation, conversation_id)
```

### Tool Calls Auditing
- `tool_calls` field provides audit trail of all MCP operations
- Query all tool invocations: `SELECT * FROM messages WHERE tool_calls IS NOT NULL`

---

## Testing Strategy

### Unit Tests
```python
@pytest.mark.asyncio
async def test_create_conversation(test_db):
    conversation_id = await create_conversation(user_id="user123")
    assert conversation_id is not None

@pytest.mark.asyncio
async def test_add_message(test_db, test_conversation):
    await add_message(
        conversation_id=test_conversation.conversation_id,
        role="user",
        content="Add a task to buy groceries"
    )

    messages = await get_conversation_history(test_conversation.conversation_id)
    assert len(messages) == 1
    assert messages[0]["role"] == "user"

@pytest.mark.asyncio
async def test_user_isolation(test_db, user1_conversation):
    # User2 tries to access User1's conversation
    result = await get_conversation(
        conversation_id=user1_conversation.conversation_id,
        user_id="user2"
    )
    assert result is None  # Access denied
```

---

**Data Model Design Complete**: 2026-01-10
**Status**: ✅ APPROVED - Ready for API Contracts (Phase 1.2)
