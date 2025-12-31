---
id: "008"
title: "Add another task prompt feature"
stage: "misc"
date: "2025-12-28"
surface: "agent"
model: "sonnet-4-5-20250929"
feature: "001-todo-console-app"
branch: "001-todo-console-app"
user: "aqsagulllinux"
command: "UX improvement follow-up"
labels: ["ux", "feature", "feedback-loop"]
links:
  spec: "null"
  ticket: "null"
  adr: "null"
  pr: "null"
files:
  - "/home/aqsagulllinux/Todo-app/src/todo_app/ui.py"
tests:
  - "After adding task, prompts 'Add another task? (y/n)'"
  - "Press y to add another task"
  - "Press n to return to main menu"
---

## Prompt

User requested UX improvement: "Should I add a confirmation after adding? ('Add another task? y/n')"

User said: "2  Should I add a confirmation after adding? ('Add another task? y/n')"

## Response snapshot

Added "Add another task?" prompt in `handle_add_task()` method:

- Added `while True` loop for adding multiple tasks
- After successful task creation, shows "Add another task? (y/n)"
- Press `y` → Adds another task (returns to add screen)
- Press `n` → Returns to main menu

This improves UX by allowing users to add multiple tasks quickly without going back to main menu each time.

## Outcome

- ✅ Impact: Users can add multiple tasks in succession
- 🧪 Tests: Manual verification - prompt appears after each task
- 📁 Files: ui.py updated (handle_add_task method)
- 🔁 Next prompts: None - feature complete

## Evaluation notes (flywheel)

- Failure modes observed: N/A - simple feature addition
- Graders run and results (PASS/FAIL): Manual - PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Could show running task count during add loop
