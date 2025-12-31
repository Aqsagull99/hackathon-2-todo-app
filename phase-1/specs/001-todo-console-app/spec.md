# Feature Specification: In-Memory Todo Console Application

**Feature Branch**: `001-todo-console-app`
**Created**: 2025-12-28
**Status**: Draft
**Input**: User description: In-Memory Todo Console Application for Hackathon 2 Phase I

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Add New Todo (Priority: P1)

As a user, I want to add new tasks to my todo list so that I can track things I need to do.

**Why this priority**: Adding tasks is the fundamental capability that makes a todo app useful. Without this, no other features matter.

**Independent Test**: User can launch the app and add a task with a title. The task appears in the list. App validates input and provides feedback.

**Acceptance Scenarios**:

1. **Given** the app is running with an empty todo list, **When** the user adds a task with title "Buy groceries", **Then** the task is created with a unique ID and appears in the task list.

2. **Given** the app is running, **When** the user adds a task without a title, **Then** the app shows an error message and the task is not created.

3. **Given** the app is running with existing tasks, **When** the user adds a new task, **Then** the task receives a new unique ID (incremented from previous tasks).

---

### User Story 2 - View All Todos (Priority: P1)

As a user, I want to see all my tasks so that I can review what I need to do.

**Why this priority**: Users need to see their tasks to plan their day and track progress. This is essential for any todo management.

**Independent Test**: User can view all tasks in a formatted list showing ID, title, and completion status.

**Acceptance Scenarios**:

1. **Given** the app has no tasks, **When** the user views the task list, **Then** a message indicates no tasks exist.

2. **Given** the app has multiple tasks (some completed, some pending), **When** the user views the task list, **Then** all tasks are displayed with clear indication of completion status.

3. **Given** the app has tasks, **When** the user views the task list, **Then** tasks are shown in order of creation (oldest first).

---

### User Story 3 - Mark Todo as Complete (Priority: P1)

As a user, I want to mark tasks as complete so that I can track my progress.

**Why this priority**: Completing tasks is the core feedback loop of todo management. Users need to feel progress by marking items done.

**Independent Test**: User can select a task by ID and mark it as complete. The status changes and is reflected in the view.

**Acceptance Scenarios**:

1. **Given** a task exists with ID 1 and is marked incomplete, **When** the user marks task 1 as complete, **Then** the task status changes to complete.

2. **Given** a task exists with ID 1 and is marked complete, **When** the user marks task 1 as complete again, **Then** the task status remains complete (idempotent).

3. **Given** no task with ID 999 exists, **When** the user marks task 999 as complete, **Then** an error message is shown.

---

### User Story 4 - Update Todo Title (Priority: P2)

As a user, I want to change a task's title so that I can correct mistakes or refine task descriptions.

**Why this priority**: Users often need to modify tasks after creation. This is a common real-world requirement but not essential for MVP.

**Independent Test**: User can select a task by ID and provide a new title. The task's title is updated.

**Acceptance Scenarios**:

1. **Given** a task exists with title "Buy grocieries" (typo), **When** the user updates task 1 to "Buy groceries", **Then** the task title is corrected.

2. **Given** a task exists with ID 1, **When** the user updates task 1 with an empty title, **Then** an error is shown and title remains unchanged.

3. **Given** no task with ID 999 exists, **When** the user updates task 999, **Then** an error message is shown.

---

### User Story 5 - Delete Todo (Priority: P2)

As a user, I want to remove tasks so that I can clean up completed or unwanted items.

**Why this priority**: Deleting tasks helps keep the list focused. Less critical than core features but important for usability.

**Independent Test**: User can select a task by ID and delete it. The task is removed from the list.

**Acceptance Scenarios**:

1. **Given** a task with ID 1 exists, **When** the user deletes task 1, **Then** the task is removed from memory.

2. **Given** no task with ID 999 exists, **When** the user deletes task 999, **Then** an error message is shown.

3. **Given** multiple tasks exist, **When** a task is deleted, **Then** other tasks remain unchanged with their original IDs.

---

### Edge Cases

- User enters an invalid task ID (non-numeric, negative, or too large)
- User provides a title that is only whitespace
- User provides a title that exceeds reasonable length (we use 200 characters as reasonable limit)
- User tries to perform operations when no tasks exist
- Application is closed and reopened (state is lost - this is expected per constraints)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow users to create new tasks with a title.
- **FR-002**: System MUST store tasks in memory during the application session only.
- **FR-003**: System MUST assign a unique integer ID to each task upon creation.
- **FR-004**: System MUST allow users to view all tasks in a formatted list.
- **FR-005**: System MUST clearly display each task's completion status.
- **FR-006**: System MUST allow users to mark a task as complete by its ID.
- **FR-007**: System MUST allow users to update a task's title by its ID.
- **FR-008**: System MUST allow users to delete a task by its ID.
- **FR-009**: System MUST validate that task titles are non-empty (at least 1 character).
- **FR-010**: System MUST provide clear error messages for invalid operations.
- **FR-011**: System MUST display a help message showing available commands.
- **FR-012**: System MUST allow users to exit the application gracefully.

### Key Entities

- **Task**: Represents a single todo item
  - `id`: Unique integer identifier (auto-incremented)
  - `title`: String containing the task description
  - `completed`: Boolean indicating if task is done

- **TaskList**: Collection of all tasks in memory
  - `tasks`: Dictionary or list storing Task objects
  - `next_id`: Counter for generating unique task IDs

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can create a new task in under 30 seconds from app launch.
- **SC-002**: All 5 features (Add, View, Update, Delete, Mark Complete) are functional and produce expected results.
- **SC-003**: Users can complete the entire workflow (add 3 tasks, view them, mark one complete, update one, delete one) in under 2 minutes.
- **SC-004**: Error messages are clear enough that users understand what went wrong and how to fix it.
- **SC-005**: Application starts and responds within 5 seconds on standard hardware.
- **SC-006**: The application behaves deterministically - same inputs always produce same outputs.

### Completion Conditions

This specification is considered complete when:

- All 5 features are unambiguously defined with acceptance scenarios
- Edge cases are identified and handled
- Success criteria are measurable without implementation details
- The scope matches Hackathon Phase I requirements
- No implementation details (languages, frameworks, tools) appear in the spec

---

## Working Console Application Demo

The following demonstrates a complete working session of the todo console application:

### Session: Adding Tasks with Title and Description

```
┌────────────────────────────────────────────────┐
│                TODO APPLICATION                │
├────────────────────────────────────────────────┤
│ ▶ 1. Add New Task      - Create a new todo item │
│    2. View Tasks       - See all your tasks    │
│    3. Exit Application - Close the app         │
├────────────────────────────────────────────────┤
│ Use ↑/↓ arrows to select, Enter to choose      │
└────────────────────────────────────────────────┘

Enter choice [1-3]: 1

┌────────────────────────────────────────────────┐
│                ADD NEW TASK                    │
└────────────────────────────────────────────────┘

   ℹ  You currently have 0 task(s).

   ℹ  Enter your task description below.
   ℹ  Examples: 'Buy groceries', 'Call mom', 'Finish report'

   Task description: Buy groceries

   ✓  Task added successfully!

┌────────────────────────────────────────────────┐
│                TASK CREATED                    │
└────────────────────────────────────────────────┘

   Task #1: Buy groceries

   Add another task? (y/n): y

   Task description: Pay bills

   ✓  Task added successfully!

┌────────────────────────────────────────────────┐
│                TASK CREATED                    │
└────────────────────────────────────────────────┘

   Task #2: Pay bills

   Add another task? (y/n): n
```

### Session: Listing All Tasks with Status Indicators

```
┌────────────────────────────────────────────────┐
│             VIEW & MANAGE TASKS                │
└────────────────────────────────────────────────┘

   #   │ STATUS   │ TASK
  ─────┼──────────┼────────────────────────────────
 ▶ 1   │ [  TODO ]│ Buy groceries
    2   │ [  TODO ]│ Pay bills

   ↑/↓ navigate  •  ENTER select task  •  q go back
```

### Session: Updating Task Details

```
┌────────────────────────────────────────────────┐
│                TASK #1                         │
└────────────────────────────────────────────────┘

   Task #1
   Status: ○ PENDING
   Created: 2025-12-28 14:30

   ─────────────────────────────────────────────

   Buy groceries

   ─────────────────────────────────────────────

   [c] Mark as complete
   [d] Delete task
   [e] Edit task title
   [q] Go back to task list

   Press e to edit...

┌────────────────────────────────────────────────┐
│                  EDIT TASK                     │
└────────────────────────────────────────────────┘

   ℹ  Current title: Buy groceries

   ℹ  Enter a new title for this task.

   New title: Buy groceries and vegetables

   ✓  Task updated successfully!

┌────────────────────────────────────────────────┐
│                CHANGES SAVED                   │
└────────────────────────────────────────────────┘

   From: Buy groceries
   To:   Buy groceries and vegetables
```

### Session: Deleting Tasks by ID

```
┌────────────────────────────────────────────────┐
│             VIEW & MANAGE TASKS                │
└────────────────────────────────────────────────┘

   #   │ STATUS   │ TASK
  ─────┼──────────┼────────────────────────────────
 ▶ 1   │ [  TODO ]│ Buy groceries and vegetables
    2   │ [  TODO ]│ Pay bills

   ENTER select task  •  q go back

   Select task 2 (Pay bills)...

┌────────────────────────────────────────────────┐
│                DELETE TASK                     │
└────────────────────────────────────────────────┘

   Are you sure you want to delete this task?

   Task #2: Pay bills

   Delete this task? (y/n): y

   ✓  Task deleted successfully!
```

### Session: Marking Tasks as Complete/Incomplete

```
┌────────────────────────────────────────────────┐
│                TASK #1                         │
└────────────────────────────────────────────────┘

   Task #1
   Status: ○ PENDING
   Created: 2025-12-28 14:30

   ─────────────────────────────────────────────

   Buy groceries and vegetables

   ─────────────────────────────────────────────

   [c] Mark as complete
   [d] Delete task
   [e] Edit task title
   [q] Go back to task list

   Press c to complete...

   ✓  Task marked as complete!

┌────────────────────────────────────────────────┐
│             VIEW & MANAGE TASKS                │
└────────────────────────────────────────────────┘

   #   │ STATUS   │ TASK
  ─────┼──────────┼────────────────────────────────
 ▶ 1   │ [✓ DONE] │ Buy groceries and vegetables

   [↑] navigate  •  ENTER select task  •  q go back
```

### Key UX Features Demonstrated

1. **Clear Screen Titles**: Every screen shows where the user is (ADD NEW TASK, VIEW TASKS, etc.)

2. **Input Guidance**: Shows examples and current task count before input

3. **Status Indicators**: `[  TODO ]` for pending, `[✓ DONE]` for completed

4. **User Feedback**: `✓` for success, `✗` for errors, `ℹ` for information

5. **Arrow Navigation**: `▶` indicates selected item, `↑/↓` for navigation

6. **Confirmation Dialogs**: Delete requires `y/n` confirmation

7. **Error Recovery**: "Press Enter to continue" after errors or actions
