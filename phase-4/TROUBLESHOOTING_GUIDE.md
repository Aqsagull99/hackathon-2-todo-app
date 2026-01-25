# Kubernetes Deployment Troubleshooting Guide

## Overview

This guide provides comprehensive troubleshooting steps for common issues encountered during the Todo App Kubernetes deployment, particularly in cross-platform scenarios where development occurs in WSL while Kubernetes runs on Windows.

## Common Issues and Solutions

### 1. ImagePullBackOff Errors

**Symptoms:**
- Pods stuck in `ImagePullBackOff` state
- Error message: "Failed to pull image"
- Cannot find the specified image

**Root Causes:**
- Images not available in the target Docker registry
- Incorrect image names or tags
- Cross-platform image transfer issues

**Solutions:**

**For Minikube:**
```bash
# Load images into Minikube's Docker environment
minikube image load todo-backend:latest
minikube image load todo-frontend:latest

# Verify images are loaded
minikube ssh -- docker images | grep todo
```

**For Docker Desktop Kubernetes:**
```bash
# Ensure images are built in the same Docker context as Kubernetes
docker images | grep todo
# Images should appear in Docker Desktop UI
```

**Cross-platform transfer:**
```bash
# In WSL - save and transfer
docker save todo-backend:latest -o todo-backend.tar
cp todo-backend.tar /mnt/c/temp/
# In Windows - load
docker load -i C:\temp\todo-backend.tar
```

### 2. Cross-Platform Docker Context Issues

**Symptoms:**
- Images built in WSL not visible to Windows Kubernetes
- Conflicting Docker contexts
- Permission errors accessing Docker socket

**Solutions:**
```bash
# Check current Docker context
docker context ls

# For Minikube on Windows:
minikube docker-env
# Run the output command in Windows PowerShell/CMD
# Example: @FOR /f "tokens=*" %i IN ('minikube -p minikube docker-env') DO @%i

# For Docker Desktop on Windows:
# Ensure WSL integration is enabled in Docker Desktop settings
```

### 3. Network Connectivity Issues

**Symptoms:**
- Services not accessible from outside cluster
- Internal service discovery failing
- Connection timeouts between services

**Diagnosis:**
```bash
# Check service endpoints
kubectl get endpoints todo-frontend
kubectl get endpoints todo-backend

# Test internal connectivity
kubectl run test-pod --image=nicolaka/netshoot --rm -it --restart=Never -- bash
# Inside pod: dig todo-frontend.default.svc.cluster.local
# Inside pod: curl -v http://todo-frontend:80
kubectl delete pod test-pod
```

**Solutions:**
```bash
# Check service configuration
kubectl describe service todo-frontend
kubectl describe service todo-backend

# Verify pod networking
kubectl get pods -o wide
kubectl describe pod <pod-name>
```

### 4. Resource Limitation Issues

**Symptoms:**
- Pods stuck in `Pending` state
- Eviction notices in events
- High memory/CPU usage warnings

**Diagnosis:**
```bash
# Check node resources
kubectl describe nodes
kubectl top nodes
kubectl top pods

# Check for resource constraints
kubectl describe pod <pod-name>
kubectl get events --sort-by='.lastTimestamp'
```

**Solutions:**
```bash
# Increase Minikube resources
minikube delete
minikube start --cpus=4 --memory=8192 --disk-size=20g

# Adjust resource requests in Helm values
# Edit values.yaml to reduce requests/limits
```

### 5. Database Connection Issues

**Symptoms:**
- Backend pods failing to start
- Database connection errors in logs
- Authentication failures

**Diagnosis:**
```bash
# Check backend logs
kubectl logs -l app.kubernetes.io/name=todo-backend

# Test database connectivity from backend pod
kubectl exec -it -l app.kubernetes.io/name=todo-backend -- bash
# Inside pod: telnet postgres 5432
# Inside pod: env | grep DATABASE
```

**Solutions:**
```bash
# Verify database is running
kubectl get pods -l app=postgres
kubectl logs -l app=postgres

# Check secrets
kubectl get secrets
kubectl describe secret <secret-name>

# Verify environment variables in deployment
kubectl describe deployment todo-backend
```

### 6. Health Check Failures

**Symptoms:**
- Pods repeatedly restarting
- Liveness/readiness probes failing
- Applications appearing healthy but being marked as unhealthy

**Diagnosis:**
```bash
# Check pod status and events
kubectl describe pod -l app.kubernetes.io/name=todo-backend

# View application logs during startup
kubectl logs -l app.kubernetes.io/name=todo-backend --previous

# Check health endpoint accessibility
kubectl exec -it -l app.kubernetes.io/name=todo-backend -- curl localhost:8000/health
```

**Solutions:**
```bash
# Adjust health check timing in Helm values
# Increase initialDelaySeconds, timeoutSeconds, or failureThreshold

# Verify application startup time
# Some applications take longer to initialize
```

### 7. Cross-Platform Path Issues

**Symptoms:**
- Helm chart paths not found
- File access errors during deployment
- Mixed path separators causing issues

**Solutions:**
```bash
# Use forward slashes in Helm commands
helm install todo-backend ./phase-4/helm/todo-backend/ --namespace default

# Verify file paths exist
# On Windows: dir .\phase-4\helm\todo-backend\
# On WSL: ls -la ./phase-4/helm/todo-backend/
```

### 8. Authentication and Security Issues

**Symptoms:**
- Unauthorized access errors
- RBAC permission denials
- Secret decryption failures

**Diagnosis:**
```bash
# Check pod security context
kubectl describe pod <pod-name>

# Verify service account permissions
kubectl get serviceaccounts
kubectl describe serviceaccount <sa-name>

# Check RBAC bindings
kubectl get rolebindings,clusterrolebindings
```

**Solutions:**
```bash
# Verify secrets are properly formatted
kubectl get secrets <secret-name> -o yaml

# Check if service account has proper permissions
kubectl auth can-i '*' '*' --as=system:serviceaccount:default:<sa-name>
```

## Diagnostic Commands

### Comprehensive Status Check
```bash
# Get overall cluster status
kubectl cluster-info
kubectl get nodes
kubectl get cs

# Check all resources in namespace
kubectl get all -n default
kubectl get pv,pvc,sc
kubectl get ingress

# View recent events
kubectl get events --sort-by='.lastTimestamp' --field-selector type!=Normal
```

### Pod-Specific Diagnostics
```bash
# Get detailed pod information
kubectl describe pod <pod-name>
kubectl get pod <pod-name> -o yaml

# Check pod logs with timestamps
kubectl logs <pod-name> --timestamps
kubectl logs <pod-name> --previous

# Exec into problematic pod
kubectl exec -it <pod-name> -- /bin/sh
```

### Service and Network Diagnostics
```bash
# Check service configuration
kubectl describe service <service-name>
kubectl get endpoints <service-name>

# Test service connectivity from inside cluster
kubectl run debug --image=nicolaka/netshoot --rm -it --restart=Never -- bash
# Inside pod: nc -vz <service-name> <port>
# Inside pod: curl -v http://<service-name>:<port>
```

## AI-Assisted Troubleshooting

### Using kubectl-ai for Diagnostics
```bash
# Ask AI to identify issues
kubectl ai describe why pods are failing
kubectl ai show me unhealthy resources
kubectl ai explain recent errors in default namespace

# Get AI suggestions
kubectl ai suggest fixes for ImagePullBackOff
kubectl ai recommend solutions for pending pods
```

### Common AI Troubleshooting Patterns
```bash
# General problem identification
kubectl ai what's wrong with deployment todo-frontend

# Specific issue diagnosis
kubectl ai explain why pods are in CrashLoopBackOff
kubectl ai show me pods that are not ready

# Resource-related issues
kubectl ai check if there's enough memory for deployment
kubectl ai show resource usage in default namespace
```

## Prevention Strategies

### 1. Pre-deployment Validation
```bash
# Validate Helm charts
helm lint ./phase-4/helm/todo-frontend/
helm lint ./phase-4/helm/todo-backend/

# Template validation
helm template test-frontend ./phase-4/helm/todo-frontend/ --dry-run
helm template test-backend ./phase-4/helm/todo-backend/ --dry-run
```

### 2. Resource Planning
```bash
# Estimate resource requirements
kubectl create deployment temp --image=todo-backend:latest --dry-run=server -o yaml
# Analyze the output for resource estimates
```

### 3. Cross-Platform Validation
```bash
# Verify image availability before deployment
# WSL: docker images | grep todo
# Windows: docker images | findstr todo
# Minikube: minikube ssh -- docker images | grep todo
```

## Recovery Procedures

### 1. Partial Rollback
```bash
# Rollback specific deployment
kubectl rollout undo deployment/todo-frontend
kubectl rollout undo deployment/todo-backend

# Rollback to specific revision
kubectl rollout undo deployment/todo-frontend --to-revision=1
```

### 2. Force Restart
```bash
# Restart all pods in deployment
kubectl rollout restart deployment/todo-frontend
kubectl rollout restart deployment/todo-backend

# Delete specific pods to force recreation
kubectl delete pod -l app.kubernetes.io/name=todo-frontend
```

### 3. Emergency Cleanup
```bash
# Uninstall problematic releases
helm uninstall todo-frontend
helm uninstall todo-backend

# Clean up leftover resources
kubectl delete pvc --all
kubectl delete secret -l app=todo-app
```

## Monitoring and Alerting

### Set up basic monitoring
```yaml
# Simple monitoring job
apiVersion: batch/v1
kind: Job
metadata:
  name: health-check-job
spec:
  template:
    spec:
      containers:
      - name: health-checker
        image: curlimages/curl
        command:
        - /bin/sh
        - -c
        - |
          # Test frontend
          if ! curl -f http://todo-frontend:80/health; then
            echo "Frontend health check failed"
            exit 1
          fi
          # Test backend
          if ! curl -f http://todo-backend:80/health; then
            echo "Backend health check failed"
            exit 1
          fi
          echo "Health checks passed"
      restartPolicy: Never
```

## Quick Reference

### Most Common Fixes

1. **Image not found**: `minikube image load <image-name>`
2. **Pod stuck in Pending**: Check node resources with `kubectl describe nodes`
3. **Service not accessible**: Check endpoints with `kubectl get endpoints <service-name>`
4. **App not responding**: Check health probes and startup time in deployment
5. **Database connection**: Verify secrets and environment variables

### Essential Commands
```bash
# Quick status
kubectl get pods,svc,deployments
kubectl describe pod <problematic-pod>
kubectl logs <pod-name>

# Quick fixes
kubectl delete pod <pod-name>  # Force restart
kubectl rollout restart deployment/<name>
kubectl scale deployment/<name> --replicas=0 && kubectl scale deployment/<name> --replicas=1
```

## When to Seek Help

Contact support or escalate when:
- Issues persist after trying all documented solutions
- Critical security vulnerabilities discovered
- Data loss or corruption suspected
- Performance significantly below baseline expectations
- Cross-platform integration issues beyond scope of this guide