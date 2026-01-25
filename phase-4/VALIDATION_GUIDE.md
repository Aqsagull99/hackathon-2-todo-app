# Kubernetes Deployment Validation Guide

## Overview

This document provides comprehensive validation procedures for the Todo App Kubernetes deployment. It includes pre-deployment, deployment-time, and post-deployment validation steps to ensure the application functions correctly in the Kubernetes environment.

## Validation Objectives

The validation process ensures:

1. Successful deployment of frontend and backend applications
2. Proper connectivity between services
3. Functionality preservation from pre-deployment state
4. Performance and reliability standards
5. Security and compliance requirements

## Pre-Deployment Validation

### 1. Environment Prerequisites

Before starting deployment, validate:

```bash
# Check Kubernetes cluster status
kubectl cluster-info
kubectl get nodes
kubectl version --client
```

Expected results:
- Kubernetes master reachable
- At least one node Ready
- kubectl client version compatible with cluster

### 2. Resource Availability

Validate sufficient cluster resources:

```bash
# Check available resources
kubectl top nodes
kubectl describe nodes
```

Expected results:
- At least 4 CPU cores available
- At least 8GB memory available
- Sufficient storage capacity

### 3. Helm Chart Validation

Validate Helm charts before deployment:

```bash
# Lint charts
helm lint ./helm/todo-frontend/
helm lint ./helm/todo-backend/

# Template validation
helm template test-frontend ./helm/todo-frontend/
helm template test-backend ./helm/todo-backend/
```

Expected results:
- No linting errors
- Valid Kubernetes manifests generated
- Proper templating syntax

### 4. Image Availability

Verify Docker images are available:

```bash
# Check images in Minikube's registry
eval $(minikube docker-env)
docker images | grep todo
```

Expected results:
- `todo-frontend:latest` available
- `todo-backend:latest` available
- Images built with proper tags

## Deployment-Time Validation

### 1. Helm Installation

Monitor installation progress:

```bash
# Install with verbose output
helm install todo-backend ./helm/todo-backend/ --namespace default --create-namespace --debug
helm install todo-frontend ./helm/todo-frontend/ --namespace default --debug

# Watch resources during installation
kubectl get pods -w
kubectl get services -w
```

Expected results:
- Charts install without errors
- All resources created successfully
- No validation warnings

### 2. Resource Creation Validation

Verify all resources are created:

```bash
# Check deployments
kubectl get deployments
kubectl describe deployment todo-frontend
kubectl describe deployment todo-backend

# Check services
kubectl get services
kubectl describe service todo-frontend
kubectl describe service todo-backend

# Check pods
kubectl get pods
kubectl describe pods -l app.kubernetes.io/name=todo-frontend
kubectl describe pods -l app.kubernetes.io/name=todo-backend
```

Expected results:
- Deployments in Running state
- Services with proper ports and selectors
- Pods scheduled and running

## Post-Deployment Validation

### 1. Pod Status Validation

Check pod health and status:

```bash
# Check pod statuses
kubectl get pods -o wide

# Verify readiness and liveness probes
kubectl describe pods -l app=todo-frontend
kubectl describe pods -l app=todo-backend

# Check pod logs
kubectl logs -l app.kubernetes.io/name=todo-frontend --tail=50
kubectl logs -l app.kubernetes.io/name=todo-backend --tail=50
```

Expected results:
- All pods in Running status
- Ready count matches desired replicas
- No crash loops or restarts
- Healthy probe responses

### 2. Service Connectivity Validation

Test service connectivity:

```bash
# Check service endpoints
kubectl get endpoints todo-frontend
kubectl get endpoints todo-backend

# Test internal connectivity
kubectl run test-pod --image=busybox --rm -it --restart=Never -- sh
# Inside pod: wget -qO- http://todo-frontend:80/health
# Inside pod: wget -qO- http://todo-backend:80/health
kubectl delete pod test-pod
```

Expected results:
- Endpoints match running pods
- Internal service connectivity works
- Health endpoints return 200 status

### 3. External Access Validation

Test external access to applications:

```bash
# Port forward for testing
kubectl port-forward svc/todo-frontend 3000:80 &
kubectl port-forward svc/todo-backend 8000:80 &

# Test external connectivity
curl -I http://localhost:3000
curl -I http://localhost:8000/health
```

Expected results:
- Frontend accessible on port 3000
- Backend health check passes on port 8000
- Proper HTTP response codes

### 4. Application Functionality Validation

Validate application functionality:

```bash
# Test API endpoints
curl -X GET http://localhost:8000/api/health
curl -X GET http://localhost:8000/api/todo

# Test database connectivity (if applicable)
curl -X GET http://localhost:8000/api/status
```

Expected results:
- Health endpoints return success
- API endpoints respond correctly
- Database connectivity established

### 5. Todo Chatbot Functionality Validation

Test specific chatbot functionality:

```bash
# Test chatbot endpoints
curl -X POST http://localhost:8000/api/chat -H "Content-Type: application/json" -d '{"message": "hello"}'

# Test task management endpoints
curl -X GET http://localhost:8000/api/tasks
curl -X POST http://localhost:8000/api/tasks -H "Content-Type: application/json" -d '{"title": "Test Task"}'
```

Expected results:
- Chatbot responds to messages
- Task operations work correctly
- Functionality matches pre-deployment state

## Automated Validation Script

Create a validation script for comprehensive testing:

```bash
#!/bin/bash
# validate_deployment.sh

set -e

echo "Starting Kubernetes Deployment Validation..."

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
if ! command_exists kubectl; then
    echo "ERROR: kubectl not found"
    exit 1
fi

if ! command_exists helm; then
    echo "ERROR: helm not found"
    exit 1
fi

echo "✓ Prerequisites validated"

# Check cluster connectivity
echo "Checking cluster connectivity..."
kubectl cluster-info > /dev/null
echo "✓ Cluster connectivity verified"

# Check deployments
echo "Checking deployments..."
FRONTEND_REPLICAS=$(kubectl get deployment todo-frontend -o jsonpath='{.status.readyReplicas}')
BACKEND_REPLICAS=$(kubectl get deployment todo-backend -o jsonpath='{.status.readyReplicas}')

if [ "$FRONTEND_REPLICAS" -gt 0 ] && [ "$BACKEND_REPLICAS" -gt 0 ]; then
    echo "✓ Deployments are ready (Frontend: $FRONTEND_REPLICAS, Backend: $BACKEND_REPLICAS)"
else
    echo "✗ Deployments not ready"
    exit 1
fi

# Check services
echo "Checking services..."
FRONTEND_SERVICE=$(kubectl get service todo-frontend -o jsonpath='{.spec.clusterIP}')
BACKEND_SERVICE=$(kubectl get service todo-backend -o jsonpath='{.spec.clusterIP}')

if [ -n "$FRONTEND_SERVICE" ] && [ -n "$BACKEND_SERVICE" ]; then
    echo "✓ Services are available"
else
    echo "✗ Services not available"
    exit 1
fi

# Check pods
echo "Checking pods..."
POD_COUNT=$(kubectl get pods --no-headers | wc -l)
READY_PODS=$(kubectl get pods --no-headers | grep -c "Running")

if [ "$POD_COUNT" -gt 0 ] && [ "$POD_COUNT" -eq "$READY_PODS" ]; then
    echo "✓ All pods are running ($READY_PODS/$POD_COUNT)"
else
    echo "✗ Not all pods are running"
    kubectl get pods
    exit 1
fi

# Test health endpoints
echo "Testing health endpoints..."
kubectl port-forward svc/todo-backend 8000:80 > /dev/null 2>&1 &
PORT_FORWARD_PID=$!
sleep 5

HEALTH_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health 2>/dev/null)
kill $PORT_FORWARD_PID 2>/dev/null

if [ "$HEALTH_STATUS" -eq 200 ]; then
    echo "✓ Health endpoint accessible (Status: $HEALTH_STATUS)"
else
    echo "✗ Health endpoint not accessible (Status: $HEALTH_STATUS)"
    exit 1
fi

echo "✓ All validations passed!"
echo "Deployment validation completed successfully."
```

## Performance Validation

### 1. Resource Utilization

Monitor resource usage:

```bash
# Check resource requests and limits
kubectl top pods
kubectl describe deployment todo-frontend
kubectl describe deployment todo-backend

# Monitor over time
kubectl top pods -w
```

### 2. Response Time Testing

Test application response times:

```bash
# Test response times
time curl -s http://localhost:3000 > /dev/null
time curl -s http://localhost:8000/health > /dev/null
```

Expected results:
- Response times under 2 seconds
- Consistent performance
- No timeouts

## Security Validation

### 1. Security Context

Verify security configurations:

```bash
# Check security contexts
kubectl describe pod -l app.kubernetes.io/name=todo-frontend
kubectl describe pod -l app.kubernetes.io/name=todo-backend

# Check for non-root users
kubectl exec -it -l app.kubernetes.io/name=todo-frontend -- ps aux
kubectl exec -it -l app.kubernetes.io/name=todo-backend -- ps aux
```

### 2. Network Policies

Verify network security:

```bash
# Check network policies
kubectl get networkpolicies
kubectl describe networkpolicy <policy-name>
```

## Rollback Validation

Test rollback procedures:

```bash
# Simulate rollback
helm rollback todo-frontend 1
helm rollback todo-backend 1

# Validate rollback success
kubectl get deployments
kubectl get pods
```

## Success Criteria

### Functional Validation
- **[T043]** Frontend application is accessible via Minikube service within 5 minutes of Helm installation
- **[T044]** Backend API is reachable and serving requests within 5 minutes of Helm installation
- **[T045]** Todo Chatbot functionality works identically to pre-deployment state
- **[T046]** Helm install and upgrade operations complete successfully without errors

### Technical Validation
- All pods in Running status
- Services properly configured and accessible
- Health checks passing
- Resource limits respected
- Security contexts applied

### Performance Validation
- Response times acceptable
- Resource utilization within limits
- No performance degradation from pre-deployment state

## Troubleshooting Checklist

### Common Validation Issues

1. **Pods not starting**
   - Check logs: `kubectl logs -l app=todo-frontend`
   - Check events: `kubectl get events --sort-by='.lastTimestamp'`
   - Check resources: `kubectl describe pod <pod-name>`

2. **Services not accessible**
   - Check endpoints: `kubectl get endpoints todo-frontend`
   - Check service configuration: `kubectl describe service todo-frontend`
   - Test internal connectivity: `kubectl exec -it <pod> -- nslookup todo-frontend`

3. **Application functionality broken**
   - Check API responses: `curl -v http://localhost:8000/health`
   - Verify environment variables: `kubectl describe deployment todo-backend`
   - Test database connectivity separately

### Validation Failure Procedures

1. Document the failure
2. Gather logs and diagnostic information
3. Attempt remediation steps
4. Retry validation
5. Escalate if necessary

## Continuous Validation

Set up continuous validation for production environments:

```yaml
# Continuous validation job
apiVersion: batch/v1
kind: Job
metadata:
  name: deployment-validation
spec:
  template:
    spec:
      containers:
      - name: validator
        image: curlimages/curl
        command:
        - /bin/sh
        - -c
        - |
          # Test frontend
          curl -f http://todo-frontend:80/health || exit 1
          # Test backend
          curl -f http://todo-backend:80/health || exit 1
          # Test functionality
          curl -f http://todo-backend:80/api/health || exit 1
          echo "Validation successful"
      restartPolicy: Never
  backoffLimit: 4
```

## Validation Reporting

Create validation reports for audit purposes:

```bash
# Generate validation report
echo "# Deployment Validation Report" > validation-report.md
echo "Date: $(date)" >> validation-report.md
echo "" >> validation-report.md
kubectl get pods >> validation-report.md
kubectl get services >> validation-report.md
kubectl get deployments >> validation-report.md
```

This validation guide ensures comprehensive testing of the Kubernetes deployment and helps maintain quality standards for the Todo App.