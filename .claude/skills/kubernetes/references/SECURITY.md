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

Following these security practices will significantly improve the security posture of your Kubernetes deployments.