# Data Model: UI Props & State

## Frontend Entities

### TaskItem (UI State)
| Attribute | Type | Description |
|-----------|------|-------------|
| id        | number | Unique identifier |
| title     | string | Task heading |
| description| string | Optional details |
| priority  | 'Low' \| 'Medium' \| 'High' | Visual badge mapping |
| isCompleted| boolean | Checkbox state |
| dueDate   | string (ISO) | Formatted display |

### UserSession
| Attribute | Type | Description |
|-----------|------|-------------|
| userId    | string | Auth ID |
| fullName  | string | Display name |
| avatarUrl | string | Profile image placeholder |

## Relationships
- **DashboardState** contains an array of **TaskItems**.
- **UserSession** controls access to primary dashboard views.
