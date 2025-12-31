# Tasks: Todo Web UI Design

**Input**: Design documents from `/specs/003-todo-web-ui/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)

## Path Conventions

- **Web app**: `frontend/src/`
- All paths are relative to `frontend/src/` unless specified otherwise

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x ] T001 Initialize Next.js project in frontend/ directory
- [ ] T002 [P] Install primary dependencies: lucide-react, better-auth, clsx, tailwind-merge
- [ ] T003 [P] Configure Tailwind CSS with Pink/White theme tokens in frontend/tailwind.config.ts

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

- [ ] T004 Setup global layout with Header and Footer components in frontend/src/components/layout/
- [ ] T005 [P] Create shared UI components: Button, Input, Card in frontend/src/components/ui/
- [ ] T006 [P] Implement Pink + White global CSS variables in frontend/src/styles/globals.css
- [ ] T007 Create AuthLayout wrapper for login/signup screens in frontend/src/components/layout/AuthLayout.tsx

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Quick Task Onboarding (Priority: P1) 🎯 MVP

**Goal**: Enable users to sign up and view an empty dashboard with "Add Task" capability.

**Independent Test**: Navigate to /signup, create account, and see the dashboard empty state.

### Implementation for User Story 1

- [ ] T008 [P] [US1] Create SignUpForm component in frontend/src/components/features/auth/SignUpForm.tsx
- [ ] T009 [P] [US1] Create Sign-up page at frontend/src/app/(auth)/signup/page.tsx
- [ ] T010 [US1] Implement empty state Dashboard at frontend/src/app/(dashboard)/page.tsx
- [ ] T011 [US1] Create AddTaskModal component in frontend/src/components/features/tasks/AddTaskModal.tsx

**Checkpoint**: User Story 1 (Sign up + Onboarding) fully functional and testable independently.

---

## Phase 4: User Story 2 - Daily Task Management (Priority: P2)

**Goal**: Enable users to view, complete, and switch views via sidebar.

**Independent Test**: View list of tasks, toggle checkbox, and use sidebar to filter "Completed" tasks.

### Implementation for User Story 2

- [ ] T012 [P] [US2] Create Sidebar component with Tasks/Completed/Settings navigation in frontend/src/components/layout/Sidebar.tsx
- [ ] T013 [P] [US2] Create TaskCard component with Priority badges and Status toggle in frontend/src/components/features/tasks/TaskCard.tsx
- [ ] T014 [US2] Implement TaskList component for Dashboard in frontend/src/components/features/tasks/TaskList.tsx
- [ ] T015 [US2] Implement Sign-in page at frontend/src/app/(auth)/signin/page.tsx
- [ ] T016 [US2] Add filtering logic to Dashboard for Tasks vs Completed views

**Checkpoint**: User Story 2 (List + State Toggle + Navigation) functional independently.

---

## Phase 5: User Story 3 - Bulk Task Cleanup (Priority: P3)

**Goal**: Enable multi-selection and bulk actions for tasks.

**Independent Test**: Select multiple tasks and use the "Mark as Complete" or "Delete" floating action bar.

### Implementation for User Story 3

- [ ] T017 [US3] Add Multi-select capability to TaskCard and TaskList components
- [ ] T018 [US3] Create BulkActionBar component in frontend/src/components/features/tasks/BulkActionBar.tsx
- [ ] T019 [US3] Integrate BulkActionBar with Dashboard state for deletion/completion

**Checkpoint**: All user stories should now be independently functional.

---

## Phase 6: Polish & Cross-Cutting Concerns

- [ ] T020 [P] Add responsive "Humburger" menu for Sidebar on mobile viewports
- [ ] T021 [P] Ensure 100% WCAG AA contrast compliance for all buttons/text in components/ui/
- [ ] T022 Implement loading skeletons for TaskList rendering in frontend/src/components/features/tasks/TaskSkeleton.tsx
- [ ] T023 Run verification against spec.md requirements

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies
- **Foundational (Phase 2)**: Depends on Phase 1
- **User Stories (Phase 3+)**: Depend on Phase 2 (Foundational)
- **Polish (Phase 6)**: Final step

### Parallel Opportunities

- T002, T003 can run in parallel
- T005, T006 can run in parallel
- Once Phase 2 is done, User Stories (US1, US2) can proceed mostly in parallel as they touch different features (Auth vs Tasks/Sidebar).
- T008, T009 (SignUp) vs T011 (AddTask) can run in parallel.

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Setup + Foundational.
2. Complete US1 (SignUp + Dashboard Empty State).
3. **VALIDATE**: Ensure user can land on dashboard after signup.

### Incremental Delivery

1. Foundation ready.
2. US1 -> Live Onboarding.
3. US2 -> List Management (Primary value).
4. US3 -> Power User features.
