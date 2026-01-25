---
name: kubernetes
description: Comprehensive Kubernetes deployment and scaling for containerized applications, from simple hello-world deployments to production-grade systems with autoscaling, security, and monitoring. Use when deploying, scaling, and managing containerized applications on Kubernetes clusters, including resource management, health checks, security policies, and production best practices.
---

# Kubernetes Deployment and Scaling Skill

This skill provides comprehensive support for deploying and scaling containerized applications on Kubernetes, from simple hello-world deployments to production-grade systems with autoscaling, security, and monitoring.

## Kubernetes Control Plane Components and Reconciliation Loop

Understanding how Kubernetes maintains desired state through its control plane components and reconciliation loop is essential for effective deployments.

### Control Plane Component Responsibilities

#### API Server (kube-apiserver)
- **Frontend of the control plane** - Exposes the Kubernetes API
- **State storage** - Stores and retrieves cluster state from etcd
- **Authentication and authorization** - Validates requests
- **Watch mechanism** - Enables controllers and kubelets to watch for changes
- **State synchronization** - Ensures all components have consistent view

#### etcd
- **Distributed key-value store** - Stores all cluster state
- **Consistency** - Ensures data consistency across control plane
- **Durability** - Persists cluster configuration and state
- **Watch notifications** - Notifies API server of state changes

#### Controller Manager (kube-controller-manager)
- **Runs controllers** - Replication, endpoints, namespace, service accounts
- **Reconciliation loop** - Continuously compares desired vs current state
- **Resource lifecycle** - Manages creation, updates, and deletion
- **Leader election** - Ensures only one active controller in HA setups

#### Scheduler (kube-scheduler)
- **Pod placement** - Selects appropriate nodes for pod deployment
- **Resource optimization** - Considers resource requirements and constraints
- **Scheduling policies** - Applies affinity, taints, and tolerations
- **Node selection** - Evaluates nodes based on filters and priorities

#### kubelet (Node Component)
- **Pod execution** - Runs containers on nodes as instructed
- **Health reporting** - Reports pod and node status to API server
- **Current state reporting** - Updates API server with actual state
- **API server communication** - Receives pod specifications and reports status

### Reconciliation Loop Process

The reconciliation loop is the core mechanism that ensures desired state matches actual state:

1. **Desired State Creation**: User creates resources via kubectl (pods, deployments, services)
2. **State Persistence**: API server stores desired state in etcd
3. **Watch Trigger**: Controllers and scheduler watch for relevant changes
4. **Current State Assessment**: Components assess current cluster state
5. **Gap Analysis**: Compare desired vs current state
6. **Action Execution**: Take actions to align current state with desired state
7. **Status Update**: Report new state back to API server
8. **Loop Continuation**: Repeat continuously to maintain consistency

### Component Collaboration Flow

```
User Action → API Server → etcd (Store Desired State)
      ↓
Scheduler Watches → Finds Suitable Node → Updates Pod Spec
      ↓
Kubelet Watches → Receives Pod Assignment → Starts Containers
      ↓
Controller Watches → Monitors Actual State → Adjusts as Needed
      ↓
Status Updates → API Server → etcd (Store Current State)
```

### Example: Pod Creation Reconciliation

1. **kubectl create -f pod.yaml** → API Server receives pod specification
2. **API Server saves** → Pod object stored in etcd with `nodeName=""`
3. **Scheduler watches** → Detects unscheduled pod, selects node
4. **Scheduler updates** → Pod object in etcd with `nodeName="node-1"`
5. **Kubelet watches** → Detects pod assigned to its node
6. **Kubelet executes** → Starts container using container runtime
7. **Kubelet reports** → Updates pod status to `Running`
8. **API Server syncs** → Updates etcd with new status

## When to Use This Skill

Use this skill when you need to:
1. Deploy containerized applications to Kubernetes clusters
2. Scale applications horizontally with Horizontal Pod Autoscaling
3. Configure resource limits and requests for optimal performance
4. Implement health checks and readiness probes
5. Apply security best practices and Pod Security Standards
6. Set up network policies and RBAC controls
7. Configure Ingress for external access
8. Implement production-ready deployment patterns
9. Understand and troubleshoot reconciliation loop behavior
10. Optimize control plane component configurations

## Prerequisites Validation

Before using this skill, verify your Kubernetes setup:

```bash
# Check kubectl version
kubectl version --client

# Verify cluster access
kubectl cluster-info

# Check available nodes
kubectl get nodes

# Test basic functionality
kubectl run test-pod --image=nginx --dry-run=client -o yaml
```

## Quick Start

### Basic Deployment Configuration
For a simple application deployment:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
  labels:
    app: my-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: my-app
        image: my-image:latest
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

### Horizontal Pod Autoscaler
For automatic scaling based on CPU utilization:

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: my-app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app
  minReplicas: 1
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 50
```

### Service Configuration
To expose the application internally:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-app-service
spec:
  selector:
    app: my-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  type: ClusterIP
```

### Ingress Configuration
To expose the application externally:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-app-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: my-app.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: my-app-service
            port:
              number: 80
```

## Production Best Practices

### Resource Management
Configure proper resource limits and requests:

```yaml
# Example with multiple containers and resource specifications
apiVersion: v1
kind: Pod
metadata:
  name: frontend
spec:
  containers:
  - name: app
    image: images.my-company.example/app:v4
    resources:
      requests:
        memory: "64Mi"
        cpu: "250m"
      limits:
        memory: "128Mi"
        cpu: "500m"
  - name: log-aggregator
    image: images.my-company.example/log-aggregator:v6
    resources:
      requests:
        memory: "64Mi"
        cpu: "250m"
      limits:
        memory: "128Mi"
        cpu: "500m"
```

### Health Checks and Probes
Implement proper liveness and readiness probes:

```yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    test: liveness
  name: liveness-http
spec:
  containers:
  - name: liveness
    image: registry.k8s.io/e2e-test-images/agnhost:2.40
    args:
    - liveness
    livenessProbe:
      httpGet:
        path: /healthz
        port: 8080
        httpHeaders:
        - name: Custom-Header
          value: Awesome
      initialDelaySeconds: 3
      periodSeconds: 3
    readinessProbe:
      httpGet:
        path: /readyz
        port: 8080
      initialDelaySeconds: 5
      periodSeconds: 5
```

### Security Best Practices
Apply Pod Security Standards and security contexts:

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

### Network Policies
Restrict network access with network policies:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: access-nginx
spec:
  podSelector:
    matchLabels:
      app: nginx
  ingress:
  - from:
    - podSelector:
        matchLabels:
          access: "true"
```

### RBAC Configuration
Set up proper Role-Based Access Control:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: default
  name: pod-reader
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "watch", "list"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: read-pods
  namespace: default
subjects:
- kind: User
  name: jane
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

## Scaling Operations

### Manual Scaling
Scale deployments manually:

```bash
# Scale to specific number of replicas
kubectl scale deployment/my-app --replicas=5

# Scale based on current state
kubectl scale --current-replicas=2 --replicas=6 deployment/my-app
```

### Auto Scaling
Configure Horizontal Pod Autoscaler:

```bash
# Create HPA based on CPU utilization
kubectl autoscale deployment my-app --cpu-percent=50 --min=1 --max=10

# Create HPA based on memory utilization
kubectl autoscale deployment my-app --memory-percent=70 --min=1 --max=5
```

### Vertical Pod Autoscaling
For resource optimization:

```yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: my-app-vpa
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app
  updatePolicy:
    updateMode: "Auto"
```

## Deployment Strategies

### Rolling Updates
Configure rolling update strategy:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
      maxSurge: 1
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: my-app
        image: my-image:v2
```

### Blue-Green Deployment
For zero-downtime deployments:

```yaml
# Blue deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app-blue
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
      version: blue
  template:
    metadata:
      labels:
        app: my-app
        version: blue
    spec:
      containers:
      - name: my-app
        image: my-image:v1
---
# Green deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app-green
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
      version: green
  template:
    metadata:
      labels:
        app: my-app
        version: green
    spec:
      containers:
      - name: my-app
        image: my-image:v2
```

## Scripts Available

See [K8S-SCRIPTS.md](references/K8S-SCRIPTS.md) for automated Kubernetes deployment and scaling scripts.

## Security Considerations

See [SECURITY.md](references/SECURITY.md) for detailed security best practices and production hardening techniques.

## Production Best Practices

See [PRODUCTION.md](references/PRODUCTION.md) for production deployment guidelines and optimization strategies.