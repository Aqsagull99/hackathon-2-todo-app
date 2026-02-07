#!/bin/bash
# Script to install ArgoCD on Kubernetes cluster
# Usage: ./install_argocd.sh

set -e  # Exit on any error

echo "Installing ArgoCD on Kubernetes cluster..."

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "Error: kubectl is not installed or not in PATH"
    exit 1
fi

# Create argocd namespace
echo "Creating argocd namespace..."
kubectl create namespace argocd --dry-run=client -o yaml | kubectl apply -f -

# Install ArgoCD
echo "Installing ArgoCD..."
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Wait for ArgoCD pods to be ready
echo "Waiting for ArgoCD pods to be ready..."
kubectl wait --for=condition=Ready pods -l app.kubernetes.io/name=argocd-server -n argocd --timeout=300s
kubectl wait --for=condition=Ready pods -l app.kubernetes.io/name=argocd-repo-server -n argocd --timeout=300s
kubectl wait --for=condition=Ready pods -l app.kubernetes.io/name=argocd-application-controller -n argocd --timeout=300s

# Get initial admin password
echo ""
echo "ArgoCD installation completed successfully!"
echo ""
echo "Initial admin password:"
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
echo ""
echo ""
echo "To access ArgoCD UI:"
echo "kubectl port-forward svc/argocd-server -n argocd 8080:443"
echo "Then open https://localhost:8080 in your browser"
echo ""
echo "To install ArgoCD CLI:"
echo "curl -sSL -o argocd-linux-amd64 https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64"
echo "sudo install argocd-linux-amd64 /usr/local/bin/argocd"
echo "chmod +x /usr/local/bin/argocd"