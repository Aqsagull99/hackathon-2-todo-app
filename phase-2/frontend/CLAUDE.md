# Claude Code Rules - Frontend

This file provides Claude Code instructions for the Next.js frontend application.

## Project Overview

**Project**: Todo App Frontend (Phase II)
**Framework**: Next.js 16+ (App Router)
**Language**: TypeScript
**Styling**: Tailwind CSS
**Authentication**: Better Auth

## How to Run

```bash
cd ~/Todo-app/frontend
npm install
npm run dev
```

Server runs at: http://localhost:3000

## Project Structure

```
frontend/
├── src/
│   ├── app/                  # App Router pages
│   │   ├── layout.tsx       # Root layout
│   │   ├── page.tsx         # Landing page (/)
│   │   ├── login/page.tsx   # Login page
│   │   ├── register/page.tsx # Register page
│   │   └── dashboard/page.tsx # Main todo interface
│   ├── components/
│   │   ├── auth/            # Auth components
│   │   ├── tasks/           # Task components
│   │   ├── ui/              # UI primitives
│   │   └── layout/          # Layout components
│   ├── lib/
│   │   ├── auth.ts          # Better Auth config
│   │   ├── auth-client.ts   # Client-side auth
│   │   └── api.ts           # API client
│   └── types/
│       └── index.ts         # TypeScript types
├── .env.local               # Environment variables
└── tailwind.config.ts       # Tailwind configuration
```

## Key Files

| File | Purpose |
|------|---------|
| `src/app/layout.tsx` | Root layout with providers |
| `src/app/dashboard/page.tsx` | Main task management |
| `src/lib/auth.ts` | Better Auth server config |
| `src/lib/auth-client.ts` | Better Auth client |
| `src/lib/api.ts` | Backend API client |

## Environment Variables

```bash
# .env.local
BETTER_AUTH_SECRET="your-jwt-secret"
BETTER_AUTH_URL="http://localhost:3000"
NEXT_PUBLIC_API_URL="http://localhost:8000"
DATABASE_URL="postgresql://..."
```

## Specifications

Read these specs before implementing:
- `specs/002-phase2-fullstack/ui/pages.md` - Page layouts
- `specs/002-phase2-fullstack/ui/components.md` - UI components
- `specs/002-phase2-fullstack/features/authentication.md` - Auth flow

## MCP Servers

Use these MCP servers for documentation:
- **context7**: Next.js, React, Tailwind docs
- **better-auth**: Better Auth configuration

## Coding Standards

- Use TypeScript with strict mode
- Follow Next.js App Router conventions
- Use Tailwind CSS for styling
- Create reusable components
- Handle loading and error states
- Implement responsive design

## Common Tasks

### Add New Page
```bash
# Create page file
touch src/app/new-page/page.tsx
```

### Add New Component
```bash
# Create component file
touch src/components/category/ComponentName.tsx
```

### API Call Pattern
```typescript
// lib/api.ts
export const api = {
  getTasks: async () => {
    const res = await fetch(`${API_URL}/api/${userId}/tasks`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    return res.json()
  }
}
```

## Testing

```bash
# Type check
npm run type-check

# Lint
npm run lint

# Build
npm run build
```
