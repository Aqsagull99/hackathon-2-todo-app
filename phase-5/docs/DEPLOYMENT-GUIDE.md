# Phase V Deployment Guide

## Prerequisites
- Kubernetes cluster (Minikube or DOKS)
- Dapr installed
- Redpanda Cloud credentials in .env
- Helm 3+

## Minikube Deployment
```bash
minikube start
dapr init -k
kubectl apply -f phase-4/helm/dapr-components/
helm install todo-backend phase-4/helm/todo-backend -f phase-4/helm/todo-backend/values-minikube.yaml
```

## DOKS Deployment
```bash
doctl kubernetes cluster create todo-cluster
dapr init -k
helm install todo-backend phase-4/helm/todo-backend -f phase-4/helm/todo-backend/values-doks.yaml
```

## Testing
Test all advanced features through chatbot interface.
