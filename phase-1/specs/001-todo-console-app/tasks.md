# Tasks: In-Memory Todo Console Application

**Input**: Design documents from `specs/001-todo-console-app/`
**Prerequisites**: plan.md (required), spec.md (required), data-model.md
**Tests**: Not required for Phase I (manual CLI testing only)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/` at repository root
- Paths: `src/todo_app/models.py`, `src/todo_app/storage.py`, `src/todo_app/cli.py`, `src/todo_app/main.py`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create UV project structure in src/todo_app/
- [x] T002 [P] Create __init__.py in src/todo_app/
- [x] T003 [P] Create empty models.py, storage.py, cli.py, main.py files

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Create Task dataclass in src/todo_app/models.py
- [x] T005 [P] Create TaskList storage class in src/todo_app/storage.py
- [x] T006 [P] Create CLI command parser in src/todo_app/cli.py
- [x] T007 Create main entry point in src/todo_app/main.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add New Todo (Priority: P1) MVP

**Goal**: Users can create new tasks with a title that are stored in memory

**Independent Test**: User runs app, types `add "Buy groceries"`, and sees task created with ID

### Implementation for User Story 1

- [x] T008 [US1] Implement add command in src/todo_app/cli.py (calls TaskList.add)
- [x] T009 [US1] Implement TaskList.add method in src/todo_app/storage.py

**Checkpoint**: User Story 1 functional - can add tasks to the list

---

## Phase 4: User Story 2 - View All Todos (Priority: P1)

**Goal**: Users can see all tasks with their completion status

**Independent Test**: User adds tasks, types `list`, and sees formatted task list

### Implementation for User Story 2

- [x] T010 [US2] Implement list command in src/todo_app/cli.py (calls TaskList.get_all)
- [x] T011 [US2] Implement TaskList.get_all method in src/todo_app/storage.py

**Checkpoint**: User Stories 1 AND 2 functional - can add and view tasks

---

## Phase 5: User Story 3 - Mark Todo as Complete (Priority: P1)

**Goal**: Users can mark tasks as complete to track progress

**Independent Test**: User adds task, types `complete 1`, task shows as complete

### Implementation for User Story 3

- [x] T012 [US3] Implement complete command in src/todo_app/cli.py (calls TaskList.toggle_complete)
- [x] T013 [US3] Implement TaskList.toggle_complete method in src/todo_app/storage.py

**Checkpoint**: All P1 features working - Add, View, Complete

---

## Phase 6: User Story 4 - Update Todo Title (Priority: P2)

**Goal**: Users can change a task's title to correct or refine descriptions

**Independent Test**: User updates task 1, task title changes, status unchanged

### Implementation for User Story 4

- [x] T014 [US4] Implement update command in src/todo_app/cli.py (calls TaskList.update_title)
- [x] T015 [US4] Implement TaskList.update_title method in src/todo_app/storage.py

**Checkpoint**: Update feature working - 4 of 5 features complete

---

## Phase 7: User Story 5 - Delete Todo (Priority: P2)

**Goal**: Users can remove tasks from the list

**Independent Test**: User deletes task 1, task removed, other tasks unchanged

### Implementation for User Story 5

- [x] T016 [US5] Implement delete command in src/todo_app/cli.py (calls TaskList.delete)
- [x] T017 [US5] Implement TaskList.delete method in src/todo_app/storage.py

**Checkpoint**: All 5 features working

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T018 [P] Add help command to show all available commands
- [x] T019 [P] Add exit command for graceful application shutdown
- [x] T020 [P] Add error handling for invalid IDs and empty titles
- [x] T021 Run quickstart.md validation to verify all features work

---

## Phase 9: UX Improvements (Working Demo Requirements)

**Purpose**: Match the working console demo requirements from spec.md

**UX Requirements from Plan**:
- Clear screen titles
- Input guidance with examples
- Status indicators ([  TODO ] / [✓ DONE])
- User feedback (✓ ✗ ℹ icons)
- Arrow navigation with ▶ indicator
- Confirmation dialogs for delete
- Error recovery prompts

### Implementation for UX Features

- [x] T022 [UX] Create InteractiveUI class in src/todo_app/ui.py for user-friendly navigation
- [x] T023 [UX] Implement clear screen titles (ADD NEW TASK, VIEW TASKS, etc.)
- [x] T024 [UX] Add input guidance with examples in handle_add_task()
- [x] T025 [UX] Display task count before adding new task
- [x] T026 [UX] Implement [  TODO ] and [✓ DONE] status indicators in task list
- [x] T027 [UX] Add arrow navigation with ▶ marker in menus
- [x] T028 [UX] Add success/error/info icons (✓ ✗ ℹ) for user feedback
- [x] T029 [UX] Implement "Add another task?" prompt after task creation
- [x] T030 [UX] Add y/n confirmation dialog for delete operation
- [x] T031 [UX] Add "Press Enter to continue" for error recovery
- [x] T032 [UX] Show before/after comparison when editing task title
- [x] T033 [UX] Add task detail screen with actions (c=complete, d=delete, e=edit, q=back)

## Phase 10: Remediation & Refinement (from sp.analyze)

**Purpose**: Fix inconsistencies and missing validations identified during analysis

- [x] T034 [Polish] Enforce 200 character limit on task titles in ui.py
- [x] T035 [UX] Consolidate status terminology to "PENDING" throughout ui.py
- [x] T036 [Performance] Remove redundant get_all() call in handle_view_tasks

**Checkpoint**: Phase 1 fully spec-compliant and optimized

---

## Dependencies & Execution Order

### Phase Dependencies

| Phase | Dependencies | Blocks |
|-------|--------------|--------|
| Setup (Phase 1) | None | Foundational |
| Foundational (Phase 2) | Setup | All User Stories |
| User Stories (3-7) | Foundational | Polish |
| Polish (Phase 8) | All User Stories | Complete |

### User Story Dependencies

| User Story | Can Start After | Dependencies |
|------------|-----------------|--------------|
| US1: Add | Foundational | Task dataclass, TaskList |
| US2: View | Foundational | Task dataclass, TaskList |
| US3: Complete | Foundational | Task dataclass, TaskList |
| US4: Update | Foundational | Task dataclass, TaskList |
| US5: Delete | Foundational | Task dataclass, TaskList |

**Note**: All user stories can proceed in parallel after Foundational phase since they all depend on the same Task/TaskList foundation.

### Within Each User Story

- Models before storage
- Storage before CLI commands
- Each story complete before moving to next (or run in parallel)

---

## Parallel Opportunities

### Independent Execution Paths

```bash
# Path A: Setup and Foundational (blocking - must complete first)
T001 → T002 → T003 → T004 → T005 → T006 → T007

# Path B: User Story 1 (can start after T004, T005)
T008, T009

# Path C: User Story 2 (can start after T004, T005)
T010, T011

# Path D: User Story 3 (can start after T004, T005)
T012, T013

# Path E: User Story 4 (can start after T004, T005)
T014, T015

# Path F: User Story 5 (can start after T004, T005)
T016, T017

# Path G: Polish (after all user stories)
T018, T019, T020, T021
```

### Parallel Example: All User Stories Together

After completing Phase 2 (Foundational), all user stories can run in parallel:

```bash
# Run these together:
T008 [US1] + T010 [US2] + T012 [US3] + T014 [US4] + T016 [US5]
T009 [US1] + T011 [US2] + T013 [US3] + T015 [US4] + T017 [US5]
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T003)
2. Complete Phase 2: Foundational (T004-T007) - CRITICAL
3. Complete Phase 3: User Story 1 (T008-T009)
4. **STOP and VALIDATE**: Test adding tasks
5. Demo basic MVP!

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test → MVP!
3. Add User Story 2 → Test → Can view tasks
4. Add User Story 3 → Test → Can mark complete
5. Add User Story 4 → Test → Can update titles
6. Add User Story 5 → Test → Can delete tasks
7. Polish → Final product

### Summary for Solo Developer

1. Setup (30 min)
2. Foundational (45 min)
3. US1-US5 each (15 min each) = 75 min
4. Polish (30 min)
5. **Total: ~3 hours**

---

## Task Summary

| Metric | Count |
|--------|-------|
| Total Tasks | 33 |
| Setup Tasks | 3 |
| Foundational Tasks | 4 |
| User Story Tasks | 10 (2 per story) |
| Polish Tasks | 4 |
| UX Tasks | 12 |

| User Story | Tasks | Priority |
|------------|-------|----------|
| US1: Add | T008, T009 | P1 |
| US2: View | T010, T011 | P1 |
| US3: Complete | T012, T013 | P1 |
| US4: Update | T014, T015 | P2 |
| US5: Delete | T016, T017 | P2 |
| UX | T022-T033 | UX |

---

## Notes

- [P] tasks = different files, no dependencies on incomplete tasks
- [Story] label maps task to specific user story for traceability
- All user stories are independently testable after Foundational phase
- Phase I uses manual CLI testing only (no automated tests)
- Commit after each task or logical group
- Stop at checkpoints to validate story independently
