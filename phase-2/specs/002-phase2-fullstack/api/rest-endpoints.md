# API Specification: REST Endpoints

**Spec ID**: 002-phase2-fullstack/api/rest-endpoints
**Version**: 1.0.0
**Status**: Draft
**Created**: 2025-12-29

---

## Base URL

```
Development: http://localhost:8000
Production:  https://api.your-domain.com
```

## Authentication

All endpoints require JWT authentication unless otherwise specified.

**Header Format:**
```
Authorization: Bearer <jwt_token>
```

## Common Headers

### Request Headers

| Header | Required | Description |
|--------|----------|-------------|
| `Authorization` | Yes | JWT bearer token |
| `Content-Type` | Yes* | `application/json` for POST/PUT |

### Response Headers

| Header | Description |
|--------|-------------|
| `Content-Type` | `application/json` |
| `X-Request-ID` | Unique request identifier |

---

## Endpoints Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/{user_id}/tasks` | List all tasks |
| POST | `/api/{user_id}/tasks` | Create new task |
| GET | `/api/{user_id}/tasks/{id}` | Get task by ID |
| PUT | `/api/{user_id}/tasks/{id}` | Update task |
| DELETE | `/api/{user_id}/tasks/{id}` | Delete task |
| PATCH | `/api/{user_id}/tasks/{id}/complete` | Toggle completion |
| GET | `/health` | Health check (no auth) |

---

## Endpoint Details

### 1. List Tasks

**GET** `/api/{user_id}/tasks`

Retrieve all tasks for the authenticated user.

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `user_id` | string | Yes | User's unique identifier |

#### Query Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `completed` | boolean | No | - | Filter by completion status |
| `skip` | integer | No | 0 | Number of records to skip |
| `limit` | integer | No | 10 | Max number of records to return |
| `sort` | string | No | `created_at` | Sort field |
| `order` | string | No | `desc` | Sort order (asc/desc) |

#### Response

**200 OK**
```json
[
  {
    "id": 1,
    "user_id": "user_abc123",
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false,
    "created_at": "2025-12-29T10:00:00Z",
    "updated_at": "2025-12-29T10:00:00Z"
  },
  {
    "id": 2,
    "user_id": "user_abc123",
    "title": "Walk the dog",
    "description": null,
    "completed": true,
    "created_at": "2025-12-29T09:00:00Z",
    "updated_at": "2025-12-29T11:00:00Z"
  }
]
```

**Empty List (200 OK)**
```json
[]
```

#### Errors

| Status | Description | Response |
|--------|-------------|----------|
| 401 | Not authenticated | `{"detail": "Not authenticated"}` |
| 403 | Access denied | `{"detail": "Access denied"}` |

#### Example

```bash
curl -X GET "http://localhost:8000/api/user_abc123/tasks" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..."
```

---

### 2. Create Task

**POST** `/api/{user_id}/tasks`

Create a new task for the authenticated user.

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `user_id` | string | Yes | User's unique identifier |

#### Request Body

```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `title` | string | Yes | 1-255 characters |
| `description` | string | No | Max 1000 characters |

#### Response

**201 Created**
```json
{
  "id": 3,
  "user_id": "user_abc123",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2025-12-29T12:00:00Z",
  "updated_at": "2025-12-29T12:00:00Z"
}
```

#### Errors

| Status | Description | Response |
|--------|-------------|----------|
| 400 | Validation error | `{"detail": "Title is required"}` |
| 401 | Not authenticated | `{"detail": "Not authenticated"}` |
| 403 | Access denied | `{"detail": "Access denied"}` |

#### Example

```bash
curl -X POST "http://localhost:8000/api/user_abc123/tasks" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..." \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries", "description": "Milk, eggs, bread"}'
```

---

### 3. Get Task

**GET** `/api/{user_id}/tasks/{id}`

Retrieve a specific task by ID.

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `user_id` | string | Yes | User's unique identifier |
| `id` | integer | Yes | Task ID |

#### Response

**200 OK**
```json
{
  "id": 1,
  "user_id": "user_abc123",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2025-12-29T10:00:00Z",
  "updated_at": "2025-12-29T10:00:00Z"
}
```

#### Errors

| Status | Description | Response |
|--------|-------------|----------|
| 401 | Not authenticated | `{"detail": "Not authenticated"}` |
| 403 | Access denied | `{"detail": "Access denied"}` |
| 404 | Task not found | `{"detail": "Task not found"}` |

#### Example

```bash
curl -X GET "http://localhost:8000/api/user_abc123/tasks/1" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..."
```

---

### 4. Update Task

**PUT** `/api/{user_id}/tasks/{id}`

Update an existing task's title and/or description.

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `user_id` | string | Yes | User's unique identifier |
| `id` | integer | Yes | Task ID |

#### Request Body

```json
{
  "title": "Buy groceries (updated)",
  "description": "Milk, eggs, bread, cheese"
}
```

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `title` | string | No | 1-255 characters if provided |
| `description` | string | No | Max 1000 characters |

#### Response

**200 OK**
```json
{
  "id": 1,
  "user_id": "user_abc123",
  "title": "Buy groceries (updated)",
  "description": "Milk, eggs, bread, cheese",
  "completed": false,
  "created_at": "2025-12-29T10:00:00Z",
  "updated_at": "2025-12-29T14:00:00Z"
}
```

#### Errors

| Status | Description | Response |
|--------|-------------|----------|
| 400 | Validation error | `{"detail": "Title cannot be empty"}` |
| 401 | Not authenticated | `{"detail": "Not authenticated"}` |
| 403 | Access denied | `{"detail": "Access denied"}` |
| 404 | Task not found | `{"detail": "Task not found"}` |

#### Example

```bash
curl -X PUT "http://localhost:8000/api/user_abc123/tasks/1" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..." \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries (updated)"}'
```

---

### 5. Delete Task

**DELETE** `/api/{user_id}/tasks/{id}`

Permanently delete a task.

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `user_id` | string | Yes | User's unique identifier |
| `id` | integer | Yes | Task ID |

#### Response

**204 No Content**
```
(Empty response body)
```

#### Errors

| Status | Description | Response |
|--------|-------------|----------|
| 401 | Not authenticated | `{"detail": "Not authenticated"}` |
| 403 | Access denied | `{"detail": "Access denied"}` |
| 404 | Task not found | `{"detail": "Task not found"}` |

#### Example

```bash
curl -X DELETE "http://localhost:8000/api/user_abc123/tasks/1" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..."
```

---

### 6. Toggle Completion

**PATCH** `/api/{user_id}/tasks/{id}/complete`

Toggle the completion status of a task.

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `user_id` | string | Yes | User's unique identifier |
| `id` | integer | Yes | Task ID |

#### Response

**200 OK**
```json
{
  "id": 1,
  "user_id": "user_abc123",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": true,
  "created_at": "2025-12-29T10:00:00Z",
  "updated_at": "2025-12-29T15:00:00Z"
}
```

#### Errors

| Status | Description | Response |
|--------|-------------|----------|
| 401 | Not authenticated | `{"detail": "Not authenticated"}` |
| 403 | Access denied | `{"detail": "Access denied"}` |
| 404 | Task not found | `{"detail": "Task not found"}` |

#### Example

```bash
curl -X PATCH "http://localhost:8000/api/user_abc123/tasks/1/complete" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..."
```

---

### 7. Health Check

**GET** `/health`

Check API server health status. **No authentication required.**

#### Response

**200 OK**
```json
{
  "status": "healthy",
  "timestamp": "2025-12-29T12:00:00Z",
  "version": "1.0.0"
}
```

#### Example

```bash
curl -X GET "http://localhost:8000/health"
```

---

## Error Response Format

All error responses follow this format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

### HTTP Status Codes

| Code | Description | When Used |
|------|-------------|-----------|
| 200 | OK | Successful GET, PUT, PATCH |
| 201 | Created | Successful POST |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Validation errors |
| 401 | Unauthorized | Missing/invalid JWT |
| 403 | Forbidden | User ID mismatch |
| 404 | Not Found | Resource doesn't exist |
| 500 | Internal Server Error | Unexpected server error |

---

## Rate Limiting (Future)

| Endpoint | Limit |
|----------|-------|
| All endpoints | 100 requests/minute per user |

---

## OpenAPI Schema

The API provides an OpenAPI 3.0 schema at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **JSON Schema**: `http://localhost:8000/openapi.json`

---

**Previous**: [../features/authentication.md](../features/authentication.md)
**Next**: [../database/schema.md](../database/schema.md)
