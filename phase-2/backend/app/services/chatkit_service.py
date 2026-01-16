"""ChatKit service for Phase III AI Chatbot using OpenAI ChatKit integration."""

from typing import Dict, Any, Optional
from uuid import UUID
import json
from datetime import datetime

from app.core.database import async_session_maker
from app.services.conversation_service import create_conversation, add_message, get_conversation_history
from app.agents.chat_agent import TodoChatAgent


class ChatKitService:
    """Service to handle ChatKit-specific functionality."""

    def __init__(self):
        pass

    def _create_agent(self, user_id: str) -> TodoChatAgent:
        """Create a new agent instance for the given user."""
        return TodoChatAgent(user_id=user_id)

    async def create_session(self, user_id: str) -> Dict[str, Any]:
        """Create a new ChatKit session for the user."""
        try:
            # Create a conversation for this session
            conversation_id = await create_conversation(UUID(user_id))

            # Return session data with client secret
            return {
                "client_secret": f"chatkit_session_{user_id}_{conversation_id}",
                "conversation_id": str(conversation_id),
                "user_id": user_id,
                "created_at": datetime.utcnow().isoformat()
            }
        except Exception as e:
            raise Exception(f"Failed to create ChatKit session: {str(e)}")

    async def refresh_session(self, token: str) -> Dict[str, Any]:
        """Refresh an existing ChatKit session."""
        try:
            # Extract user_id and conversation_id from the token
            # In a real implementation, you would validate the token properly
            parts = token.split("_")
            if len(parts) < 3:
                raise ValueError("Invalid token format")

            user_id = parts[2]
            conversation_id = parts[3] if len(parts) > 3 else None

            return {
                "client_secret": token,  # Return the same token as the new secret
                "conversation_id": conversation_id,
                "user_id": user_id,
                "refreshed_at": datetime.utcnow().isoformat()
            }
        except Exception as e:
            raise Exception(f"Failed to refresh ChatKit session: {str(e)}")

    async def handle_chatkit_request(self, payload: bytes, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle ChatKit requests and process with AI agent."""
        try:
            # Parse the ChatKit request
            request_data = json.loads(payload)

            # Extract relevant information from the request
            thread_id = request_data.get('thread_id')
            user_message = request_data.get('message')
            user_id = context.get('user_id', request_data.get('user_id'))

            if not user_message:
                return {
                    "error": "No message provided",
                    "status": "error"
                }

            # Get conversation history
            conversation_history = []
            if thread_id:
                # In a real implementation, thread_id would map to our conversation_id
                # For now, we'll use a placeholder
                conversation_history = await get_conversation_history(
                    UUID(thread_id.split('_')[1]) if '_' in thread_id else None,
                    limit=10
                )

            # Create agent for this user
            agent = self._create_agent(user_id)

            # Process message with AI agent
            result = await agent.process_message(
                user_message=user_message,
                conversation_history=conversation_history,
                user_id=user_id
            )

            # Store user message
            await add_message(
                conversation_id=UUID(thread_id.split('_')[1]) if thread_id and '_' in thread_id else None,
                role="user",
                content=user_message
            )

            # Store assistant response
            await add_message(
                conversation_id=UUID(thread_id.split('_')[1]) if thread_id and '_' in thread_id else None,
                role="assistant",
                content=result["response"],
                tool_calls=result.get("tool_calls", [])
            )

            # Return response in ChatKit format
            response = {
                "type": "thread.item.append",
                "item": {
                    "id": f"msg_{datetime.utcnow().timestamp()}",
                    "object": "thread.item",
                    "type": "message",
                    "content": [
                        {
                            "type": "text",
                            "text": {
                                "value": result["response"]
                            }
                        }
                    ],
                    "role": "assistant"
                }
            }

            # If there are tool calls, include them in the response
            if result.get("tool_calls"):
                response["tool_calls"] = result["tool_calls"]

            return response

        except Exception as e:
            return {
                "error": f"Error processing ChatKit request: {str(e)}",
                "status": "error"
            }

    async def process_streaming_response(self, user_message: str, user_id: str, thread_id: Optional[str] = None):
        """Process a message and yield streaming responses."""
        try:
            # Get conversation history
            conversation_history = []
            if thread_id:
                conversation_id = thread_id.split('_')[1] if '_' in thread_id else None
                if conversation_id:
                    conversation_history = await get_conversation_history(UUID(conversation_id), limit=10)

            # Process message with AI agent
            agent = self._create_agent(user_id)

            result = await agent.process_message(
                user_message=user_message,
                conversation_history=conversation_history,
                user_id=user_id
            )

            # Yield the response in streaming format
            yield {
                "type": "thread.item.append",
                "item": {
                    "id": f"msg_{datetime.utcnow().timestamp()}",
                    "object": "thread.item",
                    "type": "message",
                    "content": [
                        {
                            "type": "text",
                            "text": {
                                "value": result["response"]
                            }
                        }
                    ],
                    "role": "assistant"
                }
            }

            # Yield done message
            yield {
                "type": "done"
            }

        except Exception as e:
            yield {
                "type": "error",
                "message": f"Error processing message: {str(e)}"
            }