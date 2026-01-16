#!/usr/bin/env python3
"""
Test script to verify the TodoChatAgent functionality in isolation.
This bypasses the full authentication system to test the core agent logic.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the backend directory to the Python path
sys.path.insert(0, str(Path(__file__).parent))

# Mock environment variables for testing
os.environ.setdefault("OPENROUTER_API_KEY", "sk-or-v1-test-key-if-not-set")
os.environ.setdefault("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
os.environ.setdefault("OPENROUTER_MODEL", "mistralai/devstral-2512:free")

async def test_agent():
    """Test the TodoChatAgent functionality directly."""
    try:
        from app.agents.chat_agent import TodoChatAgent

        print("Creating TodoChatAgent instance...")
        agent = TodoChatAgent(user_id="test_user_123")
        print("✓ TodoChatAgent created successfully")

        print("\nTesting with English message:")
        english_result = await agent.process_message(
            user_message="Add a task to buy groceries",
            user_id="test_user_123"
        )
        print(f"Response: {english_result['response']}")
        print(f"Tool calls: {english_result.get('tool_calls', [])}")

        print("\nTesting with Urdu message:")
        urdu_result = await agent.process_message(
            user_message=" grocery خریدنے کا کام شامل کریں",
            user_id="test_user_123"
        )
        print(f"Response: {urdu_result['response']}")
        print(f"Tool calls: {urdu_result.get('tool_calls', [])}")

        print("\n✓ Agent tests completed successfully!")
        return True

    except Exception as e:
        print(f"✗ Error testing agent: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Testing TodoChatAgent functionality...")
    success = asyncio.run(test_agent())
    if success:
        print("\n✓ All tests passed!")
    else:
        print("\n✗ Some tests failed.")
        sys.exit(1)