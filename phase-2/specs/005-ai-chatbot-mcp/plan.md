# Implementation Plan: AI Chatbot for Natural Language Task Management (Phase III)

**Branch**: `005-ai-chatbot-mcp` | **Date**: 2026-01-10 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/phase-2/specs/005-ai-chatbot-mcp/spec.md` + User requirements for MCP integration with OpenRouter and Context7

**Note**: This plan follows the `/sp.plan` workflow and incorporates user-specified requirements for Phase III chatbot implementation.

## Summary

Add an AI-powered conversational interface to the existing Todo application that enables users to manage tasks through natural language. The chatbot integrates with the Phase II web application without UI redesign, using **OpenRouter API** for LLM access, **Official MCP SDK** for tool orchestration, **OpenAI ChatKit** for frontend UI, and maintains the **stateless architecture** principle with all state persisted in Neon PostgreSQL. OpenAI Agents SDK for agent creation



**Primary Requirement**: Natural language task management (add, list, update, complete, delete) via chat interface integrated into existing Dashboard.

**Technical Approach**:
1. Backend: FastAPI chat endpoint + Official MCP SDK server exposing 6 stateless task tools
2. AI: OpenRouter API (via OpenAI Agents SDK) for natural language understanding
3. Frontend: OpenAI ChatKit components integrated into Dashboard with React icon entry point
4. Database: Extend Neon PostgreSQL schema with Conversation and Message tables (no changes to Task schema)

## Technical Context

**Language/Version**: Python 3.11 (backend), TypeScript/JavaScript (frontend with Next.js 16)
**Primary Dependencies**:
- **Backend**: FastAPI 0.100+, SQLModel 0.14+, OpenAI SDK 1.40+, Official MCP SDK (mcp>=1.0.0), asyncio
- **Frontend**: Next.js 16 (App Router), OpenAI ChatKit, React 18, Tailwind CSS, Better Auth Client
- **AI/MCP**: Official MCP SDK, OpenRouter API (accessed via OpenAI SDK), OpenAI Agents SDK

**Storage**: Neon Serverless PostgreSQL (existing Phase II database + new Conversation/Message tables)

**Testing**:
- **Backend**: pytest (async tests for MCP tools, chat endpoint integration)
- **Frontend**: Jest + React Testing Library (ChatKit component tests)
- **E2E**: Playwright (full conversation flow tests)

**Target Platform**:
- **Backend**: Linux server (Railway/Render deployment, same as Phase II)
- **Frontend**: Web browsers (Chrome, Firefox, Safari) via Vercel deployment

**Project Type**: Web application (extends existing Phase II full-stack app)

**Performance Goals**:
- Chat response latency: <5 seconds (95th percentile) from user message to assistant response
- MCP tool execution: <1 second per tool call
- Conversation history retrieval: <500ms from Neon DB
- Concurrent users: 50 simultaneous conversations without degradation

**Constraints**:
- **No Phase II UI redesign**: Existing Dashboard, Sidebar, Task List remain unchanged
- **Stateless servers**: No in-memory session state; conversation context reconstructed from DB on each request
- **MCP-only agent actions**: AI agent MUST NOT directly access database; all task operations via MCP tools
- **No agent hallucination**: All task operations require actual MCP tool invocation (logged and auditable)
- **OpenRouter API**: Use OpenRouter API key (not direct OpenAI key)
- **Official MCP SDK**: Use Official MCP SDK from github.com/modelcontextprotocol/python-sdk (Hackathon requirement)
- **Dashboard integration**: Chatbot accessed via React icon on Dashboard (not separate route)

**Scale/Scope**:
- **Users**: Support 10k registered users with independent conversations
- **Conversations**: ~100 messages per conversation (typical use case)
- **Tasks**: Existing Phase II task data (~10k tasks across all users)
- **MCP Tools**: 6 stateless tools (add_task, list_tasks, complete_task, delete_task, update_task, add_tag_to_task)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### ✅ Principle I: Spec-First Development
- **Status**: PASS
- **Evidence**: Feature specification (`spec.md`) completed with 6 user stories, 34 functional requirements, 10 success criteria
- **Verification**: Spec reviewed and approved before planning phase

### ✅ Principle II: Incremental Phase Evolution
- **Status**: PASS
- **Evidence**: Phase III extends Phase II without breaking changes:
  - No modifications to existing Task, Tag, User schemas
  - New Conversation/Message tables added separately
  - Phase II UI (Dashboard, Sidebar, Task List) remains unchanged
  - Chatbot integrated via new Dashboard icon (additive change)
- **Verification**: Backward compatibility maintained; Phase II features fully functional

### ✅ Principle III: Stateless Architecture with Persistent State
- **Status**: PASS
- **Evidence**:
  - FastAPI chat endpoint reconstructs conversation context from DB on each request
  - No server-side session storage or in-memory conversation cache
  - OpenRouter API calls are stateless (no retained context)
  - Server restarts have zero impact (conversation history persists in Neon DB)
- **Verification**: FR-018 to FR-020 explicitly enforce stateless design

### ✅ Principle IV: MCP Tool Architecture
- **Status**: PASS
- **Evidence**:
  - AI agent interacts ONLY through Official MCP SDK tools (6 tools defined)
  - All tools are stateless functions (input → DB operation → output)
  - Agent cannot directly query or modify database
  - Tool invocations logged in Message.tool_calls (JSONB field)
- **Verification**: FR-008 to FR-012 enforce MCP-only access; constitution constraint "No AI hallucinated actions"

### ✅ Principle V: Natural Language Interface
- **Status**: PASS
- **Evidence**:
  - Supports all Phase I & II CRUD operations via chat (6 user stories P1-P6)
  - Multi-step reasoning enabled (FR-006: "show tasks then delete first one")
  - Clarifying questions for ambiguous input (FR-006)
  - Friendly conversational responses (FR-021 to FR-023)
- **Verification**: Spec user scenarios cover conversational task management

### ✅ Principle VI: User-Centric Simplicity
- **Status**: PASS
- **Evidence**:
  - Chat interface uses plain language (no technical jargon)
  - Chatbot entry via single Dashboard icon (no configuration)
  - Error messages guide users to resolution (FR-023, FR-029)
  - OpenAI ChatKit provides familiar chat UX
- **Verification**: Target users are non-technical (spec states clearly)

### ✅ Technology Standards (Phase III)
- **Status**: PASS
- **Evidence**:
  - ✅ Frontend: OpenAI ChatKit (as specified)
  - ✅ Backend: Python FastAPI with async/await (existing Phase II)
  - ✅ **AI**: OpenAI Agents SDK with OpenRouter API (constitution requirement + user preference)
  - ✅ **MCP**: Official MCP SDK from github.com/modelcontextprotocol/python-sdk (constitution requirement + Hackathon requirement)
  - ✅ **LLM Access**: OpenRouter API via OpenAI SDK compatibility (user preference for model access)
  - ✅ Database: Neon PostgreSQL via SQLModel (existing Phase II)
  - ✅ Authentication: Better Auth with JWT (existing Phase II)
- **Clarification**: Constitution mandates "Official MCP SDK". Using github.com/modelcontextprotocol/python-sdk as required. OpenRouter API used for LLM model access (compatible with OpenAI SDK).

### ⚠️ Phase Transition Protocol
- **Status**: PENDING (GATE WILL RE-EVALUATE AFTER PHASE 1 DESIGN)
- **Current Phase (Phase II) Status**:
  - ✅ Fully functional and tested (Task CRUD, Authentication, Dashboard UI)
  - ✅ Specifications reviewed and approved (specs 002, 003, 004 complete)
  - ⚠️ ADRs: Need to check if significant Phase II decisions documented
  - ✅ No breaking changes planned for Phase III
  - ✅ Data model extension documented (Conversation + Message tables)
- **Action Required**: Verify Phase II ADR status before proceeding to implementation

### ✅ Constraints Compliance
- ✅ **No UI redesign in Phase III**: Dashboard layout unchanged; chatbot added as side panel
- ✅ **No manual coding**: All implementation via Claude Code agents/skills
- ✅ **No AI hallucinated actions**: MCP tools enforce deterministic operations
- ✅ **No features outside scope**: Chatbot implements Phase I & II task parity only (no new features)

### Quality Gates (To Be Verified Post-Implementation)
- [ ] Specification review: ✅ COMPLETE
- [ ] Architecture review: 🔄 IN PROGRESS (this plan)
- [ ] Implementation review: ⏳ PENDING
- [ ] Functional testing: ⏳ PENDING
- [ ] Conversation persistence testing: ⏳ PENDING

**GATE DECISION**: ✅ **PASS** - Proceed to Phase 0 (Research)

**Re-evaluation Trigger**: After Phase 1 design complete (data-model.md, contracts/, quickstart.md generated)

## Project Structure

### Documentation (this feature)

```text
phase-2/specs/005-ai-chatbot-mcp/
├── spec.md              # Feature specification (COMPLETE)
├── plan.md              # This file (IN PROGRESS - Phase 0/1)
├── research.md          # Phase 0 output (PENDING)
├── data-model.md        # Phase 1 output (PENDING)
├── quickstart.md        # Phase 1 output (PENDING)
├── contracts/           # Phase 1 output (PENDING)
│   ├── chat-api.yaml           # OpenAPI spec for chat endpoints
│   ├── mcp-tools.json          # MCP tool schemas (6 tools)
│   └── frontend-types.ts       # TypeScript types for ChatKit integration
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created yet)
```

### Source Code (repository root: phase-2/)

```text
phase-2/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/
│   │   │       └── chat.py                    # NEW: Chat endpoint
│   │   ├── models/
│   │   │   ├── conversation.py                # NEW: Conversation model
│   │   │   ├── message.py                     # NEW: Message model
│   │   │   ├── task.py                        # EXISTING: No changes
│   │   │   ├── tag.py                         # EXISTING: No changes
│   │   │   └── user.py                        # EXISTING: No changes
│   │   ├── mcp/
│   │   │   ├── __init__.py                    # NEW: MCP module
│   │   │   ├── server.py                      # NEW: Context7 MCP server integration
│   │   │   ├── tools.py                       # NEW: 6 MCP tool implementations
│   │   │   └── schemas.py                     # NEW: Tool parameter schemas
│   │   ├── agents/
│   │   │   ├── __init__.py                    # NEW: Agents module
│   │   │   ├── chat_agent.py                  # NEW: OpenAI Agent with OpenRouter using openai-agents-sdk-skill
│   │   │   └── config.py                      # NEW: Agent configuration
│   │   ├── services/
│   │   │   └── conversation_service.py        # NEW: Conversation CRUD logic
│   │   └── core/
│   │       └── openrouter.py                  # NEW: OpenRouter API client config using openai-agents-sdk-skill
│   ├── tests/
│   │   ├── test_mcp_tools.py                  # NEW: MCP tool unit tests
│   │   ├── test_chat_endpoint.py              # NEW: Chat API integration tests
│   │   └── test_conversation_service.py       # NEW: Conversation service tests
│   └── .env                                    # UPDATE: Add OPENROUTER_API_KEY
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── chat/
│   │   │   │   ├── ChatWidget.tsx             # NEW: ChatKit wrapper component
│   │   │   │   ├── ChatMessage.tsx            # NEW: Message rendering
│   │   │   │   ├── ChatInput.tsx              # NEW: Message input field
│   │   │   │   └── ChatIcon.tsx               # NEW: Dashboard icon trigger
│   │   │   ├── dashboard/                     # EXISTING: No changes
│   │   │   ├── tasks/                         # EXISTING: No changes
│   │   │   └── layout/                        # EXISTING: No changes
│   │   ├── app/
│   │   │   └── dashboard/
│   │   │       └── page.tsx                   # UPDATE: Add ChatIcon component
│   │   ├── lib/
│   │   │   ├── contexts/
│   │   │   │   └── ChatContext.tsx            # NEW: Chat state management
│   │   │   ├── hooks/
│   │   │   │   └── useChat.ts                 # NEW: Chat API hook
│   │   │   └── api/
│   │   │       └── chatApi.ts                 # NEW: Chat endpoint client
│   │   └── styles/
│   │       └── chat.module.css                # NEW: ChatKit custom styles
│   ├── public/
│   │   └── icons/
│   │       └── chat-icon.svg                  # NEW: Chat icon asset
│   └── .env.local                              # UPDATE: Add NEXT_PUBLIC_API_URL
│
└── .env.example                                # UPDATE: Document new env vars
```

**Structure Decision**: **Web application (Option 2)** - Phase III extends the existing Phase II full-stack architecture with new backend MCP layer and frontend ChatKit integration. No separate Phase III directory; all code integrated into existing `backend/` and `frontend/` directories following Phase II conventions.

**Key Directories**:
- `backend/app/mcp/`: MCP tool implementations using Context7 server
- `backend/app/agents/`: OpenAI Agent configuration using openai-agents-sdk-skill with OpenRouter API
- `backend/app/models/`: New Conversation and Message SQLModel models
- `frontend/src/components/chat/`: OpenAI ChatKit UI components
- `frontend/src/lib/contexts/`: Chat state management (React Context)

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| ⚠️ **OpenRouter API instead of direct OpenAI** | User requirement: Use OpenRouter for cost optimization and multi-model access | Direct OpenAI API would increase costs and limit model selection flexibility |
| ⚠️ **Context7 MCP Server instead of custom** | User requirement: Leverage pre-built Context7 MCP server for faster implementation | Building custom MCP server would delay delivery and increase maintenance burden |

**Justification**: These deviations align with constitutional principles (statelessness, MCP architecture) while accommodating user's infrastructure preferences. OpenRouter API is OpenAI-compatible (uses same SDK with different base URL), maintaining technology standard compliance.

**Risk Mitigation**:
- OpenRouter API documentation will be researched in Phase 0 to confirm OpenAI SDK compatibility
- Context7 MCP Server setup will be validated in Phase 0 to ensure tool orchestration works as expected

---

## Phase 0: Research & Investigation

**Goal**: Resolve all "NEEDS CLARIFICATION" items from Technical Context and validate user-specified technologies (OpenRouter, Context7 MCP).

### Research Tasks

#### 1. OpenRouter API Integration Research
**Question**: How to configure OpenAI SDK to use OpenRouter API?

**Research Areas**:
- OpenRouter API documentation: Base URL, authentication headers, model selection
- OpenAI SDK configuration: Custom base URL support, API key handling
- Compatibility verification: Which OpenAI SDK features work with OpenRouter (function calling, streaming)
- Rate limiting and error handling differences

**Deliverable**: `research.md` section documenting OpenRouter setup with OpenAI SDK

#### 2. Context7 MCP Server Setup Research
**Question**: How to integrate Context7 MCP server with FastAPI backend?

**Research Areas**:
- Context7 MCP Server documentation: Installation, configuration, tool registration
- MCP protocol specification: Tool schema format, invocation protocol, response handling
- FastAPI integration patterns: Async MCP calls, error propagation, tool execution logging
- Comparison vs Official MCP SDK: Why Context7 chosen, feature parity verification

**Deliverable**: `research.md` section documenting Context7 integration architecture

#### 3. OpenAI Agents SDK with MCP Tools
**Question**: How to configure OpenAI Agents SDK to invoke MCP tools via Context7?

**Research Areas**:
- OpenAI Agents SDK documentation: Agent initialization, tool registration, conversation management
- Function calling with MCP: Mapping MCP tools to OpenAI function schemas
- Conversation context management: How to pass conversation history, message reconstruction
- Multi-step reasoning implementation: Chaining tool calls, handling tool failures
- **NEW**: Integration with openai-agents-sdk-skill for proper agent creation using OpenRouter configuration

**Deliverable**: `research.md` section documenting Agent + MCP integration pattern using openai-agents-sdk-skill

#### 4. OpenAI ChatKit Frontend Integration
**Question**: How to integrate ChatKit into existing Next.js 16 Dashboard?

**Research Areas**:
- OpenAI ChatKit documentation: Installation (npm package), React component usage
- Dashboard integration: Side panel/modal vs embedded chat, state management
- Styling consistency: Matching existing pink/black glassmorphic theme with ChatKit components
- Message streaming: Real-time message display, typing indicators

**Deliverable**: `research.md` section documenting ChatKit integration approach

#### 5. Conversation Persistence Strategy
**Question**: How to store and retrieve conversation history in Neon PostgreSQL for stateless architecture?

**Research Areas**:
- Conversation data model: Conversation vs Message entity relationship, JSONB for tool_calls
- Query optimization: Fetching last N messages efficiently, indexing strategy
- Stateless request pattern: Full context reconstruction on each request, performance implications
- Conversation lifecycle: Creation, resumption, archival/deletion policies

**Deliverable**: `research.md` section documenting conversation persistence design

#### 6. Best Practices for Stateless MCP Tools
**Question**: How to implement 6 MCP tools (add_task, list_tasks, etc.) as pure stateless functions?

**Research Areas**:
- MCP tool patterns: Input validation, error handling, response formatting
- Database interaction: SQLModel async queries, transaction management, user isolation
- Tool testing: Unit tests for each tool, mocking DB layer, contract testing
- Tool documentation: Parameter schemas, example invocations, error codes

**Deliverable**: `research.md` section documenting MCP tool implementation guidelines

### Expected Research Outcomes

After Phase 0, `research.md` MUST contain:

1. **Decision Matrix**: OpenRouter vs Direct OpenAI, Context7 vs Official MCP SDK
2. **Architecture Diagrams**:
   - Request flow: User message → ChatKit → FastAPI → Agent → MCP Tool → DB → Response
   - Stateless request cycle: Context reconstruction from DB
3. **Code Examples**:
   - OpenRouter API client configuration (Python)
   - Context7 MCP tool registration (Python)
   - ChatKit React component setup (TypeScript)
   - **NEW**: OpenAI Agents SDK implementation using openai-agents-sdk-skill
4. **Risk Assessment**: OpenRouter rate limits, Context7 stability, ChatKit browser compatibility
5. **Performance Benchmarks**: Expected latencies for each system component

**Gate**: Phase 0 complete when all NEEDS CLARIFICATION resolved and research.md written.

---

## Phase 1: Design & Contracts

**Prerequisites**: `research.md` complete with all technology decisions validated

### Phase 1.1: Data Model Design

**Goal**: Extend Phase II database schema with Conversation and Message entities

**Output**: `data-model.md` with SQLModel definitions

#### New Entities

**Conversation Entity**:
```python
class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"

    conversation_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    messages: List["Message"] = Relationship(back_populates="conversation")
    user: "User" = Relationship(back_populates="conversations")
```

**Message Entity**:
```python
class Message(SQLModel, table=True):
    __tablename__ = "messages"

    message_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    conversation_id: uuid.UUID = Field(foreign_key="conversations.conversation_id", nullable=False)
    role: str = Field(sa_column=Column(Enum("user", "assistant", name="message_role")))
    content: str = Field(nullable=False)  # Message text
    tool_calls: Optional[dict] = Field(default=None, sa_column=Column(JSON))  # JSONB array
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    conversation: Conversation = Relationship(back_populates="messages")
```

**Indexes**:
- `idx_conversations_user_id`: ON conversations(user_id)
- `idx_messages_conversation_id`: ON messages(conversation_id)
- `idx_messages_created_at`: ON messages(created_at) for ordering

**Validation Rules**:
- `role`: MUST be "user" or "assistant" (enforced by Enum)
- `content`: MUST NOT be empty (max 10,000 characters)
- `tool_calls`: MUST be valid JSON array of `{"tool": str, "parameters": dict, "result": dict}`

**Existing Entities (No Changes)**:
- Task, Tag, TaskTag, User schemas remain unchanged from Phase II

### Phase 1.2: API Contracts

**Goal**: Define FastAPI chat endpoint and MCP tool schemas

**Output**: `contracts/` directory with OpenAPI and MCP schemas

#### Chat API Contract (`contracts/chat-api.yaml`)

```yaml
openapi: 3.0.0
info:
  title: Todo Chat API
  version: 1.0.0
paths:
  /api/chat:
    post:
      summary: Send message to chatbot
      security:
        - BearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                conversation_id:
                  type: string
                  format: uuid
                  description: Existing conversation ID (omit for new conversation)
                message:
                  type: string
                  minLength: 1
                  maxLength: 1000
              required:
                - message
      responses:
        '200':
          description: Chat response
          content:
            application/json:
              schema:
                type: object
                properties:
                  conversation_id:
                    type: string
                    format: uuid
                  response:
                    type: string
                  tool_calls:
                    type: array
                    items:
                      type: object
                      properties:
                        tool:
                          type: string
                        parameters:
                          type: object
                        result:
                          type: object
        '401':
          description: Unauthorized
        '429':
          description: Rate limit exceeded
        '500':
          description: Internal server error

  /api/conversations:
    get:
      summary: List user's conversations
      security:
        - BearerAuth: []
      responses:
        '200':
          description: List of conversations
          content:
            application/json:
              schema:
                type: object
                properties:
                  conversations:
                    type: array
                    items:
                      type: object
                      properties:
                        conversation_id:
                          type: string
                          format: uuid
                        created_at:
                          type: string
                          format: date-time
                        last_message:
                          type: string

  /api/conversations/{conversation_id}/messages:
    get:
      summary: Get conversation history
      security:
        - BearerAuth: []
      parameters:
        - name: conversation_id
          in: path
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '200':
          description: Conversation messages
          content:
            application/json:
              schema:
                type: object
                properties:
                  messages:
                    type: array
                    items:
                      type: object
                      properties:
                        message_id:
                          type: string
                          format: uuid
                        role:
                          type: string
                          enum: [user, assistant]
                        content:
                          type: string
                        created_at:
                          type: string
                          format: date-time

components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
```

#### MCP Tools Contract (`contracts/mcp-tools.json`)

```json
{
  "tools": [
    {
      "name": "add_task",
      "description": "Create a new task for the user",
      "parameters": {
        "type": "object",
        "properties": {
          "user_id": {
            "type": "string",
            "format": "uuid",
            "description": "User identifier"
          },
          "title": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200,
            "description": "Task title"
          },
          "description": {
            "type": "string",
            "maxLength": 1000,
            "description": "Optional task description"
          },
          "priority": {
            "type": "string",
            "enum": ["high", "medium", "low"],
            "default": "medium",
            "description": "Task priority level"
          },
          "tag_ids": {
            "type": "array",
            "items": {
              "type": "integer"
            },
            "description": "Optional list of tag IDs"
          }
        },
        "required": ["user_id", "title"]
      },
      "returns": {
        "type": "object",
        "properties": {
          "task_id": {"type": "integer"},
          "status": {"type": "string", "enum": ["created"]},
          "title": {"type": "string"},
          "tags": {"type": "array", "items": {"type": "string"}}
        }
      }
    },
    {
      "name": "list_tasks",
      "description": "Retrieve user's tasks with optional filters",
      "parameters": {
        "type": "object",
        "properties": {
          "user_id": {"type": "string", "format": "uuid"},
          "status": {
            "type": "string",
            "enum": ["all", "pending", "completed"],
            "default": "all"
          },
          "priority": {
            "type": "string",
            "enum": ["high", "medium", "low"]
          },
          "tag_query": {
            "type": "string",
            "description": "Filter by tag name"
          },
          "sort_by": {
            "type": "string",
            "enum": ["priority", "due_date", "title", "created_at"],
            "default": "created_at"
          }
        },
        "required": ["user_id"]
      },
      "returns": {
        "type": "object",
        "properties": {
          "tasks": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {"type": "integer"},
                "title": {"type": "string"},
                "completed": {"type": "boolean"},
                "priority": {"type": "string"},
                "tags": {"type": "array", "items": {"type": "string"}}
              }
            }
          },
          "count": {"type": "integer"}
        }
      }
    },
    {
      "name": "complete_task",
      "description": "Mark a task as complete",
      "parameters": {
        "type": "object",
        "properties": {
          "user_id": {"type": "string", "format": "uuid"},
          "task_id": {"type": "integer"}
        },
        "required": ["user_id", "task_id"]
      },
      "returns": {
        "type": "object",
        "properties": {
          "task_id": {"type": "integer"},
          "status": {"type": "string", "enum": ["completed"]},
          "title": {"type": "string"}
        }
      }
    },
    {
      "name": "delete_task",
      "description": "Permanently delete a task",
      "parameters": {
        "type": "object",
        "properties": {
          "user_id": {"type": "string", "format": "uuid"},
          "task_id": {"type": "integer"}
        },
        "required": ["user_id", "task_id"]
      },
      "returns": {
        "type": "object",
        "properties": {
          "task_id": {"type": "integer"},
          "status": {"type": "string", "enum": ["deleted"]},
          "title": {"type": "string"}
        }
      }
    },
    {
      "name": "update_task",
      "description": "Update task fields",
      "parameters": {
        "type": "object",
        "properties": {
          "user_id": {"type": "string", "format": "uuid"},
          "task_id": {"type": "integer"},
          "title": {"type": "string"},
          "description": {"type": "string"},
          "priority": {"type": "string", "enum": ["high", "medium", "low"]}
        },
        "required": ["user_id", "task_id"]
      },
      "returns": {
        "type": "object",
        "properties": {
          "task_id": {"type": "integer"},
          "status": {"type": "string", "enum": ["updated"]},
          "title": {"type": "string"}
        }
      }
    },
    {
      "name": "add_tag_to_task",
      "description": "Add or create a tag and associate with task",
      "parameters": {
        "type": "object",
        "properties": {
          "user_id": {"type": "string", "format": "uuid"},
          "task_id": {"type": "integer"},
          "tag_name": {"type": "string"}
        },
        "required": ["user_id", "task_id", "tag_name"]
      },
      "returns": {
        "type": "object",
        "properties": {
          "task_id": {"type": "integer"},
          "tag_name": {"type": "string"},
          "status": {"type": "string", "enum": ["tagged", "already_tagged"]}
        }
      }
    }
  ]
}
```

#### Frontend Types (`contracts/frontend-types.ts`)

```typescript
// Chat API types
export interface ChatRequest {
  conversation_id?: string;
  message: string;
}

export interface ChatResponse {
  conversation_id: string;
  response: string;
  tool_calls: Array<{
    tool: string;
    parameters: Record<string, any>;
    result: Record<string, any>;
  }>;
}

// MCP tool types
export interface MCPTool {
  name: string;
  description: string;
  parameters: Record<string, any>;
  returns: Record<string, any>;
}

// Conversation types
export interface Conversation {
  conversation_id: string;
  created_at: string;
  updated_at: string;
}

export interface Message {
  message_id: string;
  conversation_id: string;
  role: 'user' | 'assistant';
  content: string;
  tool_calls?: Array<{
    tool: string;
    parameters: Record<string, any>;
    result: Record<string, any>;
  }>;
  created_at: string;
}

// ChatKit integration types
export interface ChatKitConfig {
  theme?: 'light' | 'dark';
  initialMessages?: Array<{role: 'user' | 'assistant'; content: string}>;
  onMessage?: (message: {role: 'user' | 'assistant'; content: string}) => void;
  onError?: (error: Error) => void;
}
```

### Phase 1.3: OpenAI Agents SDK Design

**Goal**: Design the OpenAI Agent implementation using openai-agents-sdk-skill with OpenRouter configuration

**Output**: `contracts/agent-design.md` detailing the agent architecture

#### Agent Architecture

**OpenAI Agent Configuration**:
```python
# Using openai-agents-sdk-skill for proper agent creation
import os
from agents import Agent, Runner
from agents import AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig

class TodoChatAgent:
    """AI agent for task management using openai-agents-sdk-skill patterns."""
    
    def __init__(self):
        # Use OpenRouter configuration from environment
        openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
        openrouter_base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
        openrouter_model = os.getenv("OPENROUTER_MODEL", "mistralai/devstral-2512:free")
        
        # Create AsyncOpenAI client with OpenRouter
        client = AsyncOpenAI(
            api_key=openrouter_api_key,
            base_url=openrouter_base_url,
        )
        
        # Configure model with OpenRouter
        model = OpenAIChatCompletionsModel(
            model=openrouter_model,
            openai_client=client
        )
        
        # Create run configuration using openai-agents-sdk-skill patterns
        self.config = RunConfig(
            model=model,
            model_provider=client
        )
        
        # Create agent with MCP tools
        self.agent = Agent(
            name="Todo Assistant",
            instructions="You are a helpful task management assistant. Use available MCP tools to manage user tasks.",
            tools=self.get_mcp_tools()  # MCP tools from Context7 server
        )
    
    def get_mcp_tools(self):
        """Get MCP tools from Context7 MCP server."""
        # This will be connected to the Context7 MCP server
        # that exposes the 6 task management tools
        pass
    
    async def process_message(self, message: str, context: dict):
        """Process user message using OpenAI Agents SDK."""
        # Run the agent with the message
        result = await Runner.run(
            self.agent,
            message,
            config=self.config  # Use OpenRouter configuration
        )
        return result
```

**Integration Points**:
- Agent initialization uses openai-agents-sdk-skill patterns
- OpenRouter API key from environment variables
- MCP tools connected via Context7 server
- Stateless design with conversation context passed on each call

**Design Considerations**:
- Use `openai-agents-sdk-skill` for proper agent creation patterns
- Implement proper error handling for OpenRouter API
- Integrate with conversation persistence system
- Ensure tool calls are logged for audit trail

---

## Phase 2: Implementation Plan

**Prerequisites**: All Phase 1 deliverables complete (data-model.md, contracts/, quickstart.md)

### Implementation Order

1. **Database Layer**: Create Conversation/Message models and migration
2. **MCP Layer**: Implement MCP tools with Context7 server
3. **AI Layer**: Implement OpenAI Agent using openai-agents-sdk-skill
4. **Backend API**: Create chat endpoint and conversation service
5. **Frontend UI**: Implement ChatKit integration with dashboard
6. **Integration**: Connect all components and test

**Critical Path**:
- MCP tools → Agent → Chat endpoint (backend chain)
- ChatKit → Dashboard → MCP tools (frontend chain)

**Dependencies**:
- MCP server must be running before agent implementation
- Database models must be ready before services
- Environment variables must be configured before testing

---

**Constitution**: This plan implements the AI Chatbot feature using the openai-agents-sdk-skill for agent creation with OpenRouter API integration as specified in the updated spec.
