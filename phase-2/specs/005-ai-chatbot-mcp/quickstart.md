# Quickstart Guide: Phase III AI Chatbot

**Feature**: 005-ai-chatbot-mcp
**Prerequisites**: Phase II backend + frontend running

---

## Environment Setup

### 1. Backend Configuration

Add these variables to `backend/.env`:

```bash
# OpenRouter API (User already configured ✅)
OPENROUTER_API_KEY="sk-or-v1-..."  # Already added
OPENROUTER_MODEL="openai/gpt-4o"

# Existing Phase II vars (keep as-is)
DATABASE_URL="postgresql+asyncpg://..."
JWT_SECRET="your-secret"
```

### 2. Install Dependencies

```bash
cd ~/Todo-app/phase-2/backend

# Add new dependencies to pyproject.toml (Official MCP SDK)
uv add openai>=1.40.0
uv add mcp>=1.0.0  # Official MCP SDK (Hackathon requirement)
uv add tenacity>=8.0.0  # For retry logic

# Or manually:
pip install openai mcp tenacity
```

**Important**: Use **Official MCP SDK** (`mcp>=1.0.0`), NOT Context7 or other third-party wrappers, as mandated by Hackathon constitution.

### 3. Frontend Configuration

Add to `frontend/.env.local`:

```bash
# OpenAI ChatKit (if needed)
NEXT_PUBLIC_CHAT_API_URL="http://localhost:8000/api/chat"

# Existing Phase II vars (keep)
NEXT_PUBLIC_API_URL="http://localhost:8000"
```

Install ChatKit:

```bash
cd ~/Todo-app/phase-2/frontend
npm install @openai/chatkit react-icons
```

---

## Database Migration

### Create Migration

```bash
cd ~/Todo-app/phase-2/backend

# Generate migration for Conversation + Message tables
alembic revision --autogenerate -m "Add conversation and message tables for Phase III"

# Review generated migration file
cat migrations/versions/*_add_conversation*.py

# Apply migration
alembic upgrade head
```

### Verify Tables

```bash
# Using psql or Neon console
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name IN ('conversations', 'messages');

# Should return:
# conversations
# messages
```

---

## Backend Development

### 1. Start Backend Server

```bash
cd ~/Todo-app/phase-2/backend
source .venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

**Verify**: Visit http://localhost:8000/docs

### 2. Test MCP Tools (Manual)

```python
# Quick test script: test_mcp.py
import asyncio
from app.mcp.tools import add_task, list_tasks

async def test():
    # Create task
    result = await add_task(
        user_id="test-user-123",
        title="Test task from MCP",
        priority="high"
    )
    print("Created:", result)
    
    # List tasks
    tasks = await list_tasks(user_id="test-user-123")
    print("Tasks:", tasks)

asyncio.run(test())
```

Run:
```bash
python test_mcp.py
```

### 3. Test Chat Endpoint

```bash
# Get JWT token first (from Phase II signin)
TOKEN="your-jwt-token"

# Send chat message
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "message": "Add a task to buy groceries"
  }'

# Expected response:
# {
#   "conversation_id": "uuid-here",
#   "response": "I've added 'Buy groceries' to your task list.",
#   "tool_calls": [{"tool": "add_task", ...}]
# }
```

---

## Frontend Development

### 1. Start Frontend Dev Server

```bash
cd ~/Todo-app/phase-2/frontend
npm run dev
```

**Verify**: Visit http://localhost:3000/dashboard

### 2. Test ChatKit Component

Create test component:

```tsx
// src/app/test-chat/page.tsx
'use client';

import ChatWidget from '@/components/chat/ChatWidget';

export default function TestChatPage() {
  return (
    <div className="min-h-screen bg-black p-8">
      <h1 className="text-white text-2xl mb-4">Chat Test</h1>
      <div className="w-96 h-96">
        <ChatWidget />
      </div>
    </div>
  );
}
```

Visit: http://localhost:3000/test-chat

---

## Running Tests

### Backend Tests

```bash
cd ~/Todo-app/phase-2/backend

# Run all tests
pytest

# Run specific test file
pytest tests/test_mcp_tools.py -v

# Run with coverage
pytest --cov=app --cov-report=html
```

### Frontend Tests

```bash
cd ~/Todo-app/phase-2/frontend

# Run Jest tests
npm test

# Run specific test
npm test ChatWidget.test.tsx
```

---

## End-to-End Testing

### Manual E2E Flow

1. **Start both servers** (backend:8000, frontend:3000)

2. **Sign in** at http://localhost:3000/signin

3. **Open Dashboard** → Click chat icon (bottom-right)

4. **Test conversation**:
   ```
   User: "Add a task to buy groceries"
   Bot: "I've added 'Buy groceries' to your task list."
   
   User: "Show my tasks"
   Bot: "Here are your tasks: 1. Buy groceries (pending)"
   
   User: "Mark it as complete"
   Bot: "Great job! I've marked 'Buy groceries' as complete."
   ```

5. **Verify in UI**: Task appears in Dashboard task list

6. **Verify in DB**:
   ```sql
   SELECT * FROM tasks WHERE title = 'Buy groceries';
   SELECT * FROM conversations ORDER BY created_at DESC LIMIT 1;
   SELECT * FROM messages WHERE conversation_id = '<conv-id>';
   ```

### Automated E2E (Playwright)

```bash
cd ~/Todo-app/phase-2/frontend

# Install Playwright
npm install -D @playwright/test

# Run E2E tests
npx playwright test e2e/chat-flow.spec.ts
```

---

## Deployment

### Backend (Railway)

```bash
cd ~/Todo-app/phase-2/backend

# Ensure .env vars are set in Railway dashboard:
# - OPENROUTER_API_KEY
# - DATABASE_URL
# - JWT_SECRET

# Deploy
git push railway main

# Run migration on production
railway run alembic upgrade head
```

### Frontend (Vercel)

```bash
cd ~/Todo-app/phase-2/frontend

# Set env vars in Vercel dashboard:
# - NEXT_PUBLIC_API_URL (Railway backend URL)

# Deploy
vercel --prod
```

---

## Troubleshooting

### Issue: "OpenRouter API key invalid"

**Solution**: Check backend `.env`:
```bash
cat backend/.env | grep OPENROUTER_API_KEY
# Should show: OPENROUTER_API_KEY=sk-or-v1-...
```

Verify key at: https://openrouter.ai/keys

### Issue: "Conversation not found"

**Solution**: Check DB migration:
```bash
cd backend/
alembic current  # Should show latest revision
alembic upgrade head  # If not on latest
```

### Issue: "Tool execution failed"

**Solution**: Check MCP server logs:
```bash
tail -f backend/logs/mcp_tools.log
```

Verify tool registration:
```python
from app.mcp.server import mcp_server
print(mcp_server.list_tools())
# Should show: ['add_task', 'list_tasks', ...]
```

### Issue: "ChatKit not rendering"

**Solution**: Check browser console for errors.

Verify ChatKit installation:
```bash
cd frontend/
npm list @openai/chatkit
```

### Issue: "CORS error from frontend"

**Solution**: Update backend CORS settings:
```python
# backend/app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Add this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Performance Optimization

### Backend

1. **Connection Pooling**:
   ```python
   # backend/app/core/database.py
   engine = create_async_engine(
       DATABASE_URL,
       pool_size=10,
       max_overflow=20
   )
   ```

2. **OpenRouter Timeout**:
   ```python
   client = AsyncOpenAI(
       base_url="https://openrouter.ai/api/v1",
       api_key=OPENROUTER_API_KEY,
       timeout=10.0  # 10 seconds
   )
   ```

### Frontend

1. **ChatKit Lazy Loading**:
   ```tsx
   const ChatWidget = dynamic(() => import('@/components/chat/ChatWidget'), {
     ssr: false
   });
   ```

2. **Message Pagination**: Limit conversation history to 50 messages in UI

---

## Monitoring

### Check System Health

```bash
# Backend health
curl http://localhost:8000/health

# Check active conversations
curl http://localhost:8000/api/conversations \
  -H "Authorization: Bearer $TOKEN"
```

### Logs

```bash
# Backend logs
tail -f backend/logs/app.log
tail -f backend/logs/mcp_tools.log

# Frontend logs (browser console)
# Check Network tab for API calls
```

---

## Quick Reference

### Key Files

| File | Purpose |
|------|---------|
| `backend/app/mcp/tools.py` | 6 MCP tool implementations |
| `backend/app/agents/chat_agent.py` | OpenAI agent with OpenRouter |
| `backend/app/api/routes/chat.py` | Chat endpoint |
| `backend/app/models/conversation.py` | Conversation model |
| `backend/app/models/message.py` | Message model |
| `frontend/src/components/chat/ChatWidget.tsx` | ChatKit UI |
| `frontend/src/app/dashboard/page.tsx` | Dashboard with chat icon |

### Useful Commands

```bash
# Backend
cd backend/
uvicorn app.main:app --reload --port 8000
pytest
alembic upgrade head

# Frontend
cd frontend/
npm run dev
npm test
npm run build

# Database
psql $DATABASE_URL
alembic current
```

---

**Quickstart Complete** ✅

**Next Steps**:
1. Run `/sp.tasks` to generate implementation tasks
2. Start with backend MCP tools (highest priority)
3. Then implement chat endpoint + agent
4. Finally integrate ChatKit UI

**Questions?** Check `research.md` and `plan.md` for detailed architecture.
