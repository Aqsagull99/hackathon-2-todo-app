#!/bin/bash

# Todo App Kubernetes Deployment Script
# This script automates the deployment of the Todo Chatbot application to Minikube

set -e  # Exit on any error

echo "🚀 Starting Todo App Kubernetes Deployment..."

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo "🔍 Checking prerequisites..."

if ! command_exists kubectl; then
    echo "❌ kubectl is not installed. Please install kubectl first."
    exit 1
fi

if ! command_exists minikube; then
    echo "❌ minikube is not installed. Please install minikube first."
    exit 1
fi

if ! command_exists helm; then
    echo "❌ helm is not installed. Please install helm first."
    exit 1
fi

if ! command_exists docker; then
    echo "❌ docker is not installed. Please install docker first."
    exit 1
fi

echo "✅ All prerequisites are installed."

# Start Minikube if not already running
MINIKUBE_STATUS=$(minikube status --format='{{.Host}}' 2>/dev/null || echo "stopped")
if [ "$MINIKUBE_STATUS" != "Running" ]; then
    echo "🔄 Starting Minikube cluster..."
    minikube start --cpus=4 --memory=8192 --disk-size=20g
else
    echo "✅ Minikube is already running."
fi

# Set Docker environment to use Minikube's Docker daemon
echo "🐳 Setting Docker environment to Minikube..."
eval $(minikube docker-env)

# Build Docker images
echo "🔨 Building Docker images..."

# Build backend
echo "📦 Building backend image..."
cd /home/aqsagulllinux/projects/hackathon-2-todo-app/phase-2/backend
docker build -t todo-backend:latest . || {
    echo "❌ Failed to build backend image"
    exit 1
}

# Build frontend
echo "📦 Building frontend image..."
cd /home/aqsagulllinux/projects/hackathon-2-todo-app/phase-2/frontend
docker build -t todo-frontend:latest . || {
    echo "❌ Failed to build frontend image"
    exit 1
}

echo "✅ Docker images built successfully."

# Navigate back to project root
cd /home/aqsagulllinux/projects/hackathon-2-todo-app

# Deploy using Helm
echo "🚀 Deploying application to Kubernetes..."

# Deploy backend first
echo "📦 Deploying backend..."
helm uninstall todo-backend 2>/dev/null || true  # Remove if exists
helm install todo-backend ./phase-4/helm/todo-backend/ --namespace default --create-namespace

# Deploy frontend
echo "📦 Deploying frontend..."
helm uninstall todo-frontend 2>/dev/null || true  # Remove if exists
helm install todo-frontend ./phase-4/helm/todo-frontend/ --namespace default

echo "⏳ Waiting for pods to be ready..."

# Wait for pods to be ready
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=todo-backend --timeout=300s
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=todo-frontend --timeout=300s

echo "✅ Application deployed successfully!"

# Show deployment status
echo ""
echo "📋 Deployment Status:"
echo "====================="
kubectl get pods
echo ""
kubectl get services
echo ""
kubectl get deployments

echo ""
echo "🌐 Access the application:"
echo "========================"
echo "Frontend: Run 'kubectl port-forward svc/todo-frontend 3000:80' and visit http://localhost:3000"
echo "Backend:  Run 'kubectl port-forward svc/todo-backend 8000:80' and visit http://localhost:8000"
echo ""
echo "💡 Tip: You can also run 'minikube tunnel' in another terminal to access services directly via LoadBalancer."
echo ""
echo "🎉 Deployment completed successfully!"
