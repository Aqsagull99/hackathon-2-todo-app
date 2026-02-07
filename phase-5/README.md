# Phase V - Advanced Cloud Deployment 🚀

**Status:** Production-Ready | **Version:** 1.0.0 | **Last Updated:** 2026-02-07

Advanced cloud-native deployment of AI-powered Todo Chatbot with event-driven architecture, Dapr integration, and Kubernetes orchestration.

---

## 📋 Table of Contents

- [Overview](#overview)
- [What's New in Phase V](#whats-new-in-phase-v)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Deployment Options](#deployment-options)
- [Environment Configuration](#environment-configuration)
- [Security](#security)
- [Documentation](#documentation)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

Phase V extends the fully functional AI-powered Todo application (Phases I-IV) with:

- **Advanced Features**: Recurring tasks, due dates, reminders, priorities, tags, search/filter/sort
- **Event-Driven Architecture**: Dapr + Kafka (Redpanda Cloud) integration
- **Cloud Deployment**: DigitalOcean Kubernetes Service (DOKS)
- **Production-Ready**: Comprehensive monitoring, logging, and security

### Building on Previous Phases

```
Phase I  ✅ Console Todo App (Python, in-memory)
Phase II ✅ Full-Stack Web App (Next.js + FastAPI + Neon DB + Better Auth)
Phase III ✅ AI Chatbot (OpenAI ChatKit + Agents SDK + MCP Tools)
Phase IV ✅ Local K8s (Docker + Minikube + Helm)
Phase V  🚀 Cloud Deployment (Dapr + Kafka + DOKS)
```

---

## 🆕 What's New in Phase V

### 1. Advanced Task Features
- ✅ **Recurring Tasks** - Daily, weekly, monthly patterns with auto-generation
- ✅ **Due Dates & Reminders** - Time-based notifications and alerts
- ✅ **Priorities** - High, medium, low priority levels
- ✅ **Tags** - Flexible categorization and organization
- ✅ **Smart Search** - Full-text search with filtering and sorting

### 2. Event-Driven Architecture
- ✅ **Dapr Integration** - Service mesh for microservices
- ✅ **Kafka Pub/Sub** - Redpanda Cloud for event streaming
- ✅ **State Management** - Distributed state with PostgreSQL
- ✅ **Service Invocation** - Reliable inter-service communication

### 3. Cloud Infrastructure
- ✅ **DigitalOcean Kubernetes** - Production-grade container orchestration
- ✅ **Helm Charts** - Declarative application deployment
- ✅ **Load Balancers** - External access with high availability
- ✅ **Secrets Management** - Kubernetes-native secret handling

### 4. DevOps & Monitoring
- ✅ **CI/CD Pipeline** - GitHub Actions automation (coming soon)
- ✅ **Health Checks** - Liveness and readiness probes
- ✅ **Logging** - Centralized logging infrastructure
- ✅ **Security** - Environment-based credential management

---

## 🏗️ Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    DigitalOcean Kubernetes                   │
│                                                              │
│  ┌──────────────┐                    ┌──────────────┐       │
│  │   Frontend   │◄──────────────────►│   Backend    │       │
│  │   (Next.js)  │                    │   (FastAPI)  │       │
│  │              │                    │              │       │
│  │  Port: 3000  │                    │  Port: 8000  │       │
│  └──────┬───────┘                    └──────┬───────┘       │
│         │                                   │               │
│         │  ┌────────────────────────────────┤               │
│         │  │            Dapr Sidecar        │               │
│         │  │  ┌─────────────────────────┐   │               │
│         └──┼─►│   Service Invocation    │◄──┘               │
│            │  ├─────────────────────────┤                   │
│            │  │   Kafka Pub/Sub         │◄──┐               │
│            │  ├─────────────────────────┤   │               │
│            │  │   State Management      │   │               │
│            │  ├─────────────────────────┤   │               │
│            │  │   Secrets Management    │   │               │
│            │  └─────────────────────────┘   │               │
│            │                                 │               │
│            └─────────────────────────────────┘               │
│                                                              │
└──────────────────┬───────────────────────────┬───────────────┘
                   │                           │
                   ▼                           ▼
         ┌─────────────────┐        ┌─────────────────┐
         │  Redpanda Cloud │        │   Neon DB       │
         │    (Kafka)      │        │  (PostgreSQL)   │
         └─────────────────┘        └─────────────────┘
```

### Component Breakdown

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Frontend** | Next.js 16 + React 19 | User interface with chat widget |
| **Backend** | FastAPI + Python 3.12 | REST API + AI Agent orchestration |
| **Database** | Neon PostgreSQL | Serverless database with auto-scaling |
| **Authentication** | Better Auth + JWT | Session management and auth |
| **AI Agent** | OpenAI Agents SDK | Natural language task processing |
| **MCP Tools** | Model Context Protocol | Task operations interface |
| **Chat UI** | OpenAI ChatKit | Conversational interface |
| **Service Mesh** | Dapr 1.14+ | Microservices runtime |
| **Event Streaming** | Redpanda Cloud | Kafka-compatible pub/sub |
| **Orchestration** | Kubernetes (DOKS) | Container orchestration |
| **Package Manager** | Helm 3 | Application deployment |

---

## 🛠️ Technology Stack

### Frontend
- **Framework:** Next.js 16 (App Router)
- **UI Library:** React 19
- **Styling:** Tailwind CSS 4
- **Chat:** OpenAI ChatKit
- **State:** React Context API
- **Auth:** Better Auth Client

### Backend
- **Framework:** FastAPI 0.115+
- **Language:** Python 3.12
- **ORM:** SQLModel + SQLAlchemy 2.0
- **Database:** Neon PostgreSQL (Serverless)
- **AI:** OpenAI Agents SDK
- **Tools:** MCP Server with task tools
- **Auth:** Better Auth JWT Plugin

### Infrastructure
- **Container:** Docker 24+
- **Orchestration:** Kubernetes 1.28+
- **Service Mesh:** Dapr 1.14+
- **Event Bus:** Redpanda Cloud (Kafka)
- **Package Manager:** Helm 3.13+
- **Cloud Provider:** DigitalOcean (DOKS)

### DevOps
- **Version Control:** Git + GitHub
- **CI/CD:** GitHub Actions (planned)
- **CLI Tools:** kubectl, helm, doctl, dapr
- **Secrets:** Kubernetes Secrets + Environment Variables

---

## ✅ Prerequisites

### Required Accounts
- [x] **GitHub** - Version control and CI/CD
- [x] **DigitalOcean** - Kubernetes cluster hosting
- [x] **Neon** - Serverless PostgreSQL database
- [x] **Redpanda Cloud** - Kafka event streaming
- [x] **OpenRouter/OpenAI** - AI model access

### Required Tools
```bash
# Verify installations
docker --version          # Docker 24+
kubectl version --client  # Kubernetes 1.28+
helm version             # Helm 3.13+
doctl version            # DigitalOcean CLI
dapr --version           # Dapr 1.14+
```

### System Requirements
- **OS:** Linux, macOS, or WSL2
- **RAM:** 8GB minimum (16GB recommended)
- **Disk:** 20GB free space
- **Network:** Stable internet connection

---

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/Aqsagull99/hackathon-2-todo-app.git
cd hackathon-2-todo-app/phase-5
```

### 2. Configure Environment
```bash
# Copy environment template
cp .env.example .env

# Edit with your credentials
nano .env
```

**Required Variables:**
```env
DATABASE_URL=postgresql+asyncpg://user:pass@host/db?ssl=require
REDPANDA_BOOTSTRAP_SERVERS=your-cluster.cloud.redpanda.com:9092
REDPANDA_USERNAME=your-username
REDPANDA_PASSWORD=your-password
JWT_SECRET=your-jwt-secret
OPENROUTER_API_KEY=sk-or-v1-your-api-key
```

### 3. Deploy to DigitalOcean
```bash
# Load environment variables
export $(cat .env | xargs)

# Deploy everything
chmod +x deploy-to-digitalocean.sh
./deploy-to-digitalocean.sh
```

### 4. Verify Deployment
```bash
# Check pod status
kubectl get pods

# Get external IPs
kubectl get services

# Check Dapr sidecars
kubectl get pods -l app=todo-backend -o jsonpath='{.items[0].spec.containers[*].name}'
```

### 5. Access Application
```bash
# Get frontend URL
kubectl get service todo-frontend -o jsonpath='{.status.loadBalancer.ingress[0].ip}'

# Open in browser
# http://<EXTERNAL_IP>
```

---

## 📦 Deployment Options

### Option 1: Automated Script (Recommended)
```bash
# Single command deployment
./deploy-to-digitalocean.sh
```

**What it does:**
- ✅ Validates environment variables
- ✅ Creates Kubernetes secrets
- ✅ Deploys Dapr components
- ✅ Deploys frontend and backend
- ✅ Configures services and load balancers
- ✅ Verifies deployment health

---

### Option 2: Manual Deployment
```bash
# 1. Create secrets
kubectl create secret generic neon-db-secret \
  --from-literal=database-url="$DATABASE_URL"

kubectl create secret generic redpanda-credentials \
  --from-literal=bootstrap-servers="$REDPANDA_BOOTSTRAP_SERVERS" \
  --from-literal=username="$REDPANDA_USERNAME" \
  --from-literal=password="$REDPANDA_PASSWORD"

kubectl create secret generic todo-backend-secrets \
  --from-literal=JWT_SECRET="$JWT_SECRET"

# 2. Apply Kubernetes manifests
kubectl apply -f digitalocean-deployment.yaml

# 3. Wait for deployment
kubectl wait --for=condition=ready pod -l app=todo-backend --timeout=300s
kubectl wait --for=condition=ready pod -l app=todo-frontend --timeout=300s
```

---

### Option 3: Helm Charts (Advanced)
```bash
# Install backend
helm install todo-backend ../phase-4/helm/todo-backend \
  -f cloud-values-overrides.yaml

# Install frontend
helm install todo-frontend ../phase-4/helm/todo-frontend \
  -f cloud-values-overrides.yaml
```

---

## 🔧 Environment Configuration

See `.env.example` for complete list of required environment variables.

### Key Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | Neon PostgreSQL connection | `postgresql+asyncpg://user:pass@host/db` |
| `REDPANDA_BOOTSTRAP_SERVERS` | Kafka bootstrap servers | `xxx.cloud.redpanda.com:9092` |
| `REDPANDA_USERNAME` | Kafka username | `your-username` |
| `REDPANDA_PASSWORD` | Kafka password | `your-password` |
| `JWT_SECRET` | Authentication secret | `your-secret-key` |
| `OPENROUTER_API_KEY` | AI model access | `sk-or-v1-xxx` |

---

## 🔐 Security

### ✅ Security Improvements (2026-02-07)

All deployment files have been cleaned of hardcoded secrets:

- ✅ Removed database passwords
- ✅ Removed Redpanda credentials
- ✅ Removed JWT secrets
- ✅ Removed API keys
- ✅ Replaced with environment variables
- ✅ Updated .gitignore

See `SECURITY-CLEANUP-REPORT.md` for complete audit details.

### Best Practices
1. **Never commit `.env` files** - Use `.env.example` templates
2. **Rotate secrets quarterly** - Change passwords every 90 days
3. **Use Kubernetes Secrets** - For production deployments
4. **Enable RBAC** - Limit access to sensitive resources
5. **Audit logs** - Monitor secret access patterns

---

## 📚 Documentation

### Phase V Documentation
```
phase-5/
├── README.md                           # This file
├── CLAUDE.md                           # Claude Code rules
├── SECURITY-CLEANUP-REPORT.md          # Security audit
├── SECURITY-ACTIONS-REQUIRED.md        # Pre-commit checklist
├── START-HERE.md                       # Phase V overview
├── QUICK-START-GUIDE.md                # Step-by-step tutorial
├── IMPLEMENTATION-CHECKLIST.md         # 62 tasks
├── REDPANDA-SETUP.md                   # Kafka configuration
├── SECURITY-GUIDE.md                   # Security best practices
└── .env.example                        # Environment template
```

### Key Documents

| File | Purpose |
|------|---------|
| **START-HERE.md** | Start here for Phase V |
| **QUICK-START-GUIDE.md** | Step-by-step implementation |
| **IMPLEMENTATION-CHECKLIST.md** | Task tracking (62 tasks) |
| **SECURITY-CLEANUP-REPORT.md** | Security audit report |
| **.env.example** | Configuration template |

---

## 🐛 Troubleshooting

### Common Issues

#### Pods Not Starting
```bash
kubectl get pods
kubectl logs -l app=todo-backend
kubectl describe pod <pod-name>
```

#### Database Connection Failed
```bash
kubectl get secret neon-db-secret -o yaml
kubectl get secret neon-db-secret -o jsonpath='{.data.database-url}' | base64 -d
```

#### External IP Pending
```bash
kubectl get service todo-frontend
# Wait 5-10 minutes for DigitalOcean provisioning
```

#### Dapr Sidecar Issues
```bash
kubectl get pods -n dapr-system
kubectl logs <pod-name> -c daprd
kubectl get components
```

### Debug Commands
```bash
kubectl get all
kubectl get events --sort-by='.lastTimestamp'
kubectl port-forward svc/todo-backend 8000:80
kubectl exec -it <pod-name> -- bash
```

---

## 📞 Support

- **Documentation:** See `START-HERE.md`
- **Security:** See `SECURITY-GUIDE.md`
- **Specs:** Check `specs/007-phase-v-cloud-deployment/`
- **Issues:** GitHub Issues

---

## 🎯 Next Steps

1. ✅ Read `START-HERE.md` for Phase V overview
2. ✅ Configure `.env` with your credentials
3. ✅ Run `./deploy-to-digitalocean.sh`
4. ✅ Verify deployment: `kubectl get pods`
5. ✅ Access application via external IP
6. ✅ Test AI chatbot features

---

**Built with ❤️ using Spec-Driven Development and AI-Native Tooling**

Phase V - Advanced Cloud Deployment | Hackathon 2 Todo App
