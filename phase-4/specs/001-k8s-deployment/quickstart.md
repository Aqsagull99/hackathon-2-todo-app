# Quickstart Guide: Phase IV — Local Kubernetes Deployment

## Prerequisites
- Docker Desktop with Kubernetes enabled OR Minikube installed and running
- Docker AI Agent (Gordon) configured
- Helm 3.x installed
- kubectl-ai and kagent tools installed
- Access to Docker Hub account

## Setup Process

### 1. Clone and Prepare Repository
```bash
git clone [repository-url]
cd hackathon-2-todo-app
cd phase-2
```

### 2. Containerize Applications using Docker AI (Gordon)
```bash
# Navigate to frontend directory
cd frontend
# Use Gordon to generate Dockerfile
docker ai create Dockerfile --context .

# Navigate to backend directory
cd ../backend
# Use Gordon to generate Dockerfile
docker ai create Dockerfile --context .
```

### 3. Build and Push Container Images
```bash
# Build frontend image
docker build -t [dockerhub-username]/todo-frontend:latest ./frontend
docker push [dockerhub-username]/todo-frontend:latest

# Build backend image
docker build -t [dockerhub-username]/todo-backend:latest ./backend
docker push [dockerhub-username]/todo-backend:latest
```

### 4. Set Up Kubernetes Environment
```bash
# Start Minikube (if not using Docker Desktop Kubernetes)
minikube start

# Verify Kubernetes is running
kubectl cluster-info
```

### 5. Create Helm Chart Structure
```bash
cd ../../phase-4
mkdir -p helm/todo-frontend
mkdir -p helm/todo-backend

# Initialize basic Helm chart structure (optional, can be done manually)
helm create helm/todo-frontend
helm create helm/todo-backend
```

### 6. Deploy to Kubernetes
```bash
# Navigate to Helm charts directory
cd helm

# Install frontend chart
helm install todo-frontend todo-frontend/

# Install backend chart
helm install todo-backend todo-backend/
```

### 7. Verify Deployment
```bash
# Check if pods are running
kubectl get pods

# Check services
kubectl get services

# Check deployment status
kubectl get deployments
```

### 8. Access Applications
```bash
# Get Minikube IP (if using Minikube)
minikube ip

# Or use kubectl port-forward to access services locally
kubectl port-forward svc/todo-frontend 3000:80
kubectl port-forward svc/todo-backend 8000:80
```

## AI-Assisted Commands

### Using kubectl-ai for Management
```bash
# Scale frontend to 3 replicas
kubectl-ai "scale deployment todo-frontend to 3 replicas"

# Get status of all resources
kubectl-ai "show status of all pods and services"

# Debug failing pods
kubectl-ai "show logs for failed pods in todo-backend namespace"
```

### Using kagent for Optimization
```bash
# Check cluster health
kagent health-check

# Optimize resource usage
kagent optimize-resources
```

## Troubleshooting

### Common Issues
1. **Images not pulling**: Ensure Docker Hub credentials are configured in Kubernetes
2. **Services not accessible**: Check if LoadBalancer is supported in Minikube (may need to use NodePort)
3. **DB connection failures**: Verify Neon DB connection string is correctly configured in environment variables

### Quick Fixes
```bash
# Restart all deployments
kubectl rollout restart deployment --all

# Check detailed status
kubectl describe pods

# Get detailed logs
kubectl logs -l app=todo-backend
```

## Cleanup
```bash
# Uninstall Helm releases
helm uninstall todo-frontend
helm uninstall todo-backend

# Stop Minikube (if applicable)
minikube stop
```