# Implementation Tasks: AI Chatbot for Natural Language Task Management

**Feature**: 005-ai-chatbot-mcp
**Branch**: `005-ai-chatbot-mcp`
**Generated**: 2026-01-10
**Tech Stack**: Python 3.11, FastAPI, OpenRouter API, Official MCP SDK, OpenAI ChatKit, Next.js 16, Neon PostgreSQL,OpenAI Agents SDK



---

## Implementation Strategy

**MVP Scope**: User Story 1 (P1) - Basic Task Creation via Chat
**Delivery Approach**: Incremental by user story priority (P1 → P2 → P3 → P4 → P5 → P6)
**Parallel Opportunities**: Most user stories are independent after foundational phase completes

**User Story Dependencies**:
- US1 (P1): No dependencies → **START HERE**
- US2 (P2): No dependencies (independent of US1)
- US3 (P3): Requires US2 (needs list to identify tasks)
- US4 (P4): Independent
- US5 (P5): Independent
- US6 (P6): Requires US1, US2, US3 (multi-step reasoning needs all operations)

---

## Phase 1: Setup & Prerequisites

**Goal**: Initialize project structure and install dependencies

### Backend Setup

- [X] T001 Add OpenRouter and MCP dependencies to backend/pyproject.toml (openai>=1.40.0, mcp>=1.0.0, tenacity>=8.0.0, agents>=0.1.0)
- [X] T002 Create backend/app/mcp/ module directory with __init__.py
- [X] T003 Create backend/app/agents/ module directory with __init__.py
- [X] T004 Create backend/app/services/conversation_service.py file
- [X] T005 Create backend/app/core/openrouter.py configuration file
- [X] T006 [P] Update backend/.env.example with OPENROUTER_API_KEY, OPENROUTER_BASE_URL, and OPENROUTER_MODEL variables
- [X] T007 [P] Create backend/logs/ directory for MCP tool logging

### Frontend Setup

- [X] T008 Add ChatKit dependency to frontend/package.json (@openai/chatkit, react-icons)
- [X] T009 Create frontend/src/components/chat/ directory
- [X] T010 Create frontend/src/lib/contexts/ directory for ChatContext
- [X] T011 Create frontend/src/lib/api/chatApi.ts file
- [X] T012 [P] Create frontend/src/styles/chat.module.css for theme customization
- [X] T013 [P] Update frontend/.env.local with NEXT_PUBLIC_CHAT_API_URL

### Database Setup

- [X] T014 Create Alembic migration for Conversation and Message tables in backend/migrations/
- [X] T015 Review migration script (verify indexes: idx_conversations_user_id, idx_messages_conversation_id, idx_messages_created_at)
- [X] T016 Run alembic upgrade head to apply migration

---

## Phase 2: Foundational Components (Blocking Prerequisites)

**Goal**: Implement shared infrastructure required by all user stories

### Database Models

- [X] T017 [P] Implement Conversation model in backend/app/models/conversation.py with SQLModel (conversation_id UUID, user_id FK, created_at, updated_at, relationships)
- [X] T018 [P] Implement Message model in backend/app/models/message.py with SQLModel (message_id UUID, conversation_id FK, role Enum, content Text, tool_calls JSONB, created_at)
- [X] T019 Update backend/app/models/user.py to add conversations relationship

### OpenRouter Client

- [X] T020 Implement OpenRouter client configuration in backend/app/core/openrouter.py using openai-agents-sdk-skill (AsyncOpenAI with base_url="https://openrouter.ai/api/v1", API key from env, HTTP-Referer header)
- [X] T021 [P] Implement retry decorator with tenacity in backend/app/core/openrouter.py (exponential backoff, max 3 attempts, 2-10s wait)

### MCP Server Setup

- [X] T022 Implement Official MCP server initialization in backend/app/mcp/server.py (Server instance with name="todo-mcp-server")
- [X] T023 Implement tool schema registration with @server.list_tools() decorator in backend/app/mcp/server.py (returns list[Tool] with inputSchema)
- [X] T023b Implement tool execution handler with @server.call_tool() decorator in backend/app/mcp/server.py (returns list[TextContent])
- [X] T024 [P] Enable MCP logging in backend/app/mcp/server.py (Python logging module, log_file="logs/mcp_tools.log", log_level="INFO")

### Conversation Service

- [X] T025 Implement create_conversation() in backend/app/services/conversation_service.py (accepts user_id, returns conversation_id)
- [X] T026 Implement get_conversation_history() in backend/app/services/conversation_service.py (fetch last 10 messages, return in chronological order)
- [X] T027 Implement add_message() in backend/app/services/conversation_service.py (store user/assistant message with optional tool_calls, update conversation.updated_at)
- [X] T028 [P] Implement list_user_conversations() in backend/app/services/conversation_service.py (filter by user_id, order by updated_at desc)

---

## Phase 3: User Story 1 (P1) - Basic Task Creation via Chat **[MVP START]**

**Goal**: Users can create tasks by describing them naturally

**Independent Test**: User sends "Add a task to buy groceries" → receives confirmation → task appears in Phase II UI

### MCP Tool Implementation

- [X] T029 [P] [US1] Implement add_task_impl function in backend/app/mcp/tools.py (async function with user_id, title, description, priority, tag_ids params)
- [X] T030 [US1] Validate add_task input (title 1-200 chars, priority enum, tag_ids exist) in tools.py
- [X] T031 [US1] Implement Task creation logic with SQLModel in add_task_impl (insert into tasks table, add TaskTag associations if tag_ids provided)
- [X] T032 [US1] Return structured response from add_task_impl (task_id, status="created", title, tags list, or error dict)
- [X] T033 [US1] Add add_task tool schema to @server.list_tools() in backend/app/mcp/server.py (Tool with name, description, inputSchema)
- [X] T033b [US1] Register add_task_impl in tool_map within @server.call_tool() handler in backend/app/mcp/server.py

### Agent Implementation using openai-agents-sdk-skill

- [X] T034 [US1] Implement TodoChatAgent class in backend/app/agents/chat_agent.py using openai-agents-sdk-skill patterns (init with OpenRouter client, system prompt)
- [X] T035 [US1] Implement get_mcp_function_schemas() method in chat_agent.py using openai-agents-sdk-skill (convert Official MCP tools to OpenAI function format)
- [X] T036 [US1] Implement process_message() method in chat_agent.py using openai-agents-sdk-skill (accepts user_message, conversation_history, user_id)
- [X] T037 [US1] Build message array with system prompt + history + user message in process_message() using openai-agents-sdk-skill patterns
- [X] T038 [US1] Call OpenRouter API with MCP tool schemas in process_message() using openai-agents-sdk-skill (model="openai/gpt-4o", functions=await self.get_mcp_function_schemas(), function_call="auto")
- [X] T039 [US1] Handle function_call response in process_message() using openai-agents-sdk-skill (execute MCP tool via await server.call_tool(), extract result from TextContent)
- [X] T040 [US1] Generate follow-up response from agent after tool execution in process_message() using openai-agents-sdk-skill
- [X] T041 [US1] Return dict with response text and tool_calls array from process_message() using openai-agents-sdk-skill

### Chat API Endpoint

- [X] T041 [US1] Create POST /api/chat endpoint in backend/app/api/routes/chat.py with FastAPI router
- [X] T042 [US1] Implement ChatRequest schema (conversation_id optional UUID, message required string 1-1000 chars) using Pydantic
- [X] T043 [US1] Implement ChatResponse schema (conversation_id UUID, response string, tool_calls array) using Pydantic
- [X] T044 [US1] Add JWT authentication dependency to chat endpoint (get_current_user_id from Better Auth token)
- [X] T045 [US1] Implement chat endpoint logic: get/create conversation_id, fetch history, call agent.process_message()
- [X] T046 [US1] Store user message and assistant response in Message table via conversation_service.add_message()
- [X] T047 [US1] Return ChatResponse with conversation_id, response, tool_calls
- [X] T048 [US1] Add error handling for OpenRouter rate limits (429 status, retry-after header)
- [X] T049 [US1] Add error handling for MCP tool failures (return user-friendly message)

### Frontend ChatKit Integration

- [X] T050 [P] [US1] Implement ChatWidget component in frontend/src/components/chat/ChatWidget.tsx (wrap ChatProvider, ChatMessages, ChatInput from @openai/chatkit)
- [X] T051 [P] [US1] Implement handleSendMessage function in ChatWidget.tsx (POST to /api/chat with JWT bearer token, handle conversation_id state)
- [X] T052 [P] [US1] Apply custom pink/black theme styles to ChatKit components in frontend/src/styles/chat.module.css (glassmorphic background, pink borders, white text)
- [X] T053 [US1] Implement ChatIcon component in frontend/src/components/chat/ChatIcon.tsx (MessageCircle icon from react-icons, fixed bottom-right position, pink bg)
- [X] T054 [US1] Add ChatIcon and ChatWidget to Dashboard page in frontend/src/app/dashboard/page.tsx (state for isChatOpen, slide-in panel)
- [X] T055 [US1] Implement chat API client in frontend/src/lib/api/chatApi.ts (sendMessage function with axios/fetch, JWT header, error handling)

### US1 Integration Test

- [X] T056 [US1] Verify US1 end-to-end: Open Dashboard → Click chat icon → Send "Add a task to buy groceries" → Verify task appears in Phase II task list

---

## Phase 4: User Story 2 (P2) - View and List Tasks via Chat

**Goal**: Users can ask to see their tasks and receive organized summaries

**Independent Test**: User sends "Show me my tasks" → receives formatted list with status, priorities, due dates

### MCP Tool Implementation

- [X] T057 [P] [US2] Implement list_tasks MCP tool in backend/app/mcp/tools.py (async function with user_id, status, priority, tag_query, search_query, sort_by params)
- [X] T058 [US2] Build SQLModel query in list_tasks (filter by user_id, status enum, priority enum, tag_query via join, search_query via ILIKE on title/description)
- [X] T058b [US2] Implement keyword search logic in list_tasks (case-insensitive partial match: WHERE title ILIKE '%{search_query}%' OR description ILIKE '%{search_query}%')
- [X] T059 [US2] Implement sorting logic in list_tasks (order by priority desc, due_date asc, title asc, or created_at desc based on sort_by param)
- [X] T060 [US2] Fetch tags for each task in list_tasks (join TaskTag and Tag, return tag names array)
- [X] T061 [US2] Return structured response from list_tasks (tasks array with id/title/description/completed/priority/tags, count int)
- [X] T062 [US2] Register list_tasks tool with Context7 MCP server using @mcp_server.tool decorator

### Agent Enhancement using openai-agents-sdk-skill

- [X] T063 [US2] Update TodoChatAgent system prompt in backend/app/agents/chat_agent.py to include list_tasks tool examples with search_query usage using openai-agents-sdk-skill patterns
- [X] T063b [US2] Add search intent patterns to system prompt ("find tasks about X", "search for Y", "show tasks containing Z") using openai-agents-sdk-skill
- [X] T064 [US2] Test agent response formatting for task lists (numbered list, status indicators, priority badges) using openai-agents-sdk-skill
- [X] T064b [US2] Test agent search result formatting (highlight matching keywords, show result count) using openai-agents-sdk-skill

### Frontend Enhancement

- [X] T065 [P] [US2] Implement ChatMessage component in frontend/src/components/chat/ChatMessage.tsx to render task lists with formatting (badges for priority, checkmarks for completed)

### US2 Integration Test

- [X] T066 [US2] Verify US2 end-to-end: Send "Show me my tasks" → Verify formatted list displays all tasks with status/priority/tags
- [X] T066b [US2] Verify search functionality: Send "Find tasks about groceries" → Verify only matching tasks displayed with result count

---

## Phase 5: User Story 3 (P3) - Mark Tasks Complete via Chat

**Goal**: Users can mark tasks complete by referencing them naturally

**Independent Test**: User sends "Mark 'Buy groceries' as done" → receives confirmation → task status updates in Phase II UI

**Dependencies**: Requires US2 (user needs to see tasks to identify which to complete)

### MCP Tool Implementation

- [X] T067 [P] [US3] Implement complete_task MCP tool in backend/app/mcp/tools.py (async function with user_id, task_id params)
- [X] T068 [US3] Fetch task and verify ownership in complete_task (filter by task_id AND user_id)
- [X] T069 [US3] Handle task not found error in complete_task (return error dict with status="failed")
- [X] T070 [US3] Handle already completed error in complete_task (check task.completed, return friendly message)
- [X] T071 [US3] Update task.completed=True and task.completed_at=datetime.utcnow() in complete_task
- [X] T072 [US3] Return structured response from complete_task (task_id, status="completed", title)
- [X] T073 [US3] Register complete_task tool with Context7 MCP server using @mcp_server.tool decorator

### Agent Enhancement using openai-agents-sdk-skill

- [X] T074 [US3] Update TodoChatAgent system prompt to handle task references (by title, by number from recent list) using openai-agents-sdk-skill patterns
- [X] T075 [US3] Test agent celebratory responses for task completion ("Great job!", "Well done!") using openai-agents-sdk-skill

### US3 Integration Test

- [X] T076 [US3] Verify US3 end-to-end: Send "Mark 'Buy groceries' as done" → Verify task marked complete in Phase II UI

---

## Phase 6: User Story 4 (P4) - Update Task Details via Chat

**Goal**: Users can modify task titles, descriptions, priorities through conversation

**Independent Test**: User sends "Change 'Buy groceries' to 'Buy organic groceries'" → receives confirmation → task title updates in Phase II UI

### MCP Tool Implementation

- [X] T077 [P] [US4] Implement update_task MCP tool in backend/app/mcp/tools.py (async function with user_id, task_id, title, description, priority params)
- [X] T078 [US4] Fetch task and verify ownership in update_task (filter by task_id AND user_id)
- [X] T079 [US4] Handle task not found error in update_task (return error dict)
- [X] T080 [US4] Apply updates to task fields in update_task (title if provided, description if provided, priority if provided)
- [X] T081 [US4] Update task.updated_at=datetime.utcnow() in update_task
- [X] T082 [US4] Return structured response from update_task (task_id, status="updated", title)
- [X] T083 [US4] Register update_task tool with Context7 MCP server using @mcp_server.tool decorator

### Agent Enhancement using openai-agents-sdk-skill

- [X] T084 [US4] Update TodoChatAgent system prompt to handle ambiguous update requests (ask "which task?" and "what to change?") using openai-agents-sdk-skill

### US4 Integration Test

- [X] T085 [US4] Verify US4 end-to-end: Send "Change 'Buy groceries' to 'Buy organic groceries'" → Verify title updated in Phase II UI

---

## Phase 7: User Story 5 (P5) - Delete Tasks via Chat

**Goal**: Users can remove tasks by asking the chatbot to delete them

**Independent Test**: User sends "Delete the 'Buy groceries' task" → receives confirmation → task removed from Phase II UI

### MCP Tool Implementation

- [X] T086 [P] [US5] Implement delete_task MCP tool in backend/app/mcp/tools.py (async function with user_id, task_id params)
- [X] T087 [US5] Fetch task and verify ownership in delete_task (filter by task_id AND user_id)
- [X] T088 [US5] Handle task not found error in delete_task (return error dict)
- [X] T089 [US5] Store task.title before deletion for response in delete_task
- [X] T090 [US5] Delete task from database in delete_task (session.delete(task), session.commit())
- [X] T091 [US5] Return structured response from delete_task (task_id, status="deleted", title)
- [X] T092 [US5] Register delete_task tool with Context7 MCP server using @mcp_server.tool decorator

### Agent Enhancement using openai-agents-sdk-skill

- [X] T093 [US5] Update TodoChatAgent system prompt to always confirm deletion before executing (ask "Are you sure?") using openai-agents-sdk-skill
- [X] T094 [US5] Test agent handling of cancel requests ("nevermind", "cancel") using openai-agents-sdk-skill

### US5 Integration Test

- [X] T095 [US5] Verify US5 end-to-end: Send "Delete 'Buy groceries'" → Confirm deletion → Verify task removed from Phase II UI

---

## Phase 8: User Story 6 (P6) - Multi-Step Task Workflows

**Goal**: Users can chain multiple operations in natural conversation

**Independent Test**: User sends "Show my tasks and complete the first one" → chatbot executes both operations in sequence

**Dependencies**: Requires US1, US2, US3 (needs multiple operations to chain)

### Agent Enhancement using openai-agents-sdk-skill

- [X] T096 [US6] Update TodoChatAgent to support multi-step reasoning in backend/app/agents/chat_agent.py (detect compound requests) using openai-agents-sdk-skill patterns
- [X] T097 [US6] Implement tool call chaining logic in process_message() using openai-agents-sdk-skill (execute first tool, use result in second tool decision)
- [X] T098 [US6] Handle partial success in multi-step operations using openai-agents-sdk-skill (complete step 1, report error for step 2)
- [X] T099 [US6] Update system prompt to explain multi-step execution strategy to agent using openai-agents-sdk-skill

### US6 Integration Test

- [X] T100 [US6] Verify US6 end-to-end: Send "Show my tasks then mark the first one complete" → Verify both operations execute successfully

---

## Phase 9: Intermediate Features - Tags (Already Trained)

**Goal**: Enable tag/category operations via chat

### MCP Tool Implementation

- [X] T101 [P] Implement add_tag_to_task MCP tool in backend/app/mcp/tools.py (async function with user_id, task_id, tag_name params)
- [X] T102 Get or create tag in add_tag_to_task (check if tag exists for user, create if not)
- [X] T103 Check for existing TaskTag association in add_tag_to_task (return status="already_tagged" if exists)
- [X] T104 Create TaskTag association in add_tag_to_task (insert into task_tags join table)
- [X] T105 Return structured response from add_tag_to_task (task_id, tag_name, status="tagged")
- [X] T106 Register add_tag_to_task tool with Context7 MCP server using @mcp_server.tool decorator

### Agent Enhancement using openai-agents-sdk-skill

- [X] T107 Update TodoChatAgent system prompt to handle tag operations ("tag this as work", "add urgent label") using openai-agents-sdk-skill

---

## Phase 10: Polish & Cross-Cutting Concerns

**Goal**: Production readiness and quality assurance

### Error Handling

- [X] T108 [P] Implement global error handler in backend/app/api/routes/chat.py for database connection errors (catch asyncpg exceptions, return 500 with retry message)
- [X] T109 [P] Implement validation error handler in chat.py (catch Pydantic ValidationError, return 400 with field-specific messages)
- [X] T110 [P] Add timeout handling for OpenRouter API calls in backend/app/core/openrouter.py (timeout=10.0 seconds)
- [X] T111 [P] Implement rate limit handling in chat.py (detect 429 from OpenRouter, return user-friendly backoff message)

### Security

- [X] T112 [P] Add input sanitization for Message.content in backend/app/services/conversation_service.py (max 10,000 chars, strip HTML tags)
- [X] T113 [P] Verify all MCP tools enforce user_id filter in backend/app/mcp/tools.py (prevent cross-user data access)
- [X] T114 [P] Add CORS configuration for chat endpoint in backend/app/main.py (allow frontend origin)

### Logging & Monitoring

- [X] T115 [P] Add structured logging for chat requests in backend/app/api/routes/chat.py (log user_id, conversation_id, message length, response time)
- [X] T116 [P] Verify MCP tool execution logging in backend/app/mcp/server.py (confirm log_file writes tool name, params, results)
- [X] T117 [P] Add error logging for tool failures in backend/app/agents/chat_agent.py (log exception details, tool name, params)

### Performance

- [X] T118 [P] Configure Neon connection pooling in backend/app/core/database.py (pool_size=10, max_overflow=20)
- [X] T119 [P] Add conversation history limit to get_conversation_history() in conversation_service.py (default limit=10, max=50)
- [X] T120 [P] Implement lazy loading for ChatWidget in frontend/src/app/dashboard/page.tsx (dynamic import with ssr=false)

### Documentation

- [X] T121 [P] Add docstrings to all MCP tools in backend/app/mcp/tools.py (parameters, return types, error conditions)
- [X] T122 [P] Add JSDoc comments to ChatWidget component in frontend/src/components/chat/ChatWidget.tsx (props, usage examples)
- [X] T123 [P] Update backend README.md with chat endpoint documentation (curl examples, response schemas)

### Deployment Preparation

- [X] T124 Verify all environment variables in backend/.env.example (OPENROUTER_API_KEY, OPENROUTER_BASE_URL, OPENROUTER_MODEL, DATABASE_URL, JWT_SECRET)
- [X] T125 Verify all environment variables in frontend/.env.example (NEXT_PUBLIC_API_URL, NEXT_PUBLIC_CHAT_API_URL)
- [X] T126 Create Railway deployment configuration for backend (Procfile, runtime.txt)
- [X] T127 Create Vercel deployment configuration for frontend (vercel.json with rewrites for /api)

---

## Summary

**Total Tasks**: 135 (updated for Official MCP SDK + Intermediate Level search feature + OpenAI Agents SDK integration)
**MVP Tasks (US1)**: T001-T056 (58 tasks) - **+2 tasks for Official MCP SDK + Additional tasks for OpenAI Agents SDK**
**Parallel Opportunities**: 31 tasks marked [P]

**Task Breakdown by User Story**:
- Setup & Foundational: 29 tasks (T001-T028) - **+1 task for Official MCP SDK handler (T023b)**
- US1 (P1 - MVP): 29 tasks (T029-T056) - **+1 task for tool registration (T033b) + Additional tasks for OpenAI Agents SDK integration**
- US2 (P2): 14 tasks (T057-T066b) - **UPDATED: Added keyword search (4 new tasks) + OpenAI Agents SDK enhancements**
- US3 (P3): 10 tasks (T067-T076) - **+ OpenAI Agents SDK enhancements**
- US4 (P4): 9 tasks (T077-T085) - **+ OpenAI Agents SDK enhancements**
- US5 (P5): 10 tasks (T086-T095) - **+ OpenAI Agents SDK enhancements**
- US6 (P6): 5 tasks (T096-T100) - **+ OpenAI Agents SDK enhancements**
- Tags (Intermediate): 7 tasks (T101-T107) - **+ OpenAI Agents SDK enhancements**
- Polish: 20 tasks (T108-T127)

**Technology Changes**:
- ❌ Context7 MCP Server (third-party wrapper)
- ✅ **Official MCP SDK** from github.com/modelcontextprotocol/python-sdk (Hackathon requirement)
- ✅ **OpenAI Agents SDK** with openai-agents-sdk-skill for agent creation (using OpenRouter API)

**Intermediate Level Features Added**:
- ✅ Priorities (integrated in add_task)
- ✅ Tags (Phase 9: add_tag_to_task tool)
- ✅ Search (Phase 4: search_query parameter in list_tasks - **NEW**)
- ✅ Filter (status, priority, tag filters in list_tasks)
- ✅ Sort (priority, due_date, title, created_at options)

**Independent Test Criteria**:
- US1: Task creation via chat appears in Phase II UI ✅
- US2: Task list retrieval displays formatted results ✅
- US3: Task completion updates Phase II UI status ✅
- US4: Task updates reflect in Phase II UI ✅
- US5: Task deletion removes from Phase II UI ✅
- US6: Multi-step operations execute sequentially ✅

**Parallel Execution Examples**:
- Phase 2 Models: T017 (Conversation) + T018 (Message) can run in parallel
- Phase 2 Services: T025, T026, T027, T028 can run after models complete
- US1 MCP Tool: T029-T032 can run in parallel with agent T034-T040
- US1 Frontend: T050-T052 can run in parallel with backend implementation
- Polish Tasks: Most T108-T123 can run in parallel

**Suggested MVP Scope**: Phase 1 (Setup) + Phase 2 (Foundational) + Phase 3 (US1) = 56 tasks
**Estimated MVP Time**: 2-3 days for experienced developer

**Dependencies Flowchart**:
```
Phase 1 (Setup) → Phase 2 (Foundational) → [Phase 3 (US1) MVP]
                                          ↘ Phase 4 (US2) ⤵
                                            Phase 5 (US3) ← depends on US2
                                          ↘ Phase 6 (US4)
                                          ↘ Phase 7 (US5)
                                          ↘ Phase 8 (US6) ← depends on US1, US2, US3
                                          ↘ Phase 9 (Tags)
                                          ↘ Phase 10 (Polish)
```

---

**Implementation Order Recommendation**:
1. **Week 1**: Setup (Phase 1) + Foundational (Phase 2) + US1 (Phase 3) → MVP COMPLETE
2. **Week 2**: US2 (Phase 4) + US3 (Phase 5) → List & Complete
3. **Week 3**: US4 (Phase 6) + US5 (Phase 7) → Update & Delete
4. **Week 4**: US6 (Phase 8) + Tags (Phase 9) + Polish (Phase 10) → Production Ready

---

**Generated**: 2026-01-10 by `/sp.tasks` command
**Based on**: spec.md, plan.md, data-model.md, contracts/

