"""Chat API routes for Phase III AI Chatbot."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.agents.chat_agent import TodoChatAgent
from app.api.deps import get_current_user_id
from app.services.conversation_service import (
    add_message,
    create_conversation,
    get_conversation_history
)

router = APIRouter(prefix="/api/chat", tags=["chat"])


class ChatRequest(BaseModel):
    conversation_id: Optional[str] = None
    message: str


class ToolCall(BaseModel):
    tool: str
    parameters: dict
    result: dict


class ChatResponse(BaseModel):
    conversation_id: str
    response: str
    tool_calls: Optional[list[ToolCall]] = []


@router.post("/", response_model=ChatResponse)
async def chat_endpoint(
    request: ChatRequest,
    user_id: str = Depends(get_current_user_id)
):
    """Handle chat messages and process with AI agent."""
    from app.core.database import async_session_maker

    try:
        print(f"Chat endpoint called for user: {user_id}")  # Debug log
        print(f"Received message: {request.message}")  # Debug log

        # Create or get conversation ID
        if not request.conversation_id:
            conversation_id = await create_conversation(user_id)
            print(f"Created new conversation: {conversation_id}")  # Debug log
        else:
            conversation_id = UUID(request.conversation_id)
            print(f"Using existing conversation: {conversation_id}")  # Debug log

        # Get conversation history and simplify messages for the agent
        conversation_history = await get_conversation_history(conversation_id, limit=10)
        print(f"Retrieved {len(conversation_history)} messages from history")  # Debug log
        # Agent expects simple role/content messages; strip metadata like datetimes/tool_calls
        simple_history = []
        for m in conversation_history:
            try:
                simple_history.append({"role": m.get("role"), "content": m.get("content")})
            except Exception:
                # Skip malformed items
                continue

        # Process message with AI agent
        # Note: Using agent without MCP tools to avoid connection issues
        print("Creating TodoChatAgent...")  # Debug log
        agent = TodoChatAgent(user_id=user_id)
        print("Processing message with agent...")  # Debug log

        result = await agent.process_message(
            user_message=request.message,
            conversation_history=simple_history,
            user_id=user_id
        )
        print(f"Agent response: {result['response'][:100]}...")  # Debug log

        # If the model replied that it added a task but did not invoke a tool,
        # create the task in the DB based on the user's last message (simple heuristic).
        if (not result.get("tool_calls")) and ("added" in result.get("response", "").lower()):
            print("Auto-create heuristic triggered: agent claimed to add a task but no tool_calls present")
            try:
                # Extract title from the user's message more robustly
                title = None
                if isinstance(request.message, str):
                    message_lower = request.message.lower().strip()

                    # Try to extract after common prefixes like "add task to ", "create task ", etc.
                    prefixes = ["add task to ", "add a task to ", "add ", "create task ", "create ", "make ", "please "]

                    for prefix in prefixes:
                        if message_lower.startswith(prefix):
                            title = request.message[len(prefix):].strip()
                            break

                    # If no prefix matched, try to extract after colon
                    if not title and ":" in request.message:
                        title = request.message.split(":", 1)[1].strip()

                    # If still no title found, use the entire message as title (but remove common prefixes)
                    if not title:
                        title = request.message.strip()
                        # Remove common command prefixes
                        for prefix in prefixes:
                            if title.lower().startswith(prefix):
                                title = title[len(prefix):].strip()
                                break

                if title and len(title.strip()) > 0:
                    print(f"Attempting to persist auto-created task for user {user_id}: {title}")
                    from app.core.database import async_session_maker
                    from app.services.task_service import create_task
                    from app.schemas.extended import TaskCreateExtended
                    from app.models.task import TaskPriority, RecurrencePattern
                    import traceback

                    # Extract additional properties from the message like priority, description, due date, etc.
                    description = None
                    priority = TaskPriority.MEDIUM  # default priority
                    due_date = None
                    recurrence_pattern = None
                    reminder_time = None  # Extracted reminder time

                    # Look for priority in the message
                    message_lower = request.message.lower()
                    if "priority: high" in message_lower or "high priority" in message_lower or "priority high" in message_lower:
                        priority = TaskPriority.HIGH
                    elif "priority: low" in message_lower or "low priority" in message_lower or "priority low" in message_lower:
                        priority = TaskPriority.LOW
                    elif "priority: medium" in message_lower or "medium priority" in message_lower or "priority medium" in message_lower:
                        priority = TaskPriority.MEDIUM

                    # Look for due date in the message
                    import re
                    # Look for various date patterns like "tomorrow", "next Monday", "by Friday", "on 2023-12-25", etc.
                    date_patterns = [
                        r"by\s+(.+?)(?:\s|$|,|and|but)",  # "by tomorrow", "by next Monday"
                        r"on\s+(.+?)(?:\s|$|,|and|but)",  # "on Monday", "on 2023-12-25"
                        r"due\s+(.+?)(?:\s|$|,|and|but)", # "due tomorrow", "due next week"
                        r"for\s+(.+?)(?:\s|$|,|and|but)", # "for tomorrow", "for next week"
                    ]

                    for pattern in date_patterns:
                        date_match = re.search(pattern, request.message, re.IGNORECASE)
                        if date_match:
                            date_str = date_match.group(1).strip()

                            # Simple date parsing - try to convert common expressions
                            from datetime import datetime, timedelta
                            today = datetime.now()

                            if "tomorrow" in date_str.lower():
                                due_date = today + timedelta(days=1)
                                due_date = due_date.replace(hour=9, minute=0, second=0, microsecond=0)  # Set to 9 AM
                            elif "today" in date_str.lower():
                                due_date = today.replace(hour=9, minute=0, second=0, microsecond=0)  # Set to 9 AM today
                            elif "monday" in date_str.lower():
                                days_ahead = 0 if today.weekday() == 0 else (7 - today.weekday()) if today.weekday() > 0 else 0
                                if days_ahead == 0 and today.weekday() != 0:
                                    days_ahead = 7
                                due_date = today.replace(hour=9, minute=0, second=0, microsecond=0) + timedelta(days_ahead)
                            elif "tuesday" in date_str.lower():
                                days_ahead = 1 - today.weekday()
                                if days_ahead <= 0:  # Target day already happened this week
                                    days_ahead += 7
                                due_date = today.replace(hour=9, minute=0, second=0, microsecond=0) + timedelta(days_ahead)
                            elif "wednesday" in date_str.lower():
                                days_ahead = 2 - today.weekday()
                                if days_ahead <= 0:  # Target day already happened this week
                                    days_ahead += 7
                                due_date = today.replace(hour=9, minute=0, second=0, microsecond=0) + timedelta(days_ahead)
                            elif "thursday" in date_str.lower():
                                days_ahead = 3 - today.weekday()
                                if days_ahead <= 0:  # Target day already happened this week
                                    days_ahead += 7
                                due_date = today.replace(hour=9, minute=0, second=0, microsecond=0) + timedelta(days_ahead)
                            elif "friday" in date_str.lower():
                                days_ahead = 4 - today.weekday()
                                if days_ahead <= 0:  # Target day already happened this week
                                    days_ahead += 7
                                due_date = today.replace(hour=9, minute=0, second=0, microsecond=0) + timedelta(days_ahead)
                            elif "saturday" in date_str.lower():
                                days_ahead = 5 - today.weekday()
                                if days_ahead <= 0:  # Target day already happened this week
                                    days_ahead += 7
                                due_date = today.replace(hour=9, minute=0, second=0, microsecond=0) + timedelta(days_ahead)
                            elif "sunday" in date_str.lower():
                                days_ahead = 6 - today.weekday()
                                if days_ahead <= 0:  # Target day already happened this week
                                    days_ahead += 7
                                due_date = today.replace(hour=9, minute=0, second=0, microsecond=0) + timedelta(days_ahead)
                            elif re.search(r'\d{4}-\d{2}-\d{2}', date_str):  # YYYY-MM-DD format
                                try:
                                    due_date = datetime.strptime(re.search(r'\d{4}-\d{2}-\d{2}', date_str).group(), '%Y-%m-%d')
                                    due_date = due_date.replace(hour=9, minute=0, second=0, microsecond=0)  # Set to 9 AM
                                except ValueError:
                                    pass  # Ignore if date format is invalid
                            elif re.search(r'\d{2}/\d{2}/\d{4}', date_str):  # MM/DD/YYYY format
                                try:
                                    due_date = datetime.strptime(re.search(r'\d{2}/\d{2}/\d{4}', date_str).group(), '%m/%d/%Y')
                                    due_date = due_date.replace(hour=9, minute=0, second=0, microsecond=0)  # Set to 9 AM
                                except ValueError:
                                    pass  # Ignore if date format is invalid
                            elif re.search(r'\d{2}-\d{2}-\d{4}', date_str):  # DD-MM-YYYY format
                                try:
                                    due_date = datetime.strptime(re.search(r'\d{2}-\d{2}-\d{4}', date_str).group(), '%d-%m-%Y')
                                    due_date = due_date.replace(hour=9, minute=0, second=0, microsecond=0)  # Set to 9 AM
                                except ValueError:
                                    pass  # Ignore if date format is invalid
                            break  # Take the first date found

                    # Look for recurrence pattern in the message
                    recurrence_patterns = {
                        "daily": ["daily", "every day", "each day", "everyday"],
                        "weekly": ["weekly", "every week", "each week", "every monday", "every tuesday", "every wednesday", "every thursday", "every friday", "every saturday", "every sunday"],
                        "monthly": ["monthly", "every month", "each month"]
                    }

                    for rec_pattern, keywords in recurrence_patterns.items():
                        for keyword in keywords:
                            if keyword in message_lower:
                                recurrence_pattern = RecurrencePattern(rec_pattern.upper())
                                break
                        if recurrence_pattern:
                            break

                    # Look for reminder in the message
                    # Patterns like "reminder 1 hour before", "remind me 30 minutes before", etc.
                    reminder_patterns = [
                        r"reminder\s+(.+?)\s+before",
                        r"remind\s+me\s+(.+?)\s+before",
                        r"remind\s+(.+?)\s+before",
                    ]

                    for pattern in reminder_patterns:
                        reminder_match = re.search(pattern, request.message, re.IGNORECASE)
                        if reminder_match:
                            reminder_spec = reminder_match.group(1).strip()

                            # Parse time units for reminder
                            time_match = re.search(r'(\d+)\s*(hour|minute|day|week)s?\s*(before|prior|earlier)', reminder_spec, re.IGNORECASE)
                            if time_match:
                                time_amount = int(time_match.group(1))
                                time_unit = time_match.group(2).lower()

                                # Calculate reminder time based on due date
                                if due_date:
                                    if time_unit.startswith('hour'):
                                        reminder_time = due_date - timedelta(hours=time_amount)
                                    elif time_unit.startswith('minute'):
                                        reminder_time = due_date - timedelta(minutes=time_amount)
                                    elif time_unit.startswith('day'):
                                        reminder_time = due_date - timedelta(days=time_amount)
                                    elif time_unit.startswith('week'):
                                        reminder_time = due_date - timedelta(weeks=time_amount)

                            break  # Only process the first reminder found

                    # Look for description in the message
                    desc_match = re.search(r"(?:description:|desc:)\s*(.*?)(?:\n|$|Tags:|Priority:|Due date:|due date|by |on |for )", request.message, re.IGNORECASE)
                    if desc_match:
                        description = desc_match.group(1).strip()

                    async with async_session_maker() as db:
                        task_payload = TaskCreateExtended(
                            title=title,
                            description=description,
                            priority=priority,
                            due_date=due_date,
                            recurrence_pattern=recurrence_pattern
                        )
                        task = await create_task(db, user_id, task_payload)

                        # Create reminder if specified
                        if reminder_time:
                            try:
                                from app.services import reminder_service
                                reminder = await reminder_service.create_reminder(db, task.id, reminder_time)
                                print(f"Created reminder for task {task.id} at {reminder_time}")
                            except Exception as e:
                                print(f"Failed to create reminder: {e}")

                    print(f"Auto-created extended task id={task.id} title={task.title} priority={task.priority} due_date={task.due_date} recurrence={task.recurrence_pattern} reminder={reminder_time}")

                    # Attach a tool_calls entry so frontend can react
                    tool_calls = [{
                        "tool": "create_task",
                        "parameters": {
                            "title": title,
                            "description": description,
                            "priority": priority.value if hasattr(priority, 'value') else priority,
                            "due_date": due_date.isoformat() if due_date else None,
                            "recurrence_pattern": recurrence_pattern.value if recurrence_pattern else None,
                            "reminder_time": reminder_time.isoformat() if reminder_time else None
                        },
                        "result": {
                            "id": task.id,
                            "title": task.title,
                            "description": task.description,
                            "priority": task.priority.value if hasattr(task.priority, 'value') else task.priority,
                            "due_date": task.due_date.isoformat() if task.due_date else None,
                            "recurrence_pattern": task.recurrence_pattern.value if task.recurrence_pattern else None,
                            "reminder_time": reminder_time.isoformat() if reminder_time else None,
                            "local": False
                        },
                    }]
                    result["tool_calls"] = tool_calls
                    # Augment assistant response with created ID for clarity
                    result["response"] = f"{result['response']} (Created task ID: {task.id})"
                else:
                    print("Auto-create heuristic: no title found in user message")
                    print(f"User message was: '{request.message}'")
            except Exception as e:
                import traceback
                traceback.print_exc()
                print("Failed to persist auto-created task:", e)

        # Store user message
        await add_message(
            conversation_id=conversation_id,
            role="user",
            content=request.message
        )

        # Store assistant response
        await add_message(
            conversation_id=conversation_id,
            role="assistant",
            content=result["response"],
            tool_calls=result["tool_calls"]
        )

        print("Returning response successfully")  # Debug log
        return ChatResponse(
            conversation_id=str(conversation_id),
            response=result["response"],
            tool_calls=result.get("tool_calls", [])
        )

    except Exception as e:
        error_msg = f"Chat processing error: {str(e)}"
        print(error_msg)  # Log the error for debugging
        import traceback
        traceback.print_exc()  # Print full stack trace
        raise HTTPException(status_code=500, detail=error_msg)


@router.get("/conversations")
async def list_conversations(user_id: str = Depends(get_current_user_id)):
    """List user's conversations."""
    from app.services.conversation_service import list_user_conversations
    from uuid import UUID

    conversations = await list_user_conversations(UUID(user_id))
    return {
        "conversations": [
            {
                "conversation_id": str(conv.conversation_id),
                "created_at": conv.created_at.isoformat(),
                "updated_at": conv.updated_at.isoformat()
            }
            for conv in conversations
        ]
    }


@router.get("/conversations/{conversation_id}/messages")
async def get_conversation_messages(
    conversation_id: str,
    user_id: str = Depends(get_current_user_id)
):
    """Get messages for a specific conversation."""
    from uuid import UUID
    from sqlmodel import select
    from app.models.conversation import Conversation
    from app.core.database import async_session_maker

    conv_uuid = UUID(conversation_id)

    # Verify conversation belongs to user
    async with async_session_maker() as session:
        stmt = select(Conversation).where(
            Conversation.conversation_id == conv_uuid,
            Conversation.user_id == UUID(user_id)
        )
        result = await session.execute(stmt)
        conversation = result.scalar_one_or_none()

        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")

    messages = await get_conversation_history(conv_uuid, limit=50)
    return {"messages": messages}