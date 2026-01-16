"""ChatKit API routes for Phase III AI Chatbot integration."""

from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
import json

from app.api.deps import get_current_user_id
from app.services.chatkit_service import ChatKitService

router = APIRouter(prefix="/api", tags=["chatkit"])

# Global service instance
chatkit_service = ChatKitService()


@router.post("/chatkit/session")
async def create_chatkit_session(
    user_id: str = Depends(get_current_user_id)
) -> Dict[str, Any]:
    """Create a new ChatKit session for the authenticated user."""
    try:
        session_data = await chatkit_service.create_session(user_id)
        return session_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chatkit/refresh")
async def refresh_chatkit_session(
    request: Request,
    user_id: str = Depends(get_current_user_id)
) -> Dict[str, Any]:
    """Refresh an existing ChatKit session."""
    try:
        body = await request.json()
        token = body.get("token")

        if not token:
            raise HTTPException(status_code=400, detail="Token is required for refresh")

        session_data = await chatkit_service.refresh_session(token)
        return session_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chatkit")
async def handle_chatkit_request(
    request: Request,
    user_id: str = Depends(get_current_user_id)
):
    """Handle all ChatKit requests."""
    try:
        # Get raw body for ChatKit processing
        payload = await request.body()

        # Process the request with the service
        context = {"user_id": user_id, "request": request}
        result = await chatkit_service.handle_chatkit_request(payload, context)

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ChatKit processing error: {str(e)}")


@router.post("/chatkit/stream")
async def handle_chatkit_streaming(
    request: Request,
    user_id: str = Depends(get_current_user_id)
):
    """Handle ChatKit streaming requests."""
    try:
        body = await request.json()
        user_message = body.get("message")
        thread_id = body.get("thread_id")

        if not user_message:
            raise HTTPException(status_code=400, detail="Message is required")

        async def event_generator():
            async for chunk in chatkit_service.process_streaming_response(
                user_message, user_id, thread_id
            ):
                yield f"data: {json.dumps(chunk)}\n\n"

        return StreamingResponse(
            event_generator(),
            media_type="text/event-stream"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ChatKit streaming error: {str(e)}")


@router.get("/chatkit/threads")
async def list_user_threads(
    user_id: str = Depends(get_current_user_id)
):
    """List user's ChatKit threads (conversations)."""
    try:
        # In a real implementation, this would fetch from a thread store
        # For now, we'll return a mock response
        from app.services.conversation_service import list_user_conversations
        from uuid import UUID

        conversations = await list_user_conversations(UUID(user_id))

        threads = []
        for conv in conversations:
            threads.append({
                "id": f"thread_{conv.conversation_id}",
                "title": f"Conversation {conv.conversation_id}",
                "created_at": conv.created_at.isoformat(),
                "updated_at": conv.updated_at.isoformat()
            })

        return {"threads": threads}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching threads: {str(e)}")


@router.get("/chatkit/threads/{thread_id}/messages")
async def get_thread_messages(
    thread_id: str,
    user_id: str = Depends(get_current_user_id)
):
    """Get messages for a specific ChatKit thread."""
    try:
        # Extract conversation_id from thread_id
        conversation_id_str = thread_id.replace("thread_", "")
        from uuid import UUID
        conversation_id = UUID(conversation_id_str)

        # Verify conversation belongs to user
        from sqlmodel import select
        from app.models.conversation import Conversation
        from app.core.database import async_session_maker

        async with async_session_maker() as session:
            stmt = select(Conversation).where(
                Conversation.conversation_id == conversation_id,
                Conversation.user_id == UUID(user_id)
            )
            result = await session.execute(stmt)
            conversation = result.scalar_one_or_none()

        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")

        # Get conversation history
        from app.services.conversation_service import get_conversation_history
        messages = await get_conversation_history(conversation_id, limit=50)

        return {"messages": messages}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching messages: {str(e)}")