# Feature Specification: Task CRUD Operations

**Spec ID**: 002-phase2-fullstack/features/task-crud
**Version**: 1.0.0
**Status**: Draft
**Created**: 2025-12-29

---

## Overview

This specification defines the five core task management operations for the Todo application. Each operation must enforce user isolation through JWT authentication.

## Feature Summary

| # | Feature | Operation | Endpoint |
|---|---------|-----------|----------|
| 1 | Add Todo | CREATE | POST `/api/{user_id}/tasks` |
| 2 | View Todos | READ (list) | GET `/api/{user_id}/tasks` |
| 3 | View Single | READ (single) | GET `/api/{user_id}/tasks/{id}` |
| 4 | Update Todo | UPDATE | PUT `/api/{user_id}/tasks/{id}` |
| 5 | Delete Todo | DELETE | DELETE `/api/{user_id}/tasks/{id}` |
| 6 | Mark Complete | PATCH | PATCH `/api/{user_id}/tasks/{id}/complete` |

---

## Feature 1: Add Todo (CREATE)

### Description
Create a new task for the authenticated user and persist it to the database.

### User Story
> As a logged-in user, I want to add a new task so that I can track my work.

### Acceptance Criteria

- [ ] User must be authenticated (valid JWT)
- [ ] Task title is required (non-empty string)
- [ ] Task description is optional
- [ ] Task created with `completed = false` by default
- [ ] Task assigned to authenticated user's `user_id`
- [ ] Timestamps (`created_at`, `updated_at`) auto-generated
- [ ] Returns created task with generated `id`
- [ ] Returns 201 Created on success

### Request/Response

**Request:**
```http
POST /api/{user_id}/tasks
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

**Success Response (201):**
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

**Error Responses:**

| Status | Condition | Response |
|--------|-----------|----------|
| 400 | Empty title | `{"detail": "Title is required"}` |
| 401 | No/invalid JWT | `{"detail": "Not authenticated"}` |
| 403 | Wrong user_id | `{"detail": "Access denied"}` |

### Test Cases

```gherkin
Feature: Add Todo

  Scenario: Successfully create a task
    Given I am logged in as "user_abc123"
    When I POST to "/api/user_abc123/tasks" with {"title": "Test task"}
    Then I receive status 201
    And the response contains "id" and "created_at"
    And "completed" is false

  Scenario: Fail to create task without title
    Given I am logged in as "user_abc123"
    When I POST to "/api/user_abc123/tasks" with {"title": ""}
    Then I receive status 400
    And the response contains "Title is required"

  Scenario: Fail to create task without authentication
    When I POST to "/api/user_abc123/tasks" without JWT
    Then I receive status 401

  Scenario: Fail to create task for different user
    Given I am logged in as "user_xyz789"
    When I POST to "/api/user_abc123/tasks" with {"title": "Test"}
    Then I receive status 403
```

---

## Feature 2: View Todos (READ - List)

### Description
Retrieve all tasks belonging to the authenticated user.

### User Story
> As a logged-in user, I want to see all my tasks so that I can manage my work.

### Acceptance Criteria

- [ ] User must be authenticated (valid JWT)
- [ ] Returns only tasks where `user_id` matches authenticated user
- [ ] Returns empty array if no tasks exist
- [ ] Tasks ordered by `created_at` descending (newest first)
- [ ] Returns 200 OK on success

### Request/Response

**Request:**
```http
GET /api/{user_id}/tasks
Authorization: Bearer <jwt_token>
```

**Success Response (200):**
```json
[
  {
    "id": 2,
    "user_id": "user_abc123",
    "title": "Walk the dog",
    "description": null,
    "completed": true,
    "created_at": "2025-12-29T11:00:00Z",
    "updated_at": "2025-12-29T12:00:00Z"
  },
  {
    "id": 1,
    "user_id": "user_abc123",
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false,
    "created_at": "2025-12-29T10:00:00Z",
    "updated_at": "2025-12-29T10:00:00Z"
  }
]
```

**Empty Response (200):**
```json
[]
```

### Test Cases

```gherkin
Feature: View Todos

  Scenario: Successfully list all tasks
    Given I am logged in as "user_abc123"
    And I have 3 tasks in the database
    When I GET "/api/user_abc123/tasks"
    Then I receive status 200
    And the response contains 3 tasks
    And all tasks have user_id "user_abc123"

  Scenario: List tasks returns empty for new user
    Given I am logged in as "new_user"
    And I have no tasks
    When I GET "/api/new_user/tasks"
    Then I receive status 200
    And the response is an empty array

  Scenario: Cannot view other user's tasks
    Given I am logged in as "user_xyz789"
    When I GET "/api/user_abc123/tasks"
    Then I receive status 403
```

---

## Feature 3: View Single Todo (READ - Single)

### Description
Retrieve a specific task by ID for the authenticated user.

### User Story
> As a logged-in user, I want to view details of a specific task.

### Acceptance Criteria

- [ ] User must be authenticated (valid JWT)
- [ ] Task must belong to authenticated user
- [ ] Returns 404 if task doesn't exist
- [ ] Returns 403 if task belongs to different user
- [ ] Returns 200 OK with task data on success

### Request/Response

**Request:**
```http
GET /api/{user_id}/tasks/{id}
Authorization: Bearer <jwt_token>
```

**Success Response (200):**
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

### Test Cases

```gherkin
Feature: View Single Todo

  Scenario: Successfully get task by ID
    Given I am logged in as "user_abc123"
    And task with id 1 exists for "user_abc123"
    When I GET "/api/user_abc123/tasks/1"
    Then I receive status 200
    And the response contains task with id 1

  Scenario: Task not found
    Given I am logged in as "user_abc123"
    When I GET "/api/user_abc123/tasks/999"
    Then I receive status 404

  Scenario: Cannot access other user's task
    Given I am logged in as "user_xyz789"
    And task with id 1 exists for "user_abc123"
    When I GET "/api/user_abc123/tasks/1"
    Then I receive status 403
```

---

## Feature 4: Update Todo (UPDATE)

### Description
Modify an existing task's title and/or description.

### User Story
> As a logged-in user, I want to update my task details so that I can correct or improve them.

### Acceptance Criteria

- [ ] User must be authenticated (valid JWT)
- [ ] Task must belong to authenticated user
- [ ] Can update title, description, or both
- [ ] Title cannot be empty if provided
- [ ] `updated_at` timestamp updated on change
- [ ] Returns updated task data
- [ ] Returns 200 OK on success

### Request/Response

**Request:**
```http
PUT /api/{user_id}/tasks/{id}
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "title": "Buy groceries (updated)",
  "description": "Milk, eggs, bread, cheese"
}
```

**Success Response (200):**
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

### Test Cases

```gherkin
Feature: Update Todo

  Scenario: Successfully update task
    Given I am logged in as "user_abc123"
    And task with id 1 exists for "user_abc123"
    When I PUT "/api/user_abc123/tasks/1" with {"title": "New title"}
    Then I receive status 200
    And the response contains "New title"
    And "updated_at" is updated

  Scenario: Partial update (description only)
    Given I am logged in as "user_abc123"
    And task with id 1 exists for "user_abc123"
    When I PUT "/api/user_abc123/tasks/1" with {"description": "New desc"}
    Then I receive status 200
    And the title remains unchanged

  Scenario: Cannot update with empty title
    Given I am logged in as "user_abc123"
    When I PUT "/api/user_abc123/tasks/1" with {"title": ""}
    Then I receive status 400
```

---

## Feature 5: Delete Todo (DELETE)

### Description
Permanently remove a task from the database.

### User Story
> As a logged-in user, I want to delete a task so that I can remove completed or unwanted items.

### Acceptance Criteria

- [ ] User must be authenticated (valid JWT)
- [ ] Task must belong to authenticated user
- [ ] Task permanently deleted from database
- [ ] Returns 204 No Content on success
- [ ] Returns 404 if task doesn't exist
- [ ] Returns 403 if task belongs to different user

### Request/Response

**Request:**
```http
DELETE /api/{user_id}/tasks/{id}
Authorization: Bearer <jwt_token>
```

**Success Response (204):**
```
(No content)
```

### Test Cases

```gherkin
Feature: Delete Todo

  Scenario: Successfully delete task
    Given I am logged in as "user_abc123"
    And task with id 1 exists for "user_abc123"
    When I DELETE "/api/user_abc123/tasks/1"
    Then I receive status 204
    And task with id 1 no longer exists

  Scenario: Cannot delete non-existent task
    Given I am logged in as "user_abc123"
    When I DELETE "/api/user_abc123/tasks/999"
    Then I receive status 404

  Scenario: Cannot delete other user's task
    Given I am logged in as "user_xyz789"
    And task with id 1 exists for "user_abc123"
    When I DELETE "/api/user_abc123/tasks/1"
    Then I receive status 403
```

---

## Feature 6: Mark Complete (TOGGLE)

### Description
Toggle the completion status of a task.

### User Story
> As a logged-in user, I want to mark a task as complete or incomplete so that I can track my progress.

### Acceptance Criteria

- [ ] User must be authenticated (valid JWT)
- [ ] Task must belong to authenticated user
- [ ] Toggles `completed` boolean (true ↔ false)
- [ ] Updates `updated_at` timestamp
- [ ] Returns updated task data
- [ ] Returns 200 OK on success

### Request/Response

**Request:**
```http
PATCH /api/{user_id}/tasks/{id}/complete
Authorization: Bearer <jwt_token>
```

**Success Response (200):**
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

### Test Cases

```gherkin
Feature: Mark Complete

  Scenario: Toggle incomplete to complete
    Given I am logged in as "user_abc123"
    And task with id 1 has completed=false
    When I PATCH "/api/user_abc123/tasks/1/complete"
    Then I receive status 200
    And "completed" is true

  Scenario: Toggle complete to incomplete
    Given I am logged in as "user_abc123"
    And task with id 1 has completed=true
    When I PATCH "/api/user_abc123/tasks/1/complete"
    Then I receive status 200
    And "completed" is false

  Scenario: Cannot toggle other user's task
    Given I am logged in as "user_xyz789"
    And task with id 1 exists for "user_abc123"
    When I PATCH "/api/user_abc123/tasks/1/complete"
    Then I receive status 403
```

---

## Security Requirements (All Features)

### Authentication Check
Every endpoint must:
1. Extract JWT from `Authorization: Bearer <token>` header
2. Verify JWT signature using `JWT_SECRET`
3. Check JWT expiration
4. Extract `user_id` from JWT payload (`sub` claim)

### Authorization Check
Every endpoint must:
1. Compare JWT `user_id` with URL `{user_id}` parameter
2. Return 403 Forbidden if mismatch
3. Filter database queries by `user_id`

### Common Error Responses

| Status | Condition | Response |
|--------|-----------|----------|
| 400 | Invalid request body | `{"detail": "Validation error message"}` |
| 401 | Missing/invalid JWT | `{"detail": "Not authenticated"}` |
| 403 | Wrong user_id | `{"detail": "Access denied"}` |
| 404 | Resource not found | `{"detail": "Task not found"}` |
| 500 | Server error | `{"detail": "Internal server error"}` |

---

**Previous**: [../architecture.md](../architecture.md)
**Next**: [authentication.md](./authentication.md)
