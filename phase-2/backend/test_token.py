#!/usr/bin/env python3
"""Script to generate a test JWT token for the chatbot."""

import jwt
from datetime import datetime, timedelta
from app.core.config import settings
from uuid import uuid4

# Create a test user payload with a proper UUID
user_id = str(uuid4())
payload = {
    "sub": user_id,  # Better Auth uses 'sub' for user ID
    "userId": user_id,
    "email": "test@example.com",
    "name": "Test User",
    "iat": datetime.utcnow(),
    "exp": datetime.utcnow() + timedelta(hours=24)  # Token expires in 24 hours
}

# Encode the token using the same secret and algorithm as the app
token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

print(f"Generated test token: {token}")
print(f"User ID: {user_id}")
print(f"Use this token for testing the chat endpoint:")
print(f"curl -X POST http://localhost:8000/api/chat/ \\")
print(f'-H "Content-Type: application/json" \\')
print(f'-d \'{{"message": "hello"}}\' \\')
print(f'-H "Authorization: Bearer {token}"')