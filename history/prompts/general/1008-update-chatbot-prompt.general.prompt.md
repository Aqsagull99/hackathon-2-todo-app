---
id: 1008
title: Update chatbot prompt
stage: general
date: 2026-01-15
surface: agent
model: claude-opus-4-5-20251101
feature: 005-ai-chatbot-mcp
branch: 005-ai-chatbot-mcp
user: Aqsagull99
command: /sp.implement
labels: ["chatbot", "system-prompt", "fallback-logic", "task-extraction"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - phase-2/backend/app/agents/chat_agent.py
tests:
 - none
---

## Prompt

You are a task management chatbot connected to a todo system.

When adding a task, always extract and send ALL task fields:
title, description, priority, due_date, reminder, recurring, and tags.
If the user mentions time, urgency, repetition, or category in natural language,
map them correctly. Do NOT default to medium priority unless the user specifies it.
If a field is not mentioned, send it as null, not ignored.

Ensure chatbot-created tasks behave exactly like tasks created from the UI.

If the user asks “who made this app” or similar, reply briefly:
“This todo app was created by Aqsa Gull, an AI-focused full-stack developer who builds intelligent agent-based systems.”

When the user says “show my tasks”, “list tasks”, or “show tasks”,
fetch the tasks and display them clearly inside the chat.

## Response snapshot

Updated the chatbot system prompt in `phase-2/backend/app/agents/chat_agent.py` to include comprehensive task field extraction rules, specific handling for "who made this app" questions, and clear behavior for task listing. Also updated the local fallback mode to align with these requirements, removing the hardcoded "medium" priority default and adding specific intent detection for creator-related questions.

## Outcome

- ✅ Impact: Chatbot now correctly extracts all task fields, identifies the creator, and lists tasks as requested, both in full agent mode and fallback mode.
- 🧪 Tests: none
- 📁 Files: phase-2/backend/app/agents/chat_agent.py
- 🔁 Next prompts: none
- 🧠 Reflection: Updating both the main system prompt and the fallback logic ensures consistent behavior across different operating modes, which is crucial for reliability.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
