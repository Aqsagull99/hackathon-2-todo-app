# Implementation Tasks: Todo App Phase I Extended Features

**Branch**: `002-phase1-extended-features` | **Date**: 2026-01-01
**Generated from**: [spec.md](spec.md), [plan.md](plan.md), [data-model.md](data-model.md), [contracts/commands.md](contracts/commands.md)

---

## Summary

**Total Tasks**: 38
**Task Distribution**:
- Setup: 2 tasks
- Foundational: 3 tasks
- User Story 1 (Priorities & Tags): 10 tasks
- User Story 2 (Search): 4 tasks
- User Story 3 (Filter & Sort): 8 tasks
- User Story 4 (Recurring & Reminders): 8 tasks
- Polish: 3 tasks

**MVP Scope**: Complete Phase 1 (Setup) + Phase 2 (Foundational) + User Story 1 (Priorities & Tags)
**Parallel Opportunities**: Identified within each user story phase

---

## Dependency Graph

```
Phase 1 (Setup)
    ↓
Phase 2 (Foundational)
    ↓
    ├─→ Phase 3 (US1: Priorities & Tags) [P1]
    ├─→ Phase 4 (US2: Search) [P1]
    ├─→ Phase 5 (US3: Filter & Sort) [P2]
    └─→ Phase 6 (US4: Recurring & Reminders) [P2]
              ↓
        Phase 7 (Polish)
```

**Notes**:
- User Stories 1 and 2 are independent and can be implemented in parallel after Phase 2
- User Stories 3 and 4 are independent of each other
- All user stories share Phase 2 as a dependency

---

## Phase 1: Setup

**Goal**: Initialize project infrastructure for extended features

### Tasks

- [X] T001 Create notification_manager.py skeleton in Phase-one/src/todo_app/notifications.py
- [X] T002 Add import statements to main.py for new modules in src/todo_app/main.py

**Independent Test Criteria**: App starts without import errors, notification module accessible

---

## Phase 2: Foundational

**Goal**: Extend data model with enums and optional fields

### Tasks

- [X] T003 [P] Create Priority enum in src/todo_app/models.py
- [X] T004 [P] Create Recurrence enum in src/todo_app/models.py
- [X] T005 Extend Task dataclass with priority, tags, due_date, recurrence fields in src/todo_app/models.py

**Independent Test Criteria**:
- Priority and Recurrence enums defined with correct values
- Task dataclass compiles with new fields and defaults
- Existing Phase I code still imports Task successfully

---

## Phase 3: User Story 1 - Task Organization (Priorities & Tags)

**Priority**: P1 | **Goal**: Users can assign priorities and tags to tasks

### Independent Test Criteria
1. User can create a task with priority and tags
2. User can view task priority and tags in task list
3. User can update task priority
4. User can add and remove tags from tasks
5. All operations work alongside existing CRUD

### Tasks

**Model Updates**:
- [X] T006 [US1] Add priority field to Task constructor in src/todo_app/models.py
- [X] T007 [US1] Add tags field to Task constructor in src/todo_app/models.py

**Storage Methods**:
- [X] T008 [US1] Implement update_priority method in src/todo_app/storage.py
- [X] T009 [US1] Implement add_tags method in src/todo_app/storage.py
- [X] T010 [US1] Implement remove_tags method in src/todo_app/storage.py

**CLI Commands**:
- [X] T011 [US1] Implement priority command handler in src/todo_app/cli.py
- [X] T012 [US1] Implement tag command handler in src/todo_app/cli.py
- [X] T013 [US1] Implement untag command handler in src/todo_app/cli.py
- [X] T014 [US1] Update add command to accept optional priority and tags arguments in src/todo_app/cli.py

**UI Updates**:
- [X] T015 [US1] Update task display to show priority and tags in src/todo_app/ui.py

**Parallel Opportunities**:
- T011, T012, T013 can be implemented in parallel (different files, no shared dependencies)

---

## Phase 4: User Story 2 - Search and Discovery

**Priority**: P1 | **Goal**: Users can search tasks by keyword

### Independent Test Criteria
1. User can search by keyword matching titles
2. User can search by keyword matching tags
3. Search returns "No matching tasks found" when no results
4. Search is case-insensitive

### Tasks

**Storage Methods**:
- [X] T016 [US2] Implement search method in src/todo_app/storage.py

**CLI Commands**:
- [X] T017 [US2] Implement search command handler in src/todo_app/cli.py
- [X] T018 [US2] Register search command in command dispatcher in src/todo_app/cli.py

**UI Updates**:
- [X] T019 [US2] Create search results display function in src/todo_app/ui.py

**Parallel Opportunities**:
- T017, T018 can be implemented in parallel after T016

---

## Phase 5: User Story 3 - Filtering and Sorting

**Priority**: P2 | **Goal**: Users can filter and sort task list

### Independent Test Criteria
1. User can filter by status (pending/completed)
2. User can filter by priority (High/Medium/Low)
3. User can filter by due date range
4. User can sort by due date, priority, or name
5. Filters can be combined
6. Sort order can be ascending or descending

### Tasks

**Storage Methods**:
- [X] T020 [US3] Implement filter_by_status method in src/todo_app/storage.py
- [X] T021 [US3] Implement filter_by_priority method in src/todo_app/storage.py
- [X] T022 [US3] Implement filter_by_due_date method in src/todo_app/storage.py
- [X] T023 [US3] Implement sort_by_date method in src/todo_app/storage.py
- [X] T024 [US3] Implement sort_by_priority method in src/todo_app/storage.py
- [X] T025 [US3] Implement sort_by_name method in src/todo_app/storage.py

**CLI Commands**:
- [X] T026 [US3] Implement filter command handler with option parsing in src/todo_app/cli.py
- [X] T027 [US3] Implement sort command handler with option parsing in src/todo_app/cli.py

**UI Updates**:
- [X] T028 [US3] Update task list display to work with sorted results in src/todo_app/ui.py

**Parallel Opportunities**:
- T020-T025 can be implemented in parallel (independent methods)
- T026, T027 can be implemented in parallel after storage methods complete

---

## Phase 6: User Story 4 - Intelligent Features (Recurring & Reminders)

**Priority**: P2 | **Goal**: Tasks can repeat and trigger reminders

### Independent Test Criteria
1. User can set recurrence pattern (Daily/Weekly/None)
2. User can set due date and time
3. Completing a recurring task creates a new instance for next period
4. check-reminders triggers notifications for overdue tasks
5. Notifications work on Linux, macOS, Windows (or fallback to console)

### Tasks

**Model Updates**:
- [X] T029 [US4] Create RecurrenceManager class with calculate_next_due_date method in src/todo_app/models.py

**Storage Methods**:
- [X] T030 [US4] Implement set_due_date method in src/todo_app/storage.py
- [X] T031 [US4] Implement set_recurrence method in src/todo_app/storage.py
- [X] T032 [US4] Modify toggle_complete to create recurring instances in src/todo_app/storage.py
- [X] T033 [US4] Implement create_recurring_instance method in src/todo_app/storage.py
- [X] T034 [US4] Implement check_reminders method in src/todo_app/storage.py

**Notification System**:
- [X] T035 [US4] Implement NotificationManager class in src/todo_app/notifications.py
- [X] T036 [US4] Implement platform detection in src/todo_app/notifications.py
- [X] T037 [US4] Implement _notify_linux method in src/todo_app/notifications.py
- [X] T038 [US4] Implement _notify_macos method in src/todo_app/notifications.py
- [X] T039 [US4] Implement _notify_windows method in src/todo_app/notifications.py
- [X] T040 [US4] Implement _notify_console fallback method in src/todo_app/notifications.py

**CLI Commands**:
- [X] T041 [US4] Implement due command handler in src/todo_app/cli.py
- [X] T042 [US4] Implement recurring command handler in src/todo_app/cli.py
- [X] T043 [US4] Implement check-reminders command handler in src/todo_app/cli.py

**UI Updates**:
- [X] T044 [US4] Update add command UI to accept optional extended fields in src/todo_app/ui.py
- [X] T045 [US4] Add due date display to task view in src/todo_app/ui.py

**Parallel Opportunities**:
- T037-T040 can be implemented in parallel (independent platform methods)
- T041, T042, T043 can be implemented in parallel (different commands)

---

## Phase 7: Polish & Cross-Cutting Concerns

**Goal**: Final integration, error handling, and user experience polish

### Tasks

- [X] T046 Update main menu to include all new commands in src/todo_app/ui.py
- [X] T047 Add validation and error messages for all extended commands in src/todo_app/cli.py
- [X] T048 Update help text to document all new commands and options in src/todo_app/cli.py

---

## Dependencies

### Phase Dependencies
- **Phase 1**: No dependencies
- **Phase 2**: Depends on Phase 1
- **Phase 3 (US1)**: Depends on Phase 2
- **Phase 4 (US2)**: Depends on Phase 2
- **Phase 5 (US3)**: Depends on Phase 2
- **Phase 6 (US4)**: Depends on Phase 2
- **Phase 7**: Depends on Phases 3-6

### User Story Dependencies
- **US1**: No external story dependencies
- **US2**: No external story dependencies
- **US3**: No external story dependencies
- **US4**: No external story dependencies

### Task Dependencies within Stories

**US1 Dependencies**:
- T014 depends on T006, T007, T011-T013
- T015 depends on T014

**US2 Dependencies**:
- T018 depends on T017
- T019 depends on T016

**US3 Dependencies**:
- T028 depends on T023-T027

**US4 Dependencies**:
- T032 depends on T029-T034
- T041-T043 depend on T030, T031, T034, T035-T040
- T045 depends on T041
- T044 depends on T011-T013 (reuses add command structure)

---

## Implementation Strategy

### MVP Approach (Incremental Delivery)

1. **MVP 1**: Complete Phases 1-3 (US1: Priorities & Tags)
   - Enables basic organization features
   - Testable independently
   - High user value (P1 priority)

2. **MVP 2**: Add Phase 4 (US2: Search)
   - Enables task discovery
   - Low risk, independent
   - P1 priority

3. **MVP 3**: Add Phase 5 (US3: Filter & Sort)
   - Advanced organization features
   - P2 priority
   - Completes organization suite

4. **MVP 4**: Add Phase 6 (US4: Recurring & Reminders)
   - Intelligent features
   - P2 priority
   - Complete feature set

5. **Final**: Phase 7 (Polish)
   - Integration testing
   - Error handling polish
   - Documentation updates

### Incremental Delivery Checklist

- [X] Each user story independently testable after completion
- [X] Backward compatibility verified after each phase
- [X] Manual CLI testing after each story
- [X] No breaking changes to existing CRUD operations
- [X] All extended features optional (defaults applied)

---

## Testing Strategy

### Manual Testing Approach

**Per User Story**:
1. **Unit Test**: Test each new CLI command individually
2. **Integration Test**: Test command combinations (e.g., add with priority + tags, then search)
3. **Regression Test**: Verify existing commands (add, list, complete, delete) still work
4. **Edge Case Test**: Test with empty lists, invalid inputs, special characters

**Cross-Cutting Tests**:
- Verify notifications trigger on all platforms (or fallback gracefully)
- Test recurring task boundary conditions (month end, leap year)
- Test filter + sort combinations
- Verify search accuracy (100% keyword matching)

---

## Definition of Done

- [X] All 48 tasks marked complete
- [X] All user stories pass independent test criteria
- [X] Backward compatibility verified (Phase I CRUD still works)
- [X] Manual CLI testing completed for all features
- [X] Code review: No external dependencies, clean structure
- [X] Ready for Phase II (full-stack web app migration)

---

**Version**: 1.0.0 | **Status**: READY FOR IMPLEMENTATION | **Total Tasks**: 48
