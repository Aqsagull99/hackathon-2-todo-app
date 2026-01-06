#!/usr/bin/env python3
"""
Test script to verify that extended task creation works with the backend
"""

import asyncio
import httpx
import json
from datetime import datetime, timedelta

async def test_extended_task_creation():
    print("Testing extended task creation...")

    # Use one of the existing user IDs from the database
    user_id = "tLBRNC9Fh5yhPwE18oYSJAlZSpxSOfAm"

    # Create a proper JWT token for testing (this would normally come from the frontend)
    # For now, we'll test with a dummy token to see if the endpoint structure is correct
    extended_task_data = {
        "title": "Test Extended Task with All Features",
        "description": "This task has all extended features enabled",
        "priority": "high",
        "due_date": (datetime.now() + timedelta(days=2)).isoformat(),
        "due_date_tz": "UTC",
        "recurrence_pattern": "daily",
        "tag_ids": []  # Will be empty for now
    }

    print(f"Creating extended task with data: {json.dumps(extended_task_data, indent=2)}")

    async with httpx.AsyncClient() as client:
        try:
            # Try creating with the extended endpoint
            response = await client.post(
                "http://localhost:8000/api/tasks",
                json=extended_task_data,
                headers={"Authorization": "Bearer dummy_token_for_test"}
            )
            print(f"Extended endpoint response: {response.status_code}")
            print(f"Response: {response.text}")
        except Exception as e:
            print(f"Error with extended endpoint: {e}")

    # Also test the basic endpoint for comparison
    basic_task_data = {
        "title": "Test Basic Task",
        "description": "Basic task description"
    }

    print(f"\nCreating basic task with data: {basic_task_data}")

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"http://localhost:8000/api/{user_id}/tasks",
                json=basic_task_data,
                headers={"Authorization": "Bearer dummy_token_for_test"}
            )
            print(f"Basic endpoint response: {response.status_code}")
            print(f"Response: {response.text}")
        except Exception as e:
            print(f"Error with basic endpoint: {e}")

if __name__ == "__main__":
    asyncio.run(test_extended_task_creation())