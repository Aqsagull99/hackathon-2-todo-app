# Todo App Backend API

This is the backend API for the Todo application, built with FastAPI. It provides REST endpoints for managing tasks, users, and conversations with AI chatbot functionality.

## Features

- **Task Management**: Create, read, update, and delete tasks
- **User Authentication**: JWT-based authentication
- **AI Chatbot**: Natural language interface for task management
- **Tagging System**: Organize tasks with customizable tags
- **Task Priorities**: Set high, medium, or low priority levels
- **Due Dates & Reminders**: Schedule tasks and receive notifications

## API Endpoints

### Chat Endpoints

#### POST `/api/chat`

Send a message to the AI chatbot and receive a response.

**Headers:**
```
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

**Request Body:**
```json
{
  "conversation_id": "string (optional, UUID)",
  "message": "string (required, 1-1000 characters)"
}
```

**Example Request:**
```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Add a task to buy groceries"
  }'
```

**Response:**
```json
{
  "conversation_id": "string (UUID)",
  "response": "string (chatbot response)",
  "tool_calls": [
    {
      "tool": "string (tool name)",
      "parameters": "object (tool parameters)",
      "result": "object (tool result)"
    }
  ]
}
```

**Example Response:**
```json
{
  "conversation_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "response": "I've added the task 'buy groceries' for you.",
  "tool_calls": [
    {
      "tool": "add_task",
      "parameters": {
        "user_id": "user123",
        "title": "buy groceries",
        "priority": "medium"
      },
      "result": {
        "task_id": 123,
        "status": "created",
        "title": "buy groceries"
      }
    }
  ]
}
```

#### GET `/api/conversations`

Get a list of user's conversations.

**Headers:**
```
Authorization: Bearer {jwt_token}
```

**Response:**
```json
{
  "conversations": [
    {
      "conversation_id": "string (UUID)",
      "created_at": "string (ISO date)",
      "last_message": "string"
    }
  ]
}
```

#### GET `/api/conversations/{conversation_id}/messages`

Get the message history for a specific conversation.

**Headers:**
```
Authorization: Bearer {jwt_token}
```

**Response:**
```json
{
  "messages": [
    {
      "message_id": "string (UUID)",
      "role": "string ('user' or 'assistant')",
      "content": "string (message content)",
      "created_at": "string (ISO date)",
      "tool_calls": "object (optional, tool call details)"
    }
  ]
}
```

### Task Endpoints

#### GET `/api/{user_id}/tasks`

Get all tasks for a user.

**Headers:**
```
Authorization: Bearer {jwt_token}
```

#### POST `/api/{user_id}/tasks`

Create a new task.

**Headers:**
```
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

**Request Body:**
```json
{
  "title": "string (required)",
  "description": "string (optional)",
  "priority": "string ('high'|'medium'|'low', default: 'medium')",
  "due_date": "string (optional, ISO date)",
  "tag_ids": "array of integers (optional)"
}
```

#### PUT `/api/{user_id}/tasks/{id}`

Update a task.

#### DELETE `/api/{user_id}/tasks/{id}`

Delete a task.

#### PATCH `/api/{user_id}/tasks/{id}/complete`

Toggle task completion status.

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```bash
# Database
DATABASE_URL="postgresql+asyncpg://user:password@localhost/dbname"

# JWT Authentication
JWT_SECRET="your-super-secret-jwt-key"
JWT_ALGORITHM="HS256"

# OpenRouter (for AI chatbot)
OPENROUTER_API_KEY="your-openrouter-api-key"
OPENROUTER_BASE_URL="https://openrouter.ai/api/v1"
OPENROUTER_MODEL="mistralai/mistral-7b-instruct:free"

# Server
BACKEND_PORT=8000
FRONTEND_URL="http://localhost:3000"
```

## Running the Application

1. Install dependencies:
```bash
pip install -e .
```

2. Set up environment variables (see above)

3. Run the application:
```bash
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`.

## Database Migrations

Apply database migrations:
```bash
alembic upgrade head
```

Create a new migration:
```bash
alembic revision --autogenerate -m "Description of changes"
```

## License

MIT