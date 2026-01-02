# Feature Specification: Todo App  Phase I Extended Features

**Feature Branch**: `002-phase1-extended-features`
**Created**: 2026-01-01
**Status**: Draft
**Input**: User description for Phase I Extended Features (Priorities, Tags, Search, Filter, Sort, Recurring, Due Dates/Reminders)

## User Scenarios & Testing

### User Story 1 - Task Organization (Priorities & Tags) (Priority: P1)
As a user, I want to categorize and prioritize my tasks so that I can focus on what's important.

**Independent Test**: User can assign a priority (High/Medium/Low) and add tags (e.g., "Work") to a task. These details are visible in the task list.

**Acceptance Scenarios**:
1. **Given** a task list, **When** the user adds a task with priority "High" and tag "Urgent", **Then** the task is stored with these attributes and they appear when viewing the task.
2. **Given** an existing task, **When** the user updates its priority to "Low", **Then** the change is saved and displayed correctly.

---

### User Story 2 - Search and Discovery (Priority: P1)
As a user, I want to search through my tasks by keyword so that I can find specific items quickly.

**Independent Test**: User enters a keyword, and only tasks containing that keyword (in title or tags) are displayed.

**Acceptance Scenarios**:
1. **Given** tasks "Buy milk" and "Pay rent", **When** the user searches for "milk", **Then** only "Buy milk" is displayed.
2. **Given** no matching tasks, **When** the user searches for "xyz", **Then** the system shows "No matching tasks found".

---

### User Story 3 - Filtering and Sorting (Priority: P2)
As a user, I want to filter and sort my list so that I can see tasks grouped by my current context (e.g., by due date or priority).

**Independent Test**: User applies a filter (e.g., Status: Pending) and a sort (e.g., Due Date), and the list updates instantly to show the narrowed, ordered items.

**Acceptance Scenarios**:
1. **Given** mixed tasks, **When** user filters by "Status: Completed", **Then** only completed tasks appear.
2. **Given** tasks with different priorities, **When** user sorts by "Priority", **Then** tasks appear in order (High > Medium > Low).

---

### User Story 4 - Intelligent Features (Recurring & Reminders) (Priority: P2)
As a user, I want tasks to repeat and remind me so that I don't forget routine or time-sensitive responsibilities.

**Independent Test**: User sets a task to repeat "Daily" and assigns a due time. The task auto-respawns upon completion and triggers a reminder at the set time.

**Acceptance Scenarios**:
1. **Given** a daily recurring task "Drink water", **When** the user marks it complete, **Then** a new instance of "Drink water" is created for the next day.
2. **Given** a task with a due time, **When** the time is reached, **Then** the application triggers a browser/system notification.

---

## Requirements

### Functional Requirements
- **FR-001**: System MUST allow assigning priority levels (High, Medium, Low) to tasks.
- **FR-002**: System MUST allow adding multiple tags/labels to a task.
- **FR-003**: System MUST provide a search function that filters the task list by keyword (matching title or tags).
- **FR-004**: System MUST allow filtering the task list by Status, Priority, or Due Date.
- **FR-005**: System MUST allow sorting the task list by Name (alphabetical), Priority, or Due Date.
- **FR-006**: System MUST support recurring tasks with "Daily" and "Weekly" frequencies.
- **FR-007**: System MUST automatically create a new task instance for recurring tasks upon completion of the current one.
- **FR-008**: System MUST allow assigning a Due Date and Time to tasks.
- **FR-009**: System MUST trigger a notification (browser-based) when a task's reminder time is reached.
- **FR-010**: System MUST validate that due dates and recurrence patterns follow simple, predictable rules.

### Key Entities
- **Priority**: Enum {High, Medium, Low}
- **Tag**: String label
- **Recurrence**: Enum {None, Daily, Weekly}
- **Reminder**: DateTime timestamp
- **Task (Updated)**:
  - id, title, completed (inherited)
  - priority: Priority
  - tags: List[Tag]
  - due_date: DateTime
  - recurrence: Recurrence

## Success Criteria

### Measurable Outcomes
- **SC-001**: Users can filter a list of 50 tasks in under 2 seconds.
- **SC-002**: Recurring tasks correctly reschedule within 1 second of marks-complete action.
- **SC-003**: Reminders trigger within ±5 seconds of the set time.
- **SC-004**: Search results are 100% accurate based on keyword matches in titles and tags.

### Completion Conditions
- All organization features (Priority, Tags, Search, Filter, Sort) are implemented and verifiable.
- Intelligent features (Recurring, Reminders) are functional and reliable.
- Existing CRUD functionality remains unchanged and fully compatible.

---

## Assumptions
- Due dates and reminders are handled based on the local system time.
- Recurring tasks logic simple: completion triggers new task + X days.
- Browser notifications used for reminders (shim/mock if console-only, or integrated if UI supports it).
