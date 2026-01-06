#!/usr/bin/env python3
"""
Test script to check the API endpoints and try creating extended tasks
"""

import requests
import json

def test_api_endpoints():
    print("Testing API endpoints...")

    # Check the API root
    try:
        response = requests.get("http://localhost:8000/")
        print(f"API Root: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Error accessing API root: {e}")

    # Check the API docs to see available endpoints
    print("\nCheck http://localhost:8000/docs for available endpoints")

    # Try to create a basic task first (this might be what the frontend is using)
    # This requires a proper JWT token, but we can check the response
    basic_task_data = {
        "title": "Test Basic Task",
        "description": "This is a basic task"
    }

    # Try with the basic endpoint (with user_id in path)
    user_id = "tLBRNC9Fh5yhPwE18oYSJAlZSpxSOfAm"  # Use an existing user ID
    try:
        response = requests.post(
            f"http://localhost:8000/api/{user_id}/tasks",
            json=basic_task_data,
            headers={"Authorization": "Bearer dummy_token"}
        )
        print(f"Basic task endpoint response: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error with basic task endpoint: {e}")

    # Try with the extended endpoint (without user_id in path)
    extended_task_data = {
        "title": "Test Extended Task",
        "description": "This is an extended task",
        "priority": "high",
        "tag_ids": []
    }

    try:
        response = requests.post(
            "http://localhost:8000/api/tasks",
            json=extended_task_data,
            headers={"Authorization": "Bearer dummy_token"}
        )
        print(f"Extended task endpoint response: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error with extended task endpoint: {e}")

if __name__ == "__main__":
    test_api_endpoints()