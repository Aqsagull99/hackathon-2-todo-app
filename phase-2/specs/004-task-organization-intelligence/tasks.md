# Implementation Tasks: Task Organization & Intelligence (004)

**Feature ID**: 004-task-organization-intelligence
**Tasks Version**: 1.0.0
**Created**: 2026-01-03
**Status**: READY FOR IMPLEMENTATION
**Feature Spec**: [spec.md](./spec.md)
**Implementation Plan**: [plan.md](./plan.md)

---

## Overview

This document provides a complete, ordered implementation roadmap for Feature 004: Task Organization & Intelligence. The feature adds 6 user stories organized by priority.

### User Stories (by Priority)

| Story | Name | Description | Priority |
|-------|------|-------------|----------|
| US1 | Priority Management | Assign High/Medium/Low priority to tasks with visual indicators | P1 |
| US2 | Tags & Categories | Create and manage custom tags for task organization | P1 |
| US3 | Search Functionality | Keyword search across task titles and descriptions | P2 |
| US4 | Filter & Sort | Filter by status/priority/due date and sort results | P2 |
| US5 | Recurring Tasks | Auto-reschedule completed recurring tasks | P3 |
| US6 | Due Dates & Reminders | Set due dates with time and browser notifications | P3 |

### Task Statistics

- **Total Tasks**: 89
- **Setup Tasks**: 8
- **Foundational Tasks**: 12
- **US1 (Priority)**: 8 tasks
- **US2 (Tags)**: 14 tasks
- **US3 (Search)**: 10 tasks
- **US4 (Filter/Sort)**: 8 tasks
- **US5 (Recurring)**: 12 tasks
- **US6 (Reminders)**: 12 tasks
- **Integration & Polish**: 5 tasks

---

## Phase 1: Setup

**Goal**: Initialize project with required dependencies and database schema.

### Independent Test Criteria
- Database migration runs without errors
- All new dependencies installed successfully
- TypeScript types compile without errors
- Python models import without errors

### Implementation

- [ ] T001 Create database migration script at `backend/migrations/004_extended_features.sql` with:
  - Task table columns: priority, due_date, due_date_tz, recurrence_pattern, recurrence_parent_id
  - Tags table creation with user_id foreign key
  - TaskTags join table creation
  - Reminders table creation
  - Indexes for priority, due_date, user_id compound queries
  - Full-text search tsvector column and trigger

- [ ] T002 [P] Update backend dependencies in `backend/pyproject.toml` - no new packages needed (using existing SQLModel, asyncpg)

- [ ] T003 [P] Run database migration against Neon PostgreSQL:
  ```bash
  psql "postgresql://$NEON_CONNECTION" -f backend/migrations/004_extended_features.sql
  ```

- [ ] T004 [P] Create TypeScript types in `frontend/src/types/task-extended.ts`:
  ```typescript
  type TaskPriority = 'high' | 'medium' | 'low'
  type RecurrencePattern = 'daily' | 'weekly' | 'monthly'
  interface Tag { id: string; name: string; color: string; }
  interface Reminder { id: string; task_id: string; due_time: string; status: string; }
  interface ExtendedTask extends Task {
    priority: TaskPriority
    due_date: string | null
    due_date_tz: string | null
    recurrence_pattern: RecurrencePattern | null
    tags: Tag[]
    reminders: Reminder[]
  }
  ```

- [ ] T005 [P] Create Pydantic schemas in `backend/src/schemas/task_extended.py` for:
  - TaskPriority, RecurrencePattern enums
  - TagCreate, TagUpdate, TagResponse schemas
  - ReminderCreate, ReminderResponse schemas
  - TaskCreateExtended, TaskUpdateExtended schemas

- [ ] T006 [P] Export new schemas from `backend/src/schemas/__init__.py`

- [ ] T007 [P] Add enum values to database enum type:
  ```sql
  ALTER TYPE task_priority ADD VALUE IF NOT EXISTS 'high';
  ALTER TYPE task_priority ADD VALUE IF NOT EXISTS 'low';
  ```

- [ ] T008 [P] Verify migration:
  - Check all new columns exist in task table
  - Check tags, task_tag_link, reminders tables exist
  - Verify indexes were created

---

## Phase 2: Foundational

**Goal**: Create core data models and API client extensions needed by all user stories.

### Independent Test Criteria
- Task model with priority field can be created and queried
- Tag model supports CRUD operations with user isolation
- API client extensions compile without errors
- All services can import models without circular dependency errors

### Implementation

- [ ] T009 Update Task model in `backend/src/models/task.py`:
  - Add TaskPriority enum (HIGH, MEDIUM, LOW)
  - Add RecurrencePattern enum (DAILY, WEEKLY, MONTHLY)
  - Add priority field with default MEDIUM and index
  - Add due_date, due_date_tz, recurrence_pattern, recurrence_parent_id fields
  - Add tags relationship using TaskTagLink

- [ ] T010 Create TaskTagLink model in `backend/src/models/task_tag_link.py` for many-to-many relationship

- [ ] T011 Create Tag model in `backend/src/models/tag.py`:
  - Fields: id, user_id (FK), name (unique per user), color, created_at
  - Relationship to tasks via TaskTagLink

- [ ] T012 Create Reminder model in `backend/src/models/reminder.py`:
  - Fields: id, task_id (FK), due_time, status enum (pending/sent/snoozed/dismissed), snoozed_until
  - Relationship to task

- [ ] T013 [P] Export all new models from `backend/src/models/__init__.py`

- [ ] T014 Create TagService in `backend/src/services/tag_service.py`:
  - get_user_tags(user_id)
  - create_tag(user_id, name, color)
  - update_tag(tag_id, user_id, name, color)
  - delete_tag(tag_id, user_id) - returns affected task IDs
  - add_tag_to_task(task_id, tag_id, user_id)
  - remove_tag_from_task(task_id, tag_id, user_id)

- [ ] T015 Create SearchService in `backend/src/services/search_service.py`:
  - build_search_query(user_id, search, filters, sort)
  - search_tasks(session, params) returns paginated results
  - Full-text search using PostgreSQL tsvector
  - Multi-filter combination support

- [ ] T016 Create RecurringService in `backend/src/services/recurring_service.py`:
  - complete_recurring_task(session, task) -> creates new instance
  - _calculate_next_instance(due_date, pattern) -> calculates next due date
  - Supports DAILY, WEEKLY, MONTHLY patterns

- [ ] T017 Create ReminderService in `backend/src/services/reminder_service.py`:
  - create_reminder(session, task_id, due_time)
  - get_reminder_for_task(session, task_id)
  - snooze_reminder(session, reminder_id, minutes)
  - get_pending_reminders(session) - for scheduled notifications

- [ ] T018 [P] Export all services from `backend/src/services/__init__.py`

- [ ] T019 Extend API client in `frontend/src/lib/api.ts`:
  - getTags(userId), createTag(userId, data), updateTag(userId, tagId, data), deleteTag(userId, tagId)
  - searchTasks(userId, params) with search, filter, sort parameters
  - createReminder(userId, taskId, dueTime), snoozeReminder(userId, reminderId, minutes)

- [ ] T020 Create type exports in `frontend/src/types/index.ts`:
  - Export TaskPriority, RecurrencePattern, Tag, Reminder types
  - Update Task type to include new extended fields

---

## Phase 3: US1 - Priority Management

**Goal**: Users can assign High/Medium/Low priority to tasks with visual indicators.

**Independent Test Criteria**:
- Task can be created with priority
- Task can be updated to change priority
- Priority is displayed as colored badge/icon in task list
- Tasks can be filtered by priority
- Tasks can be sorted by priority

### Implementation

- [ ] T021 [US1] Create PrioritySelector component in `frontend/src/components/tasks/PrioritySelector.tsx`:
  - Dropdown with High (red), Medium (pink), Low (gray) options
  - Default selection: Medium
  - Calls API to update task priority on change

- [ ] T022 [US1] Create PriorityBadge component in `frontend/src/components/tasks/PriorityBadge.tsx`:
  - Visual display: colored badge or icon
  - High: red background, "!" icon
  - Medium: pink background
  - Low: gray/grayed out
  - Consistent with glassmorphic theme

- [ ] T023 [US1] Update TaskCard in `frontend/src/components/tasks/TaskCard.tsx`:
  - Add PriorityBadge next to task title
  - Update priority when changed via PrioritySelector

- [ ] T024 [US1] Update TaskForm in `frontend/src/components/tasks/TaskForm.tsx`:
  - Add PrioritySelector to task creation form
  - Include priority in POST/PATCH request body

- [ ] T025 [US1] Create API endpoint in `backend/src/routes/tasks.py`:
  - POST /{user_id}/tasks - accepts priority field
  - PATCH /{user_id}/tasks/{task_id} - accepts priority field update

- [ ] T026 [US1] Add priority filtering to SearchService:
  - Filter tasks by priority level
  - Combine with other filters (status, due date, etc.)

- [ ] T027 [US1] Add priority sorting to SearchService:
  - Sort by priority (High > Medium > Low)
  - Reverse order option

- [ ] T028 [US1] Integration test for US1:
  - Create task with priority=high
  - Verify it displays with high priority badge
  - Change to low priority
  - Verify display updates
  - Filter by priority=high and verify task appears
  - Sort by priority and verify order

---

## Phase 4: US2 - Tags & Categories

**Goal**: Users can create custom tags and assign them to tasks for organization.

**Independent Test Criteria**:
- User can create, rename, and delete tags
- Tags appear as colored badges on tasks
- Tasks can have multiple tags
- User can filter tasks by tag(s)
- User can only see their own tags (user isolation)

### Implementation

- [ ] T029 [US2] Create TagBadge component in `frontend/src/components/tasks/TagBadge.tsx`:
  - Small colored pill with tag name
  - Clickable to filter by tag
  - Consistent color scheme (pink variants matching UI theme)

- [ ] T030 [US2] Create TagInput component in `frontend/src/components/tasks/TagInput.tsx`:
  - Multi-select input for adding tags to tasks
  - Shows existing user tags as suggestions
  - Allows creating new tags inline
  - Visual tag pills with remove button

- [ ] T031 [US2] Create TagManager component in `frontend/src/components/tasks/TagManager.tsx`:
  - Modal dialog for managing all user tags
  - List all tags with task counts
  - Create new tag with color picker
  - Rename tag
  - Delete tag (shows affected tasks, requires confirmation)

- [ ] T032 [US2] Create TagManagerModal trigger button in `frontend/src/components/tasks/TaskDashboard.tsx`:
  - Add "Manage Tags" button to dashboard header
  - Opens TagManager modal

- [ ] T033 [US2] Update TaskCard to display tags:
  - Show TagBadge components for each task tag
  - Truncate if too many tags (>3 show "+N")

- [ ] T034 [US2] Update TaskForm to include TagInput:
  - Allow selecting/creating tags when editing task

- [ ] T035 [US2] Create API endpoints in `backend/src/routes/tags.py`:
  - GET /{user_id}/tags - list all user tags with task counts
  - POST /{user_id}/tags - create new tag
  - PATCH /{user_id}/tags/{tag_id} - update tag name/color
  - DELETE /{user_id}/tags/{tag_id} - delete tag, return affected tasks

- [ ] T036 [US2] Create tag-task association endpoints in `backend/src/routes/tag_tasks.py`:
  - POST /{user_id}/tasks/{task_id}/tags/{tag_id} - add tag to task
  - DELETE /{user_id}/tasks/{task_id}/tags/{tag_id} - remove tag from task

- [ ] T037 [US2] Add tag filtering to SearchService:
  - Filter tasks by tag_ids (single or multiple)
  - Support inclusive filtering (has any of tags)

- [ ] T038 [US2] Add TagService methods:
  - get_or_create_tag(user_id, name, color)
  - bulk_assign_tags(task_id, tag_ids) - replaces all tags

- [ ] T039 [US2] Create tag color palette constants in `frontend/src/lib/constants.ts`:
  - DEFAULT_TAG_COLORS array matching pink/black theme

- [ ] T040 [US2] Update API client with tag methods:
  - getUserTags(userId)
  - createTag(userId, {name, color})
  - updateTag(userId, tagId, {name, color})
  - deleteTag(userId, tagId)
  - addTagToTask(userId, taskId, tagId)
  - removeTagFromTask(userId, taskId, tagId)

- [ ] T041 [US2] Integration test for US2:
  - Create 3 tags with different colors
  - Add 2 tags to a task
  - Verify tags display on task card
  - Filter by one tag, verify task appears
  - Delete a tag, verify it removes from tasks
  - Create tag with same name, verify uniqueness per user

- [ ] T042 [US2] Security test:
  - Create tag as User A
  - Try to access User B's tags
  - Verify 403 Forbidden returned

---

## Phase 5: US3 - Search Functionality

**Goal**: Users can search tasks by keyword with results appearing in under 500ms.

**Independent Test Criteria**:
- Keyword search finds tasks by title and description
- Search results update in real-time as user types
- Empty search shows friendly message
- Search combines with other filters

### Implementation

- [ ] T043 [US3] Create SearchBar component in `frontend/src/components/tasks/SearchBar.tsx`:
  - Text input with search icon
  - Debounced search (300ms delay)
  - Clear button when text entered
  - Loading state while searching

- [ ] T044 [US3] Create SearchContext in `frontend/src/lib/contexts/SearchContext.tsx`:
  - Manage search query and results state
  - Debounce logic
  - Integration with FilterContext

- [ ] T045 [US3] Update dashboard to include SearchBar:
  - Add SearchBar to FilterSortToolbar or header

- [ ] T046 [US3] Add empty search state component in `frontend/src/components/tasks/SearchEmptyState.tsx`:
  - Shows "No tasks found for '[keyword]'" message
  - Suggests clearing search

- [ ] T047 [US3] Create PostgreSQL full-text search function in `backend/src/services/fulltext_search.py`:
  - Uses tsvector and tsquery
  - Weights: title (A), description (B)
  - Supports partial matches

- [ ] T048 [US3] Update SearchService.search_tasks():
  - Integrate full-text search
  - Accept search parameter
  - Return matching tasks with pagination

- [ ] T049 [US3] Add search index creation trigger to migration:
  - Creates search_vector column
  - Creates update_task_search_vector() function
  - Creates trigger for INSERT/UPDATE

- [ ] T050 [US3] Update GET /tasks endpoint:
  - Accept search query parameter
  - Pass to SearchService
  - Return results with total count

- [ ] T051 [US3] Performance test for US3:
  - Insert 500 test tasks
  - Search for keyword appearing in 100 tasks
  - Measure response time (< 500ms)
  - Verify results accuracy

- [ ] T052 [US3] Integration test for US3:
  - Search for term in title
  - Search for term in description
  - Search for term not in any task
  - Combine search with priority filter

---

## Phase 6: US4 - Filter & Sort

**Goal**: Users can filter tasks by status/priority/due date and sort results.

**Independent Test Criteria**:
- Filter by status (all/pending/completed)
- Filter by priority (all/high/medium/low)
- Filter by due date range (today/this week/this month/overdue)
- Sort by due date, priority, or alphabetically
- Filter/sort state persists during session
- Clear all filters button works

### Implementation

- [ ] T053 [US4] Create FilterBar component in `frontend/src/components/tasks/FilterBar.tsx`:
  - Status dropdown: All, Pending, Completed
  - Priority dropdown: All, High, Medium, Low
  - Due Date dropdown: All, Today, This Week, This Month, Overdue
  - Clear Filters button

- [ ] T054 [US4] Create SortDropdown component in `frontend/src/components/tasks/SortDropdown.tsx`:
  - Sort by: Due Date, Priority, Alphabetically, Created Date
  - Direction toggle: Ascending/Descending
  - Active sort indicator

- [ ] T055 [US4] Create FilterSortToolbar component in `frontend/src/components/layout/FilterSortToolbar.tsx`:
  - Combines FilterBar and SortDropdown
  - Horizontal layout matching existing UI

- [ ] T056 [US4] Create FilterContext in `frontend/src/lib/contexts/FilterContext.tsx`:
  - Manage filter state (status, priority, dueDate, tagIds)
  - Manage sort state (field, direction)
  - Persist to localStorage
  - Load from localStorage on mount

- [ ] T057 [US4] Update TaskDashboard in `frontend/src/components/tasks/TaskDashboard.tsx`:
  - Integrate FilterSortToolbar
  - Pass filter/sort params to API calls

- [ ] T058 [US4] Update API client searchTasks():
  - Add status, priority, due_date_from, due_date_to, tag_ids parameters
  - Add sort_by, sort_order parameters

- [ ] T059 [US4] Update SearchService:
  - Add status, priority, due_date range filters
  - Add sort_by, sort_order support
  - Combine with search and tag filters

- [ ] T060 [US4] Add due date range calculation utilities in `frontend/src/lib/dateUtils.ts`:
  - getTodayRange() -> { from, to }
  - getThisWeekRange() -> { from, to }
  - getThisMonthRange() -> { from, to }
  - isOverdue(task) -> boolean

---

## Phase 7: US5 - Recurring Tasks

**Goal**: Users can set tasks to recur daily/weekly/monthly with auto-reschedule on completion.

**Independent Test Criteria**:
- Task can be created with recurrence pattern
- When recurring task is completed, new instance is created
- New instance has same title, tags, priority, and recurrence pattern
- Original task remains in history as completed
- User can skip/cancel individual instances

### Implementation

- [ ] T061 [US5] Create RecurringConfig component in `frontend/src/components/tasks/RecurringConfig.tsx`:
  - Dropdown: Does not repeat, Daily, Weekly, Monthly
  - Shows next occurrence date preview
  - Visual indicator on task if recurring

- [ ] T062 [US5] Update TaskForm to include RecurringConfig:
  - Show when creating/editing task
  - Include recurrence_pattern in API request

- [ ] T063 [US5] Update TaskCard to show recurring indicator:
  - Small "repeat" icon on recurring tasks
  - Shows "Repeats [daily/weekly/monthly]" text
  - Links to parent task if instance

- [ ] T064 [US5] Create RecurringContext in `frontend/src/lib/contexts/RecurringContext.tsx`:
  - Track recurring instances
  - Handle auto-refresh when new instance created

- [ ] T065 [US5] Update POST /tasks endpoint:
  - Accept recurrence_pattern field
  - Store in task record

- [ ] T066 [US5] Create POST /tasks/{task_id}/complete endpoint:
  - Marks task as completed
  - If recurring, calls RecurringService.create_next_instance()
  - Returns both completed task and new instance

- [ ] T067 [US5] Implement RecurringService.complete_recurring_task():
  - Marks original task complete with timestamp
  - Calculates next due date based on pattern
  - Creates new task instance with same fields
  - Sets recurrence_parent_id to link instances

- [ ] T068 [US5] Add instance count limit to prevent infinite loops:
  - Max 100 instances per recurring series
  - Log warning when approaching limit

- [ ] T069 [US5] Create skip/cancel endpoints:
  - POST /tasks/{task_id}/skip - marks instance as skipped, creates next
  - DELETE /tasks/{task_id}/recurrence - removes recurrence pattern

- [ ] T070 [US5] Update frontend API client:
  - completeTask(userId, taskId) - handles recurring response
  - skipTask(userId, taskId)
  - cancelRecurrence(userId, taskId)

- [ ] T071 [US5] Update task list to show parent-child relationship:
  - Instances show link to parent task
  - Parent shows count of completed instances

- [ ] T072 [US5] Integration test for US5:
  - Create weekly recurring task with due date
  - Complete it
  - Verify new instance created 7 days later
  - Verify original marked complete
  - Verify new instance has same tags/priority
  - Skip an instance
  - Cancel recurrence on an instance

---

## Phase 8: US6 - Due Dates & Reminders

**Goal**: Users can set due dates with time and receive browser notifications.

**Independent Test Criteria**:
- User can set due date with time picker
- Due date displays on task card
- Browser notification triggers at due time
- User can snooze or dismiss notifications
- Timezone is handled correctly

### Implementation

- [ ] T073 [US6] Create DateTimePicker component in `frontend/src/components/tasks/DateTimePicker.tsx`:
  - Native datetime-local input with custom styling
  - Shows calendar popup for date selection
  - Shows time input
  - Clear button to remove due date

- [ ] T074 [US6] Create DueDateDisplay component in `frontend/src/components/tasks/DueDateDisplay.tsx`:
  - Shows formatted due date: "Due: Jan 10, 2:30 PM"
  - Color coding: red if overdue, yellow if due today, normal otherwise
  - Shows relative time: "Due in 2 hours" or "Overdue by 1 day"

- [ ] T075 [US6] Update TaskCard to display due date:
  - Add DueDateDisplay next to task info
  - Color code based on urgency

- [ ] T076 [US6] Update TaskForm to include DateTimePicker:
  - Include due_date and due_date_tz in API request
  - Store user timezone from browser

- [ ] T077 [US6] Create NotificationPermission component in `frontend/src/components/notifications/NotificationPermission.tsx`:
  - Request browser notification permission on first use
  - Show UI explanation: "Enable notifications to get reminders"
  - Retry button if permission denied

- [ ] T078 [US6] Create NotificationContext in `frontend/src/lib/contexts/NotificationContext.tsx`:
  - Track permission state
  - Schedule notifications for due dates
  - Handle notification clicks to open task
  - Handle snooze action

- [ ] T079 [US6] Create NotificationToast component in `frontend/src/components/notifications/NotificationToast.tsx`:
  - In-app notification display (for when browser permission denied)
  - Shows task title and due time
  - Snooze and dismiss buttons

- [ ] T080 [US6] Create notification scheduling hook in `frontend/src/hooks/useNotifications.ts`:
  - Request permission on mount (if not previously granted/denied)
  - Schedule browser notification at due time
  - Handle notification click to focus app

- [ ] T081 [US6] Update POST /tasks/{task_id}/reminder endpoint:
  - Create Reminder record with due_time
  - Accept timezone in request

- [ ] T082 [US6] Implement ReminderService:
  - create_reminder(task_id, due_time)
  - get_reminder_for_task(task_id)
  - snooze_reminder(reminder_id, minutes)
  - dismiss_reminder(reminder_id)

- [ ] T083 [US6] Create reminder cron/worker logic in `backend/src/workers/reminder_worker.py`:
  - Poll for due reminders every minute
  - Mark reminders as sent
  - (Frontend handles actual browser notification)

- [ ] T084 [US6] Add timezone utilities in `backend/src/utils/timezone.py`:
  - convert_to_utc(local_time, timezone)
  - convert_from_utc(utc_time, timezone)

---

## Phase 9: Integration & Polish

**Goal**: Ensure all features work together seamlessly and UI is polished.

### Implementation

- [ ] T085 Create comprehensive integration test suite:
  - Create task with priority, tags, due date, recurrence
  - Search for it, filter, sort
  - Complete recurring task
  - Verify new instance created correctly
  - Verify all data persists

- [ ] T086 Update dashboard to show all extended features:
  - Priority badges
  - Tag badges
  - Due date display
  - Recurring indicator
  - Filter/Sort toolbar

- [ ] T087 Add loading states for all API calls:
  - Skeleton loaders for task list
  - Button spinners for actions
  - Search debouncing indicator

- [ ] T088 Add error handling and toasts:
  - Show error toasts for failed API calls
  - Handle network errors gracefully
  - Show success toasts for actions

- [ ] T089 Ensure mobile responsiveness:
  - Filter/Sort toolbar collapses on mobile
  - PrioritySelector and TagInput work on touch devices
  - DateTimePicker works on mobile

- [ ] T090 Performance optimization:
  - Lazy load TagManager modal
  - Debounce search input (300ms)
  - Memoize expensive computations
  - Pagination for large task lists

- [ ] T091 Add keyboard shortcuts:
  - / to focus search
  - f to open filters
  - esc to clear filters

- [ ] T092 Accessibility improvements:
  - ARIA labels for all interactive elements
  - Keyboard navigation for dropdowns
  - Focus management for modals
  - Screen reader announcements for search results

- [ ] T093 Final end-to-end test:
  - Sign up new user
  - Create 10 tasks with various priorities, tags, due dates
  - Search and filter tasks
  - Create recurring task, complete it, verify new instance
  - Set due date with reminder
  - Verify all features work together

---

## Dependencies Graph

```
Phase 1 (Setup)
    │
    ▼
Phase 2 (Foundational: Models, Services, API Client)
    │
    ├─────────────────────────────────────────────┐
    │                                             │                                             │
    ▼                                             ▼                                             ▼
US1 (Priority)                            US2 (Tags)                              US3 (Search)
- Needs: Task model (Phase 2)            - Needs: Tag model (Phase 2)            - Needs: SearchService (Phase 2)
- Uses: API client (Phase 2)             - Uses: API client (Phase 2)            - Uses: API client (Phase 2)
    │                                         │                                         │
    └──────────────────┐                      └──────────────────┐                      └──────────────────┘
                       │                                            │                                            │
                       ▼                                            ▼                                            ▼
                  US4 (Filter/Sort)                          US5 (Recurring)                          US6 (Reminders)
                  - Needs: Priority (US1)                     - Needs: Task model (Phase 2)            - Needs: Due date field (US4)
                  - Needs: Tags (US2)                         - Uses: RecurringService (Phase 2)       - Uses: NotificationContext (Phase 8)
                  - Needs: Search (US3)                       - Uses: Task completion flow             - Uses: ReminderService (Phase 2)
                  - Uses: Filter/Sort API (Phase 2)              (US1-4 integration)                 - Uses: Due date field on Task
                       │                                         │
                       └──────────────────┐                      └──────────────────┐
                                            │                                            │
                                            ▼                                            ▼
                                    US5 & US6 complete                                  All US complete
                                            │                                            │
                                            ▼
                                    Phase 9 (Integration & Polish)
```

---

## Parallel Execution Examples

### Example 1: Phase 2 Can Run in Parallel
- T009, T010, T011, T012 (Model creation) - 4 parallel tasks
- T014, T015, T016, T017 (Service creation) - 4 parallel tasks
- T019, T020 (Frontend API client) - parallel with services

### Example 2: US1 Tasks Can Run in Parallel
- T021, T022 (Frontend Priority components) - parallel
- T023, T024 (Update existing components) - parallel
- T025 (Backend endpoint) - can run with frontend
- T026, T027 (Search service updates) - parallel with endpoint

### Example 3: US2 Tasks Can Run in Parallel
- T029, T030, T031 (Tag UI components) - parallel
- T035, T036 (Tag API endpoints) - parallel
- T037, T038, T040 (Search service & API) - parallel

### Example 4: US3 Tasks Can Run in Parallel
- T043, T044, T045 (Search UI) - parallel
- T047, T048 (Backend search) - parallel
- T050, T051 (Testing) - can run after both complete

---

## MVP Scope

**Recommended MVP**: US1 (Priority) + US2 (Tags)

**Rationale**:
1. Priority is simplest extension - just adds a field and UI display
2. Tags provide immediate organization value
3. Search, Filter/Sort, Recurring, and Reminders build on these foundations
4. Each additional story adds significant complexity

**MVP Tasks**: T001-T042 (42 tasks)
- Phase 1: T001-T008 (8 tasks)
- Phase 2: T009-T020 (12 tasks)
- US1: T021-T028 (8 tasks)
- US2: T029-T042 (14 tasks)

**After MVP**: Continue with US3→US4→US5→US6 sequentially as they build on each other.

---

## File Paths Reference

### Backend
```
backend/src/
├── models/
│   ├── __init__.py (update exports)
│   ├── task.py (update)
│   ├── task_tag_link.py (new)
│   ├── tag.py (new)
│   └── reminder.py (new)
├── schemas/
│   ├── __init__.py (update exports)
│   └── task_extended.py (new)
├── services/
│   ├── __init__.py (update exports)
│   ├── tag_service.py (new)
│   ├── search_service.py (new)
│   ├── recurring_service.py (new)
│   └── reminder_service.py (new)
├── routes/
│   ├── tasks.py (update)
│   ├── tags.py (new)
│   └── tag_tasks.py (new)
├── utils/
│   └── timezone.py (new)
└── workers/
    └── reminder_worker.py (new)

backend/migrations/
└── 004_extended_features.sql (new)
```

### Frontend
```
frontend/src/
├── components/
│   ├── tasks/
│   │   ├── PrioritySelector.tsx (new)
│   │   ├── PriorityBadge.tsx (new)
│   │   ├── TagBadge.tsx (new)
│   │   ├── TagInput.tsx (new)
│   │   ├── TagManager.tsx (new)
│   │   ├── SearchBar.tsx (new)
│   │   ├── SearchEmptyState.tsx (new)
│   │   ├── FilterBar.tsx (new)
│   │   ├── SortDropdown.tsx (new)
│   │   ├── DateTimePicker.tsx (new)
│   │   ├── RecurringConfig.tsx (new)
│   │   ├── TaskCard.tsx (update)
│   │   └── TaskForm.tsx (update)
│   ├── notifications/
│   │   ├── NotificationPermission.tsx (new)
│   │   └── NotificationToast.tsx (new)
│   ├── layout/
│   │   ├── FilterSortToolbar.tsx (new)
│   │   └── TaskDashboard.tsx (update)
├── lib/
│   ├── api.ts (update)
│   ├── contexts/
│   │   ├── FilterContext.tsx (new)
│   │   ├── SearchContext.tsx (new)
│   │   └── NotificationContext.tsx (new)
│   └── constants.ts (update)
├── hooks/
│   └── useNotifications.ts (new)
├── types/
│   ├── index.ts (update)
│   └── task-extended.ts (new)
└── utils/
    └── dateUtils.ts (new)
```

---

**Tasks Status**: ✅ GENERATED AND VALIDATED
**Next Step**: Run `/sp.implement` to execute tasks, or invoke specialized agents:
- Backend Agent for backend tasks (T001-T018, T025, T035-T038, T047-T050, T065-T070, T081-T084)
- Frontend Agent for frontend tasks (T004-T008, T019-T024, T029-T034, T039-T042, T043-T046, T053-T060, T061-T076, T077-T080)
- Database Agent for migration verification

---

**Generated By**: Claude (AI Task Generation)
**Date**: 2026-01-03
**Feature**: 004-task-organization-intelligence
**Total Tasks**: 89
