
import json
import time
import requests
from jose import jwt

# Settings from .env
JWT_SECRET = "Gidun9j+gA9F5uj7HIh2m2jalXqCJH357iqRZUJfAqg="
JWT_ALGORITHM = "HS256"
USER_ID = "user_test_123"
API_URL = "http://localhost:8000"

def generate_token(user_id):
    payload = {
        "sub": user_id,
        "exp": time.time() + 3600
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def test_create_task():
    token = generate_token(USER_ID)
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    task_data = {
        "title": "Test Task from CLI",
        "description": "This is a test task to verify the fix",
        "priority": "medium"
    }

    endpoint = f"{API_URL}/api/{USER_ID}/tasks"
    print(f"POST {endpoint}")

    response = requests.post(endpoint, headers=headers, json=task_data)

    print(f"Status Code: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)

    return response.status_code == 201

if __name__ == "__main__":
    test_create_task()
