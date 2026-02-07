# Phase V: DigitalOcean Deployment

## Overview
This document outlines the deployment of the Phase V event-driven Todo App to DigitalOcean Kubernetes (DOKS).

## Architecture
- **Backend**: FastAPI application with Dapr sidecar
- **Frontend**: Next.js application with Dapr sidecar
- **Event System**: Dapr pub/sub with Redpanda Cloud Kafka
- **Database**: Neon PostgreSQL
- **Load Balancer**: DigitalOcean Load Balancer for frontend access

## Deployment Steps

### 1. Prerequisites
- DigitalOcean CLI (`doctl`) installed and configured
- `kubectl` installed and configured
- Docker images pushed to DigitalOcean Container Registry

### 2. Initialize Dapr
```bash
# Initialize Dapr on the cluster
kubectl apply -f https://github.com/dapr/dapr/releases/latest/download/install.yaml

# Wait for Dapr to be ready
kubectl wait --for=condition=ready pod -l app=dapr-operator --timeout=300s -n dapr-system
```

### 3. Create Infrastructure Secrets
```bash
# Create Neon DB secret
kubectl create secret generic neon-db-secret \
  --from-literal=database-url="your-neon-db-connection-string" \
  --from-literal=jwt-secret="your-jwt-secret"

# Create Redpanda credentials secret
kubectl create secret generic redpanda-credentials \
  --from-literal=bootstrap-servers="your-redpanda-bootstrap-servers" \
  --from-literal=username="your-redpanda-username" \
  --from-literal=password="your-redpanda-password"
```

### 4. Apply Dapr Components
```bash
# Apply Kafka pubsub component
kubectl apply -f dapr-components/pubsub-kafka.yaml

# Apply PostgreSQL state store component
kubectl apply -f dapr-components/state-postgres.yaml
```

### 5. Deploy Applications
```bash
# Deploy backend with Dapr annotation
kubectl apply -f deployments/backend.yaml

# Deploy frontend with Dapr annotation and LoadBalancer service
kubectl apply -f deployments/frontend.yaml
```

## Dapr Annotations
Both applications use these Dapr annotations:
- `dapr.io/enabled: "true"` - Enable Dapr sidecar injection
- `dapr.io/app-id: "backend-todo"` or `"frontend-todo"` - Unique app identifier
- `dapr.io/app-port: "8000"` or `"3000"` - Application port for Dapr
- `dapr.io/log-level: "info"` - Dapr sidecar log level

## Services Configuration
- **Backend**: ClusterIP service (internal communication)
- **Frontend**: LoadBalancer service (external access via DigitalOcean LB)

## Event-Driven Features
- **Task Events**: Published to `task-events` topic via Kafka
- **Reminder Events**: Published to `reminders` topic via Kafka
- **Recurring Tasks**: Automatically spawn next occurrences via event handlers
- **Real-time Sync**: Via `task-updates` topic for client synchronization

## Verification Commands
```bash
# Check pod status (should show 2/2 READY for apps with Dapr sidecars)
kubectl get pods

# Check services
kubectl get services

# Check Dapr components
kubectl get components.dapr.io

# Check Dapr sidecar logs
kubectl logs <pod-name> -c daprd

# Get external IP
kubectl get service todo-frontend -o jsonpath='{.status.loadBalancer.ingress[0].ip}'
```

## Expected Results
- Pods show 2/2 READY (app + Dapr sidecar)
- External IP assigned to frontend LoadBalancer
- Dapr sidecars connected to Redpanda Cloud
- Applications connected to Neon PostgreSQL
- Event publishing/subscribing working

## Troubleshooting
- If pods show 1/2 READY, check Dapr sidecar logs
- If no external IP, check DigitalOcean LoadBalancer quota
- If Kafka connection fails, verify Redpanda credentials
- If database connection fails, verify Neon DB connection string

## Security Notes
- All credentials stored in Kubernetes secrets
- Dapr components use `secretKeyRef` (no hardcoded credentials)
- SSL/TLS enforced for all external connections
- SASL/SCRAM authentication for Kafka

## Success Metrics
- [ ] External IP assigned to frontend (LoadBalancer)
- [ ] Dapr sidecars running with 2/2 container readiness
- [ ] Kafka pub/sub connected to Redpanda Cloud
- [ ] PostgreSQL state store connected to Neon DB
- [ ] Applications responding to health checks
- [ ] Event publishing working through Dapr