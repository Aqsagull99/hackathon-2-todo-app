# Complete Kubernetes Deployment Guide for Todo App

## Overview

This comprehensive guide provides step-by-step instructions to deploy the Todo Chatbot application to a local Kubernetes cluster using Minikube and Helm. The guide addresses the cross-platform scenario where Minikube and Helm are installed on Windows while development occurs in WSL.

## Prerequisites

Before starting the deployment, ensure you have the following tools available:

### On Windows Side (Where Minikube and Helm are installed):
- Docker Desktop with Kubernetes enabled OR Minikube
- Helm 3.x
- kubectl
- kubectl-ai (optional, for AI-assisted operations)
- kagent (optional, for AI-assisted operations)

### On WSL Side (Where Docker images are built):
- Docker Engine (for building images)
- Access to source code in `/home/aqsagulllinux/projects/hackathon-2-todo-app`

## Architecture Overview

The deployed application consists of:
- **Frontend Service**: Next.js application serving the UI
- **Backend Service**: FastAPI application with AI chatbot capabilities
- **PostgreSQL Database**: Persistent storage for todos and conversations
- **Services**: Kubernetes services to route traffic
- **Load Balancer**: Service to route traffic to frontend

## Cross-Platform Deployment Strategy

Due to the mixed environment setup, the deployment process involves:

1. **Image Building** (WSL): Build Docker images in WSL environment
2. **Image Transfer** (WSL ↔ Windows): Make images available to Windows Kubernetes
3. **Deployment** (Windows): Deploy using Helm on Windows-side cluster
4. **Validation** (Both): Validate functionality across environments

## Step 1: Prepare Docker Images in WSL

First, ensure the Docker images are built in the WSL environment:

```bash
# Navigate to project directory in WSL
cd /home/aqsagulllinux/projects/hackathon-2-todo-app

# Build backend image
cd /home/aqsagulllinux/projects/hackathon-2-todo-app/phase-2/backend
docker build -t todo-backend:latest .

# Build frontend image
cd /home/aqsagulllinux/projects/hackathon-2-todo-app/phase-2/frontend
docker build -t todo-frontend:latest .

# Verify images are built
docker images | grep todo-
```

Expected output should show:
```
todo-backend:latest    205519ea597c    679MB
todo-frontend:latest   [image-id]      [size]
```

## Step 2: Prepare Images for Windows Environment

### Option A: Save/Load Method (Recommended for cross-platform)

```bash
# In WSL - Save images as tar files
cd /home/aqsagulllinux/projects/hackathon-2-todo-app
docker save -o todo-backend.tar todo-backend:latest
docker save -o todo-frontend.tar todo-frontend:latest

# Move files to shared location accessible from Windows
# (Use Windows file system path like /mnt/c/temp/)
mv todo-backend.tar /mnt/c/temp/
mv todo-frontend.tar /mnt/c/temp/
```

### Option B: Private Registry Method (Alternative)

```bash
# Tag images for registry
docker tag todo-backend:latest localhost:5000/todo-backend:latest
docker tag todo-frontend:latest localhost:5000/todo-frontend:latest

# Start local registry (if not already running)
docker run -d -p 5000:5000 --name registry registry:2

# Push to local registry
docker push localhost:5000/todo-backend:latest
docker push localhost:5000/todo-frontend:latest
```

## Step 3: Transfer Images to Windows Environment

### For Option A (Save/Load Method):

1. **On Windows Command Prompt**:
   ```cmd
   # Load images into Windows Docker
   docker load -i C:\temp\todo-backend.tar
   docker load -i C:\temp\todo-frontend.tar

   # Verify images are loaded
   docker images | findstr todo
   ```

2. **If using Minikube**:
   ```cmd
   # Set Docker environment to use Minikube's Docker daemon
   minikube docker-env

   # Load images into Minikube's registry
   minikube image load todo-backend:latest
   minikube image load todo-frontend:latest
   ```

### For Option B (Registry Method):

1. **Ensure registry is accessible from Windows**:
   ```cmd
   # On Windows, pull images from registry
   docker pull localhost:5000/todo-backend:latest
   docker pull localhost:5000/todo-frontend:latest
   ```

## Step 4: Start Kubernetes Cluster (On Windows)

```cmd
# Start Minikube with sufficient resources
minikube start --cpus=4 --memory=8192 --disk-size=20g

# Verify cluster is running
kubectl cluster-info
kubectl get nodes
```

## Step 5: Update Helm Chart Values

Before deploying, update the values in the Helm charts with your actual database connection details and API keys. Since the files are in WSL, you'll need to edit them there and they'll be accessible from Windows due to shared file system.

### Backend Values
```bash
# On WSL side, update backend values with your actual database connection string and API keys
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
# On WSL side, update frontend values with your auth secret
vim /home/aqsagulllinux/projects/hackathon-2-todo-app/phase-4/helm/todo-frontend/values.yaml
```

Update the secrets section:
```yaml
secrets:
  create: true
  betterAuthSecret: "your_secure_better_auth_secret_here"
  databaseUrl: "postgresql://user:your_password@postgres:5432/todoapp"
```

## Step 6: Deploy the Application (On Windows)

### 1. Deploy Backend First
```cmd
# Navigate to the project directory in Windows Command Prompt
cd C:\path\to\hackathon-2-todo-app  # Map to your WSL path

# Deploy backend using Helm
helm install todo-backend .\phase-4\helm\todo-backend\ --namespace default --create-namespace
```

### 2. Deploy Frontend
```cmd
# Deploy frontend
helm install todo-frontend .\phase-4\helm\todo-frontend\ --namespace default
```

## Step 7: Verify Deployment (On Windows)

Check that all pods are running successfully:

```cmd
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

## Step 8: Access the Application

### Option 1: Using Port Forwarding
```cmd
# Forward frontend port
kubectl port-forward svc/todo-frontend 3000:80

# In another terminal, forward backend port
kubectl port-forward svc/todo-backend 8000:80
```

Then access:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000

### Option 2: Using Minikube Tunnel (for LoadBalancer services)
```cmd
# Run tunnel in a separate terminal (Windows)
minikube tunnel
```

Then check the external IP:
```cmd
kubectl get services
```

## Step 9: AI-Assisted Operations (If Available)

### Using kubectl-ai on Windows
```cmd
# Get resources with natural language
kubectl ai get pods in default namespace
kubectl ai show me deployments in default
kubectl ai list services in default namespace

# Scale resources
kubectl ai scale deployment todo-frontend --replicas=2
kubectl ai scale deployment todo-backend --replicas=2

# View logs
kubectl ai show me logs from deployment/todo-backend
kubectl ai get logs from deployment/todo-frontend
```

### Using kagent on Windows
```cmd
# Perform cluster health checks
kagent check cluster health
kagent analyze default namespace
kagent optimize resource usage in default
```

## Troubleshooting Cross-Platform Issues

### Common Issues and Solutions

1. **ImagePullBackOff errors**
   ```cmd
   # Ensure images are loaded into the correct Docker environment
   # For Minikube: use minikube image load
   # For Docker Desktop K8s: ensure images are in Docker Desktop's registry
   ```

2. **Path Issues Between WSL and Windows**
   ```cmd
   # Use proper path mapping
   # WSL: /home/aqsagulllinux/projects/hackathon-2-todo-app
   # Windows: C:\Users\[username]\[mapped-path]\hackathon-2-todo-app
   ```

3. **Network Connectivity Issues**
   ```cmd
   # Check Minikube status
   minikube status
   minikube ip

   # Verify Docker is using correct context
   docker context ls
   ```

4. **Permission Issues**
   ```cmd
   # Run Windows commands as Administrator if needed
   # Ensure proper file permissions in WSL
   ```

### Useful Debugging Commands

```cmd
# Describe a specific pod for detailed information
kubectl describe pod <pod-name>

# Check events for recent issues
kubectl get events --sort-by='.lastTimestamp'

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

```cmd
# Update backend
helm upgrade todo-backend .\phase-4\helm\todo-backend\ -f values-prod.yaml

# Update frontend
helm upgrade todo-frontend .\phase-4\helm\todo-frontend\ -f values-prod.yaml
```

## Cleaning Up

To remove the deployed application:

```cmd
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
8. **Image Registry**: Use secure, private image registries

## Success Criteria Verification

After completing the deployment, verify:

- [ ] Frontend application accessible via Minikube service within 5 minutes
- [ ] Backend API reachable and serving requests within 5 minutes
- [ ] Todo Chatbot functionality works identically to pre-deployment state
- [ ] Helm install and upgrade operations complete without errors
- [ ] At least 3 Kubernetes operations performed successfully using kubectl-ai (if available)
- [ ] Entire deployment workflow reproducible from spec + prompts
- [ ] No manual Dockerfile or YAML editing required during the process
- [ ] All AI-assisted tools (Gordon, kubectl-ai, kagent) used successfully (where available)

## Summary

This cross-platform deployment approach allows you to leverage the Docker build capabilities in WSL while utilizing the Kubernetes cluster managed on Windows. The key is proper image transfer between environments and careful attention to path mappings and Docker contexts.

The deployment follows best practices for security, scalability, and maintainability while supporting the AI-assisted operations where available.