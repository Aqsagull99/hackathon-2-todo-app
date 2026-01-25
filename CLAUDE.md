# Claude Code Rules - Master Orchestrator

This file provides the high-level project roadmap and directs you to the specific phase environments.

## Project Evolution

1.  **Phase I: Console Todo App** (COMPLETED)
    - Source and Docs: `Phase-one/`
    - Status: Uploaded to GitHub subfolder.
2.  **Phase II: Full-Stack Web App** (ACTIVE)
    - Source and Docs: `Phase-two/`
    - Backend: `backend/` (FastAPI)
    - Frontend: `frontend/` (Next.js)
3.  **Phase III: AI Chatbot** (ACTIVE)
    - Technology: OpenAI ChatKit + Agents SDK + MCP Tools
    - Backend: `backend/` (extends Phase II)
    - Frontend: `frontend/` (extends Phase II)
    - Features: Natural language task management via chat

## Project Structure

```
Todo-app/
├── backend/          # FastAPI logic (Phase 2)
├── frontend/         # Next.js UI (Phase 2)
├── Phase-one/        # Legacy Console App (Completed)
├── Phase-two/        # Active Phase 2 Specifications & History
└── CLAUDE.md         # This Orchestrator file
```

## How to Work

### Phase 1 Development (Console App - COMPLETED)
- **Agents**:
  - `todo-main-agent` - Phase I coordinator (in-memory Python console app)
  - `terminal-ui-designer` - Console UI design patterns

- **Skills**:
  - `console-io-skill` - Console input/output handling
  - `task-crud-skill` - Basic task CRUD operations (in-memory)

- **Status**: ✅ Completed and archived in `Phase-one/`

---

### Phase 2 Development (Full-Stack Web App - ACTIVE)
- **Refer to**: `Phase-two/specs/`, `Phase-two/history/prompts/`
- **Guidelines**: `Phase-two/.specify/memory/constitution.md`

- **Agents**:
  - `todo-main-agent-phase2` - Phase II coordinator (Next.js + FastAPI)
  - `requirement-driven-ux-ui-designer` - UI/UX design from requirements

- **Skills**:
  - **Frontend**:
    - `nextjs-skill` - Next.js 16+ App Router patterns
    - `tailwind-skill` - Tailwind CSS utility patterns
    - `signup-skill` - Black-pink glassmorphic signup UI
    - `SignIn-skill` - Sign-in experience matching signup theme
    - `Dashbaord-skill` - Task dashboard UI with same theme
    - `homepage-skill` - Animated homepage with hero section
    - `componenet-ui-skill` - Premium UI components (Quick Add, Next Action)
    - `better-auth-skill` - Better Auth with JWT plugin

  - **Backend**:
    - `fastapi-skill` - FastAPI REST endpoint patterns
    - `sqlmodel-skill` - SQLModel ORM with async operations
    - `neon-db-skill` - Neon PostgreSQL serverless operations
    - `rest-api-skill` - REST API design patterns

  - **Shared**:
    - `task-crud-skill` - Task CRUD operations (database-backed)
    - `mcp-client` - Compiled MCP client skill (98-99% token reduction)

- **Implementation**:
  - Backend: `backend/` (FastAPI + SQLModel + Neon DB)
  - Frontend: `frontend/` (Next.js 16 + Better Auth + Tailwind)

---

### Phase 3 Development (AI Chatbot - ACTIVE)
- **Technology**: OpenAI ChatKit + Agents SDK + MCP Tools
- **Extension of**: Phase II (same codebase)

- **Agents**:
  - `todo-ai-chat-phase3` - Phase III coordinator (chatbot orchestration)
  - `task-reasoning-agent` - Natural language intent detection & reasoning
  - `task-mcp-executor` - MCP tool execution (CRUD via Neon PostgreSQL)
  - `chatkit-ui-agent` - Frontend chat UI implementation
  - `fastapi-chat-agent` - Backend chat API endpoints

- **Skills**:
  - `chatkit-ui-skill` - OpenAI ChatKit conversation UI (React components)
  - `fastapi-chat-skill` - Chat endpoint patterns (stateless API + conversation persistence)
  - `task-intent-skill` - NLP intent detection (Basic + Intermediate features)
  - `task-mcp-skill` - MCP tools (add/list/complete/delete/update/tag_task)

  - **Phase II Skills (Reused)**:
    - `better-auth-skill` - JWT authentication for chat endpoints
    - `neon-db-skill` - Conversation & Message persistence
    - `sqlmodel-skill` - Database models (Conversation, Message)
    - `nextjs-skill` - Chat widget integration in dashboard

- **Feature Coverage**:
  - **Basic**: Add, Delete, Update, View List, Mark Complete (100%)
  - **Intermediate**: Priorities, Tags, Search/Filter, Sort (100%)
  - **Advanced**: Recurring Tasks, Due Dates, Reminders (Phase IV)

- **Implementation**:
  - Backend: `backend/app/agents/`, `backend/app/mcp/`, `backend/app/api/routes/chat.py`
  - Frontend: `frontend/src/components/chat/`, `frontend/src/lib/contexts/ChatContext.tsx`
  - Database: Extend Phase II (add Conversation, Message models)
  - Specs: Create in `Phase-two/specs/005-ai-chatbot/`

---

## Active Specs
- **Phase 1**: Archived in `Phase-one/`
- **Phase 2**: `Phase-two/specs/002-phase2-fullstack/`, `003-todo-web-ui/`, `004-task-organization-intelligence/`
- **Phase 3**: Create in `Phase-two/specs/005-ai-chatbot/`

---

## Agent & Skill Location
All agents and skills are globally available from:
- **Agents**: `.claude/agents/` (11 agents total)
- **Skills**: `.claude/skills/` (21 skills total)


