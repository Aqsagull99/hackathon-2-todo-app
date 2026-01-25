# Todo App Kubernetes Deployment Guide

This guide provides step-by-step instructions to deploy the Todo Chatbot application to a local Kubernetes cluster using Minikube and Helm.

## Prerequisites

Before starting the deployment, ensure you have the following tools installed:

- Docker Desktop or Docker Engine
- kubectl
- Minikube
- Helm 3

### Install Prerequisites

```bash
# Install kubectl (Linux)
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Install Minikube (Linux)
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Install Helm (Linux)
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```

## Start Minikube Cluster

```bash
# Start Minikube with sufficient resources for the application
minikube start --cpus=4 --memory=8192 --disk-size=20g

# Verify cluster is running
kubectl cluster-info
kubectl get nodes
```

## Build Docker Images

First, you need to build the Docker images for both frontend and backend services. Make sure you're in the project root directory:

```bash
# Set Docker environment to use Minikube's Docker daemon
eval $(minikube docker-env)

# Build backend image
cd /home/aqsagulllinux/projects/hackathon-2-todo-app/phase-2/backend
docker build -t todo-backend:latest .

# Build frontend image
cd /home/aqsagulllinux/projects/hackathon-2-todo-app/phase-2/frontend
docker build -t todo-frontend:latest .

# Verify images are built
docker images | grep todo-
```

## Update Helm Chart Values

Before deploying, update the values in the Helm charts with your actual database connection details and API keys. Edit the following files:

### Backend Values
```bash
# Update backend values with your actual database connection string and API keys
vim /home/aqsagulllinux/projects/hackathon-2-todo-app/phase-4/helm/todo-backend/values.yaml
```

Update the secrets section:
```yaml
secrets:
  create: true
  databaseUrl: "postgresql+asyncpg://user:your_password@postgres:5432/todoapp"
  jwtSecret: "your_secure_jwt_secret_here"
  openrouterApiKey: "your_openrouter_api_key"  # Optional
  openaiApiKey: "your_openai_api_key"  # Optional
```

### Frontend Values
```bash
# Update frontend values with your auth secret
vim /home/aqsagulllinux/projects/hackathon-2-todo-app/phase-4/helm/todo-frontend/values.yaml
```

Update the secrets section:
```yaml
secrets:
  create: true
  betterAuthSecret: "your_secure_better_auth_secret_here"
  databaseUrl: "postgresql://user:your_password@postgres:5432/todoapp"
```

## Deploy the Application

### 1. Deploy Backend First
```bash
# Navigate to the project root
cd /home/aqsagulllinux/projects/hackathon-2-todo-app

# Deploy backend
helm install todo-backend ./phase-4/helm/todo-backend/ --namespace default --create-namespace
```

### 2. Deploy Frontend
```bash
# Deploy frontend
helm install todo-frontend ./phase-4/helm/todo-frontend/ --namespace default
```

## Verify Deployment

Check that all pods are running successfully:

```bash
# Check all pods
kubectl get pods

# Check services
kubectl get services

# Check deployments
kubectl get deployments

# View pod logs
kubectl logs -l app.kubernetes.io/name=todo-backend
kubectl logs -l app.kubernetes.io/name=todo-frontend
```

## Access the Application

### Option 1: Using Port Forwarding
```bash
# Forward frontend port
kubectl port-forward svc/todo-frontend 3000:80

# In another terminal, forward backend port
kubectl port-forward svc/todo-backend 8000:80
```

Then access:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000

### Option 2: Using Minikube Tunnel (for LoadBalancer services)
```bash
# Run tunnel in a separate terminal
minikube tunnel
```

Then check the external IP:
```bash
kubectl get services
```

## Troubleshooting

### Common Issues and Solutions

1. **Pods stuck in Pending state**
   ```bash
   # Check events
   kubectl get events --sort-by='.lastTimestamp'

   # Check node resources
   kubectl describe nodes
   ```

2. **ImagePullBackOff errors**
   ```bash
   # Make sure you built images using Minikube's Docker environment
   eval $(minikube docker-env)
   # Then rebuild images
   ```

3. **Database connection issues**
   ```bash
   # Check if database pod is running
   kubectl get pods -l app=postgres

   # Check database logs
   kubectl logs -l app=postgres
   ```

4. **Health check failures**
   ```bash
   # Check application logs
   kubectl logs -l app.kubernetes.io/name=todo-backend
   kubectl logs -l app.kubernetes.io/name=todo-frontend
   ```

### Useful Debugging Commands

```bash
# Describe a specific pod for detailed information
kubectl describe pod <pod-name>

# Exec into a pod for debugging
kubectl exec -it <pod-name> -- /bin/sh

# Check all resources in the namespace
kubectl get all

# Get detailed service information
kubectl describe service todo-frontend
kubectl describe service todo-backend
```

## Updating the Deployment

To update your deployment with new values or image versions:

```bash
# Update backend
helm upgrade todo-backend ./phase-4/helm/todo-backend/ -f values-prod.yaml

# Update frontend
helm upgrade todo-frontend ./phase-4/helm/todo-frontend/ -f values-prod.yaml
```

## Cleaning Up

To remove the deployed application:

```bash
# Uninstall releases
helm uninstall todo-frontend
helm uninstall todo-backend

# Optionally stop Minikube
minikube stop
```

## Production Considerations

For production deployments, consider the following:

1. **Persistent Storage**: Use cloud provider storage solutions
2. **Secrets Management**: Use external secret managers (HashiCorp Vault, AWS Secrets Manager)
3. **Ingress Controller**: Set up ingress for external access
4. **Monitoring**: Implement Prometheus and Grafana
5. **Logging**: Set up centralized logging solution
6. **Backup Strategy**: Regular database backups
7. **Security Scanning**: Scan images for vulnerabilities

## Architecture Overview

The deployed application consists of:

- **Frontend Service**: Next.js application serving the UI
- **Backend Service**: FastAPI application with AI chatbot capabilities
- **PostgreSQL Database**: Persistent storage for todos and conversations
- **Redis** (if configured): Caching and session storage
- **Load Balancer**: Service to route traffic to frontend

This architecture supports the Todo Chatbot functionality with natural language processing and task management capabilities.