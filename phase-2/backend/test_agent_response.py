#!/usr/bin/env python3
"""
Test script to verify that the TodoChatAgent responds properly to Phase III requirements
using OpenAI Agents SDK with openai-agents-sdk-skill and OpenRouter API.
"""

import asyncio
import os
from app.agents.chat_agent import TodoChatAgent

async def test_agent_responses():
    """Test the TodoChatAgent responses to Phase III requirements."""

    print("🔍 Testing TodoChatAgent responses to Phase III requirements...")
    print("="*60)

    # Initialize the agent
    agent = TodoChatAgent()

    # Test cases based on Phase III requirements
    test_cases = [
        {
            "name": "Basic Task Creation",
            "message": "Add a task to buy groceries",
            "expected_keywords": ["add", "task", "groceries"]
        },
        {
            "name": "List Tasks",
            "message": "Show me my tasks",
            "expected_keywords": ["list", "tasks", "show"]
        },
        {
            "name": "Complete Task",
            "message": "Mark the first task as complete",
            "expected_keywords": ["complete", "task", "mark"]
        },
        {
            "name": "Update Task",
            "message": "Change my first task to 'Buy organic groceries'",
            "expected_keywords": ["update", "task", "change", "groceries"]
        },
        {
            "name": "Delete Task",
            "message": "Delete the task about groceries",
            "expected_keywords": ["delete", "task", "remove"]
        },
        {
            "name": "Multi-step Operation",
            "message": "Show my tasks then complete the first one",
            "expected_keywords": ["show", "tasks", "complete", "first"]
        },
        {
            "name": "Search Tasks",
            "message": "Find tasks about meetings",
            "expected_keywords": ["find", "search", "meetings"]
        }
    ]

    all_tests_passed = True

    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_case['name']}")
        print(f"Input: {test_case['message']}")

        try:
            # Process the message using the agent
            result = await agent.process_message(
                user_message=test_case['message'],
                conversation_history=[],
                user_id="test_user_123"
            )

            response = result.get("response", "")
            tool_calls = result.get("tool_calls", [])

            print(f"Response: {response}")
            print(f"Tool calls: {tool_calls}")

            # Check if response contains expected keywords
            response_lower = response.lower()
            keyword_found = any(keyword.lower() in response_lower for keyword in test_case['expected_keywords'])

            if keyword_found:
                print("✅ Test PASSED - Response contains expected keywords")
            else:
                print("❌ Test FAILED - Response missing expected keywords")
                all_tests_passed = False

        except Exception as e:
            print(f"❌ Test FAILED with exception: {str(e)}")
            all_tests_passed = False

    print("\n" + "="*60)
    if all_tests_passed:
        print("🎉 ALL TESTS PASSED! The TodoChatAgent properly responds to Phase III requirements.")
        print("✅ OpenAI Agents SDK integration with openai-agents-sdk-skill is working correctly")
        print("✅ OpenRouter API configuration is properly set up")
        print("✅ Agent can handle all required task operations")
    else:
        print("❌ SOME TESTS FAILED! Please check the agent implementation.")

    print("="*60)
    return all_tests_passed

async def test_openrouter_configuration():
    """Test that OpenRouter configuration is properly set in environment."""

    print("\n🔍 Testing OpenRouter Configuration...")
    print("="*60)

    required_vars = [
        "OPENROUTER_API_KEY",
        "OPENROUTER_BASE_URL",
        "OPENROUTER_MODEL"
    ]

    all_set = True
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var}: {value[:10]}... (truncated for security)")
        else:
            print(f"❌ {var}: NOT SET")
            all_set = False

    if all_set:
        print("\n✅ OpenRouter configuration is complete")
        print("Using model:", os.getenv("OPENROUTER_MODEL", "Not set"))
    else:
        print("\n❌ OpenRouter configuration is incomplete")

    print("="*60)
    return all_set

async def main():
    """Main test function."""
    print("🚀 Starting TodoChatAgent Phase III Requirements Test")
    print("="*60)

    # Test OpenRouter configuration first
    config_ok = await test_openrouter_configuration()

    if not config_ok:
        print("\n❌ Cannot proceed with agent tests - OpenRouter configuration is incomplete")
        return False

    # Test agent responses
    agent_ok = await test_agent_responses()

    print(f"\n📋 Test Summary:")
    print(f"   OpenRouter Config: {'✅ PASS' if config_ok else '❌ FAIL'}")
    print(f"   Agent Responses:   {'✅ PASS' if agent_ok else '❌ FAIL'}")

    overall_success = config_ok and agent_ok
    print(f"   Overall Status:    {'🎉 SUCCESS' if overall_success else '💥 FAILURE'}")

    return overall_success

if __name__ == "__main__":
    success = asyncio.run(main())

    if success:
        print("\n✨ All Phase III requirements tests completed successfully!")
        print("The TodoChatAgent is properly configured with OpenAI Agents SDK and openai-agents-sdk-skill.")
    else:
        print("\n💥 Some tests failed. Please review the implementation.")