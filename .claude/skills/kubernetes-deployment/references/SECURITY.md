# Kubernetes Security Best Practices

This document outlines security best practices for Kubernetes deployments, particularly for production environments.

## Pod Security Standards

### Configure Pod Security Admission
Apply Pod Security Standards to namespaces:

```bash
# Enforce baseline security standard
kubectl label --overwrite namespace production \
  pod-security.kubernetes.io/enforce=baseline \
  pod-security.kubernetes.io/enforce-version=latest

# Warn for restricted standard
kubectl label --overwrite namespace production \
  pod-security.kubernetes.io/warn=restricted \
  pod-security.kubernetes.io/warn-version=latest

# Audit for restricted standard
kubectl label --overwrite namespace production \
  pod-security.kubernetes.io/audit=restricted \
  pod-security.kubernetes.io/audit-version=latest
```

### Pod Security Configuration
Configure Pod Security Admission in cluster:

```yaml
apiVersion: apiserver.config.k8s.io/v1
kind: AdmissionConfiguration
plugins:
- name: PodSecurity
  configuration:
    apiVersion: pod-security.admission.config.k8s.io/v1
    kind: PodSecurityConfiguration
    defaults:
      enforce: "restricted"
      enforce-version: "latest"
      audit: "restricted"
      audit-version: "latest"
      warn: "baseline"
      warn-version: "latest"
    exemptions:
      usernames: []
      runtimeClasses: []
      namespaces: ["kube-system"]
```

## Security Context Configuration

### Pod Security Context
Set security context at the pod level:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secure-pod
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    runAsGroup: 3000
    fsGroup: 2000
  containers:
  - name: app
    image: my-app:latest
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      runAsNonRoot: true
      capabilities:
        drop:
        - ALL
```

### Container Security Context
Apply security context to individual containers:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: secure-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: secure-app
  template:
    metadata:
      labels:
        app: secure-app
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 2000
      containers:
      - name: secure-app
        image: my-image:latest
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          runAsNonRoot: true
          runAsUser: 1000
          capabilities:
            drop:
            - ALL
            add:
            - NET_BIND_SERVICE
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: "64Mi"
            cpu: "250m"
          limits:
            memory: "128Mi"
            cpu: "500m"
```

### Secure Resource Management
Proper resource management is also a security consideration to prevent resource exhaustion attacks:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secure-resource-pod
spec:
  containers:
  - name: secure-app
    image: my-app:latest
    resources:
      requests:
        memory: "128Mi"
        cpu: "250m"
      limits:
        memory: "512Mi"
        cpu: "500m"
    # Additional security context for resource management
    securityContext:
      allowPrivilegeEscalation: false
      # Prevent fork bombs by limiting processes
      capabilities:
        drop:
        - ALL
    # Prevent resource exhaustion by limiting file descriptors
    env:
    - name: GOMAXPROCS
      valueFrom:
        resourceFieldRef:
          resource: limits.cpu
    - name: GOMEMLIMIT
      valueFrom:
        resourceFieldRef:
          resource: limits.memory
```

## Network Security

### Network Policies
Implement network policies to restrict traffic:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: frontend-netpol
spec:
  podSelector:
    matchLabels:
      app: frontend
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: proxy
    ports:
    - protocol: TCP
      port: 8080
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          name: backend
    ports:
    - protocol: TCP
      port: 3306
```

### Isolate Critical Applications
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-dns
spec:
  podSelector: {}
  policyTypes:
  - Egress
  egress:
  - ports:
    - protocol: UDP
      port: 53
    - protocol: TCP
      port: 53
```

## RBAC Best Practices

### Least Privilege RBAC
Create roles with minimal required permissions:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: production
  name: pod-viewer
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list", "watch"]
- apiGroups: [""]
  resources: ["pods/log"]
  verbs: ["get"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: read-pods
  namespace: production
subjects:
- kind: ServiceAccount
  name: my-app
  namespace: production
roleRef:
  kind: Role
  name: pod-viewer
  apiGroup: rbac.authorization.k8s.io
```

### Cluster Role for Cluster-Wide Resources
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: node-monitor
rules:
- apiGroups: [""]
  resources: ["nodes"]
  verbs: ["get", "list", "watch"]
- apiGroups: [""]
  resources: ["nodes/proxy"]
  verbs: ["get"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: monitor-nodes
subjects:
- kind: ServiceAccount
  name: node-monitor
  namespace: monitoring
roleRef:
  kind: ClusterRole
  name: node-monitor
  apiGroup: rbac.authorization.k8s.io
```

## Secrets Management

### Use Kubernetes Secrets
Store sensitive information securely:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: db-secret
type: Opaque
data:
  username: YWRtaW4=  # base64 encoded
  password: MWYyZDFlMmU2N2Rm  # base64 encoded
---
apiVersion: v1
kind: Pod
metadata:
  name: secret-test-pod
spec:
  containers:
  - name: test-container
    image: nginx
    env:
    - name: DB_USERNAME
      valueFrom:
        secretKeyRef:
          name: db-secret
          key: username
    - name: DB_PASSWORD
      valueFrom:
        secretKeyRef:
          name: db-secret
          key: password
    volumeMounts:
    - name: secret-volume
      mountPath: /etc/secret-volume
      readOnly: true
  volumes:
  - name: secret-volume
    secret:
      secretName: db-secret
```

### Use External Secrets
For production environments, use external secret stores:

```yaml
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: vault-backend
spec:
  provider:
    vault:
      server: "https://vault.example.com"
      path: "secret"
      version: "v2"
      auth:
        kubernetes:
          mountPath: "kubernetes"
          role: "external-secrets"
---
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: db-credentials
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: vault-backend
    kind: SecretStore
  target:
    name: db-credentials
  data:
  - secretKey: username
    remoteRef:
      key: database
      property: username
  - secretKey: password
    remoteRef:
      key: database
      property: password
```

## Image Security

### Use Trusted Images
Always use verified and trusted base images:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: secure-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: secure-app
  template:
    metadata:
      labels:
        app: secure-app
    spec:
      containers:
      - name: secure-app
        image: nginx:1.21.6-alpine  # Pin to specific version
        imagePullPolicy: IfNotPresent
```

### Image Pull Secrets
Configure image pull secrets for private registries:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: regcred
type: kubernetes.io/dockerconfigjson
data:
  .dockerconfigjson: <base64-encoded-docker-config>
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: private-app
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: private-app
        image: my-private-registry/my-app:latest
      imagePullSecrets:
      - name: regcred
```

## Security Scanning and Monitoring

### Implement Security Scanning
Use tools like Trivy or Clair to scan images:

```bash
# Scan image with Trivy
trivy image my-registry/my-app:latest

# Scan Kubernetes manifests
trivy config --security-checks config .
```

### Runtime Security Monitoring
Deploy runtime security monitoring tools:

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: falco-daemonset
spec:
  selector:
    matchLabels:
      app: falco
  template:
    metadata:
      labels:
        app: falco
    spec:
      hostPID: true
      hostNetwork: true
      containers:
      - name: falco
        image: falcosecurity/falco:latest
        securityContext:
          privileged: true
        volumeMounts:
        - mountPath: /host/var/run/docker.sock
          name: docker-sock
          readOnly: true
        - mountPath: /host/proc
          name: proc-fs
          readOnly: true
      volumes:
      - name: docker-sock
        hostPath:
          path: /var/run/docker.sock
      - name: proc-fs
        hostPath:
          path: /proc
```

## Security Hardening Checklist

- [ ] Verify secure cluster access: Check kubectl configuration doesn't expose credentials
- [ ] Configure Pod Security Standards
- [ ] Set non-root user in containers
- [ ] Drop unnecessary capabilities
- [ ] Enable read-only root filesystem
- [ ] Configure network policies
- [ ] Implement RBAC with least privilege
- [ ] Use secrets for sensitive data
- [ ] Pin image versions
- [ ] Configure image pull secrets
- [ ] Enable audit logging
- [ ] Implement runtime security monitoring
- [ ] Regular security scanning of images and configurations
- [ ] Secure API server configuration (TLS, authentication, authorization)
- [ ] Protect etcd with TLS and access controls
- [ ] Enable leader election with secure lease API
- [ ] Configure secure reconciliation loop (watch timeouts, rate limiting)
- [ ] Secure kubeconfig files with proper permissions (chmod 600)
- [ ] Use context isolation for different environments (dev, staging, prod)

## Reconciliation Loop Security Considerations

### API Server Security
The reconciliation loop depends heavily on the API server, so securing it is critical:

```yaml
# Secure API server configuration
apiVersion: kubeadm.k8s.io/v1beta3
kind: ClusterConfiguration
apiServer:
  extraArgs:
    # Authentication and authorization
    enable-admission-plugins: "AlwaysPullImages,DenyEscalatingExec,NodeRestriction"
    # TLS configuration
    tls-cert-file: "/etc/kubernetes/pki/apiserver.crt"
    tls-private-key-file: "/etc/kubernetes/pki/apiserver.key"
    # Audit logging
    audit-log-path: "/var/log/kubernetes/audit.log"
    audit-log-maxage: "30"
    audit-log-maxbackup: "10"
    audit-log-maxsize: "100"
    # Rate limiting to prevent abuse
    max-requests-inflight: "400"
    max-mutating-requests-inflight: "200"
```

### Controller Security
Secure controller components that participate in the reconciliation loop:

```yaml
# Secure controller manager configuration
apiVersion: kubeadm.k8s.io/v1beta3
kind: ClusterConfiguration
controllerManager:
  extraArgs:
    # Secure leader election
    leader-elect: "true"
    leader-elect-resource-lock: "leases"
    # Secure service account tokens
    use-service-account-credentials: "true"
    # Secure cloud provider integration
    configure-cloud-routes: "false"  # Only if not using cloud provider routes
```

### Watch Mechanism Security
Secure the watch mechanisms used in reconciliation:

```yaml
# Configure secure watch timeouts and resource limits
apiVersion: v1
kind: ConfigMap
metadata:
  name: secure-watch-config
  namespace: kube-system
data:
  # Configure reasonable timeouts for watches
  watch-timeout-seconds: "600"
  # Limit resources consumed by watches
  max-watch-events-per-second: "1000"
  # Secure resource version tracking
  secure-resource-version-checks: "true"
```

### Reconciliation Loop Security Patterns

#### 1. Secure Resource Validation
Always validate resources before processing in custom controllers:

```go
// Example secure validation in a custom controller
func (r *MyAppReconciler) validateResource(instance *myappv1.MyApp) error {
    // Validate resource ownership
    if instance.OwnerReferences == nil {
        return errors.New("resource must have owner references")
    }

    // Validate resource limits
    if instance.Spec.Resources.Limits.Memory().Value() == 0 {
        return errors.New("memory limit must be specified")
    }

    // Validate security context
    if instance.Spec.SecurityContext == nil {
        return errors.New("security context must be specified")
    }

    return nil
}
```

#### 2. Secure State Transitions
Implement secure state transition logic:

```yaml
# Example: Secure state management in a custom resource
apiVersion: myapp.example.com/v1
kind: MyApp
metadata:
  name: secure-app
spec:
  replicas: 3
  image: myapp:latest
  # Explicit security configuration
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    fsGroup: 2000
  # Explicit resource configuration
  resources:
    requests:
      memory: "64Mi"
      cpu: "250m"
    limits:
      memory: "128Mi"
      cpu: "500m"
status:
  # Secure status updates only through reconciliation loop
  phase: Pending  # Valid values: Pending, Running, Failed, Terminated
  conditions:
    - type: Ready
      status: "False"
      reason: "Initializing"
      message: "Resource is initializing"
```

## Secure Deployment Update Strategies

### Secure Rolling Updates
Implement security-aware deployment updates:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: secure-app
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
      maxSurge: 1
  selector:
    matchLabels:
      app: secure-app
  template:
    metadata:
      labels:
        app: secure-app
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 2000
      containers:
      - name: secure-app
        image: my-image:latest
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          runAsNonRoot: true
          runAsUser: 1000
          capabilities:
            drop:
            - ALL
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: "64Mi"
            cpu: "250m"
          limits:
            memory: "128Mi"
            cpu: "500m"
        # Security-focused health checks
        livenessProbe:
          httpGet:
            path: /healthz
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /readyz
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
```

### Secure Rollback Procedures
Follow security best practices when rolling back deployments:

```bash
# Always verify the image signatures before rollback
kubectl rollout history deployment/secure-app --revision=2

# Check the deployment manifest before undoing
kubectl get deployment secure-app --revision=2 -o yaml

# Perform the rollback
kubectl rollout undo deployment/secure-app --to-revision=2

# Verify the rollback security posture
kubectl describe deployment secure-app
kubectl get pods -l app=secure-app -o yaml
```

### Image Security During Updates
Maintain security during deployment updates:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: secure-update-app
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: "10%"  # Conservative for security-sensitive apps
      maxSurge: "10%"
  selector:
    matchLabels:
      app: secure-update-app
  template:
    metadata:
      labels:
        app: secure-update-app
    spec:
      containers:
      - name: secure-app
        image: my-image:latest  # Always use specific version tags in production
        imagePullPolicy: IfNotPresent  # Prevent pulling unsigned images
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          runAsNonRoot: true
          runAsUser: 1000
          capabilities:
            drop:
            - ALL
        resources:
          requests:
            memory: "128Mi"
            cpu: "250m"
          limits:
            memory: "256Mi"
            cpu: "500m"
```

### Monitoring Secure Rollouts
Track security aspects during deployment updates:

```bash
# Monitor for security policy violations during rollout
kubectl get events --field-selector involvedObject.name=secure-app --sort-by='.lastTimestamp'

# Check for pods that violate security policies
kubectl get pods -l app=secure-app -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.securityContext}{"\n"}'

# Verify that all pods are running with proper security context
kubectl describe rs -l app=secure-app
```

### Secure Service Configuration
Configure Services with security best practices:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: secure-service
spec:
  # Use ClusterIP for internal services (default)
  type: ClusterIP
  # Ensure proper label selectors to prevent unauthorized pod access
  selector:
    app: secure-app
    environment: production
    security-level: high
  ports:
  - name: https
    port: 443
    targetPort: 8443
    protocol: TCP
  # Enable session affinity only when necessary
  sessionAffinity: None  # Default, more secure
  # Restrict load balancer access for external services
  loadBalancerSourceRanges:
  - 10.0.0.0/8
  - 192.168.0.0/16
  # Do not expose services unnecessarily
  externalTrafficPolicy: Cluster  # Default, more secure
```

### Secure DNS Configuration
Protect service discovery mechanisms:

```bash
# Use secure DNS resolution patterns
# Verify DNS resolution works as expected
kubectl exec -it <secure-pod> -- nslookup secure-service.secure-namespace.svc.cluster.local

# Monitor DNS queries for anomalies
kubectl logs -n kube-system -l k8s-app=kube-dns

# Restrict DNS access with network policies
kubectl get networkpolicy -A
```

### Service Endpoint Security
Secure service endpoints and connectivity:

```bash
# Verify service endpoints match expectations
kubectl get endpoints secure-service -o yaml

# Check for unexpected pod access to services
kubectl get pods --show-labels -l app=secure-app

# Monitor service connectivity for suspicious patterns
kubectl get endpointslices -l kubernetes.io/service-name=secure-service

# Use network policies to restrict service access
kubectl describe networkpolicy service-access-policy
```

### Namespace Security and Resource Isolation
Secure namespace resource management and isolation:

```yaml
# ResourceQuota with security-focused limits
apiVersion: v1
kind: ResourceQuota
metadata:
  name: secure-quota
  namespace: secure-app
spec:
  hard:
    # Prevent resource exhaustion attacks
    requests.cpu: "2"
    limits.cpu: "4"
    requests.memory: 4Gi
    limits.memory: 8Gi
    # Limit object creation to prevent namespace pollution
    pods: "10"
    configmaps: "5"
    secrets: "10"
    services: "5"
    # Prevent creation of privileged services
    services.nodeports: "0"  # Disallow NodePort services
---
# LimitRange with security-focused defaults
apiVersion: v1
kind: LimitRange
metadata:
  name: secure-limits
  namespace: secure-app
spec:
  limits:
  - type: Container
    # Prevent containers from requesting excessive resources
    max:
      cpu: "500m"
      memory: 1Gi
    min:
      cpu: "10m"
      memory: 10Mi
    # Set secure defaults
    default:
      cpu: "100m"
      memory: 128Mi
    defaultRequest:
      cpu: "50m"
      memory: 64Mi
    # Prevent excessive ratio between limits and requests
    maxLimitRequestRatio:
      cpu: "2"
      memory: "2"
---
# Namespace with security labels and annotations
apiVersion: v1
kind: Namespace
metadata:
  name: secure-app
  labels:
    environment: production
    security-level: high
    team: secure-team
  annotations:
    description: "Secure application namespace with resource restrictions"
    owner: "security-team@example.com"
    security-classification: "high"
    compliance: "SOC2,PCI-DSS"
```

### Secure Configuration Management
Best practices for secure ConfigMap and Secret management:

```yaml
# Secure ConfigMap with validation
apiVersion: v1
kind: ConfigMap
metadata:
  name: secure-app-config
  namespace: secure-app
  labels:
    app: secure-app
    security-level: high
  annotations:
    description: "Configuration for secure application"
    security.classification: "public"  # Non-sensitive configuration
data:
  LOG_LEVEL: "info"
  API_TIMEOUT: "30s"
  FEATURE_FLAGS: "enabled"
---
# Secure Secret with sensitive data
apiVersion: v1
kind: Secret
metadata:
  name: secure-app-secrets
  namespace: secure-app
  labels:
    app: secure-app
    security-level: high
  annotations:
    description: "Sensitive configuration for secure application"
    security.classification: "confidential"  # Sensitive data
type: Opaque
data:
  # Base64 encoded sensitive values
  DATABASE_PASSWORD: <base64-encoded-password>
  API_KEY: <base64-encoded-api-key>
  ENCRYPTION_KEY: <base64-encoded-key>
---
# Secure Pod with proper volume mounts and security context
apiVersion: v1
kind: Pod
metadata:
  name: secure-app-pod
  namespace: secure-app
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    fsGroup: 2000
  containers:
  - name: secure-app
    image: my-app:latest
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      runAsNonRoot: true
      runAsUser: 1000
      capabilities:
        drop:
        - ALL
    # Mount secrets as volumes instead of environment variables
    volumeMounts:
    - name: config-volume
      mountPath: /etc/config
      readOnly: true
    - name: secrets-volume
      mountPath: /etc/secrets
      readOnly: true
      # Mount specific secret items with restrictive permissions
    env:
    # Use valueFrom for specific config values
    - name: LOG_LEVEL
      valueFrom:
        configMapKeyRef:
          name: secure-app-config
          key: LOG_LEVEL
  volumes:
  - name: config-volume
    configMap:
      name: secure-app-config
  - name: secrets-volume
    secret:
      secretName: secure-app-secrets
      defaultMode: 256  # 0400 in octal - readable only by owner
```

### Configuration Security Best Practices
Secure practices for ConfigMap and Secret usage:

```bash
# 1. Verify ConfigMap and Secret permissions
kubectl get secrets -n secure-app -o yaml
kubectl get configmaps -n secure-app -o yaml

# 2. Check for sensitive data in ConfigMaps (should be in Secrets)
kubectl get configmaps -n secure-app -o yaml | grep -i "password\|key\|token"

# 3. Verify that secrets are mounted as volumes, not environment variables
kubectl describe pod secure-app-pod -n secure-app

# 4. Check that pods don't have excessive privileges
kubectl describe pod secure-app-pod -n secure-app | grep -i "privileged\|root"

# 5. Verify encryption at rest configuration
kubectl get encryptionconfig -o yaml

# 6. Review RBAC permissions for secret access
kubectl auth can-i get secrets -n secure-app --as=system:serviceaccount:secure-app:app-sa
```

### Secure Debugging and Resource Management
Best practices for secure debugging and resource management:

```bash
# 1. Use secure debugging practices
# Avoid using privileged debugging pods
kubectl debug <pod-name> -it --image=nicolaka/netshoot --copy-to=<secure-debug-pod>

# 2. Limit debug access with RBAC
kubectl auth can-i create pods --subresource=debug

# 3. Verify QoS class assignments don't compromise security
kubectl describe pod <pod-name> | grep -i "qos"

# 4. Check resource limits prevent DoS attacks
kubectl describe pod <pod-name> | grep -A 10 "Resources"

# 5. Validate that critical pods have Guaranteed QoS when needed
kubectl get pod <critical-pod> -o jsonpath='{.status.qosClass}'

# 6. Monitor for pods with excessive resource requests
kubectl top pods --containers
```

```yaml
# Secure resource configuration with appropriate QoS
apiVersion: v1
kind: Pod
metadata:
  name: secure-critical-pod
  namespace: secure-app
spec:
  containers:
  - name: secure-app
    image: my-app:latest
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      runAsNonRoot: true
      runAsUser: 1000
      capabilities:
        drop:
        - ALL
    # Use Guaranteed QoS for critical applications
    resources:
      requests:
        memory: "1Gi"
        cpu: "1000m"
      limits:
        memory: "1Gi"  # Equal to requests for Guaranteed QoS
        cpu: "1000m"   # Equal to requests for Guaranteed QoS
    # Security-focused health checks
    livenessProbe:
      httpGet:
        path: /healthz
        port: 8080
      initialDelaySeconds: 30
      periodSeconds: 10
      timeoutSeconds: 5
      failureThreshold: 3
    readinessProbe:
      httpGet:
        path: /readyz
        port: 8080
      initialDelaySeconds: 5
      periodSeconds: 5
      timeoutSeconds: 3
      failureThreshold: 3
```

### Secure HPA Configuration
Best practices for secure Horizontal Pod Autoscaler configuration:

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: secure-hpa
  namespace: secure-app
  labels:
    app: secure-app
    security-level: high
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: secure-app
  minReplicas: 2  # Prevent resource exhaustion attacks with appropriate min
  maxReplicas: 10 # Prevent resource exhaustion with reasonable max
  metrics:
  # Use secure resource metrics
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  # Validate custom metrics come from trusted sources
  - type: Pods
    pods:
      metric:
        name: requests-per-second
        selector:
          matchLabels:
            trusted: "true"  # Only trust metrics from trusted sources
      target:
        type: AverageValue
        averageValue: "1k"
  behavior:
    # Configure secure scaling behavior to prevent DoS
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      # Limit scale-down rate to prevent service disruption
      - type: Percent
        value: 10
        periodSeconds: 60
    scaleUp:
      # Limit scale-up rate to prevent resource exhaustion
      stabilizationWindowSeconds: 30
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
      - type: Pods
        value: 4
        periodSeconds: 60
      selectPolicy: Max
```

### Batch Workload Security Considerations
Secure practices for Job and CronJob configurations:

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: secure-batch-job
  namespace: secure-namespace
  labels:
    app: secure-batch-job
    security-level: high
spec:
  completions: 1
  parallelism: 1
  backoffLimit: 3
  # Security context for the job
  template:
    metadata:
      labels:
        app: secure-batch-job
    spec:
      # Security context for the pod
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 2000
        seccompProfile:
          type: RuntimeDefault
      restartPolicy: Never
      containers:
      - name: secure-batch-processor
        image: secure-batch-image:latest
        # Container security context
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          runAsNonRoot: true
          runAsUser: 1000
          capabilities:
            drop:
            - ALL
            add:
            - SETPCAP  # Only add minimal required capabilities
        command: ["/bin/sh", "-c"]
        args:
        - |
          # Validate inputs before processing
          if [ ! -f "/input/data.txt" ]; then
            echo "ERROR: Input file not found"
            exit 1
          fi

          # Process data securely
          /app/secure_processor --input /input/data.txt --output /output/results.txt
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        volumeMounts:
        - name: secure-input
          mountPath: /input
          readOnly: true
        - name: secure-output
          mountPath: /output
      volumes:
      - name: secure-input
        persistentVolumeClaim:
          claimName: secure-input-pvc
      - name: secure-output
        persistentVolumeClaim:
          claimName: secure-output-pvc
---
# Secure CronJob with proper security context
apiVersion: batch/v1
kind: CronJob
metadata:
  name: secure-cronjob
  namespace: secure-namespace
  labels:
    app: secure-cronjob
    security-level: high
spec:
  schedule: "0 2 * * *"  # Daily at 2 AM
  concurrencyPolicy: Forbid  # Prevent concurrent runs that might conflict
  # Security configuration for scheduled jobs
  jobTemplate:
    spec:
      template:
        spec:
          # Restrict security context
          securityContext:
            runAsNonRoot: true
            runAsUser: 1000
            fsGroup: 2000
            seccompProfile:
              type: RuntimeDefault
          restartPolicy: Never
          containers:
          - name: secure-scheduled-processor
            image: secure-scheduled-image:latest
            securityContext:
              allowPrivilegeEscalation: false
              readOnlyRootFilesystem: true
              runAsNonRoot: true
              runAsUser: 1000
              capabilities:
                drop:
                - ALL
            env:
            # Use secret for sensitive configuration
            - name: API_TOKEN
              valueFrom:
                secretKeyRef:
                  name: secure-api-credentials
                  key: token
            command: ["/bin/sh", "-c"]
            args:
            - |
              # Verify current date before processing
              DATE=$(date +%Y-%m-%d)
              echo "Starting scheduled processing for $DATE"

              # Perform secure processing
              /app/secure_scheduled_processor --date "$DATE"

              echo "Scheduled processing completed for $DATE"
            resources:
              requests:
                memory: "512Mi"
                cpu: "500m"
              limits:
                memory: "1Gi"
                cpu: "1000m"
---
# RBAC configuration for batch workload management
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: batch-workload-manager
  namespace: secure-namespace
rules:
# Allow managing jobs
- apiGroups: ["batch"]
  resources: ["jobs"]
  verbs: ["get", "list", "create", "update", "patch", "delete"]
# Allow managing cronjobs
- apiGroups: ["batch"]
  resources: ["cronjobs"]
  verbs: ["get", "list", "create", "update", "patch", "delete"]
# Allow managing pods (for job troubleshooting)
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list", "watch"]
# Allow viewing pod logs
- apiGroups: [""]
  resources: ["pods/log"]
  verbs: ["get", "list"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: batch-workload-manager-binding
  namespace: secure-namespace
subjects:
- kind: ServiceAccount
  name: batch-processor-sa
  namespace: secure-namespace
roleRef:
  kind: Role
  name: batch-workload-manager
  apiGroup: rbac.authorization.k8s.io
```

### Health Probe Security Considerations
Secure practices for health probe configuration:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: secure-probes-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: secure-probes-app
  template:
    metadata:
      labels:
        app: secure-probes-app
    spec:
      containers:
      - name: secure-app
        image: my-app:latest
        # Secure probe configuration
        livenessProbe:
          httpGet:
            path: /healthz  # Use secure health check endpoint
            port: 8080
            scheme: HTTPS   # Use HTTPS for probe endpoints when possible
            # Don't include sensitive headers in probes
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /readyz
            port: 8080
            scheme: HTTPS
          initialDelaySeconds: 5
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
        startupProbe:
          httpGet:
            path: /startupz
            port: 8080
            scheme: HTTPS
          initialDelaySeconds: 10
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 30  # Allow more time during startup
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          runAsNonRoot: true
          runAsUser: 1000
          capabilities:
            drop:
            - ALL
```

#### Secure Probe Endpoint Implementation
Implement secure health check endpoints in your application:

```bash
# Example of secure health check implementation (in application code)
# Don't expose sensitive information in health check responses
# Health check should be fast and not perform expensive operations

# GOOD - Secure health check endpoint
GET /healthz
Response: {"status": "healthy", "timestamp": "2023-10-27T10:00:00Z"}

# AVOID - Exposing sensitive information
GET /healthz
Response: {"status": "healthy", "db_connection": "mysql://admin:password@db:3306/app", "version": "1.2.3-exploit-me"}

# GOOD - Separate readiness endpoint
GET /readyz
Response: {"status": "ready", "dependencies": {"database": "connected", "cache": "ready"}}
```

#### Probe Security Verification
Verify probe security configuration:

```bash
# 1. Check that probe endpoints are not exposing sensitive information
kubectl exec <pod-name> -c <container-name> -- curl -s http://localhost:<port>/healthz

# 2. Verify that probe endpoints are protected with appropriate authentication if needed
kubectl exec <pod-name> -c <container-name> -- curl -s -w "Response code: %{response_code}\n" http://localhost:<port>/healthz

# 3. Check for probe endpoints that might be accessible externally
kubectl get svc <service-name> -o yaml | grep -A 10 -B 10 ports

# 4. Verify probe configurations don't use insecure schemes unnecessarily
kubectl get deployment <deployment-name> -o yaml | grep -A 20 -B 5 "livenessProbe\|readinessProbe\|startupProbe"
```

### AI-Assisted Development Security Considerations
Secure practices for using AI tools in Kubernetes manifest generation:

```bash
# 1. Validate AI-generated manifests before application
# Always review and validate AI-generated Kubernetes manifests
kubectl apply --dry-run=client -f ai-generated-manifest.yaml

# 2. Use validation tools to check AI-generated manifests
kubeval --strict ai-generated-manifest.yaml
kube-score score ai-generated-manifest.yaml

# 3. Check for security misconfigurations in AI-generated manifests
grep -i "privileged\|allowprivilegeescalation\|hostpath\|hostnetwork" ai-generated-manifest.yaml

# 4. Verify that AI-generated manifests don't expose sensitive information
grep -i "password\|secret\|token\|key" ai-generated-manifest.yaml

# 5. Ensure proper security contexts are applied in AI-generated manifests
grep -A 10 -B 5 "securityContext" ai-generated-manifest.yaml

# 6. Check that AI-generated manifests follow least-privilege principle
kubectl explain deployment.spec.template.spec.containers.securityContext --recursive | grep -E "(runAsNonRoot|runAsUser|allowPrivilegeEscalation|readOnlyRootFilesystem)"
```

#### Secure AI Prompt Engineering
Best practices for prompting AI tools for Kubernetes manifests:

```yaml
# GOOD: Secure prompt example
# Request: "Create a secure Deployment for nginx with proper security context, resource limits, and health checks"
apiVersion: apps/v1
kind: Deployment
metadata:
  name: secure-nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: secure-nginx
  template:
    metadata:
      labels:
        app: secure-nginx
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 2000
      containers:
      - name: nginx
        image: nginx:latest
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          runAsNonRoot: true
          runAsUser: 1000
          capabilities:
            drop:
            - ALL
        resources:
          requests:
            memory: "64Mi"
            cpu: "250m"
          limits:
            memory: "128Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /
            port: 80
        readinessProbe:
          httpGet:
            path: /
            port: 80
```

```yaml
# AVOID: Insecure prompt example
# Request: "Create a Deployment for nginx" (without security requirements)
# This may generate a manifest without proper security configurations
apiVersion: apps/v1
kind: Deployment
metadata:
  name: insecure-nginx  # This is what NOT to generate
spec:
  replicas: 3
  selector:
    matchLabels:
      app: insecure-nginx
  template:
    metadata:
      labels:
        app: insecure-nginx
    spec:
      # Missing securityContext entirely!
      containers:
      - name: nginx
        image: nginx:latest
        # Missing securityContext for container!
        # Missing resource limits!
        # Missing health checks!
```

### RBAC Security Best Practices
Secure practices for RBAC configuration:

```yaml
# Secure Role with minimal permissions
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: secure-app-role
  namespace: secure-app
  labels:
    app: secure-app
    security-level: high
rules:
# Allow only required permissions for application
- apiGroups: [""]
  resources: ["pods", "pods/log"]
  verbs: ["get", "list", "watch"]  # Read-only access
- apiGroups: [""]
  resources: ["configmaps"]
  verbs: ["get", "list"]  # Read-only access
- apiGroups: [""]
  resources: ["secrets"]
  verbs: ["get"]  # Minimal access to secrets
---
# Secure ServiceAccount with token management
apiVersion: v1
kind: ServiceAccount
metadata:
  name: secure-app-sa
  namespace: secure-app
  labels:
    app: secure-app
    security-level: high
automountServiceAccountToken: false  # Disable token mounting unless required
---
# Secure RoleBinding with specific subject
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: secure-app-rolebinding
  namespace: secure-app
  labels:
    app: secure-app
    security-level: high
subjects:
- kind: ServiceAccount
  name: secure-app-sa
  namespace: secure-app  # Explicit namespace to prevent cross-namespace access
roleRef:
  kind: Role
  name: secure-app-role
  apiGroup: rbac.authorization.k8s.io
```

### HPA Security Considerations
Secure practices for HPA configuration:

```bash
# 1. Verify HPA configurations don't allow unlimited scaling
kubectl get hpa -A -o yaml | grep -A 10 -B 10 "maxReplicas"

# 2. Check for overly permissive custom metrics
kubectl get hpa -A -o yaml | grep -A 15 -B 5 "custom.metrics.k8s.io"

# 3. Validate that HPA targets trusted workloads
kubectl get hpa <hpa-name> -n <namespace> -o jsonpath='{.spec.scaleTargetRef}'

# 4. Monitor HPA events for unusual scaling activity
kubectl get events -A --field-selector involvedObject.kind=HorizontalPodAutoscaler

# 5. Verify RBAC permissions for HPA management
kubectl auth can-i get horizontalpodautoscalers --as=system:serviceaccount:<namespace>:<service-account>

# 6. Check metrics-server security configuration
kubectl describe deployment metrics-server -n kube-system
```

### RBAC Security Verification
Best practices for verifying RBAC security:

```bash
# 1. Check for overly permissive roles
kubectl get clusterroles,roles -A -o yaml | grep -A 5 -B 5 "verbs.*\*\|resources.*\*"

# 2. Verify ServiceAccounts don't have unnecessary permissions
kubectl get rolebindings,clusterrolebindings -o yaml | grep -A 10 -B 10 "system:serviceaccount"

# 3. Check for cluster-admin access (avoid unless necessary)
kubectl get clusterrolebindings -o yaml | grep -A 5 -B 5 "cluster-admin"

# 4. Verify no users in system:masters group
kubectl get clusterrolebindings -o yaml | grep -A 10 -B 10 "system:masters"

# 5. Check for anonymous access
kubectl get clusterrolebindings -o yaml | grep -A 10 -B 10 "system:unauthenticated"

# 6. Validate that ServiceAccounts only have required permissions
kubectl auth can-i --list --as=system:serviceaccount:<namespace>:<service-account> --namespace=<namespace>

# 7. Audit RBAC changes in cluster events
kubectl get events --field-selector involvedObject.kind=Role,involvedObject.kind=ClusterRole,involvedObject.kind=RoleBinding,involvedObject.kind=ClusterRoleBinding

# 8. Check for wildcard resource access in roles
kubectl get roles,clusterroles -A -o yaml | grep -C 3 "resources.*\*"
```

Following these security practices will significantly improve the security posture of your Kubernetes deployments.