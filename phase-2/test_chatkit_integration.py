"""Test script to verify ChatKit integration for Phase III AI Chatbot."""

import asyncio
import json
import httpx


async def test_chatkit_integration():
    """Test the ChatKit integration endpoints."""
    base_url = "http://localhost:8000"

    print("Testing ChatKit integration...")

    # Test 1: Create a ChatKit session
    print("\n1. Testing session creation...")
    try:
        # Note: This requires authentication, so we'll test the route exists
        async with httpx.AsyncClient() as client:
            # We'll check if the route exists by making a request without proper auth
            # This should return a 401 or 422 error, but if we get a 404, the route doesn't exist
            response = await client.post(f"{base_url}/api/chatkit/session")
            print(f"   Status: {response.status_code}")
            if response.status_code == 401:  # Unauthorized (expected)
                print("   ✓ Session endpoint exists (requires authentication)")
            elif response.status_code == 422:  # Validation error (also expected)
                print("   ✓ Session endpoint exists (validation error as expected)")
            else:
                print(f"   ⚠ Unexpected status: {response.status_code}")
    except Exception as e:
        print(f"   ✗ Error testing session endpoint: {e}")

    # Test 2: Check if the main chatkit endpoint exists
    print("\n2. Testing main ChatKit endpoint...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{base_url}/api/chatkit")
            print(f"   Status: {response.status_code}")
            if response.status_code in [401, 422]:
                print("   ✓ Main ChatKit endpoint exists")
            else:
                print(f"   ⚠ Unexpected status: {response.status_code}")
    except Exception as e:
        print(f"   ✗ Error testing main ChatKit endpoint: {e}")

    # Test 3: Check if refresh endpoint exists
    print("\n3. Testing refresh endpoint...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{base_url}/api/chatkit/refresh")
            print(f"   Status: {response.status_code}")
            if response.status_code in [401, 422]:
                print("   ✓ Refresh endpoint exists")
            else:
                print(f"   ⚠ Unexpected status: {response.status_code}")
    except Exception as e:
        print(f"   ✗ Error testing refresh endpoint: {e}")

    print("\n4. Testing if all required dependencies are installed...")
    try:
        import openai
        import better_auth
        from app.services.chatkit_service import ChatKitService
        from app.api.routes.chatkit import chatkit_service
        print("   ✓ All required dependencies are available")
    except ImportError as e:
        print(f"   ⚠ Missing dependency: {e}")

    print("\nIntegration test completed!")
    print("\nTo fully test the ChatKit integration:")
    print("1. Start the backend server: uvicorn app.main:app --reload --port 8000")
    print("2. Start the frontend: npm run dev")
    print("3. The ChatKit-powered chat interface should now be available in the dashboard")


if __name__ == "__main__":
    asyncio.run(test_chatkit_integration())