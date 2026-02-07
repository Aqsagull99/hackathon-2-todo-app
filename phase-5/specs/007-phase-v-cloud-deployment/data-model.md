# Data Model: Advanced Cloud Deployment of AI-Native Todo Chatbot

## Task Entity
```
Task {
  id: UUID (primary key)
  userId: string (foreign key to user)
  title: string (required, 1-200 chars)
  description: string (optional, max 1000 chars)
  status: enum ['pending', 'completed', 'archived']
  priority: enum ['low', 'medium', 'high']
  tags: string[] (optional, max 10 tags)
  dueDate: DateTime (optional)
  recurrencePattern: string (optional, cron-like)
  createdAt: DateTime
  updatedAt: DateTime
  completedAt: DateTime (optional)
}
```

## Event Entity
```
Event {
  id: UUID (primary key)
  eventType: enum ['created', 'updated', 'completed', 'deleted', 'reminder-triggered']
  taskId: UUID (foreign key to task)
  userId: string (user context)
  eventData: JSON (payload for processing)
  timestamp: DateTime
  processed: boolean
}
```

## Conversation Entity
```
Conversation {
  id: UUID (primary key)
  userId: string (foreign key to user)
  title: string (auto-generated or user-provided)
  createdAt: DateTime
  updatedAt: DateTime
}
```

## Message Entity
```
Message {
  id: UUID (primary key)
  conversationId: UUID (foreign key to conversation)
  userId: string (foreign key to user)
  role: enum ['user', 'assistant']
  content: string (message text)
  timestamp: DateTime
  metadata: JSON (processing info)
}
```

## User Entity
```
User {
  id: string (primary key, from auth system)
  email: string (unique)
  name: string (optional)
  preferences: JSON (user settings)
  createdAt: DateTime
  updatedAt: DateTime
}
```