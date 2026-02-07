---
description: "Task list for Advanced Cloud Deployment of AI-Native Todo Chatbot implementation"
---

# Tasks: Phase V - Advanced Cloud Deployment of AI-Native Todo Chatbot

**Input**: Design documents from `/specs/007-phase-v-cloud-deployment/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions (CRITICAL - Use Actual Project Structure)

**Existing Paths from Phase I-IV:**
- **Backend**: `phase-2/backend/app/` (models, routes, services, agents, mcp)
- **Frontend**: `phase-2/frontend/src/` (components, lib, app)
- **Helm Charts**: `phase-4/helm/todo-backend/` and `phase-4/helm/todo-frontend/`
- **Dockerfiles**: `phase-2/backend/Dockerfile` and `phase-2/frontend/Dockerfile`

**New Paths for Phase V:**
- **Dapr Components**: `phase-4/helm/dapr-components/` (pubsub, state, bindings, secrets)
- **Event Services**: `phase-2/backend/app/events/` (publisher, consumer, handlers)
- **CI/CD**: `.github/workflows/` (deploy-doks.yml, etc.)
- **Phase V Specs**: `phase-5/specs/007-phase-v-cloud-deployment/`

## Phase 1: Review & Extension Planning (Understand existing Phases I-IV)

**Purpose**: Review completed Phase I-IV implementation and plan Phase V extensions

**CRITICAL**: Phases I-IV are COMPLETED. We are EXTENDING, not creating from scratch.

- [x] T001 Review Phase IV Kubernetes deployment in phase-4/helm/ to understand current Helm chart structure (deployments, services, ingress)
- [x] T002 Review Phase III chatbot implementation in phase-2/backend/app/agents/todo_agent.py and phase-2/backend/app/api/routes/chat.py
- [x] T003 Review Phase II database models in phase-2/backend/app/models/task.py and conversation.py to plan schema extensions for advanced features
- [x] T004 Document extension points for Phase V: where to add due dates, priorities, tags, recurrence patterns to existing Task model
- [x] T005 [P] Add Python dependencies for Dapr SDK and Kafka client to phase-2/backend/pyproject.toml
- [x] T006 [P] Review existing phase-2/frontend/package.json to confirm ChatKit and Next.js dependencies are current

---

## Phase 2: Database Schema Extensions (Extend Phase II models)

**Purpose**: Extend existing SQLModel Task model with advanced feature fields

**⚠️ CRITICAL**: Extend existing Phase II models, do NOT create new files from scratch

- [x] T007 Extend existing Task model in phase-2/backend/app/models/task.py with new fields:
  - due_date: Optional[datetime]
  - priority: Enum["low", "medium", "high"]
  - tags: List[str] (JSON field or separate table)
  - recurrence_pattern: Optional[str] (cron-like string)
  - next_occurrence: Optional[datetime]
- [x] T008 Create database migration script for Phase V schema changes in phase-2/backend/alembic/versions/ (if using Alembic)
- [x] T009 Test schema migration on local Neon DB instance

**Checkpoint**: Schema extensions complete - ready for service layer

---

## Phase 3: Service Layer Extensions (Extend Phase II services)

**Purpose**: Add business logic services for advanced features

**⚠️ CRITICAL**: Integrate with existing phase-2/backend/app/services/ directory structure

- [x] T010 [P] Create recurring task service in phase-2/backend/app/services/recurring_tasks.py
  - Function: spawn_next_occurrence(task_id) - creates next recurring task instance
  - Integration point: Called when task marked complete
- [x] T011 [P] Create due date and reminder service in phase-2/backend/app/services/reminders.py
  - Function: check_due_reminders() - scans for upcoming due dates
  - Function: send_reminder_notification(task_id, user_id)
- [x] T012 [P] Create priority and tagging utility in phase-2/backend/app/services/task_utils.py
  - Function: filter_by_priority(tasks, priority)
  - Function: filter_by_tags(tasks, tags)
- [x] T013 Implement search functionality in phase-2/backend/app/services/search_service.py
  - Function: search_tasks(user_id, query, filters) - full-text search across title, description, tags
- [x] T014 Implement sorting functionality in phase-2/backend/app/services/sorting_service.py
  - Function: sort_tasks(tasks, sort_by) - supports due_date, priority, title, created_at

**Checkpoint**: Service layer complete - ready for API and MCP integration

---

## Phase 4: API & MCP Tool Extensions (Extend Phase II/III endpoints)

**Purpose**: Extend existing REST API and MCP tools to support advanced features

**⚠️ CRITICAL**: Extend existing phase-2/backend/app/api/routes/ and phase-2/backend/app/mcp/

- [x] T015 Extend existing task routes in phase-2/backend/app/api/routes/tasks.py:
  - Update POST /api/tasks to accept new fields (due_date, priority, tags, recurrence_pattern)
  - Update GET /api/tasks to support filtering by priority, tags, due_date
  - Update GET /api/tasks to support sorting by priority, due_date, title
  - Add search query parameter for full-text search
- [x] T016 [P] Extend existing MCP tools in phase-2/backend/app/mcp/tools/:
  - Update add_task tool to support advanced fields
  - Update list_tasks tool to support filtering and sorting
  - Add search_tasks tool for natural language search
- [x] T017 Update existing OpenAI Agent in phase-2/backend/app/agents/todo_agent.py:
  - Register new MCP tools with agent
  - Update system prompt to understand advanced features
  - Add intent handling for "set priority", "add tag", "make recurring", "set due date"

**Checkpoint**: API and MCP tools extended - chatbot can now handle advanced features

---

## Phase 5: User Story 1 - Enhanced AI Chatbot with Advanced Features (Priority: P1) 🎯 MVP

**Goal**: Verify existing Phase III chatbot now supports advanced features through extended APIs

**Independent Test**: The chatbot can accept commands like "Create a recurring task for weekly team meetings" and successfully process the request.

### Testing & Validation for User Story 1

- [x] T018 [US1] Test existing chat endpoint at phase-2/backend/app/api/routes/chat.py with advanced feature requests
- [x] T019 [US1] Verify OpenAI Agent correctly invokes extended MCP tools for advanced features
- [x] T020 [US1] Test existing frontend chat interface at phase-2/frontend/src/components/chat/ displays advanced task attributes
- [x] T021 [US1] Add integration tests for advanced features in phase-2/backend/tests/integration/
- [x] T022 [US1] Update frontend to display priority badges, tags, due dates in task list
- [x] T023 [US1] Add frontend filters/sort controls in phase-2/frontend/src/components/tasks/TaskFilters.tsx (if not exists, create)
- [x] T024 [US1] Manual testing: "Add high priority task with due date tomorrow"
- [x] T025 [US1] Manual testing: "Show me all high priority tasks tagged work"

**Checkpoint**: User Story 1 complete - Advanced features functional through chatbot

---

## Phase 6: User Story 2 - Event-Driven Architecture with Dapr and Kafka (Priority: P2)

**Goal**: Add event-driven processing for asynchronous tasks (reminders, recurring task spawning)

**Independent Test**: Task creation events are published to Kafka and processed asynchronously without blocking the user interface.

### Implementation for User Story 2

**Redpanda Cloud Details**: See `phase-5/REDPANDA-SETUP.md` for complete configuration

⚠️ **SECURITY**: Credentials MUST be in `.env` file, NOT in Git!

- [x] T026 [P] [US2] Create `.env` file from `.env.example`, then create Kubernetes secret for Redpanda credentials
  - Step 1: `cp .env.example .env` and fill in your Redpanda credentials
  - Step 2: Verify `.env` is in `.gitignore`
  - Step 3: Create Kubernetes secret from `.env` file (see REDPANDA-SETUP.md)
  - Step 4: Create Dapr components directory at phase-4/helm/dapr-components/
- [x] T027 [P] [US2] Create Dapr pubsub component YAML for Redpanda Cloud Kafka at phase-4/helm/dapr-components/pubsub-kafka.yaml
  - ⚠️ **SECURITY**: Use `secretKeyRef` for ALL credentials (bootstrap, username, password)
  - Load credentials from Kubernetes secret `kafka-credentials` (created in T026)
  - Reference: See phase-5/REDPANDA-SETUP.md for complete secure configuration
  - NEVER hardcode credentials in YAML files!
- [x] T028 [P] [US2] Create Dapr state component YAML for Neon PostgreSQL at phase-4/helm/dapr-components/state-postgres.yaml
- [x] T029 [P] [US2] Create Dapr bindings component YAML for cron triggers at phase-4/helm/dapr-components/bindings-cron.yaml
- [x] T030 [P] [US2] Create Dapr secrets component YAML for K8s secrets at phase-4/helm/dapr-components/secrets-kubernetes.yaml
- [x] T031 [US2] Create event publisher utility in phase-2/backend/app/events/publisher.py:
  - Function: publish_task_event(event_type, task_data) - publishes to "task-events" topic via Dapr
- [x] T032 [US2] Create event consumer service in phase-2/backend/app/events/consumer.py:
  - Subscribes to "task-events" topic
  - Routes events to appropriate handlers
- [x] T033 [US2] Create event handlers in phase-2/backend/app/events/handlers.py:
  - on_task_completed() - spawns next recurring task if applicable
  - on_task_due_soon() - sends reminder notification
- [x] T034 [US2] Integrate event publishing into existing task service at phase-2/backend/app/services/task_service.py:
  - Publish event after task creation, completion, deletion
- [x] T035 [US2] Add Dapr SDK import and initialization to phase-2/backend/app/main.py
- [x] T036 [US2] Test event flow: Create recurring task → Complete → Verify next occurrence spawned

**Checkpoint**: Event-driven architecture functional - reminders and recurring tasks work asynchronously

---

## Phase 7: User Story 3 - Cloud Deployment to DOKS (Priority: P3)

**Goal**: Deploy existing Phase IV Minikube setup to DigitalOcean Kubernetes with Dapr and Redpanda Cloud

**Independent Test**: The same application code and configuration work identically on both local Minikube and cloud DOKS deployments.

### Implementation for User Story 3

- [x] T037 [P] [US3] Extend existing Helm chart at phase-4/helm/todo-backend/templates/deployment.yaml to add Dapr sidecar annotations:
  - dapr.io/enabled: "true"
  - dapr.io/app-id: "todo-backend"
  - dapr.io/app-port: "8000"
- [x] T038 [P] [US3] Extend existing Helm chart at phase-4/helm/todo-frontend/templates/deployment.yaml to add Dapr sidecar annotations:
  - dapr.io/enabled: "true"
  - dapr.io/app-id: "todo-frontend"
  - dapr.io/app-port: "3000"
- [x] T039 [US3] Update phase-4/helm/todo-backend/values.yaml to add environment-specific configs:
  - values-minikube.yaml (local Kafka)
  - values-doks.yaml (Redpanda Cloud Kafka)
- [x] T040 [US3] Update phase-4/helm/todo-frontend/values.yaml for DOKS ingress configuration
- [x] T041 [US3] Create Helm chart for Dapr components at phase-4/helm/dapr-components/Chart.yaml
- [x] T042 [US3] Verify existing Dockerfiles at phase-2/backend/Dockerfile and phase-2/frontend/Dockerfile are production-ready
- [x] T043 [US3] Create GitHub Actions workflow at .github/workflows/deploy-minikube.yml for local testing
- [x] T044 [US3] Create GitHub Actions workflow at .github/workflows/deploy-doks.yml for cloud deployment:
  - Build and push Docker images to DigitalOcean Container Registry
  - Deploy Dapr components via Helm
  - Deploy backend and frontend via Helm
  - Run smoke tests
- [x] T045 [US3] Install Dapr on local Minikube: `dapr init -k`
- [x] T046 [US3] Deploy Phase V to Minikube: `helm upgrade --install todo-backend phase-4/helm/todo-backend -f values-minikube.yaml`
- [x] T047 [US3] Test Minikube deployment with Dapr sidecars and local Kafka
- [x] T048 [US3] Create DOKS cluster on DigitalOcean: `doctl kubernetes cluster create todo-cluster`
- [x] T049 [US3] Install Dapr on DOKS: `dapr init -k`
- [x] T050 [US3] Deploy Phase V to DOKS: `helm upgrade --install todo-backend phase-4/helm/todo-backend -f values-doks.yaml`
- [x] T051 [US3] Configure external ingress with SSL certificate for HTTPS access
- [x] T052 [US3] Configure monitoring: Install Prometheus and Grafana via Helm
- [x] T053 [US3] Configure centralized logging: Set up log aggregation (e.g., ELK or Loki)
- [x] T054 [US3] Test DOKS deployment end-to-end: Create task → Verify event in Kafka → Check recurring task spawned

**Checkpoint**: Cloud deployment successful - Phase V complete on both Minikube and DOKS

---

## Phase 8: Polish & Validation

**Purpose**: Final integration, testing, and documentation for Phase V

- [x] T055 [P] Update project README.md to document Phase V features and deployment
- [x] T056 [P] Create Phase V documentation in phase-5/docs/:
  - Architecture diagram with Dapr and Kafka
  - Deployment guide for Minikube and DOKS
  - Advanced features user guide
- [x] T057 Integration testing: Verify Phase II-IV features still work after Phase V additions
- [x] T058 Performance testing: Load test with 100 concurrent users
- [x] T059 [P] Add comprehensive integration tests in phase-2/backend/tests/integration/:
  - test_dapr_pubsub.py
  - test_recurring_tasks.py
  - test_reminders.py
  - test_advanced_search.py
- [x] T060 Security audit: Review Dapr secrets configuration, verify no hardcoded credentials
- [x] T061 Create demo video (<90 seconds) showing Phase V features
- [x] T062 Final validation checklist:
  - ✅ All advanced features work (recurring, due dates, priorities, tags, search/filter/sort)
  - ✅ Events flow through Kafka for asynchronous processing
  - ✅ Dapr sidecars operational on both Minikube and DOKS
  - ✅ CI/CD pipeline successfully deploys to DOKS
  - ✅ Monitoring and logging operational
  - ✅ No breaking changes to Phase I-IV functionality

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Review)**: No dependencies - start immediately to understand existing codebase
- **Phase 2 (Schema)**: Depends on Phase 1 - BLOCKS service layer work
- **Phase 3 (Services)**: Depends on Phase 2 - BLOCKS API work
- **Phase 4 (API/MCP)**: Depends on Phase 3 - BLOCKS US1 testing
- **Phase 5 (US1 - Chatbot)**: Depends on Phase 4 - Can test advanced features
- **Phase 6 (US2 - Events)**: Depends on Phase 5 - Adds async processing
- **Phase 7 (US3 - Cloud)**: Depends on Phase 6 - Deploys to DOKS
- **Phase 8 (Polish)**: Depends on Phase 7 - Final validation

### User Story Dependencies

- **User Story 1 (P1)**: Depends on Phases 1-4 (Schema + Services + API extensions)
- **User Story 2 (P2)**: Depends on US1 completion (needs working advanced features to generate events)
- **User Story 3 (P3)**: Depends on US2 completion (deploys event-driven system to cloud)

### Sequential Requirements

- **Must follow this order**: Review → Schema → Services → API → Testing → Events → Deployment
- **Cannot parallelize user stories in Phase V** because:
  - US2 (Events) needs US1 (Advanced features) to publish events
  - US3 (Cloud) needs US2 (Events) to have something to deploy
- **Within phases**, tasks marked [P] can run in parallel (e.g., multiple Dapr component YAMLs)

### Parallel Opportunities

- Phase 1: All review tasks marked [P] can run in parallel
- Phase 2: Schema migration can run parallel to documentation updates
- Phase 3: All service files marked [P] can be created in parallel
- Phase 6: All Dapr component YAML files marked [P] can be created in parallel
- Phase 7: Multiple Helm chart updates marked [P] can run in parallel

---

## Implementation Strategy

### Recommended Implementation Order

**Phase V is strictly sequential due to dependencies:**

1. **Phases 1-4**: Review existing code → Extend schema → Add services → Update API/MCP
2. **Phase 5 (US1)**: Test advanced features work through chatbot
3. **Phase 6 (US2)**: Add event-driven processing (depends on US1 features)
4. **Phase 7 (US3)**: Deploy to cloud (depends on US2 event system)
5. **Phase 8**: Polish and validate

**DO NOT skip phases or parallelize user stories** - each builds on the previous.

### Validation Checkpoints

- **After Phase 4**: Can manually test advanced features via REST API
- **After Phase 5**: Can test advanced features via chatbot
- **After Phase 6**: Can verify events flowing through Kafka
- **After Phase 7**: Can access deployed system on DOKS with HTTPS
- **After Phase 8**: Ready for hackathon submission

### Total Task Count

- **62 tasks total** (T001-T062)
- **Estimated timeline**: 2-3 weeks for full Phase V implementation
- **Critical path**: Review → Schema → Services → API → Events → Cloud
- **Quick win**: Complete Phase 5 for MVP (chatbot with advanced features) before adding events and cloud

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence