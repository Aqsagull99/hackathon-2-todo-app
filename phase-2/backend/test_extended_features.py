#!/usr/bin/env python3
"""
Test script to create a task with extended features (tags, reminders)
"""

import asyncio
import httpx
from datetime import datetime, timedelta

# Test creating a task with extended features
async def test_extended_task_creation():
    # Replace with your actual user ID from the existing tasks
    user_id = "tLBRNC9Fh5yhPwE18oYSJAlZSpxSOfAm"  # Using one of the existing user IDs

    # Create a test tag first
    print("Creating a test tag...")
    async with httpx.AsyncClient() as client:
        # This would require authentication, but we'll test the API structure
        # For now, let's just test the structure of the API call

        # Create a tag
        tag_data = {
            "name": "test-tag",
            "color": "#FF5733"
        }

        # This would need a proper JWT token, so we'll just check the route exists
        print(f"Would create tag with data: {tag_data}")

        # Now create a task with extended features
        task_data = {
            "title": "Test Task with Extended Features",
            "description": "This is a test task with tags and reminders",
            "priority": "high",
            "due_date": (datetime.now() + timedelta(days=1)).isoformat(),
            "due_date_tz": "UTC",
            "recurrence_pattern": "daily",
            "tag_ids": []  # Would add tag IDs here if we had them
        }

        print(f"Would create task with data: {task_data}")

        # Make the request to the extended tasks endpoint
        try:
            # We'll use a dummy token since we're just testing if the endpoint exists
            response = await client.post(
                f"http://localhost:8000/api/tasks",
                json=task_data,
                headers={"Authorization": "Bearer dummy_token_for_test"}
            )
            print(f"Response status: {response.status_code}")
            print(f"Response: {response.json()}")
        except Exception as e:
            print(f"Error making request: {e}")

if __name__ == "__main__":
    asyncio.run(test_extended_task_creation())