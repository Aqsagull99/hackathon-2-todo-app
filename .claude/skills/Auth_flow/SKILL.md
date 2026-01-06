# 🔐 Authentication Architecture Skill (Better Auth)

## Purpose
Define a clean, predictable, and auth-state driven authentication flow for modern web applications using Better Auth (or any similar auth provider).

This skill ensures:
- Clear separation of UI, authentication state, and backend protection
- No confusion between login, signup, and OAuth flows
- Reusable architecture across multiple projects

---

## Assumptions
- Application routes already exist
- No UI or route redesign is required
- Authentication is session-based or JWT-based
- An external auth provider (e.g., Better Auth) is used
- Focus is on behavior and flow, not implementation code

---

## Core Rules (Reusable Across Projects)

### 1. Authentication State
- Only **two authentication states** are allowed:
  - `authenticated`
  - `unauthenticated`
- Auth state must be derived from the auth provider (session/JWT)
- All UI and routing decisions depend only on this state

---

### 2. Header Behavior (Global Navigation)
- Header must be **fully auth-state driven**

**Unauthenticated (Guest):**
- Show: `Sign In`
- Show: `Sign Up`

**Authenticated (Logged In):**
- Show: `Dashboard`
- Show: `Logout`

Rules:
- Header must never show `Sign Up` after login
- Header must update immediately after login/logout

---

### 3. Home Page CTA (Landing Page)
- Home page must contain **one primary CTA only**

**CTA Button:** `Get Started`

Behavior:
- If unauthenticated → redirect to `Sign Up`
- If authenticated → redirect to `Dashboard`

Rules:
- `Get Started` exists ONLY on the Home page
- `Get Started` must NOT appear in the header

---

### 4. Authentication Pages
- Sign In and Sign Up pages must support:
  - Email + Password
  - Google OAuth
  - Facebook OAuth

Rules:
- Google/Facebook buttons trigger the **same auth flow**
- Auth provider decides internally:
  - New user → signup
  - Existing user → login
- End result of ALL auth methods is identical:
  - `authenticated` state

---

### 5. Middleware Usage
- Middleware is used ONLY for protection, not UI logic

Apply middleware to:
- Protected pages (e.g., `/todos`)
- Protected APIs (e.g., `/api/tasks`)

Do NOT apply middleware to:
- Public routes (`/`, `/login`, `/signup`)

Middleware responsibility:
- Verify authentication validity (session/JWT)
- Allow or deny access

---

## Output Rules (When Using This Skill)
- Do NOT generate code unless explicitly asked
- Explain using clear bullet points
- Use simple, beginner-friendly language
- Focus on flow, clarity, and correctness
- Do not redesign routes or UI structure

---

## Core Principle (Mental Model)
> Authentication methods may differ,  
> but the application always operates on a single auth state.

---

## Reusability Note
This skill is provider-agnostic:
- Better Auth
- Auth.js
- Clerk
- Firebase Auth

Only the auth provider changes —  
**the architecture remains the same.**



┌────────────────────────────────────────────────────┐
│                    USER OPENS APP                  │
│                   (Home Page "/")                  │
└────────────────────────────────────────────────────┘
                           │
                           ▼
                ┌───────────────────┐
                │   AUTH STATE CHECK │
                │ (from Better Auth) │
                └───────────────────┘
                    │           │
        unauthenticated        authenticated
                    │           │
                    ▼           ▼
┌────────────────────────┐   ┌────────────────────────┐
│        HEADER           │   │        HEADER           │
│------------------------│   │------------------------│
│  Sign In               │   │  Dashboard             │
│  Sign Up               │   │  Logout                │
└────────────────────────┘   └────────────────────────┘
                    │           │
                    └─────┬─────┘
                          ▼
┌────────────────────────────────────────────────────┐
│                  HOME PAGE CTA                     │
│                (Big Hero Section)                  │
│                                                    │
│                  [ Get Started ]                   │
│                                                    │
│  If unauthenticated → Redirect to Sign Up          │
│  If authenticated   → Redirect to Dashboard        │
└────────────────────────────────────────────────────┘
                          │
                          ▼
┌────────────────────────────────────────────────────┐
│            AUTHENTICATION PAGES                     │
│----------------------------------------------------│
│  • Email + Password                                │
│  • Google OAuth                                    │
│  • Facebook OAuth                                  │
│                                                    │
│  Note:                                              │
│  - Google/Facebook use same auth flow               │
│  - Better Auth decides signup vs login              │
│  - End result is always: authenticated              │
└────────────────────────────────────────────────────┘
                          │
                          ▼
┌────────────────────────────────────────────────────┐
│             AUTHENTICATED STATE                    │
│                                                    │
│  • Session / JWT issued by Better Auth              │
│  • UI updates automatically                         │
│  • Header switches to Dashboard / Logout            │
└────────────────────────────────────────────────────┘
                          │
                          ▼
┌────────────────────────────────────────────────────┐
│            PROTECTED AREA (TODOS)                  │
│----------------------------------------------------│
│  /todos                                            │
│  /api/tasks                                        │
│                                                    │
│  Backend Middleware:                               │
│  - Checks session / JWT                            │
│  - Allows or blocks access                         │
│                                                    │
│  Public routes (/ , /login, /signup)               │
│  → NO middleware                                   │
└────────────────────────────────────────────────────┘
