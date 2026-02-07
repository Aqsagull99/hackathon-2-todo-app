# Implementation Plan: Phase V - Advanced Cloud Deployment of AI-Native Todo Chatbot

## Technical Context

### Architecture Overview
Phase V extends the existing Phase I-IV system with event-driven architecture using Dapr and Kafka (Redpanda Cloud), deployed on DigitalOcean Kubernetes (DOKS) with continued local development support on Minikube.

**Existing Components (Phase I-IV) ✅**:
- Frontend: Next.js 16+ with ChatKit UI (phase-2/frontend/)
- Backend: FastAPI + SQLModel + Better Auth JWT (phase-2/backend/)
- AI Agent: OpenAI Agents SDK (phase-2/backend/app/agents/)
- MCP Server: Official MCP SDK with task tools (phase-2/backend/app/mcp/)
- Database: Neon PostgreSQL serverless
- Kubernetes: Local deployment on Minikube (Phase IV)
- Helm Charts: todo-backend and todo-frontend (phase-4/helm/)

**New Components (Phase V)**:
- Dapr Sidecars: Handles pub/sub, state, bindings, secrets (injected into existing pods)
- Kafka: Event streaming via Redpanda Cloud
- Event Services: Recurring tasks, reminders, notifications (new microservices)
- DOKS: DigitalOcean managed Kubernetes (cloud deployment)
- CI/CD: GitHub Actions pipeline
- Monitoring: Prometheus/Grafana + Dapr observability

**Technologies**:
- Cloud: DigitalOcean Kubernetes Service (DOKS) - new in Phase V
- Orchestration: Kubernetes with extended Helm charts from Phase IV
- Service Mesh: Dapr (Distributed Application Runtime) - new in Phase V
- Event Streaming: Apache Kafka via Redpanda Cloud - new in Phase V
- Container Runtime: Docker (existing from Phase IV)
- CI/CD: GitHub Actions - enhanced in Phase V
- Monitoring: Kubernetes native + Dapr observability - enhanced in Phase V

### Existing Assets to Leverage
- Phase II Backend: `phase-2/backend/app/` with models, routes, services
- Phase II Frontend: `phase-2/frontend/src/` with chat components
- Phase III AI Agent: `phase-2/backend/app/agents/todo_agent.py`
- Phase III MCP Tools: `phase-2/backend/app/mcp/` (add_task, list_tasks, etc.)
- Phase IV Helm Charts: `phase-4/helm/todo-backend/` and `phase-4/helm/todo-frontend/`
- Phase IV Dockerfiles: Should exist in phase-2/backend/ and phase-2/frontend/

### Unknowns/Dependencies
- [NEEDS CLARIFICATION]: Specific resource requirements for DOKS cluster (likely 2-4 nodes, 2GB RAM each)
- [NEEDS CLARIFICATION]: Exact Dapr component configurations for production (will start with defaults)
- [NEEDS CLARIFICATION]: Kafka topic partitioning and replication settings (suggest 3 partitions, replication factor 2)
- [TO VERIFY]: Current Phase IV Helm chart structure and values

## Constitution Check

### Compliance Verification
- [x] Accuracy through primary source verification - Plan incorporates official documentation from Dapr, Kafka, Kubernetes
- [x] Clarity for academic audience - Plan written with clear explanations and industry-standard terminology
- [x] Reproducibility through scripted deployments - All deployment steps documented in scripts/configuration files
- [x] Rigor in peer-reviewed standards - Architecture follows proven cloud-native patterns
- [x] Event-driven architecture with Dapr and Kafka - Plan explicitly implements pub/sub patterns
- [x] Cloud-agnostic code with infrastructure abstraction - Application code separated from infrastructure configuration

### Potential Violations
None identified - all implementation approaches comply with constitution principles.

## Phase 0: Outline & Research

### Research Tasks

#### 0.1 Event Bus Technology Research
**Decision**: Kafka (Redpanda Cloud) vs. alternatives (RabbitMQ, NATS)
**Rationale**: Kafka provides superior scalability, durability, and cloud integration for event-driven architecture
**Alternatives Considered**:
- RabbitMQ: Good for simple queuing but lacks event streaming capabilities
- NATS: Lightweight but limited persistence and replay features
- Apache Pulsar: Similar to Kafka but less mature ecosystem

#### 0.2 Deployment Platform Research
**Decision**: Minikube (local dev) vs. DOKS (cloud prod)
**Rationale**: Minikube provides local development parity while DOKS offers production-grade scalability
**Tradeoffs**:
- Local: Reproducibility, resource constraints, limited scale
- Cloud: Scalability, cost, network dependencies

#### 0.3 CI/CD Pipeline Research
**Decision**: GitHub Actions vs. other pipelines
**Rationale**: Tight integration with GitHub repositories, extensive marketplace, proven reliability
**Alternatives Considered**:
- Jenkins: More complex setup, maintenance overhead
- GitLab CI: Would require repository migration
- CircleCI: Good but additional billing consideration

#### 0.4 Monitoring Strategy Research
**Decision**: Kubernetes native logging vs. external observability tools
**Rationale**: Combination approach - native tools for basics, external for advanced monitoring
**Considerations**:
- Prometheus/Grafana: Kubernetes-native, extensive community support
- ELK Stack: More complex but feature-rich
- Cloud-native tools: May tie to specific vendor

## Phase 1: Design & Contracts

### 1.1 Data Model Design

#### Task Entity
```
Task {
  id: UUID (primary key)
  userId: string (foreign key to user)
  title: string (required, 1-200 chars)
  description: string (optional, max 1000 chars)
  status: enum ['pending', 'completed', 'archived']
  priority: enum ['low', 'medium', 'high']
  tags: string[] (optional, max 10 tags)
  dueDate: DateTime (optional)
  recurrencePattern: string (optional, cron-like)
  createdAt: DateTime
  updatedAt: DateTime
  completedAt: DateTime (optional)
}
```

#### Event Entity
```
Event {
  id: UUID (primary key)
  eventType: enum ['created', 'updated', 'completed', 'deleted', 'reminder-triggered']
  taskId: UUID (foreign key to task)
  userId: string (user context)
  eventData: JSON (payload for processing)
  timestamp: DateTime
  processed: boolean
}
```

#### Conversation Entity
```
Conversation {
  id: UUID (primary key)
  userId: string (foreign key to user)
  title: string (auto-generated or user-provided)
  createdAt: DateTime
  updatedAt: DateTime
}
```

#### Message Entity
```
Message {
  id: UUID (primary key)
  conversationId: UUID (foreign key to conversation)
  userId: string (foreign key to user)
  role: enum ['user', 'assistant']
  content: string (message text)
  timestamp: DateTime
  metadata: JSON (processing info)
}
```

### 1.2 API Contract Design

#### Task Management Endpoints
```
POST /api/v1/tasks
- Create new task
- Requires: { title, description?, status?, priority?, tags?, dueDate? }
- Returns: Task object

GET /api/v1/tasks
- List tasks with filtering
- Query params: status, priority, tags, dueDate, search
- Returns: Array of Task objects

GET /api/v1/tasks/{id}
- Get specific task
- Returns: Task object

PUT /api/v1/tasks/{id}
- Update task
- Requires: Partial Task object
- Returns: Updated Task object

DELETE /api/v1/tasks/{id}
- Delete task
- Returns: Success confirmation

PATCH /api/v1/tasks/{id}/complete
- Toggle completion status
- Returns: Updated Task object
```

#### Chat Endpoints
```
POST /api/v1/chat
- Send message and get AI response
- Requires: { message, conversationId? }
- Returns: { response, conversationId, toolCalls? }

GET /api/v1/chat/conversations
- List user conversations
- Returns: Array of Conversation objects

GET /api/v1/chat/conversations/{id}/messages
- Get conversation history
- Returns: Array of Message objects
```

### 1.3 Infrastructure Contracts

#### Dapr Components
- **pubsub.kafka**: For event streaming between services
- **state.postgresql**: For conversation state management
- **bindings.kafka**: For cron-based recurring task triggers
- **secretstores.kubernetes**: For secure credential management

#### Kubernetes Resources
- **Deployments**: For frontend, backend, and MCP services
- **Services**: For internal and external networking
- **ConfigMaps**: For configuration management
- **Secrets**: For sensitive data
- **Ingress**: For external access

## Phase 2: Implementation Preparation

### 2.1 Development Environment Setup
- Install Docker and Docker Compose
- Install kubectl and configure for Minikube
- Install Helm and verify charts
- Install Dapr CLI and initialize locally
- Set up GitHub repository with Actions workflows

### 2.2 Infrastructure Prerequisites
- DigitalOcean account with API token
- Redpanda Cloud account with cluster access
- Domain name for production deployment
- SSL certificate for HTTPS

### 2.3 Deployment Strategy
- **Local**: Minikube with Dapr installed
- **Staging**: DOKS cluster with limited resources
- **Production**: DOKS cluster with auto-scaling
- **Migration**: Blue-green deployment strategy

## Phase 3: Development Approach

### 3.1 Iterative Development
1. Core functionality (basic task operations)
2. Advanced features (recurring tasks, due dates, reminders)
3. Event-driven architecture (Kafka integration)
4. Dapr integration (pub/sub, state management)
5. Cloud deployment (DOKS configuration)
6. Monitoring and observability

### 3.2 Quality Assurance
- Unit tests for all components
- Integration tests for service interactions
- End-to-end tests for user flows
- Performance testing under load
- Security scanning for vulnerabilities

### 3.3 Success Metrics
- Feature completeness: All advanced features functional
- Performance: Response time < 1s for API calls
- Reliability: 99.9% uptime in production
- Scalability: Support 1000+ concurrent users
- Observability: 100% of events logged and traceable