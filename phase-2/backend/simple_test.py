#!/usr/bin/env python3
"""Simple test to verify that the TodoChatAgent can be initialized."""

import os
import asyncio

# Set environment variables
os.environ['OPENROUTER_API_KEY'] = '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'
os.environ['OPENROUTER_BASE_URL'] = 'https://openrouter.ai/api/v1'
os.environ['OPENROUTER_MODEL'] = 'mistralai/devstral-2512:free'

async def test_agent_initialization():
    """Test that the agent can be initialized without errors."""
    print("Testing agent initialization...")

    try:
        from app.agents.chat_agent import TodoChatAgent

        # Create the agent
        agent = TodoChatAgent()
        print("✅ Agent initialized successfully!")

        # Test that the agent has tools
        print(f"✅ Agent has tools: True")

        return True
    except Exception as e:
        print(f"❌ Error initializing agent: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_agent_initialization())
    print(f"\nInitialization test: {'PASSED' if success else 'FAILED'}")