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

## Phase 1: Setup (Shared Infrastructure) ✅ COMPLETED

**Purpose**: Project initialization and basic structure

- [x] T001 Initialize Next.js project in frontend/ directory
- [x] T002 [P] Install primary dependencies: lucide-react, better-auth, clsx, tailwind-merge
- [x] T003 [P] Configure Tailwind CSS with Pink/White theme tokens in frontend/tailwind.config.ts

---

## Phase 2: Foundational (Blocking Prerequisites) ✅ COMPLETED

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

- [x] T004 Setup global layout with Header and Footer components in frontend/src/components/layout/
- [x] T005 [P] Create shared UI components: Button, Input, Card in frontend/src/components/ui/
- [x] T006 [P] Implement Pink + White global CSS variables in frontend/src/app/globals.css
- [x] T007 Create AuthLayout wrapper for login/signup screens in frontend/src/components/layout/AuthLayout.tsx

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 2.5: Route Cleanup & CSS Fixes 🔧 IN PROGRESS

**Purpose**: Remove duplicate routes, fix CSS loading, ensure consistent Pink/White theme

- [x] T006A Clean up duplicate authentication routes (removed (auth) folder)
- [x] T006B Remove duplicate CSS file (removed src/styles/globals.css)
- [x] T006C **Update /login page with consistent Pink/White theme and proper layout**
- [x] T006D **Update /register page with consistent Pink/White theme and proper layout**
- [x] T006E **Verify all UI components use CSS variables from globals.css**
- [x] T006F **Test responsive behavior on mobile/tablet/desktop**

**Checkpoint**: Clean routing structure with consistent theming across all pages

---

## Phase 3: User Story 1 - Quick Task Onboarding (Priority: P1) 🎯 MVP (PARTIAL)

**Goal**: Enable users to sign up and view an empty dashboard with "Add Task" capability.

**Independent Test**: Navigate to /register, create account, and see the dashboard empty state.

### Implementation for User Story 1

- [x] T008 [P] [US1] Create RegisterForm component (Better Auth integrated)
- [x] T009 [P] [US1] Create Register page at frontend/src/app/register/page.tsx
- [x] T010 [US1] Implement Dashboard at frontend/src/app/dashboard/page.tsx (with Better Auth)
- [x] T011 [US1] Create AddTaskModal component in frontend/src/components/features/tasks/AddTaskModal.tsx

**Status**: Core functionality complete, CSS refinement needed

---

## Phase 4: User Story 2 - Daily Task Management (Priority: P2) (PARTIAL)

**Goal**: Enable users to view, complete, and switch views via sidebar.

**Independent Test**: View list of tasks, toggle checkbox, and use sidebar to filter "Completed" tasks.

### Implementation for User Story 2

- [x] T012 [P] [US2] Create Sidebar component in frontend/src/components/layout/Sidebar.tsx
- [x] T013 [P] [US2] Create TaskCard component in frontend/src/components/features/tasks/TaskCard.tsx
- [x] T014 [US2] Implement TaskList component in frontend/src/components/features/tasks/TaskList.tsx
- [x] T015 [US2] Implement Login page at frontend/src/app/login/page.tsx (Better Auth integrated)
- [x] T016 [US2] Add filtering logic to Dashboard for Tasks vs Completed views

**Status**: ✅ COMPLETE - Dashboard with Sidebar filtering fully functional

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

- [ ] T020 [P] Add responsive "Hamburger" menu for Sidebar on mobile viewports
- [ ] T021 [P] Ensure 100% WCAG AA contrast compliance for all buttons/text in components/ui/
- [ ] T022 Implement loading skeletons for TaskList rendering in frontend/src/components/features/tasks/TaskSkeleton.tsx
- [ ] T023 Run verification against spec.md requirements

---

## Current Priority Tasks (Next Steps)

**Focus**: Complete Phase 2.5 CSS fixes before proceeding with new features

1. **T006C** - Update /login page theme consistency
2. **T006D** - Update /register page theme consistency
3. **T006E** - Verify component CSS variable usage
4. **T006F** - Test responsive behavior
5. **T016** - Add Dashboard filtering logic

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
