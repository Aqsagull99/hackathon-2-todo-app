# Claude Code Rules - Phase V Deployment Orchestrator

This file provides Claude Code orchestration rules for Phase V (Advanced Cloud Deployment) work.

---

## Project Phase

**Current Phase**: Phase V - Advanced Cloud Deployment
**Status**: Production-Ready
**Last Updated**: 2026-02-07

---

## Phase V Overview

Phase V extends the fully functional AI-powered Todo application (Phases I-IV) with:

1. **Advanced Features**: Recurring tasks, due dates, reminders, priorities, tags, search/filter/sort
2. **Event-Driven Architecture**: Dapr + Kafka (Redpanda Cloud) integration
3. **Cloud Deployment**: DigitalOcean Kubernetes Service (DOKS)
4. **DevOps**: Automated deployment scripts, Helm charts, secrets management

---

## Project Context

### Building on Previous Phases

```
Phase I  ✅ Console Todo App (Phase-one/)
Phase II ✅ Full-Stack Web App (phase-2/backend/, phase-2/frontend/)
Phase III ✅ AI Chatbot (phase-2/backend/app/agents/, phase-2/frontend/src/components/chat/)
Phase IV ✅ Local K8s (phase-4/helm/)
Phase V  🚀 Cloud Deployment (phase-5/)
```

### Codebase Structure

```
hackathon-2-todo-app/
├── phase-2/
│   ├── backend/                # FastAPI + SQLModel + Better Auth
│   │   ├── app/
│   │   │   ├── api/routes/     # REST API endpoints
│   │   │   ├── agents/         # OpenAI Agents SDK
│   │   │   ├── mcp/            # MCP Tools
│   │   │   ├── models/         # SQLModel schemas
│   │   │   ├── services/       # Business logic
│   │   │   └── events/         # Dapr event handlers (Phase V)
│   │   └── pyproject.toml
│   └── frontend/               # Next.js 16 + React 19
│       └── src/
│           ├── app/            # App Router
│           ├── components/     # UI components
│           └── lib/            # Utilities
├── phase-4/
│   └── helm/                   # Kubernetes Helm charts
│       ├── todo-backend/
│       └── todo-frontend/
├── phase-5/                    # Current work directory
│   ├── README.md               # Phase V documentation
│   ├── CLAUDE.md               # This file
│   ├── .env.example            # Environment template
│   ├── deploy-to-digitalocean.sh    # Deployment script
│   ├── digitalocean-deployment.yaml # K8s manifests
│   ├── cloud-values-overrides.yaml  # Helm values
│   └── specs/
│       └── 007-phase-v-cloud-deployment/
│           ├── spec.md         # Feature specification
│           ├── plan.md         # Implementation plan
│           └── tasks.md        # Task breakdown (T001-T062)
└── .gitignore                  # Protected files
```

---

## Technology Stack

### Backend (phase-2/backend/)
- **Framework**: FastAPI 0.115+
- **Language**: Python 3.12
- **ORM**: SQLModel + SQLAlchemy 2.0
- **Database**: Neon PostgreSQL (Serverless)
- **Authentication**: Better Auth JWT Plugin
- **AI**: OpenAI Agents SDK
- **Tools**: MCP Server with task tools
- **Events**: Dapr pub/sub with Kafka

### Frontend (phase-2/frontend/)
- **Framework**: Next.js 16 (App Router)
- **UI**: React 19 + Tailwind CSS 4
- **Chat**: OpenAI ChatKit
- **Auth**: Better Auth Client

### Infrastructure (phase-4/, phase-5/)
- **Container**: Docker 24+
- **Orchestration**: Kubernetes 1.28+ (DigitalOcean DOKS)
- **Service Mesh**: Dapr 1.14+
- **Event Bus**: Redpanda Cloud (Kafka-compatible)
- **Package Manager**: Helm 3.13+

---

## Available Agents

When working on Phase V tasks, you have access to these specialized agents:

### DevOps & Deployment Agents
- **`k8s-deployment-coordinator`** - Kubernetes deployment coordination (Docker, Helm, K8s)
  - Use for: Containerization, Helm charts, K8s manifests

- **`docker-deployment`** - Docker containerization for Python/FastAPI apps
  - Use for: Dockerfile creation, multi-stage builds

- **`helm-charts`** - Helm chart creation and management
  - Use for: Chart scaffolding, values files, templates

- **`kubernetes-deployment`** - Kubernetes deployment and scaling
  - Use for: Deployments, services, health checks

- **`dapr-deployment`** - Distributed Application Runtime for microservices
  - Use for: Dapr components, pub/sub, state management

- **`kafka-events`** - Apache Kafka for event-driven architectures
  - Use for: Kafka configuration, Redpanda Cloud setup

- **`gitops-deployment`** - GitOps with ArgoCD
  - Use for: CI/CD pipelines (planned)

### Development Agents (Phase II/III - Reusable)
- **`todo-main-agent-phase2`** - Phase II coordinator
- **`fastapi-chat-agent`** - Backend chat API endpoints
- **`chatkit-ui-agent`** - Frontend chat UI implementation

---

## Available Skills

### DevOps Skills
- **`docker-deployment`** - Docker containerization patterns
- **`production-dockerfile`** - Production-ready Dockerfiles
- **`helm-charts`** - Helm chart patterns
- **`kubernetes-deployment`** - K8s deployment patterns
- **`dapr-deployment`** - Dapr integration patterns
- **`kafka-events`** - Kafka/Redpanda patterns
- **`gitops-deployment`** - GitOps/ArgoCD patterns

### Backend Skills (Reusable)
- **`fastapi-skill`** - FastAPI REST patterns
- **`sqlmodel-skill`** - SQLModel ORM patterns
- **`neon-db-skill`** - Neon PostgreSQL patterns
- **`better-auth-skill`** - Better Auth patterns
- **`openai-agents-sdk-skill`** - OpenAI Agents SDK patterns
- **`task-crud-skill`** - Task CRUD operations
- **`task-mcp-skill`** - MCP tools patterns

### Frontend Skills (Reusable)
- **`nextjs-skill`** - Next.js 16 patterns
- **`tailwind-skill`** - Tailwind CSS patterns
- **`chatkit-ui-skill`** - OpenAI ChatKit patterns

### Documentation Skills
- **`browsing-with-context7`** - Fetch documentation via Context7 MCP
- **`browsing-with-playwright`** - Browser automation

---

## Working on Phase V

### Primary Work Directory
```bash
cd phase-5/
```

### Implementation Workflow

1. **Read Specifications**
   - Start with `START-HERE.md` for overview
   - Review `specs/007-phase-v-cloud-deployment/spec.md`
   - Check `specs/007-phase-v-cloud-deployment/tasks.md` for detailed tasks

2. **Environment Setup**
   - Copy `.env.example` to `.env`
   - Never commit `.env` (git-ignored)
   - Use environment variables for all secrets

3. **Deployment Files**
   - `deploy-to-digitalocean.sh` - Main deployment script
   - `digitalocean-deployment.yaml` - K8s manifests
   - `cloud-values-overrides.yaml` - Helm values
   - All files use environment variables or placeholders (no hardcoded secrets)

4. **Testing**
   - Local: Minikube with Helm charts from phase-4/
   - Cloud: DigitalOcean Kubernetes with phase-5/ scripts

---

## Security Requirements 🔒

### CRITICAL: Secret Management

**✅ DO:**
- Store secrets in `.env` file (git-ignored)
- Use environment variables in scripts
- Use Kubernetes Secret references in manifests
- Use placeholders in template files (`.env.example`)

**❌ NEVER:**
- Hardcode passwords, API keys, or tokens in code
- Commit `.env` files to git
- Put base64-encoded secrets in tracked files
- Share credentials in plain text

### Protected Files (Must Not Commit)
```
phase-5/.env                          # Real credentials
todo-cluster-kubeconfig.yaml          # Cluster access
phase-4/k8s-manifests/secrets.yaml    # K8s secrets with real values
*-credentials.json                    # Service accounts
*.pem, *.pfx, *.p12                  # SSL certificates
```

### Safe Template Files (Can Commit)
```
phase-5/.env.example                  # Template only
phase-4/k8s-manifests/secrets.yaml.example  # Template only
phase-5/deploy-to-digitalocean.sh     # Uses $VARIABLES
phase-5/digitalocean-deployment.yaml  # Uses <PLACEHOLDERS>
phase-5/cloud-values-overrides.yaml   # Uses secret references
```

### Verification Before Commit
```bash
# Check for leaked secrets
git diff --cached | grep -iE "(password|secret|key|token)" | grep -v "PLACEHOLDER"

# Verify .env is ignored
git check-ignore phase-5/.env

# Verify no base64 secrets
git diff --cached | grep -E "^[A-Za-z0-9+/]{20,}={0,2}$"
```

---

## Common Tasks

### 1. Deploy to DigitalOcean
```bash
cd phase-5/
export $(cat .env | xargs)
./deploy-to-digitalocean.sh
```

### 2. Create Secrets Manually
```bash
kubectl create secret generic neon-db-secret \
  --from-literal=database-url="$DATABASE_URL"

kubectl create secret generic redpanda-credentials \
  --from-literal=bootstrap-servers="$REDPANDA_BOOTSTRAP_SERVERS" \
  --from-literal=username="$REDPANDA_USERNAME" \
  --from-literal=password="$REDPANDA_PASSWORD"
```

### 3. Deploy with Helm
```bash
helm install todo-backend ../phase-4/helm/todo-backend \
  -f cloud-values-overrides.yaml
```

### 4. Check Deployment Status
```bash
kubectl get pods
kubectl get services
kubectl logs -l app=todo-backend
```

### 5. Debug Issues
```bash
kubectl describe pod <pod-name>
kubectl logs <pod-name> -c todo-backend
kubectl logs <pod-name> -c daprd
kubectl get events --sort-by='.lastTimestamp'
```

---

## File Modification Rules

### Backend Code (phase-2/backend/)
- **Modify**: `app/events/` for Dapr event handlers
- **Modify**: `app/services/` for business logic
- **Modify**: `app/api/routes/` for new endpoints
- **DO NOT**: Change core auth, database, or agent code unless necessary

### Frontend Code (phase-2/frontend/)
- **Modify**: `src/components/` for UI updates
- **DO NOT**: Break existing chat or dashboard functionality

### Deployment Files (phase-5/)
- **Modify**: Deployment scripts and manifests
- **ALWAYS**: Use environment variables for secrets
- **NEVER**: Hardcode credentials

### Helm Charts (phase-4/helm/)
- **Modify**: Values files for different environments
- **ADD**: Dapr annotations to deployment templates
- **DO NOT**: Break existing chart structure

---

## Documentation Requirements

When creating or updating Phase V files:

1. **Code Comments**
   - Explain Dapr-specific configurations
   - Document environment variable usage
   - Note Kubernetes-specific patterns

2. **README Updates**
   - Keep `phase-5/README.md` current
   - Update deployment instructions
   - Document troubleshooting steps

3. **Spec Updates**
   - Track completed tasks in `tasks.md`
   - Update status in `spec.md`
   - Document lessons learned in `plan.md`

---

## Integration Points

### Phase II Backend Integration
```python
# Location: phase-2/backend/app/events/
from app.services.task_service import TaskService
from app.services.search_service import SearchService
from app.core.database import get_db
```

### Phase III AI Agent Integration
```python
# Location: phase-2/backend/app/agents/
from app.mcp.task_tools import add_task, list_tasks, complete_task
```

### Phase IV Helm Integration
```yaml
# Location: phase-4/helm/todo-backend/templates/deployment.yaml
annotations:
  dapr.io/enabled: "true"
  dapr.io/app-id: "backend-todo"
  dapr.io/app-port: "8000"
```

---

## External Services Configuration

### Neon Database
- **Type**: Serverless PostgreSQL
- **Config**: `DATABASE_URL` in `.env`
- **Format**: `postgresql+asyncpg://user:pass@host/db?ssl=require`

### Redpanda Cloud
- **Type**: Kafka-compatible event streaming
- **Config**: `REDPANDA_BOOTSTRAP_SERVERS`, `REDPANDA_USERNAME`, `REDPANDA_PASSWORD`
- **Usage**: Dapr pub/sub component

### DigitalOcean
- **Type**: Kubernetes cluster (DOKS)
- **CLI**: `doctl` for cluster management
- **Auth**: `doctl auth init` with API token

### OpenRouter/OpenAI
- **Type**: AI model access
- **Config**: `OPENROUTER_API_KEY` or `OPENAI_API_KEY`
- **Usage**: OpenAI Agents SDK

---

## Debugging & Troubleshooting

### Common Issues

1. **Pods Not Starting**
   - Check: `kubectl get pods`
   - Logs: `kubectl logs <pod-name>`
   - Events: `kubectl describe pod <pod-name>`

2. **Database Connection Failed**
   - Verify: `kubectl get secret neon-db-secret -o yaml`
   - Decode: `kubectl get secret neon-db-secret -o jsonpath='{.data.database-url}' | base64 -d`

3. **Dapr Sidecar Issues**
   - Check: `kubectl get pods -n dapr-system`
   - Logs: `kubectl logs <pod-name> -c daprd`
   - Components: `kubectl get components`

4. **External IP Pending**
   - Wait: 5-10 minutes for DigitalOcean provisioning
   - Check: `kubectl describe service todo-frontend`

---

## Reference Documents

### Phase V Documentation
- **START-HERE.md** - Phase V introduction
- **QUICK-START-GUIDE.md** - Step-by-step tutorial
- **IMPLEMENTATION-CHECKLIST.md** - Task tracking (62 tasks)
- **SECURITY-CLEANUP-REPORT.md** - Security audit
- **SECURITY-GUIDE.md** - Security best practices
- **REDPANDA-SETUP.md** - Kafka configuration

### Specifications
- **spec.md** - Feature specification
- **plan.md** - Implementation plan
- **tasks.md** - Task breakdown (T001-T062)

### External Documentation
- [Dapr Docs](https://docs.dapr.io/)
- [Redpanda Cloud](https://docs.redpanda.com/cloud/)
- [DigitalOcean K8s](https://docs.digitalocean.com/products/kubernetes/)
- [OpenAI Agents SDK](https://github.com/openai/openai-agents-sdk)

---

## Success Criteria

Phase V is complete when:

- ✅ All advanced features implemented (recurring tasks, due dates, reminders, priorities, tags, search)
- ✅ Dapr integration working (pub/sub, state management, service invocation)
- ✅ Cloud deployment successful on DigitalOcean DOKS
- ✅ All deployment files cleaned of hardcoded secrets
- ✅ Health checks passing for all services
- ✅ Documentation complete and accurate
- ✅ No breaking changes to Phase I-IV functionality

---

## Contact & Support

- **Documentation**: Start with `START-HERE.md`
- **Issues**: Check `specs/007-phase-v-cloud-deployment/`
- **Security**: See `SECURITY-CLEANUP-REPORT.md`
- **Specs**: Review `spec.md`, `plan.md`, `tasks.md`

---

**Phase V - Advanced Cloud Deployment**
**Status**: Production-Ready | **Hackathon 2 Todo App**
