#!/bin/bash
# Script to deploy a Dapr-enabled application to Kubernetes in container mode
# Usage: ./deploy_dapr_k8s.sh <app-name> <image> [namespace]
#
# This script deploys a Dapr application in container mode where:
# - Your application runs in one container
# - Dapr sidecar (daprd) runs in a separate container within the same pod
# - Both containers share the same network namespace
# - Communication happens via localhost using standard Dapr ports:
#   - HTTP: 3500 (default) - For HTTP API calls to Dapr
#   - gRPC: 50001 (default) - For gRPC API calls to Dapr
# - The Dapr sidecar is automatically injected by the Dapr operator

set -e  # Exit on any error

APP_NAME=${1:-"dapr-app"}
IMAGE=${2:-"nginx:latest"}
NAMESPACE=${3:-"default"}

echo "Deploying Dapr application to Kubernetes: $APP_NAME"
echo "Image: $IMAGE"
echo "Namespace: $NAMESPACE"
echo "Mode: Container mode (Dapr sidecar runs as separate container in same pod)"

# Validate inputs
if [[ -z "$APP_NAME" ]]; then
    echo "Error: App name cannot be empty"
    exit 1
fi

if [[ -z "$IMAGE" ]]; then
    echo "Error: Image cannot be empty"
    exit 1
fi

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "Error: kubectl is not installed or not in PATH"
    exit 1
fi

# Check if Dapr is installed in Kubernetes
if ! kubectl get pods -n dapr-system &> /dev/null; then
    echo "Dapr is not installed in Kubernetes. Installing Dapr..."
    dapr init -k
    sleep 10
fi

# Create namespace if it doesn't exist
kubectl get namespace "$NAMESPACE" &> /dev/null || kubectl create namespace "$NAMESPACE"

echo "Deploying Dapr application in container mode..."
echo "Architecture: Container mode"
echo "- Your application runs in one container"
echo "- Dapr sidecar runs in a separate container within the same pod"
echo "- Communication via localhost using standard Dapr APIs"
echo "- Essential annotations: enabled, app-id, app-port"

# Create the deployment with Dapr annotations
cat <<EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: $APP_NAME
  namespace: $NAMESPACE
  labels:
    app: $APP_NAME
spec:
  replicas: 1
  selector:
    matchLabels:
      app: $APP_NAME
  template:
    metadata:
      labels:
        app: $APP_NAME
      annotations:
        dapr.io/enabled: "true"              # Essential: Enables Dapr sidecar injection
        dapr.io/app-id: "$APP_NAME"          # Essential: Unique application ID
        dapr.io/app-port: "3000"             # Essential: Port where your app is listening
        dapr.io/config: "appconfig"
        dapr.io/enable-metrics: "true"
        dapr.io/metrics-port: "9090"
        # Dapr ports in container mode (accessible via localhost from app container)
        # HTTP: 3500 (default) - For HTTP API calls to Dapr
        # gRPC: 50001 (default) - For gRPC API calls to Dapr
    spec:
      containers:
      - name: $APP_NAME
        image: $IMAGE
        ports:
        - containerPort: 3000
        env:
        - name: DAPR_API_TOKEN
          valueFrom:
            secretKeyRef:
              name: dapr-api-token
              key: token
---
apiVersion: v1
kind: Service
metadata:
  name: $APP_NAME-service
  namespace: $NAMESPACE
spec:
  selector:
    app: $APP_NAME
  ports:
    - protocol: TCP
      port: 80
      targetPort: 3000
  type: LoadBalancer
EOF

echo "Waiting for deployment to be ready..."
kubectl rollout status deployment/$APP_NAME -n $NAMESPACE --timeout=300s

echo ""
echo "Dapr application $APP_NAME deployed successfully to Kubernetes!"
echo "Service: $APP_NAME-service in namespace $NAMESPACE"
echo ""
echo "Container mode details:"
echo "- Dapr sidecar automatically injected as separate container"
echo "- Both containers share network namespace (localhost communication)"
echo "- Standard Dapr ports available: HTTP:3500, gRPC:50001"
echo ""
echo "To check status: kubectl get pods -n $NAMESPACE"
echo "To view logs: kubectl logs -l app=$APP_NAME -n $NAMESPACE"
echo "To view Dapr sidecar logs: kubectl logs -l app=$APP_NAME -n $NAMESPACE -c daprd"
echo "To port forward: kubectl port-forward svc/$APP_NAME-service -n $NAMESPACE 3000:80"