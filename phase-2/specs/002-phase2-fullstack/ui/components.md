# UI Specification: Components

**Spec ID**: 002-phase2-fullstack/ui/components
**Version**: 1.0.0
**Status**: Draft
**Created**: 2025-12-29

---

## Component Architecture

```
frontend/src/components/
├── auth/
│   ├── LoginForm.tsx
│   ├── RegisterForm.tsx
│   └── LogoutButton.tsx
├── tasks/
│   ├── TaskList.tsx
│   ├── TaskItem.tsx
│   ├── TaskForm.tsx
│   ├── TaskActions.tsx
│   └── EmptyState.tsx
├── ui/
│   ├── Button.tsx
│   ├── Input.tsx
│   ├── Modal.tsx
│   ├── LoadingSpinner.tsx
│   └── Alert.tsx
└── layout/
    ├── Header.tsx
    ├── Footer.tsx
    └── Container.tsx
```

---

## Authentication Components

### LoginForm

**Purpose**: Handle user login with email and password.

```
┌────────────────────────────────────────────┐
│            Welcome back                     │
│                                            │
│  ┌──────────────────────────────────────┐  │
│  │ Email                                │  │
│  │ user@example.com                     │  │
│  └──────────────────────────────────────┘  │
│                                            │
│  ┌──────────────────────────────────────┐  │
│  │ Password                             │  │
│  │ ••••••••                             │  │
│  └──────────────────────────────────────┘  │
│                                            │
│  [Error message appears here if any]       │
│                                            │
│  ┌──────────────────────────────────────┐  │
│  │           Sign In                    │  │
│  └──────────────────────────────────────┘  │
│                                            │
│  Don't have an account? Register           │
└────────────────────────────────────────────┘
```

**Props**:
```typescript
interface LoginFormProps {
  onSuccess?: () => void;
  onError?: (error: string) => void;
}
```

**States**:
- `email`: string
- `password`: string
- `isLoading`: boolean
- `error`: string | null

**Behavior**:
- Validates email format
- Shows loading spinner during submit
- Displays error messages
- Redirects to dashboard on success

---

### RegisterForm

**Purpose**: Handle new user registration.

```
┌────────────────────────────────────────────┐
│         Create your account                 │
│                                            │
│  ┌──────────────────────────────────────┐  │
│  │ Email                                │  │
│  │ user@example.com                     │  │
│  └──────────────────────────────────────┘  │
│                                            │
│  ┌──────────────────────────────────────┐  │
│  │ Password                             │  │
│  │ ••••••••                             │  │
│  └──────────────────────────────────────┘  │
│                                            │
│  ┌──────────────────────────────────────┐  │
│  │ Confirm Password                     │  │
│  │ ••••••••                             │  │
│  └──────────────────────────────────────┘  │
│                                            │
│  [Error message appears here if any]       │
│                                            │
│  ┌──────────────────────────────────────┐  │
│  │        Create Account                │  │
│  └──────────────────────────────────────┘  │
│                                            │
│  Already have an account? Login            │
└────────────────────────────────────────────┘
```

**Props**:
```typescript
interface RegisterFormProps {
  onSuccess?: () => void;
  onError?: (error: string) => void;
}
```

**Validations**:
- Email: valid format
- Password: minimum 8 characters
- Confirm: must match password

---

### LogoutButton

**Purpose**: Sign out user and clear session.

```
┌────────────────┐
│    Logout      │
└────────────────┘
```

**Props**:
```typescript
interface LogoutButtonProps {
  variant?: 'primary' | 'ghost' | 'danger';
  onLogout?: () => void;
}
```

---

## Task Components

### TaskList

**Purpose**: Display list of tasks with filtering options.

```
┌──────────────────────────────────────────────────────────┐
│  ┌──────────────────────────────────────────────────┐    │
│  │ Filter: [All ▼]  Sort: [Newest ▼]               │    │
│  └──────────────────────────────────────────────────┘    │
│                                                          │
│  ┌──────────────────────────────────────────────────┐    │
│  │ ☐ Buy groceries                                  │    │
│  │   Milk, eggs, bread                              │    │
│  │   Created: Dec 29, 2025          [Edit] [Delete] │    │
│  └──────────────────────────────────────────────────┘    │
│                                                          │
│  ┌──────────────────────────────────────────────────┐    │
│  │ ☑ Walk the dog                                   │    │
│  │   Morning walk in the park                       │    │
│  │   Created: Dec 29, 2025          [Edit] [Delete] │    │
│  └──────────────────────────────────────────────────┘    │
│                                                          │
│  ┌──────────────────────────────────────────────────┐    │
│  │ ☐ Finish project                                 │    │
│  │   Complete Phase II implementation               │    │
│  │   Created: Dec 29, 2025          [Edit] [Delete] │    │
│  └──────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────┘
```

**Props**:
```typescript
interface TaskListProps {
  tasks: Task[];
  isLoading: boolean;
  onToggleComplete: (id: number) => void;
  onEdit: (task: Task) => void;
  onDelete: (id: number) => void;
}
```

**Features**:
- Filter by: All, Completed, Pending
- Sort by: Newest, Oldest, Title
- Empty state when no tasks

---

### TaskItem

**Purpose**: Display single task with actions.

```
┌──────────────────────────────────────────────────────────┐
│ [☐/☑] Task Title                                         │
│       Optional description text...                        │
│       Created: Dec 29, 2025                [Edit][Delete]│
└──────────────────────────────────────────────────────────┘
```

**Props**:
```typescript
interface TaskItemProps {
  task: Task;
  onToggleComplete: (id: number) => void;
  onEdit: (task: Task) => void;
  onDelete: (id: number) => void;
}
```

**States**:
- Completed: strikethrough title, muted colors
- Pending: normal styling
- Hover: show action buttons

**Styling (Tailwind)**:
```tsx
// Completed task
<div className="bg-gray-50 border-gray-200">
  <span className="line-through text-gray-500">{title}</span>
</div>

// Pending task
<div className="bg-white border-gray-300 hover:border-blue-400">
  <span className="text-gray-900">{title}</span>
</div>
```

---

### TaskForm

**Purpose**: Create or edit a task.

```
┌────────────────────────────────────────────┐
│  Add New Task / Edit Task                  │
│                                            │
│  ┌──────────────────────────────────────┐  │
│  │ Title *                              │  │
│  │ Enter task title...                  │  │
│  └──────────────────────────────────────┘  │
│                                            │
│  ┌──────────────────────────────────────┐  │
│  │ Description (optional)               │  │
│  │                                      │  │
│  │                                      │  │
│  └──────────────────────────────────────┘  │
│                                            │
│  [Cancel]                    [Save Task]   │
└────────────────────────────────────────────┘
```

**Props**:
```typescript
interface TaskFormProps {
  task?: Task;  // If provided, edit mode
  onSubmit: (data: TaskCreate | TaskUpdate) => void;
  onCancel: () => void;
  isLoading: boolean;
}
```

**Validation**:
- Title: required, 1-255 characters
- Description: optional, max 1000 characters

---

### TaskActions

**Purpose**: Action buttons for a task.

```
┌────────────┐ ┌────────────┐
│    Edit    │ │   Delete   │
└────────────┘ └────────────┘
```

**Props**:
```typescript
interface TaskActionsProps {
  task: Task;
  onEdit: () => void;
  onDelete: () => void;
}
```

---

### EmptyState

**Purpose**: Display when no tasks exist.

```
┌──────────────────────────────────────────────────────────┐
│                                                          │
│                    📝                                    │
│                                                          │
│              No tasks yet                                │
│                                                          │
│     Create your first task to get started!               │
│                                                          │
│            [+ Add Your First Task]                       │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

**Props**:
```typescript
interface EmptyStateProps {
  onAddTask: () => void;
}
```

---

## UI Components (Primitives)

### Button

**Purpose**: Reusable button component.

**Variants**:
```
Primary:    [████████████]  (Blue background, white text)
Secondary:  [████████████]  (Gray background, dark text)
Danger:     [████████████]  (Red background, white text)
Ghost:      [████████████]  (Transparent, blue text)
```

**Props**:
```typescript
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'danger' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
  disabled?: boolean;
  children: React.ReactNode;
  onClick?: () => void;
  type?: 'button' | 'submit';
}
```

**Tailwind Classes**:
```tsx
const variants = {
  primary: 'bg-blue-600 hover:bg-blue-700 text-white',
  secondary: 'bg-gray-200 hover:bg-gray-300 text-gray-900',
  danger: 'bg-red-600 hover:bg-red-700 text-white',
  ghost: 'bg-transparent hover:bg-gray-100 text-blue-600'
};

const sizes = {
  sm: 'px-3 py-1.5 text-sm',
  md: 'px-4 py-2 text-base',
  lg: 'px-6 py-3 text-lg'
};
```

---

### Input

**Purpose**: Reusable input field.

```
┌──────────────────────────────────────┐
│ Label                                │
│ ┌──────────────────────────────────┐ │
│ │ Placeholder text...              │ │
│ └──────────────────────────────────┘ │
│ Helper text or error message         │
└──────────────────────────────────────┘
```

**Props**:
```typescript
interface InputProps {
  label?: string;
  placeholder?: string;
  type?: 'text' | 'email' | 'password';
  error?: string;
  helperText?: string;
  value: string;
  onChange: (value: string) => void;
  required?: boolean;
  disabled?: boolean;
}
```

---

### Modal

**Purpose**: Dialog overlay for forms and confirmations.

```
┌──────────────────────────────────────────┐
│ ╔══════════════════════════════════════╗ │
│ ║  Modal Title                    [X]  ║ │
│ ╠══════════════════════════════════════╣ │
│ ║                                      ║ │
│ ║  Modal content goes here...          ║ │
│ ║                                      ║ │
│ ╠══════════════════════════════════════╣ │
│ ║  [Cancel]              [Confirm]     ║ │
│ ╚══════════════════════════════════════╝ │
└──────────────────────────────────────────┘
       (backdrop: semi-transparent)
```

**Props**:
```typescript
interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: React.ReactNode;
  footer?: React.ReactNode;
}
```

---

### LoadingSpinner

**Purpose**: Display loading state.

```
    ◌
   ╱ ╲
  ╱   ╲
   ╲ ╱
    ◌
```

**Props**:
```typescript
interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg';
  color?: string;
}
```

**Tailwind**:
```tsx
<div className="animate-spin rounded-full border-2 border-gray-300 border-t-blue-600 h-6 w-6" />
```

---

### Alert

**Purpose**: Display success/error/warning messages.

```
Success: ┌──────────────────────────────────────┐
         │ ✓ Task created successfully!        │
         └──────────────────────────────────────┘

Error:   ┌──────────────────────────────────────┐
         │ ✗ Failed to delete task              │
         └──────────────────────────────────────┘

Warning: ┌──────────────────────────────────────┐
         │ ⚠ Are you sure you want to delete?  │
         └──────────────────────────────────────┘
```

**Props**:
```typescript
interface AlertProps {
  type: 'success' | 'error' | 'warning' | 'info';
  message: string;
  onDismiss?: () => void;
}
```

---

## Layout Components

### Header

**Purpose**: Top navigation bar.

```
┌────────────────────────────────────────────────────────────┐
│  📝 Todo App                              [user@] [Logout] │
└────────────────────────────────────────────────────────────┘
```

**Props**:
```typescript
interface HeaderProps {
  user?: User;
  onLogout: () => void;
}
```

---

### Container

**Purpose**: Centered content wrapper.

```
│          ┌─────────────────────────┐          │
│          │                         │          │
│          │    Content goes here    │          │
│          │                         │          │
│          └─────────────────────────┘          │
│                                               │
           max-width: 1024px
           padding: 1rem (mobile) / 2rem (desktop)
```

**Tailwind**:
```tsx
<div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
  {children}
</div>
```

---

## Responsive Breakpoints

| Breakpoint | Width | Target |
|------------|-------|--------|
| `sm` | 640px+ | Mobile landscape |
| `md` | 768px+ | Tablet |
| `lg` | 1024px+ | Desktop |
| `xl` | 1280px+ | Large desktop |

---

## Accessibility Requirements

- All form inputs have associated labels
- Focus states visible on all interactive elements
- Color contrast meets WCAG AA standards
- Keyboard navigation supported
- Screen reader compatible

---

**Previous**: [../database/schema.md](../database/schema.md)
**Next**: [pages.md](./pages.md)
