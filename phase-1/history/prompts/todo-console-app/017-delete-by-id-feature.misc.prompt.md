---
id: "017"
title: "Add direct delete by ID feature"
stage: "misc"
date: "2025-12-29"
surface: "agent"
model: "sonnet-4-5-20250929"
feature: "001-todo-console-app"
branch: "001-todo-console-app"
user: "aqsagulllinux"
command: "Add direct 'Delete by ID' option to main menu"
labels: ["feature", "delete", "ux", "ui"]
links:
  spec: "/home/aqsagulllinux/Todo-app/specs/001-todo-console-app/spec.md"
  plan: "null"
  ticket: "null"
  adr: "null"
  pr: "null"
files:
  - "/home/aqsagulllinux/Todo-app/src/todo_app/ui.py"
tests:
  - "Main menu shows 'Delete Task' option"
  - "Arrow navigation works with 4 options"
  - "handle_delete_by_id shows task list"
  - "Invalid ID shows error"
  - "Confirmation dialog appears"
  - "Success message on delete"
---

## Prompt

User reported: "Deleting tasks by ID ye misstig gai" and requested "Delete by ID" option in main menu.

After discussion, user chose: "Both methods" - keep existing (view task → delete) AND add direct delete by ID.

## Response snapshot

Added direct "Delete Task by ID" feature to main menu:

### Changes to ui.py

1. **Updated main menu** (`draw_main_menu`):
   - Added "Delete Task - Remove a task by ID" option
   - Now 4 options instead of 3

2. **Updated navigation** (line 211-216):
   - Changed modulo from 3 to 4 for arrow navigation

3. **Updated Enter handler** (line 196-212):
   - Added `elif selected == 2: self.handle_delete_by_id()`

4. **Added `handle_delete_by_id()` method** (line 371-436):
   - Shows all tasks with IDs first
   - Prompts for task ID input
   - Validates ID (must be number)
   - Shows task not found error
   - Displays confirmation dialog with task details
   - Calls `tasklist.delete(task.id)` on confirmation

### New Main Menu Options
```
1. Add New Task      - Create a new todo item
2. View Tasks        - See all your tasks
3. Delete Task       - Remove a task by ID  [NEW]
4. Exit Application  - Close the app
```

### Delete by ID Flow
```
┌────────────────────────────────────────────────┐
│                DELETE TASK BY ID               │
└────────────────────────────────────────────────┘

   ℹ  Available tasks:

   #1: [  TODO ] Buy groceries
   #2: [✓ DONE] Pay bills

   Enter task ID to delete: 1

┌────────────────────────────────────────────────┐
│                DELETE TASK                     │
└────────────────────────────────────────────────┘

   Are you sure you want to delete this task?

   Task #1: Buy groceries

   Delete this task? (y/n): y

   ✓  Task deleted successfully!
```

## Outcome

- ✅ Impact: Users can now delete tasks by ID directly from main menu
- 🧪 Tests: Manual verification - syntax check passed
- 📁 Files: 1 file modified (ui.py)
- 🔁 Next prompts: None - feature complete
- 🧠 Reflection: Both delete methods now available for convenience

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Syntax check PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Could add numeric shortcuts (press 3 for delete)
