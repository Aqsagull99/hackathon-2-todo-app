# UI Specification: Pages

**Spec ID**: 002-phase2-fullstack/ui/pages
**Version**: 1.0.0
**Status**: Draft
**Created**: 2025-12-29

---

## Page Structure (App Router)

```
frontend/src/app/
├── layout.tsx           # Root layout
├── page.tsx             # Landing page (/)
├── login/
│   └── page.tsx         # Login page (/login)
├── register/
│   └── page.tsx         # Register page (/register)
├── dashboard/
│   ├── layout.tsx       # Dashboard layout
│   └── page.tsx         # Dashboard page (/dashboard)
└── api/
    └── auth/
        └── [...all]/
            └── route.ts # Better Auth API routes
```

---

## Page Overview

| Route | Page | Auth Required | Description |
|-------|------|---------------|-------------|
| `/` | Landing | No | Welcome page with CTA |
| `/login` | Login | No | User login form |
| `/register` | Register | No | User registration form |
| `/dashboard` | Dashboard | Yes | Main task management |

---

## Page 1: Landing Page (/)

### Purpose
Welcome page that directs users to login or register.

### Layout

```
┌────────────────────────────────────────────────────────────────────┐
│  📝 Todo App                                    [Login] [Register] │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│                                                                    │
│                        ✅ Todo App                                 │
│                                                                    │
│            Manage your tasks with ease                             │
│                                                                    │
│       A simple, powerful task management application               │
│         built with Next.js, FastAPI, and PostgreSQL                │
│                                                                    │
│                                                                    │
│                    [Get Started →]                                 │
│                                                                    │
│                                                                    │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐       │
│  │   📝 Create    │  │   ✓ Complete   │  │   🗑️ Delete    │       │
│  │   Add tasks    │  │   Mark done    │  │   Remove tasks │       │
│  │   quickly      │  │   track work   │  │   when done    │       │
│  └────────────────┘  └────────────────┘  └────────────────┘       │
│                                                                    │
├────────────────────────────────────────────────────────────────────┤
│  Built with ❤️ using Spec-Driven Development                       │
└────────────────────────────────────────────────────────────────────┘
```

### Behavior

- If user is logged in → Redirect to `/dashboard`
- "Get Started" button → Navigate to `/register`
- "Login" button → Navigate to `/login`
- "Register" button → Navigate to `/register`

### Implementation

```tsx
// app/page.tsx
import { redirect } from 'next/navigation'
import { auth } from '@/lib/auth'
import Link from 'next/link'

export default async function LandingPage() {
  const session = await auth.api.getSession()

  if (session) {
    redirect('/dashboard')
  }

  return (
    <main className="min-h-screen flex flex-col">
      <header className="flex justify-between items-center p-4">
        <h1 className="text-xl font-bold">📝 Todo App</h1>
        <nav className="space-x-4">
          <Link href="/login">Login</Link>
          <Link href="/register">Register</Link>
        </nav>
      </header>

      <section className="flex-1 flex flex-col items-center justify-center text-center px-4">
        <h2 className="text-4xl font-bold mb-4">✅ Todo App</h2>
        <p className="text-xl text-gray-600 mb-8">
          Manage your tasks with ease
        </p>
        <Link href="/register" className="btn-primary">
          Get Started →
        </Link>
      </section>

      {/* Feature cards */}
      <section className="grid grid-cols-1 md:grid-cols-3 gap-4 p-8">
        {/* ... feature cards ... */}
      </section>
    </main>
  )
}
```

---

## Page 2: Login Page (/login)

### Purpose
Allow existing users to authenticate.

### Layout

```
┌────────────────────────────────────────────────────────────────────┐
│  📝 Todo App                                                       │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│                     ┌─────────────────────────┐                    │
│                     │                         │                    │
│                     │     Welcome back        │                    │
│                     │                         │                    │
│                     │  ┌───────────────────┐  │                    │
│                     │  │ Email             │  │                    │
│                     │  │ user@example.com  │  │                    │
│                     │  └───────────────────┘  │                    │
│                     │                         │                    │
│                     │  ┌───────────────────┐  │                    │
│                     │  │ Password          │  │                    │
│                     │  │ ••••••••          │  │                    │
│                     │  └───────────────────┘  │                    │
│                     │                         │                    │
│                     │  [Error message here]   │                    │
│                     │                         │                    │
│                     │  ┌───────────────────┐  │                    │
│                     │  │     Sign In       │  │                    │
│                     │  └───────────────────┘  │                    │
│                     │                         │                    │
│                     │  Don't have an account? │                    │
│                     │  Register               │                    │
│                     │                         │                    │
│                     └─────────────────────────┘                    │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

### Behavior

- If user is logged in → Redirect to `/dashboard`
- On successful login → Redirect to `/dashboard`
- On error → Show error message
- "Register" link → Navigate to `/register`

### Implementation

```tsx
// app/login/page.tsx
'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { authClient } from '@/lib/auth-client'
import Link from 'next/link'

export default function LoginPage() {
  const router = useRouter()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    setError('')

    try {
      await authClient.signIn.email({ email, password })
      router.push('/dashboard')
    } catch (err) {
      setError('Invalid email or password')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <main className="min-h-screen flex items-center justify-center">
      <div className="w-full max-w-md p-8 bg-white rounded-lg shadow">
        <h1 className="text-2xl font-bold text-center mb-6">Welcome back</h1>

        <form onSubmit={handleSubmit} className="space-y-4">
          <Input
            label="Email"
            type="email"
            value={email}
            onChange={setEmail}
            required
          />
          <Input
            label="Password"
            type="password"
            value={password}
            onChange={setPassword}
            required
          />

          {error && <Alert type="error" message={error} />}

          <Button type="submit" isLoading={isLoading}>
            Sign In
          </Button>
        </form>

        <p className="text-center mt-4">
          Don't have an account? <Link href="/register">Register</Link>
        </p>
      </div>
    </main>
  )
}
```

---

## Page 3: Register Page (/register)

### Purpose
Allow new users to create an account.

### Layout

```
┌────────────────────────────────────────────────────────────────────┐
│  📝 Todo App                                                       │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│                     ┌─────────────────────────┐                    │
│                     │                         │                    │
│                     │   Create your account   │                    │
│                     │                         │                    │
│                     │  ┌───────────────────┐  │                    │
│                     │  │ Email             │  │                    │
│                     │  │ user@example.com  │  │                    │
│                     │  └───────────────────┘  │                    │
│                     │                         │                    │
│                     │  ┌───────────────────┐  │                    │
│                     │  │ Password          │  │                    │
│                     │  │ ••••••••          │  │                    │
│                     │  └───────────────────┘  │                    │
│                     │                         │                    │
│                     │  ┌───────────────────┐  │                    │
│                     │  │ Confirm Password  │  │                    │
│                     │  │ ••••••••          │  │                    │
│                     │  └───────────────────┘  │                    │
│                     │                         │                    │
│                     │  [Error message here]   │                    │
│                     │                         │                    │
│                     │  ┌───────────────────┐  │                    │
│                     │  │  Create Account   │  │                    │
│                     │  └───────────────────┘  │                    │
│                     │                         │                    │
│                     │  Already have account?  │                    │
│                     │  Login                  │                    │
│                     │                         │                    │
│                     └─────────────────────────┘                    │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

### Validations

- Email: valid format
- Password: minimum 8 characters
- Confirm: must match password

### Behavior

- If user is logged in → Redirect to `/dashboard`
- On successful registration → Redirect to `/dashboard`
- On error → Show error message
- "Login" link → Navigate to `/login`

---

## Page 4: Dashboard Page (/dashboard)

### Purpose
Main task management interface.

### Layout

```
┌────────────────────────────────────────────────────────────────────┐
│  📝 Todo App                                user@email.com [Logout]│
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  My Tasks                                         [+ Add Task]     │
│                                                                    │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ Filter: [All ▼]              Sort: [Newest ▼]               │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                    │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ ☐ Buy groceries                                             │   │
│  │   Milk, eggs, bread                                         │   │
│  │   Created: Dec 29, 2025                     [Edit] [Delete] │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                    │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ ☑ Walk the dog                              ──────────────  │   │
│  │   ~~Morning walk in the park~~                              │   │
│  │   Created: Dec 29, 2025                     [Edit] [Delete] │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                    │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ ☐ Finish project                                            │   │
│  │   Complete Phase II implementation                          │   │
│  │   Created: Dec 29, 2025                     [Edit] [Delete] │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                    │
│  Showing 3 tasks                                                   │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

### Empty State

```
┌────────────────────────────────────────────────────────────────────┐
│  📝 Todo App                                user@email.com [Logout]│
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  My Tasks                                         [+ Add Task]     │
│                                                                    │
│                                                                    │
│                                                                    │
│                            📝                                      │
│                                                                    │
│                      No tasks yet                                  │
│                                                                    │
│             Create your first task to get started!                 │
│                                                                    │
│                   [+ Add Your First Task]                          │
│                                                                    │
│                                                                    │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

### Add Task Modal

```
┌────────────────────────────────────────────────────────────────────┐
│                                                                    │
│         ╔═══════════════════════════════════════════════╗          │
│         ║  Add New Task                            [X]  ║          │
│         ╠═══════════════════════════════════════════════╣          │
│         ║                                               ║          │
│         ║  ┌─────────────────────────────────────────┐  ║          │
│         ║  │ Title *                                 │  ║          │
│         ║  │ Enter task title...                     │  ║          │
│         ║  └─────────────────────────────────────────┘  ║          │
│         ║                                               ║          │
│         ║  ┌─────────────────────────────────────────┐  ║          │
│         ║  │ Description (optional)                  │  ║          │
│         ║  │                                         │  ║          │
│         ║  │                                         │  ║          │
│         ║  └─────────────────────────────────────────┘  ║          │
│         ║                                               ║          │
│         ╠═══════════════════════════════════════════════╣          │
│         ║  [Cancel]                       [Add Task]    ║          │
│         ╚═══════════════════════════════════════════════╝          │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

### Delete Confirmation Modal

```
┌────────────────────────────────────────────────────────────────────┐
│                                                                    │
│         ╔═══════════════════════════════════════════════╗          │
│         ║  Delete Task                             [X]  ║          │
│         ╠═══════════════════════════════════════════════╣          │
│         ║                                               ║          │
│         ║  Are you sure you want to delete this task?   ║          │
│         ║                                               ║          │
│         ║  "Buy groceries"                              ║          │
│         ║                                               ║          │
│         ║  This action cannot be undone.                ║          │
│         ║                                               ║          │
│         ╠═══════════════════════════════════════════════╣          │
│         ║  [Cancel]                       [Delete]      ║          │
│         ╚═══════════════════════════════════════════════╝          │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

### Behavior

- Requires authentication (redirect to `/login` if not)
- Fetch tasks on page load
- Add Task → Show modal → Create task → Refresh list
- Edit Task → Show modal → Update task → Refresh list
- Delete Task → Show confirmation → Delete → Refresh list
- Toggle Complete → Update task → Refresh item
- Filter → Re-filter displayed tasks
- Logout → Clear session → Redirect to `/login`

### Implementation

```tsx
// app/dashboard/page.tsx
'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { authClient } from '@/lib/auth-client'
import { TaskList, TaskForm, EmptyState } from '@/components/tasks'
import { Modal, Button } from '@/components/ui'
import { Task, TaskCreate } from '@/types'
import { api } from '@/lib/api'

export default function DashboardPage() {
  const router = useRouter()
  const [tasks, setTasks] = useState<Task[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [showAddModal, setShowAddModal] = useState(false)
  const [editingTask, setEditingTask] = useState<Task | null>(null)
  const [deletingTask, setDeletingTask] = useState<Task | null>(null)
  const [filter, setFilter] = useState<'all' | 'completed' | 'pending'>('all')

  const session = authClient.useSession()

  useEffect(() => {
    if (!session.data) {
      router.push('/login')
      return
    }
    fetchTasks()
  }, [session])

  const fetchTasks = async () => {
    try {
      const data = await api.getTasks()
      setTasks(data)
    } catch (error) {
      console.error('Failed to fetch tasks')
    } finally {
      setIsLoading(false)
    }
  }

  const handleAddTask = async (data: TaskCreate) => {
    await api.createTask(data)
    setShowAddModal(false)
    fetchTasks()
  }

  const handleToggleComplete = async (id: number) => {
    await api.toggleComplete(id)
    fetchTasks()
  }

  const handleDelete = async () => {
    if (deletingTask) {
      await api.deleteTask(deletingTask.id)
      setDeletingTask(null)
      fetchTasks()
    }
  }

  const filteredTasks = tasks.filter(task => {
    if (filter === 'completed') return task.completed
    if (filter === 'pending') return !task.completed
    return true
  })

  return (
    <div className="max-w-4xl mx-auto p-4">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">My Tasks</h1>
        <Button onClick={() => setShowAddModal(true)}>+ Add Task</Button>
      </div>

      {tasks.length === 0 ? (
        <EmptyState onAddTask={() => setShowAddModal(true)} />
      ) : (
        <TaskList
          tasks={filteredTasks}
          isLoading={isLoading}
          onToggleComplete={handleToggleComplete}
          onEdit={setEditingTask}
          onDelete={setDeletingTask}
        />
      )}

      {/* Add Task Modal */}
      <Modal isOpen={showAddModal} onClose={() => setShowAddModal(false)} title="Add New Task">
        <TaskForm onSubmit={handleAddTask} onCancel={() => setShowAddModal(false)} />
      </Modal>

      {/* Delete Confirmation Modal */}
      <Modal isOpen={!!deletingTask} onClose={() => setDeletingTask(null)} title="Delete Task">
        <p>Are you sure you want to delete "{deletingTask?.title}"?</p>
        <div className="flex justify-end gap-2 mt-4">
          <Button variant="secondary" onClick={() => setDeletingTask(null)}>Cancel</Button>
          <Button variant="danger" onClick={handleDelete}>Delete</Button>
        </div>
      </Modal>
    </div>
  )
}
```

---

## Route Protection (Middleware)

```typescript
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

const protectedRoutes = ['/dashboard']
const authRoutes = ['/login', '/register']

export function middleware(request: NextRequest) {
  const token = request.cookies.get('session')?.value
  const { pathname } = request.nextUrl

  // Protected routes require authentication
  if (protectedRoutes.some(route => pathname.startsWith(route))) {
    if (!token) {
      return NextResponse.redirect(new URL('/login', request.url))
    }
  }

  // Auth routes redirect if already logged in
  if (authRoutes.includes(pathname)) {
    if (token) {
      return NextResponse.redirect(new URL('/dashboard', request.url))
    }
  }

  return NextResponse.next()
}

export const config = {
  matcher: ['/dashboard/:path*', '/login', '/register']
}
```

---

## Root Layout

```tsx
// app/layout.tsx
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata = {
  title: 'Todo App',
  description: 'A simple task management application'
}

export default function RootLayout({
  children
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        {children}
      </body>
    </html>
  )
}
```

---

## Responsive Design

### Mobile Layout (< 640px)

```
┌──────────────────────────┐
│ 📝 Todo      [≡]         │
├──────────────────────────┤
│ My Tasks    [+ Add]      │
│                          │
│ ┌────────────────────┐   │
│ │ ☐ Task 1           │   │
│ │   Description...   │   │
│ │   [Edit] [Delete]  │   │
│ └────────────────────┘   │
│                          │
│ ┌────────────────────┐   │
│ │ ☑ Task 2           │   │
│ │   Description...   │   │
│ │   [Edit] [Delete]  │   │
│ └────────────────────┘   │
└──────────────────────────┘
```

### Desktop Layout (≥ 1024px)

```
┌──────────────────────────────────────────────────────────────────┐
│ 📝 Todo App                               user@email.com [Logout]│
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│    My Tasks                                      [+ Add Task]    │
│                                                                  │
│    ┌─────────────────────────────────────────────────────────┐   │
│    │ ☐ Task 1                                 [Edit][Delete] │   │
│    └─────────────────────────────────────────────────────────┘   │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

**Previous**: [components.md](./components.md)
**Related**: [../features/task-crud.md](../features/task-crud.md)
