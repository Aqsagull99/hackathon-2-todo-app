# Kubernetes Health Probe Debugging Guide

## Common Probe Issues and Solutions

### 1. Startup Probe Failures

**Symptoms:**
- Pod stuck in "ContainerCreating" state
- Pod restarts repeatedly during startup
- "Startup probe failed" in pod events

**Diagnosis Commands:**
```bash
# Check pod events for startup issues
kubectl describe pod <pod-name> | grep -A 10 -B 10 "Startup\|Failed"

# Check if startup time exceeds probe limits
kubectl get pod <pod-name> -o yaml | grep -A 15 -B 5 startupProbe

# Monitor startup process in logs
kubectl logs <pod-name> --timestamps
```

**Solutions:**
- Increase `failureThreshold` to allow more time
- Increase `timeoutSeconds` for slow operations
- Use `exec` probe instead of `httpGet` for complex checks
- Optimize application startup time

### 2. Liveness Probe Failures

**Symptoms:**
- Pod restarts unexpectedly
- "Liveness probe failed" in pod events
- Application appears healthy but gets restarted

**Diagnosis Commands:**
```bash
# Check liveness probe events
kubectl describe pod <pod-name> | grep -A 10 -B 10 "Liveness\|Killing\|Restarted"

# Verify probe configuration
kubectl get pod <pod-name> -o jsonpath='{.spec.containers[0].livenessProbe}'

# Monitor application during probe failures
kubectl logs <pod-name> --since=5m

# Check resource usage during failures
kubectl top pod <pod-name>
```

**Solutions:**
- Increase `timeoutSeconds` for slow operations
- Increase `periodSeconds` to reduce frequency
- Increase `failureThreshold` for more tolerance
- Optimize application health check endpoint
- Address resource constraints causing slowness

### 3. Readiness Probe Failures

**Symptoms:**
- Pod not receiving traffic despite being healthy
- Service endpoints don't include the pod
- "Readiness probe failed" in events

**Diagnosis Commands:**
```bash
# Check readiness status
kubectl get pod <pod-name> -o jsonpath='{.status.conditions[?(@.type=="Ready")]}'

# Check endpoints
kubectl get endpoints <service-name>

# Check readiness probe events
kubectl describe pod <pod-name> | grep -A 10 -B 10 "Readiness\|NotReady"

# Monitor service connectivity
kubectl get svc <service-name> -o wide
```

**Solutions:**
- Adjust `initialDelaySeconds` for proper initialization
- Increase `timeoutSeconds` for slow startups
- Modify application logic to return ready status properly
- Check dependencies (databases, caches, etc.) that affect readiness

## Advanced Debugging Techniques

### 1. Simulate Probe Behavior

```bash
# Port forward to test probe endpoints
kubectl port-forward <pod-name> 8080:8080

# Test probe endpoints manually
curl -v http://localhost:8080/healthz
curl -v http://localhost:8080/readyz
curl -v http://localhost:8080/startup

# Check response time
time curl -s http://localhost:8080/healthz
```

### 2. Monitor Resource Impact

```bash
# Monitor CPU/Memory during probe execution
kubectl top pod <pod-name> --containers

# Check if probes cause resource spikes
kubectl top nodes

# Monitor application resource usage during startup
kubectl describe pod <pod-name> | grep -A 20 -B 5 "resources\|limits\|requests"
```

### 3. Check Network Connectivity

```bash
# Test internal connectivity
kubectl exec <pod-name> -- nc -zv localhost 8080

# Test from other pods in the same namespace
kubectl run debug --image=curlimages/curl -it --rm -- curl -v http://<pod-ip>:8080/healthz

# Check service network policies
kubectl get networkpolicy
```

## AI/ML Workload Specific Debugging

### 1. Model Loading Issues
For applications with heavy model loading:

```bash
# Check model loading status
kubectl exec <pod-name> -- ls -la /models/

# Monitor disk and memory during loading
kubectl exec <pod-name> -- df -h /models/
kubectl exec <pod-name> -- free -m

# Check if model loading is complete
kubectl exec <pod-name> -- test -f /app/model_loaded_flag && echo "Model loaded" || echo "Model not loaded"
```

### 2. GPU Resource Issues
For GPU-accelerated applications:

```bash
# Check GPU availability
kubectl describe node <node-name> | grep -i gpu

# Verify GPU resource requests/limits
kubectl get pod <pod-name> -o jsonpath='{.spec.containers[0].resources}'

# Check GPU utilization
kubectl exec <pod-name> -- nvidia-smi
```

## Probe Configuration Best Practices for Troubleshooting

### 1. Verbose Logging
Add logging to health check endpoints:

```yaml
# In your application, log probe requests
livenessProbe:
  httpGet:
    path: /healthz?debug=1  # Add debug parameter to trace requests
  initialDelaySeconds: 30
  periodSeconds: 10
```

### 2. Separate Health Check Endpoints
Use different endpoints for different concerns:

```yaml
# Different endpoints for different checks
startupProbe:
  httpGet:
    path: /startupz  # Check if app has started
readinessProbe:
  httpGet:
    path: /readyz    # Check if app is ready for traffic
livenessProbe:
  httpGet:
    path: /healthz   # Check if app is healthy overall
```

### 3. Gradual Rollout for Probe Changes
When updating probe configurations:

```bash
# 1. First, patch only one replica
kubectl patch deployment <deployment-name> -p '{"spec":{"replicas":1}}'

# 2. Verify probe changes work
kubectl get pods -l app=<app-label>

# 3. Scale back up if successful
kubectl patch deployment <deployment-name> -p '{"spec":{"replicas":<original-count>}}'
```

## Diagnostic Scripts

### 1. Probe Status Checker
Script to check probe status across all pods:

```bash
#!/bin/bash
# probe-status-checker.sh
NAMESPACE=${1:-default}

echo "Checking probe configurations for all pods in namespace: $NAMESPACE"
kubectl get pods -n $NAMESPACE --no-headers | awk '{print $1}' | while read pod; do
  echo "=== Pod: $pod ==="
  echo "Startup Probe:"
  kubectl get pod $pod -n $NAMESPACE -o jsonpath='{.spec.containers[0].startupProbe}' 2>/dev/null || echo "No startup probe configured"
  echo -e "\nLiveness Probe:"
  kubectl get pod $pod -n $NAMESPACE -o jsonpath='{.spec.containers[0].livenessProbe}' 2>/dev/null || echo "No liveness probe configured"
  echo -e "\nReadiness Probe:"
  kubectl get pod $pod -n $NAMESPACE -o jsonpath='{.spec.containers[0].readinessProbe}' 2>/dev/null || echo "No readiness probe configured"
  echo -e "\n"
done
```

### 2. Probe Failure Analyzer
Script to analyze recent probe failures:

```bash
#!/bin/bash
# probe-failure-analyzer.sh
NAMESPACE=${1:-default}

echo "Analyzing recent probe failures in namespace: $NAMESPACE"
kubectl get events -n $NAMESPACE --field-selector reason=Unhealthy,type=Warning --sort-by='.lastTimestamp'
```

## Quick Remediation Steps

When facing probe-related issues:

1. **Immediate**: Check `kubectl describe pod <pod-name>` for error details
2. **Verify**: Check probe configuration against application requirements
3. **Test**: Manually test probe endpoints using port-forward
4. **Adjust**: Increase timeouts/thresholds if application needs more time
5. **Monitor**: Watch pod behavior after changes
6. **Document**: Record the issue and solution for future reference