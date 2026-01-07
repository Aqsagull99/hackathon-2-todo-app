---
name: better-auth-skill
description: Reusable Better Auth skill with JWT plugin, OAuth providers, and session management. Use with Better Auth MCP server.
---

# Better Auth Skill

Use this skill when implementing authentication with Better Auth in Next.js frontend.

## Basic Setup

```typescript
// lib/auth.ts
import { createAuth } from "better-auth";
import { jwt } from "better-auth/plugins/jwt";

export const auth = createAuth({
  plugins: [
    jwt({
      secret: process.env.BETTER_AUTH_SECRET,
      expiresIn: 60 * 60 * 24 * 7, // 7 days
    }),
  ],
  // Add providers as needed
  // google: {
  //   clientId: process.env.GOOGLE_CLIENT_ID,
  //   clientSecret: process.env.GOOGLE_CLIENT_SECRET,
  // },
});
```

## Environment Variables

```bash
# .env.local
BETTER_AUTH_SECRET="your-32-character-secret-key-minimum"
```

## Getting Session

```typescript
// In server components
import { auth } from "@/lib/auth";

export async function getSession() {
  const session = await auth.getSession();
  return session;
}

// In client components
import { useSession } from "better-auth/react";

const { data: session } = useSession();
```

## Sign In / Sign Out

```typescript
import { signIn, signOut, useSession } from "better-auth/react";

function AuthButton() {
  const { data: session, isLoading } = useSession();

  if (isLoading) {
    return <span>Loading...</span>;
  }

  if (session) {
    return (
      <button onClick={() => signOut()}>
        Sign out ({session.user.email})
      </button>
    );
  }

  return (
    <button onClick={() => signIn("google")}>
      Sign in with Google
    </button>
  );
}
```

## Getting Access Token

```typescript
// Get session and access token in client
import { useSession } from "better-auth/react";

function ApiExample() {
  const { data: session } = useSession();

  const makeRequest = async () => {
    const token = session?.accessToken;

    const response = await fetch("http://localhost:8000/api/tasks", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    return response.json();
  };

  return <button onClick={makeRequest}>Fetch Tasks</button>;
}
```

## API Route Handler (Next.js)

```typescript
// app/api/auth/[...nextauth]/route.ts
import { auth } from "@/lib/auth";
import { NextResponse } from "next/server";

export const { GET, POST } = auth((req) => {
  const requestUrl = new URL(req.url);

  // Handle sign-in callback
  if (requestUrl.pathname === "/api/auth/callback/google") {
    return NextResponse.redirect(new URL("/tasks", requestUrl));
  }

  // Handle sign-out
  if (requestUrl.pathname === "/api/auth/signout") {
    return NextResponse.redirect(new URL("/", requestUrl));
  }

  return NextResponse.next();
});
```

## Protected Route (Server Component)

```typescript
// app/tasks/page.tsx
import { auth } from "@/lib/auth";
import { redirect } from "next/navigation";
import { api } from "@/lib/api";

export default async function TasksPage() {
  const session = await auth();

  if (!session) {
    redirect("/");
  }

  // Fetch tasks with token
  const tasks = await api.getTasks();

  return (
    <div>
      <h1>My Tasks</h1>
      {/* Render tasks */}
    </div>
  );
}
```

## Protected Route (Client Component)

```typescript
// components/ProtectedComponent.tsx
"use client";

import { useSession } from "better-auth/react";

export function ProtectedComponent() {
  const { data: session, isAuthenticated } = useSession();

  if (!isAuthenticated) {
    return <p>Please sign in to view this content.</p>;
  }

  return <p>Welcome, {session?.user?.name}!</p>;
}
```

## Better Auth MCP Usage

Use `@better-auth:list_files` to see available documentation:
```typescript
// List all knowledge base files
@better-auth:list_files
```

Use `@better-auth:search` to find specific topics:
```typescript
// Search for JWT configuration
@better-auth:search query="jwt plugin configuration"
```

## Best Practices

1. Use environment variables for all secrets
2. Set `BETTER_AUTH_SECRET` to 32+ characters
3. Use HTTPS in production
4. Configure CORS on backend for your frontend origin
5. Handle 401 errors by redirecting to login
6. Store tokens securely (HTTP-only cookies preferred for production)
7. Set reasonable token expiration (7 days is common)
