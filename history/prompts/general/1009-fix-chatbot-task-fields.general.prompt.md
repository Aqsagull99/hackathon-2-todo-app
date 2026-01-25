---
id: 1009
title: Fix chatbot task fields
stage: general
date: 2026-01-15
surface: agent
model: claude-opus-4-5-20251101
feature: 005-ai-chatbot-mcp
branch: 005-ai-chatbot-mcp
user: Aqsagull99
command: /sp.implement
labels: ["chatbot", "task-fields", "frontend-ui", "backend-schema", "priority", "tags", "due-date"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - phase-2/backend/app/schemas/task.py
 - phase-2/backend/app/services/task_service.py
 - phase-2/backend/app/agents/chat_agent.py
 - phase-2/frontend/src/components/tasks/TaskItem.tsx
tests:
 - none
---

## Prompt

yes now all is well and good but there is only one issue chatbot jo Your task "Buy groceries" has been created with: • Items: Milk, eggs, bread • Priority: High • Tags: Personal, Urgent • Due: Tomorrow • Reminder: 1 hour before ⏳ Note: Reminders are being set up and will be activated soon. You can still view and manage this task. ye sub add kar raha hai wo chatbot par id k sath nhi araha and frontend par only title description araha hai and tag

## Response snapshot

Fixed the issue where extended task fields (priority, due_date, tags) were being acknowledged by the chatbot but not actually saved to the database or displayed on the frontend. The fix involved updating the full stack:
1. Updated backend Pydantic schemas (`TaskCreate`, `TaskRead`, `TaskUpdate`) to include extended fields.
2. Updated `TaskService.create_task` to handle these fields and persist them to the database.
3. Updated `TodoChatAgent.add_task_tool` to correctly map agent parameters to the updated schema.
4. Added basic priority parsing to the agent's fallback logic for auto-create scenarios.
5. Updated frontend `TaskItem.tsx` to visualize priority badges, tags, and due dates.

## Outcome

- ✅ Impact: Tasks created via chatbot now correctly persist all metadata (priority, due dates, tags) and display them in the UI.
- 🧪 Tests: none
- 📁 Files: phase-2/backend/app/schemas/task.py, phase-2/backend/app/services/task_service.py, phase-2/backend/app/agents/chat_agent.py, phase-2/frontend/src/components/tasks/TaskItem.tsx
- 🔁 Next prompts: none
- 🧠 Reflection: The issue revealed a disconnect between the agent's ability to "understand" and confirm fields versus the backend's ability to actually store them.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
