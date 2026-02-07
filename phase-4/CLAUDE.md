# Claude Code Rules - Phase IV: Kubernetes Deployment

## Project Overview

**Project**: Todo App Kubernetes Deployment (Phase IV)
**Orchestration**: Kubernetes with Minikube
**Packaging**: Helm Charts
**Containerization**: Docker with AI assistance
**Applications**: Frontend (Next.js) + Backend (FastAPI)

## Objective

Deploy the existing Phase III Todo Chatbot (frontend + backend) on a **local Kubernetes cluster (Minikube)** using **Docker AI (Gordon)**, **Helm Charts**, and **AI-assisted Kubernetes tooling (kubectl-ai, kagent)**, following **Spec-Driven Development** with no manual coding.

## Directory Structure

```
phase-4/
├── helm/
│   ├── todo-frontend/    # Frontend Helm chart
│   └── todo-backend/     # Backend Helm chart
├── specs/
│   └── 001-k8s-deployment/ # Deployment specifications
│       ├── spec.md       # Feature specification
│       ├── plan.md       # Implementation plan
│       └── tasks.md      # Detailed tasks
└── CLAUDE.md            # This file
```

## Technology Stack

| Component | Technology |
|-----------|------------|
| Containerization | Docker, Docker Desktop |
| AI Docker Ops | Docker AI Agent (Gordon) |
| Orchestration | Kubernetes (Minikube) |
| Package Manager | Helm Charts |
| AI DevOps | kubectl-ai, kagent |
| Application | Phase III Todo Chatbot |

## Setup Requirements

### Prerequisites
- Docker installed and running
- kubectl installed
- Minikube installed (will be installed if missing)
- Helm installed (will be installed if missing)

### Installation Commands
```bash
# Install Minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Install Helm
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```

## Deployment Strategy

### Phase 1: Containerization
- Use Docker AI (Gordon) to generate Dockerfiles for frontend and backend
- Build Docker images from `/phase-2` source code
- Verify containers run correctly locally

### Phase 2: Helm Packaging
- Create Helm charts for both frontend and backend
- Configure services, deployments, and ingress
- Set up environment variables for Neon DB connection

### Phase 3: Kubernetes Deployment
- Start Minikube cluster
- Deploy applications using Helm charts
- Verify applications are running and accessible

## Containerization Guidelines

### Frontend (Next.js)
- Use Node.js base image optimized for Next.js
- Multi-stage build for production
- Proper environment variable handling
- Health checks for production readiness

### Backend (FastAPI)
- Use Python base image optimized for FastAPI
- Multi-stage build with dependency optimization
- Non-root user for security
- Health checks and proper port exposure

## Helm Chart Structure

### Standard Templates
- deployment.yaml
- service.yaml
- ingress.yaml (optional for local)
- hpa.yaml (optional for local)
- configmap.yaml (for environment variables)
- secret.yaml (for sensitive data)

### Values Configuration
- Image repository and tag
- Resource limits and requests
- Environment variables
- Service configuration
- Replica count

## Environment Variables

### Backend Configuration
```yaml
DATABASE_URL: "postgresql://..."  # Neon DB connection
JWT_SECRET: "..."                 # Same as frontend
BACKEND_PORT: 8000
FRONTEND_URL: "http://frontend-service:3000"
```

### Frontend Configuration
```yaml
NEXT_PUBLIC_API_URL: "http://backend-service:8000"
BETTER_AUTH_URL: "http://frontend-service:3000"
BETTER_AUTH_SECRET: "..."         # Same as backend JWT_SECRET
```

## Common Commands

### Local Development
```bash
# Start Minikube
minikube start

# Build and deploy
helm install frontend ./helm/todo-frontend
helm install backend ./helm/todo-backend

# Check status
kubectl get pods
kubectl get services
```

### Troubleshooting
```bash
# Check pod logs
kubectl logs -l app=todo-frontend
kubectl logs -l app=todo-backend

# Port forward for testing
kubectl port-forward svc/todo-frontend 3000:80
kubectl port-forward svc/todo-backend 8000:80
```

## Success Criteria

### Functional Verification
- Frontend accessible via Minikube service
- Backend reachable and serving API
- Todo Chatbot functionality works identically to pre-deployment state
- Helm install/upgrade operations work without errors

### Technical Verification
- No manual Dockerfile or YAML editing required
- AI-assisted tools (Gordon, kubectl-ai, kagent) used successfully
- Entire workflow reproducible from spec + prompts