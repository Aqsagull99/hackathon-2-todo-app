#!/bin/bash

# Todo App Cleanup Script
# This script removes the Todo Chatbot application from Kubernetes

echo "🧹 Cleaning up Todo App deployment..."

# Uninstall Helm releases
echo "🗑️ Removing Helm releases..."
helm uninstall todo-frontend 2>/dev/null || echo "⚠️  todo-frontend not found or already removed"
helm uninstall todo-backend 2>/dev/null || echo "⚠️  todo-backend not found or already removed"

# Remove any remaining resources
echo "🗑️ Removing any remaining resources..."
kubectl delete pvc postgres-pvc 2>/dev/null || echo "⚠️  PVC not found or already removed"
kubectl delete secret postgres-secrets 2>/dev/null || echo "⚠️  postgres-secrets not found or already removed"

# Check if resources were removed
echo "📋 Remaining resources in default namespace:"
kubectl get all

echo "✅ Cleanup completed!"
echo ""
echo "💡 To stop Minikube, run: minikube stop"