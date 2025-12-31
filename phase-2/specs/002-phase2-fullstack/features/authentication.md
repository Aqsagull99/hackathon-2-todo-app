# Feature Specification: Authentication

**Spec ID**: 002-phase2-fullstack/features/authentication
**Version**: 1.0.0
**Status**: Draft
**Created**: 2025-12-29

---

## Overview

This specification defines the authentication flow using Better Auth with JWT tokens. The frontend handles user registration and login via Better Auth, while the backend verifies JWT tokens for API access.

## Authentication Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                        FRONTEND                               │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                    Better Auth Client                    │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │ │
│  │  │   Register   │  │    Login     │  │   Logout     │   │ │
│  │  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘   │ │
│  │         │                 │                  │           │ │
│  │         └─────────────────┼──────────────────┘           │ │
│  │                           │                               │ │
│  │                    ┌──────▼──────┐                       │ │
│  │                    │  JWT Token  │                       │ │
│  │                    │  (stored)   │                       │ │
│  │                    └──────┬──────┘                       │ │
│  └───────────────────────────┼──────────────────────────────┘ │
│                              │                                 │
│                    Authorization: Bearer <token>               │
│                              │                                 │
└──────────────────────────────┼─────────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│                        BACKEND                                │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                   JWT Verification                       │ │
│  │  ┌──────────────────────────────────────────────────┐   │ │
│  │  │ 1. Extract token from Authorization header       │   │ │
│  │  │ 2. Verify signature with BETTER_AUTH_SECRET      │   │ │
│  │  │ 3. Check expiration                              │   │ │
│  │  │ 4. Extract user_id from 'sub' claim              │   │ │
│  │  │ 5. Validate user_id matches URL parameter        │   │ │
│  │  └──────────────────────────────────────────────────┘   │ │
│  └─────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

## Feature 1: User Registration

### Description
Allow new users to create an account using Better Auth.

### User Story
> As a new user, I want to register an account so that I can use the todo application.

### Acceptance Criteria

- [ ] User provides email and password
- [ ] Email must be valid format
- [ ] Password must meet minimum requirements (8+ characters)
- [ ] Better Auth creates user in database
- [ ] User receives JWT token after registration
- [ ] User redirected to dashboard after success
- [ ] Display error for duplicate email

### UI Flow

```
┌────────────────────────────────────────┐
│           Register Page                │
├────────────────────────────────────────┤
│                                        │
│   Create your account                  │
│                                        │
│   ┌──────────────────────────────────┐ │
│   │ Email                            │ │
│   │ user@example.com                 │ │
│   └──────────────────────────────────┘ │
│                                        │
│   ┌──────────────────────────────────┐ │
│   │ Password                         │ │
│   │ ••••••••                         │ │
│   └──────────────────────────────────┘ │
│                                        │
│   ┌──────────────────────────────────┐ │
│   │ Confirm Password                 │ │
│   │ ••••••••                         │ │
│   └──────────────────────────────────┘ │
│                                        │
│   [        Create Account        ]     │
│                                        │
│   Already have an account? Login       │
│                                        │
└────────────────────────────────────────┘
```

### Test Cases

```gherkin
Feature: User Registration

  Scenario: Successfully register new user
    Given I am on the register page
    When I enter email "newuser@example.com"
    And I enter password "SecurePass123"
    And I confirm password "SecurePass123"
    And I click "Create Account"
    Then I am redirected to "/dashboard"
    And I receive a valid JWT token

  Scenario: Fail registration with existing email
    Given "existing@example.com" is already registered
    When I try to register with "existing@example.com"
    Then I see error "Email already registered"

  Scenario: Fail registration with weak password
    When I enter password "123"
    Then I see error "Password must be at least 8 characters"

  Scenario: Fail registration with mismatched passwords
    When I enter password "SecurePass123"
    And I confirm password "DifferentPass456"
    Then I see error "Passwords do not match"
```

---

## Feature 2: User Login

### Description
Allow existing users to authenticate and receive a JWT token.

### User Story
> As a registered user, I want to log in so that I can access my tasks.

### Acceptance Criteria

- [ ] User provides email and password
- [ ] Better Auth verifies credentials
- [ ] User receives JWT token on success
- [ ] JWT contains user_id in 'sub' claim
- [ ] User redirected to dashboard after success
- [ ] Display error for invalid credentials
- [ ] Show loading state during authentication

### UI Flow

```
┌────────────────────────────────────────┐
│             Login Page                 │
├────────────────────────────────────────┤
│                                        │
│   Welcome back                         │
│                                        │
│   ┌──────────────────────────────────┐ │
│   │ Email                            │ │
│   │ user@example.com                 │ │
│   └──────────────────────────────────┘ │
│                                        │
│   ┌──────────────────────────────────┐ │
│   │ Password                         │ │
│   │ ••••••••                         │ │
│   └──────────────────────────────────┘ │
│                                        │
│   [           Sign In            ]     │
│                                        │
│   Don't have an account? Register      │
│                                        │
└────────────────────────────────────────┘
```

### Test Cases

```gherkin
Feature: User Login

  Scenario: Successfully login
    Given "user@example.com" is registered with password "SecurePass123"
    When I enter email "user@example.com"
    And I enter password "SecurePass123"
    And I click "Sign In"
    Then I am redirected to "/dashboard"
    And I receive a valid JWT token

  Scenario: Fail login with wrong password
    Given "user@example.com" is registered
    When I enter wrong password
    Then I see error "Invalid credentials"

  Scenario: Fail login with non-existent email
    When I enter email "notfound@example.com"
    And I click "Sign In"
    Then I see error "Invalid credentials"
```

---

## Feature 3: User Logout

### Description
Allow users to end their session and clear authentication state.

### User Story
> As a logged-in user, I want to log out so that my session is securely ended.

### Acceptance Criteria

- [ ] Logout button visible when authenticated
- [ ] Clicking logout clears JWT token
- [ ] User redirected to login page
- [ ] Subsequent API calls fail with 401

### Test Cases

```gherkin
Feature: User Logout

  Scenario: Successfully logout
    Given I am logged in
    When I click "Logout"
    Then my JWT token is cleared
    And I am redirected to "/login"

  Scenario: Cannot access dashboard after logout
    Given I have logged out
    When I try to access "/dashboard"
    Then I am redirected to "/login"
```

---

## Feature 4: JWT Verification (Backend)

### Description
Backend middleware to verify JWT tokens on protected endpoints.

### Implementation

```python
# core/security.py
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def verify_jwt(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """
    Verify JWT token and extract payload.

    Returns:
        dict: JWT payload containing user_id in 'sub' claim

    Raises:
        HTTPException: 401 if token invalid/expired
    """
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )


async def get_current_user_id(
    payload: dict = Depends(verify_jwt)
) -> str:
    """Extract user_id from verified JWT payload."""
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )
    return user_id


async def verify_user_access(
    user_id_from_url: str,
    current_user_id: str = Depends(get_current_user_id)
) -> str:
    """
    Verify the authenticated user matches the URL user_id.

    Raises:
        HTTPException: 403 if user_id mismatch
    """
    if user_id_from_url != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    return current_user_id
```

### JWT Token Structure

```json
{
  "header": {
    "alg": "HS256",
    "typ": "JWT"
  },
  "payload": {
    "sub": "user_abc123",
    "email": "user@example.com",
    "name": "John Doe",
    "iat": 1735488000,
    "exp": 1735491600
  }
}
```

### Verification Steps

1. **Extract Token**: Get token from `Authorization: Bearer <token>` header
2. **Decode JWT**: Parse header, payload, signature
3. **Verify Signature**: HMAC-SHA256 with `BETTER_AUTH_SECRET`
4. **Check Expiration**: Compare `exp` claim with current time
5. **Extract User ID**: Get `sub` claim from payload
6. **Validate Access**: Compare with URL `{user_id}` parameter

### Test Cases

```gherkin
Feature: JWT Verification

  Scenario: Valid token accepted
    Given I have a valid JWT for "user_abc123"
    When I call API with "Authorization: Bearer <valid_token>"
    Then the request is processed successfully

  Scenario: Missing token rejected
    When I call API without Authorization header
    Then I receive status 401
    And response contains "Not authenticated"

  Scenario: Invalid token rejected
    When I call API with "Authorization: Bearer invalid_token"
    Then I receive status 401
    And response contains "Invalid token"

  Scenario: Expired token rejected
    Given I have an expired JWT
    When I call API with the expired token
    Then I receive status 401
    And response contains "Invalid token"

  Scenario: User ID mismatch rejected
    Given I have a valid JWT for "user_xyz789"
    When I call "/api/user_abc123/tasks"
    Then I receive status 403
    And response contains "Access denied"
```

---

## Feature 5: Protected Routes (Frontend)

### Description
Frontend middleware to protect routes requiring authentication.

### Implementation

```typescript
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  const token = request.cookies.get('session')?.value

  const protectedPaths = ['/dashboard']
  const authPaths = ['/login', '/register']

  const isProtectedPath = protectedPaths.some(path =>
    request.nextUrl.pathname.startsWith(path)
  )
  const isAuthPath = authPaths.some(path =>
    request.nextUrl.pathname.startsWith(path)
  )

  // Redirect to login if accessing protected route without token
  if (isProtectedPath && !token) {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  // Redirect to dashboard if accessing auth routes with valid token
  if (isAuthPath && token) {
    return NextResponse.redirect(new URL('/dashboard', request.url))
  }

  return NextResponse.next()
}

export const config = {
  matcher: ['/dashboard/:path*', '/login', '/register']
}
```

### Route Protection Summary

| Route | Auth Required | Redirect If |
|-------|---------------|-------------|
| `/` | No | - |
| `/login` | No | Has token → `/dashboard` |
| `/register` | No | Has token → `/dashboard` |
| `/dashboard` | Yes | No token → `/login` |
| `/dashboard/*` | Yes | No token → `/login` |

---

## Environment Variables

### Frontend (.env.local)

```bash
# Better Auth
BETTER_AUTH_SECRET="your-secret-key-min-32-chars"
BETTER_AUTH_URL="http://localhost:3000"

# Database for Better Auth
DATABASE_URL="postgresql://user:pass@host/db?sslmode=require"
```

### Backend (.env)

```bash
# JWT (must match BETTER_AUTH_SECRET)
JWT_SECRET="your-secret-key-min-32-chars"
JWT_ALGORITHM="HS256"
JWT_EXPIRATION_MINUTES=30
```

### Important Notes

1. **Shared Secret**: `BETTER_AUTH_SECRET` (frontend) and `JWT_SECRET` (backend) MUST be identical
2. **Never Commit**: All `.env` files must be in `.gitignore`
3. **Minimum Length**: Secret key should be at least 32 characters

---

## Better Auth Configuration (Frontend)

```typescript
// lib/auth.ts
import { betterAuth } from "better-auth"
import { Pool } from "pg"

export const auth = betterAuth({
  database: new Pool({
    connectionString: process.env.DATABASE_URL
  }),
  emailAndPassword: {
    enabled: true,
    minPasswordLength: 8
  },
  session: {
    expiresIn: 60 * 30, // 30 minutes
    updateAge: 60 * 15  // 15 minutes
  }
})
```

---

**Previous**: [task-crud.md](./task-crud.md)
**Next**: [../api/rest-endpoints.md](../api/rest-endpoints.md)
