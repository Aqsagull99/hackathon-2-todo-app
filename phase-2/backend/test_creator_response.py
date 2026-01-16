
import asyncio
import os
from app.agents.chat_agent import TodoChatAgent

async def test_creator_question():
    # Set a dummy user ID
    user_id = "test_user_123"

    # Initialize the agent
    print("Initializing agent...")
    agent = TodoChatAgent(user_id=user_id)

    # Force use_fallback to True to test logic first (bypassing LLM API)
    agent.use_fallback = True
    print("\n--- Testing Fallback Logic ---")
    response_fallback = await agent.process_message("who made this app", [], user_id)
    print(f"Fallback Response: {response_fallback['response']}")

    response_fallback_urdu = await agent.process_message("ye kisne banaya", [], user_id)
    print(f"Fallback Response (Urdu): {response_fallback_urdu['response']}")

    # Now basic check if instructions are set (we can't easily mock the LLM call without an API key)
    print("\n--- Verifying System Instructions ---")
    if hasattr(agent, 'agent') and hasattr(agent.agent, 'instructions'):
        instructions = agent.agent.instructions
        if "Aqsa Gull" in instructions:
            print("SUCCESS: System instructions contain 'Aqsa Gull'")
        else:
            print("FAILURE: System instructions DO NOT contain 'Aqsa Gull'")
            print(f"Instructions excerpt: {instructions[:200]}...")
    else:
        print("Could not access agent instructions directly")

if __name__ == "__main__":
    # We need to run this from the backend directory so imports work
    # cd phase-2/backend && uv run python test_creator_response.py
    asyncio.run(test_creator_question())
