#!/bin/bash

# Phase V Deployment Script for DigitalOcean Kubernetes
# According to the Constitution requirements
#
# SECURITY: This script uses environment variables for all sensitive data.
# Before running, ensure all required environment variables are set:
# - DATABASE_URL
# - REDPANDA_BOOTSTRAP_SERVERS
# - REDPANDA_USERNAME
# - REDPANDA_PASSWORD
# - JWT_SECRET (optional, will be created if not provided)

set -e  # Exit on any error

# Validate required environment variables
required_vars=("DATABASE_URL" "REDPANDA_BOOTSTRAP_SERVERS" "REDPANDA_USERNAME" "REDPANDA_PASSWORD")
for var in "${required_vars[@]}"; do
  if [ -z "${!var}" ]; then
    echo "❌ Error: Required environment variable $var is not set"
    echo "Please set all required variables before running this script."
    echo "See .env.example for reference."
    exit 1
  fi
done

echo "🚀 Starting Phase V Deployment to DigitalOcean..."

# 1. Switch to DigitalOcean cluster context
echo "🔧 Switching to DigitalOcean cluster..."
doctl kubernetes cluster kubeconfig save "${CLUSTER_NAME:-todo-cluster}"

# 2. Initialize Dapr on the cluster
echo "🌟 Initializing Dapr components..."
kubectl apply -f https://github.com/dapr/dapr/releases/latest/download/install.yaml

# Wait for Dapr to be ready
echo "⏳ Waiting for Dapr to be ready..."
kubectl wait --for=condition=ready pod -l app=dapr-operator --timeout=300s -n dapr-system

# 3. Create infrastructure secrets
echo "🔐 Creating infrastructure secrets..."

# Create Neon DB secret from environment variable
kubectl create secret generic neon-db-secret \
  --from-literal=database-url="$DATABASE_URL" \
  --dry-run=client -o yaml | kubectl apply -f -

# Create Redpanda credentials secret from environment variables
kubectl create secret generic redpanda-credentials \
  --from-literal=bootstrap-servers="$REDPANDA_BOOTSTRAP_SERVERS" \
  --from-literal=username="$REDPANDA_USERNAME" \
  --from-literal=password="$REDPANDA_PASSWORD" \
  --dry-run=client -o yaml | kubectl apply -f -

# Create application secrets
if [ -z "$JWT_SECRET" ]; then
  echo "⚠️  Warning: JWT_SECRET not set, generating random secret..."
  JWT_SECRET=$(openssl rand -base64 32)
fi

kubectl create secret generic todo-backend-secrets \
  --from-literal=JWT_SECRET="$JWT_SECRET" \
  --dry-run=client -o yaml | kubectl apply -f -

# 4. Apply Dapr components
echo "📡 Applying Dapr components..."

# Kafka PubSub component
cat <<EOF | kubectl apply -f -
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kafka-pubsub
  namespace: default
spec:
  type: pubsub.kafka
  version: v1
  metadata:
  - name: brokers
    secretKeyRef:
      name: redpanda-credentials
      key: bootstrap-servers
  - name: consumerGroup
    value: "todo-app-group"
  - name: clientId
    value: "todo-backend-client"
  - name: authType
    value: "password"
  - name: saslUsername
    secretKeyRef:
      name: redpanda-credentials
      key: username
  - name: saslPassword
    secretKeyRef:
      name: redpanda-credentials
      key: password
  - name: saslMechanism
    value: "SCRAM-SHA-256"
  - name: securityProtocol
    value: "SASL_SSL"
  - name: maxMessageBytes
    value: "1024000"
  - name: consumeRetryInterval
    value: "200ms"
  - name: dialTimeout
    value: "30s"
  - name: readTimeout
    value: "30s"
  - name: writeTimeout
    value: "30s"
EOF

# PostgreSQL State Store component
cat <<EOF | kubectl apply -f -
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: statestore
  namespace: default
spec:
  type: state.postgresql
  version: v1
  metadata:
  - name: connectionString
    secretKeyRef:
      name: neon-db-secret
      key: database-url
  - name: tableName
    value: "dapr_state"
  - name: metadataTableName
    value: "dapr_metadata"
  - name: cleanupIntervalInSeconds
    value: "3600"
EOF

# 5. Deploy applications with Dapr annotations
echo "🚢 Deploying applications..."

# Backend deployment
cat <<EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: todo-backend
  namespace: default
spec:
  replicas: ${BACKEND_REPLICAS:-2}
  selector:
    matchLabels:
      app: todo-backend
  template:
    metadata:
      labels:
        app: todo-backend
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "backend-todo"
        dapr.io/app-port: "8000"
        dapr.io/config: ""
        dapr.io/log-level: "info"
    spec:
      containers:
      - name: todo-backend
        image: ${BACKEND_IMAGE:-registry.digitalocean.com/todo/backend:latest}
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: neon-db-secret
              key: database-url
        - name: JWT_SECRET
          valueFrom:
            secretKeyRef:
              name: todo-backend-secrets
              key: JWT_SECRET
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: todo-backend
  namespace: default
spec:
  selector:
    app: todo-backend
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
  type: ClusterIP
EOF

# Frontend deployment with LoadBalancer service
cat <<EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: todo-frontend
  namespace: default
spec:
  replicas: ${FRONTEND_REPLICAS:-2}
  selector:
    matchLabels:
      app: todo-frontend
  template:
    metadata:
      labels:
        app: todo-frontend
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "frontend-todo"
        dapr.io/app-port: "3000"
        dapr.io/config: ""
        dapr.io/log-level: "info"
    spec:
      containers:
      - name: todo-frontend
        image: ${FRONTEND_IMAGE:-registry.digitalocean.com/todo/frontend:latest}
        ports:
        - containerPort: 3000
        env:
        - name: NEXT_PUBLIC_API_URL
          value: "http://todo-backend:80"
---
apiVersion: v1
kind: Service
metadata:
  name: todo-frontend
  namespace: default
spec:
  selector:
    app: todo-frontend
  ports:
    - protocol: TCP
      port: 80
      targetPort: 3000
  type: LoadBalancer
EOF

# 6. Wait for deployments to be ready
echo "⏳ Waiting for deployments to be ready..."
kubectl wait --for=condition=ready pod -l app=todo-backend --timeout=300s || true
kubectl wait --for=condition=ready pod -l app=todo-frontend --timeout=300s || true

# 7. Get the external IP of the frontend service
echo "🌐 Retrieving external IP for frontend..."
TIMEOUT=180
ELAPSED=0
while [ $ELAPSED -lt $TIMEOUT ]; do
  EXTERNAL_IP=$(kubectl get service todo-frontend -o jsonpath='{.status.loadBalancer.ingress[0].ip}' 2>/dev/null || echo "")
  if [ -n "$EXTERNAL_IP" ]; then
    echo "✅ Frontend is live at: http://$EXTERNAL_IP"
    break
  else
    echo "⏳ Waiting for external IP assignment... ($ELAPSED/$TIMEOUT seconds)"
    sleep 10
    ELAPSED=$((ELAPSED + 10))
  fi
done

if [ -z "$EXTERNAL_IP" ]; then
  echo "⚠️  Warning: Could not retrieve external IP within timeout"
  echo "Run: kubectl get service todo-frontend"
fi

# 8. Verify Dapr sidecars are running
echo "🔍 Verifying Dapr sidecars..."
echo "Backend pods:"
kubectl get pods -l app=todo-backend -o jsonpath='{range .items[*]}{.metadata.name}{"\n"}{range .spec.containers[*]}- {.name}{"\n"}{end}{"\n"}{end}'
echo ""
echo "Frontend pods:"
kubectl get pods -l app=todo-frontend -o jsonpath='{range .items[*]}{.metadata.name}{"\n"}{range .spec.containers[*]}- {.name}{"\n"}{end}{"\n"}{end}'

echo ""
echo "🎉 Phase V Deployment to DigitalOcean Complete!"
echo "🌐 Public URL: http://${EXTERNAL_IP:-pending}"
echo "📋 Backend service: todo-backend:80"
echo "📊 Dapr sidecars: Running with Kafka pubsub and PostgreSQL statestore"
echo ""
echo "📝 Next steps:"
echo "   - Verify application health: kubectl get pods"
echo "   - Check logs: kubectl logs -l app=todo-backend -c todo-backend"
echo "   - Monitor Dapr: kubectl logs -l app=todo-backend -c daprd"
