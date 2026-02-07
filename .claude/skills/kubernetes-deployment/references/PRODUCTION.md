# Kubernetes Production Best Practices

This document covers production best practices for Kubernetes deployments, focusing on reliability, scalability, and maintainability.

## Resource Management

### Proper Resource Requests and Limits
Configure appropriate resource requests and limits:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: production-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: production-app
  template:
    metadata:
      labels:
        app: production-app
    spec:
      containers:
      - name: app
        image: my-app:latest
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
```

### Advanced Resource Management
For production environments, consider more sophisticated resource configurations:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: advanced-production-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: advanced-production-app
  template:
    metadata:
      labels:
        app: advanced-production-app
    spec:
      containers:
      - name: app
        image: my-app:latest
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
            # For applications that use huge pages
            # hugepages-2Mi: "1Gi"
          limits:
            memory: "1Gi"
            cpu: "1000m"
            # hugepages-2Mi: "1Gi"
        # Resource quality of service considerations
        env:
        # Access resource limits from within the container
        - name: LIMITS_CPU
          valueFrom:
            resourceFieldRef:
              containerName: app
              resource: limits.cpu
        - name: LIMITS_MEMORY
          valueFrom:
            resourceFieldRef:
              containerName: app
              resource: limits.memory
        - name: REQUESTS_CPU
          valueFrom:
            resourceFieldRef:
              containerName: app
              resource: requests.cpu
        - name: REQUESTS_MEMORY
          valueFrom:
            resourceFieldRef:
              containerName: app
              resource: requests.memory
```

### Quality of Service (QoS) Classes
Understand how resource configuration affects QoS:

```yaml
# Guaranteed QoS - limits equal requests
resources:
  requests:
    memory: "1Gi"
    cpu: "1000m"
  limits:
    memory: "1Gi"
    cpu: "1000m"
---
# Burstable QoS - limits higher than requests
resources:
  requests:
    memory: "512Mi"
    cpu: "500m"
  limits:
    memory: "1Gi"
    cpu: "1000m"
---
# BestEffort QoS - no limits or requests
resources: {}
```

## Health Checks and Probes

### Liveness and Readiness Probes
Implement proper health checks:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: health-checked-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: health-checked-app
  template:
    metadata:
      labels:
        app: health-checked-app
    spec:
      containers:
      - name: app
        image: my-app:latest
        livenessProbe:
          httpGet:
            path: /healthz
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
          successThreshold: 1
        readinessProbe:
          httpGet:
            path: /readyz
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
          successThreshold: 1
        startupProbe:
          httpGet:
            path: /startup
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 30
```

## Scaling Strategies

### Horizontal Pod Autoscaling
Configure HPA for automatic scaling:

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: production-app
  minReplicas: 3
  maxReplicas: 15
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 10
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15
      - type: Pods
        value: 4
        periodSeconds: 15
      selectPolicy: Max
```

### Vertical Pod Autoscaling
For resource optimization:

```yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: app-vpa
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: production-app
  updatePolicy:
    updateMode: "Auto"
  resourcePolicy:
    containerPolicies:
    - containerName: app
      minAllowed:
        cpu: 100m
        memory: 100Mi
      maxAllowed:
        cpu: 2
        memory: 2Gi
      controlledResources: ["cpu", "memory"]
      controlledValues: RequestsAndLimits
```

## Deployment Strategies

### Rolling Updates
Configure safe rolling updates:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rolling-update-app
spec:
  replicas: 5
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
      maxSurge: 1
  selector:
    matchLabels:
      app: rolling-update-app
  template:
    metadata:
      labels:
        app: rolling-update-app
    spec:
      containers:
      - name: app
        image: my-app:latest
        ports:
        - containerPort: 8080
```

### Production-Ready Rolling Update Configuration
For production environments, use more conservative settings:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: production-rolling-update
spec:
  replicas: 10
  strategy:
    type: RollingUpdate
    rollingUpdate:
      # Conservative settings for production
      maxUnavailable: "10%"    # Allow 10% of pods to be unavailable during update
      maxSurge: "10%"        # Allow 10% more pods than desired during update
  selector:
    matchLabels:
      app: production-app
  template:
    metadata:
      labels:
        app: production-app
    spec:
      containers:
      - name: app
        image: my-app:latest
        # Robust health checks for safe rolling updates
        livenessProbe:
          httpGet:
            path: /healthz
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
          successThreshold: 1
        readinessProbe:
          httpGet:
            path: /readyz
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
          successThreshold: 1
        startupProbe:
          httpGet:
            path: /startup
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 30
```

### Deployment Rollback Configuration
Configure your deployment for easy rollbacks:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rollback-ready-app
spec:
  replicas: 5
  revisionHistoryLimit: 10  # Keep 10 revisions for rollback capability
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: "10%"
      maxSurge: "10%"
  selector:
    matchLabels:
      app: rollback-ready-app
  template:
    metadata:
      labels:
        app: rollback-ready-app
      annotations:
        # Use annotations to track deployments for easier rollback identification
        deployment.kubernetes.io/revision: "1"
        deployment.timestamp: "{{ timestamp }}"
    spec:
      containers:
      - name: app
        image: my-app:latest
        env:
        # Pass version information to the application
        - name: APP_VERSION
          valueFrom:
            fieldRef:
              fieldPath: metadata.labels.version
```

### Deployment Monitoring and Rollback Commands
Essential commands for managing production deployments:

```bash
# Check rollout history for rollback options
kubectl rollout history deployment/production-app

# Monitor rollout status
kubectl rollout status deployment/production-app --timeout=10m

# Pause rollout if issues are detected
kubectl rollout pause deployment/production-app

# Resume rollout after fixing issues
kubectl rollout resume deployment/production-app

# Roll back to previous version
kubectl rollout undo deployment/production-app

# Roll back to specific revision
kubectl rollout undo deployment/production-app --to-revision=3

# View detailed rollout events
kubectl describe deployment production-app

# Check ReplicaSet status during rollout
kubectl get replicasets -l app=production-app

# View all events related to deployment
kubectl get events --field-selector involvedObject.name=production-app
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
        image: my-app:v1.0
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
        image: my-app:v2.0
---
# Service routing to blue initially
apiVersion: v1
kind: Service
metadata:
  name: my-app-service
spec:
  selector:
    app: my-app
    version: blue  # Route to blue initially
  ports:
  - port: 80
    targetPort: 8080
  type: ClusterIP
```

## Pod Disruption Budgets

### Maintain Availability During Maintenance
Configure Pod Disruption Budgets:

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: app-pdb
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: production-app
---
# Or use maxUnavailable
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: app-pdb-max
spec:
  maxUnavailable: 1
  selector:
    matchLabels:
      app: production-app
```

## Monitoring and Observability

### Service Monitoring
Implement proper monitoring:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: app-service
  annotations:
    prometheus.io/scrape: "true"
    prometheus.io/port: "8080"
    prometheus.io/path: "/metrics"
spec:
  selector:
    app: production-app
  ports:
  - port: 80
    targetPort: 8080
---
# ServiceMonitor for Prometheus Operator
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: app-monitor
spec:
  selector:
    matchLabels:
      app: production-app
  endpoints:
  - port: http
    interval: 30s
    path: /metrics
```

### Logging Configuration
Set up centralized logging:

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluentd
spec:
  selector:
    matchLabels:
      name: fluentd
  template:
    metadata:
      labels:
        name: fluentd
    spec:
      serviceAccount: fluentd
      serviceAccountName: fluentd
      tolerations:
      - key: node-role.kubernetes.io/master
        effect: NoSchedule
      containers:
      - name: fluentd
        image: fluent/fluentd-kubernetes-daemonset
        env:
        - name: FLUENT_ELASTICSEARCH_HOST
          value: "elasticsearch.logging.svc.cluster.local"
        - name: FLUENT_ELASTICSEARCH_PORT
          value: "9200"
        volumeMounts:
        - name: varlog
          mountPath: /var/log
        - name: varlibdockercontainers
          mountPath: /var/lib/docker/containers
          readOnly: true
      terminationGracePeriodSeconds: 30
      volumes:
      - name: varlog
        hostPath:
          path: /var/log
      - name: varlibdockercontainers
        hostPath:
          path: /var/lib/docker/containers
```

## Storage Management

### Persistent Volume Claims
Configure storage properly:

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: app-storage
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
  storageClassName: fast-ssd
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: database
spec:
  serviceName: database
  replicas: 3
  selector:
    matchLabels:
      app: database
  template:
    metadata:
      labels:
        app: database
    spec:
      containers:
      - name: db
        image: postgres:13
        volumeMounts:
        - name: db-storage
          mountPath: /var/lib/postgresql/data
        env:
        - name: POSTGRES_DB
          value: "myapp"
        - name: POSTGRES_USER
          value: "user"
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: password
  volumeClaimTemplates:
  - metadata:
      name: db-storage
    spec:
      accessModes: [ "ReadWriteOnce" ]
      storageClassName: "fast-ssd"
      resources:
        requests:
          storage: 10Gi
```

## Networking Best Practices

### Service Configuration
Production-ready Service configuration:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: production-service
  labels:
    app: production-app
    version: v1.0.0
  annotations:
    # Service annotations for load balancer configuration
    service.beta.kubernetes.io/aws-load-balancer-type: nlb
    service.beta.kubernetes.io/aws-load-balancer-cross-zone-load-balancing-enabled: "true"
    # Health check configuration
    service.beta.kubernetes.io/aws-load-balancer-healthcheck-healthy-threshold: "2"
    service.beta.kubernetes.io/aws-load-balancer-healthcheck-unhealthy-threshold: "2"
spec:
  # Use appropriate service type for production
  type: LoadBalancer  # or ClusterIP for internal services
  # Use selectors that match your production deployment
  selector:
    app: production-app
    version: v1.0.0
    environment: production
  ports:
    - name: http
      port: 80
      targetPort: 8080
      protocol: TCP
      # nodePort: 30080  # Only for NodePort services
  # Restrict load balancer source ranges in production
  loadBalancerSourceRanges:
    - 10.0.0.0/8
    - 192.168.0.0/16
  # Session affinity for stateful applications
  sessionAffinity: ClientIP
  sessionAffinityConfig:
    clientIP:
      timeoutSeconds: 10800
```

### Service Type Selection for Production
Choose the right service type based on your requirements:

```yaml
# Internal cluster services (most common)
apiVersion: v1
kind: Service
metadata:
  name: internal-service
spec:
  type: ClusterIP  # Default, internal cluster access only
  selector:
    app: internal-service
  ports:
    - name: http
      port: 80
      targetPort: 8080
---
# External access via cloud load balancer (recommended for production)
apiVersion: v1
kind: Service
metadata:
  name: external-service
spec:
  type: LoadBalancer  # Use cloud provider's load balancer
  selector:
    app: external-service
  ports:
    - name: http
      port: 80
      targetPort: 8080
  # Secure with source IP restrictions
  loadBalancerSourceRanges:
    - 0.0.0.0/0  # In production, restrict to specific ranges
---
# Headless service for StatefulSets
apiVersion: v1
kind: Service
metadata:
  name: headless-service
spec:
  clusterIP: None  # No cluster IP, direct pod access
  selector:
    app: stateful-app
  ports:
    - name: http
      port: 80
      targetPort: 8080
```

### Label Selector Best Practices
Use precise and consistent label selectors:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: production-service
spec:
  selector:
    # Use multiple labels for precision
    app: production-app
    version: v1.0.0
    environment: production
    tier: frontend
    # Use matchExpressions for complex logic
    matchExpressions:
    - key: environment
      operator: In
      values: ["production", "staging"]
    - key: version
      operator: NotIn
      values: ["canary", "test"]
  ports:
    - name: http
      port: 80
      targetPort: 8080
```

### DNS Configuration and Discovery
Best practices for service discovery:

```bash
# Production DNS resolution patterns
# Same namespace: service-name
curl http://app-service:80

# Cross-namespace: service-name.namespace
curl http://app-service.production:80

# Fully qualified: service-name.namespace.svc.cluster.local
curl http://app-service.production.svc.cluster.local:80

# Use stable DNS names in application configuration
DATABASE_HOST: "database-service.database.svc.cluster.local"
CACHE_HOST: "redis-service.cache.svc.cluster.local"
```

### Service Monitoring and Troubleshooting
Essential commands for production service management:

```bash
# Monitor service endpoints
kubectl get endpoints production-service

# Check service connectivity
kubectl run debug-pod --image=nicolaka/netshoot -it --rm
# Inside debug pod:
curl http://production-service:80
nslookup production-service

# Monitor service performance
kubectl top service production-service

# Check service events
kubectl describe service production-service

# Verify DNS resolution
kubectl exec -it <any-pod> -- nslookup production-service.production.svc.cluster.local

# Check endpoint slices (modern approach)
kubectl get endpointslices -l kubernetes.io/service-name=production-service

# Verify pod readiness for service endpoints
kubectl get pods -l app=production-app -o wide
```

### Ingress Configuration
Configure proper ingress for external access:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    nginx.ingress.kubernetes.io/rate-limit: "100"
    nginx.ingress.kubernetes.io/rate-limit-window: "1m"
spec:
  tls:
  - hosts:
    - myapp.example.com
    secretName: myapp-tls
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: app-service
            port:
              number: 80
```

### Load Balancing
Configure service for proper load balancing:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: load-balanced-service
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: nlb
    service.beta.kubernetes.io/aws-load-balancer-cross-zone-load-balancing-enabled: "true"
spec:
  type: LoadBalancer
  externalTrafficPolicy: Local
  selector:
    app: production-app
  ports:
  - name: http
    port: 80
    targetPort: 8080
    protocol: TCP
  - name: https
    port: 443
    targetPort: 8443
    protocol: TCP
```

## Backup and Disaster Recovery

### Backup Strategy
Implement backup strategies:

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: database-backup
spec:
  schedule: "0 2 * * *"  # Daily at 2 AM
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: backup
            image: postgres:13
            command:
            - /bin/bash
            - -c
            - pg_dump -h database-service -U postgres -d myapp > /backup/backup-$(date +%Y%m%d).sql
            env:
            - name: PGPASSWORD
              valueFrom:
                secretKeyRef:
                  name: db-secret
                  key: password
            volumeMounts:
            - name: backup-storage
              mountPath: /backup
          volumes:
          - name: backup-storage
            persistentVolumeClaim:
              claimName: backup-pvc
          restartPolicy: OnFailure
```

## Production Checklist

### Pre-Deployment Checklist
- [ ] Verify cluster connectivity: `kubectl cluster-info`
- [ ] Check node status: `kubectl get nodes`
- [ ] Confirm current context: `kubectl config current-context`
- [ ] Validate target namespace exists: `kubectl get namespace <namespace>`
- [ ] Check ResourceQuota status: `kubectl describe resourcequota -n <namespace>`
- [ ] Validate namespace permissions: `kubectl auth can-i get pods -n <namespace>`
- [ ] Resource requests and limits configured
- [ ] Health checks implemented (liveness, readiness, startup)
- [ ] Horizontal Pod Autoscaler configured
- [ ] Pod Disruption Budget set
- [ ] Security context configured
- [ ] Network policies applied
- [ ] RBAC rules defined
- [ ] Secrets management implemented
- [ ] Monitoring and logging configured
- [ ] Backup strategy in place
- [ ] Load testing completed
- [ ] Security scanning passed
- [ ] Reconciliation loop considerations for controllers
- [ ] Control plane resource allocation planned

### Namespace Resource Management Checklist
- [ ] ResourceQuotas configured for production namespace
- [ ] LimitRanges set for default resource values
- [ ] Namespace isolation policies implemented
- [ ] Cross-namespace access controls configured
- [ ] Multi-environment namespace strategy implemented (dev/staging/prod)
- [ ] Namespace quotas monitored regularly
- [ ] Quota limits appropriate for expected load

### Configuration and Secret Management Checklist
- [ ] ConfigMaps validated for production settings
- [ ] Secrets stored securely using Kubernetes Secrets
- [ ] Secrets mounted as volumes instead of environment variables
- [ ] Secrets encrypted at rest in etcd
- [ ] RBAC rules limit secret access to authorized services
- [ ] ConfigMaps and Secrets reviewed for sensitive data
- [ ] Pod Security Standards applied to protect secrets
- [ ] Secret rotation strategy implemented
- [ ] External secret management considered (HashiCorp Vault, AWS Secrets Manager)

### Debugging and Resource Management Checklist
- [ ] QoS class configured appropriately for each workload (Guaranteed/Burstable/BestEffort)
- [ ] Resource requests and limits match QoS requirements
- [ ] Systematic debugging approach documented for common issues
- [ ] Failure state diagnosis procedures established
- [ ] Monitoring and alerting configured for resource utilization
- [ ] Node resource capacity planned for workload requirements
- [ ] Pod priority and preemption configured for critical workloads
- [ ] Resource quotas and limits enforced per namespace
- [ ] Diagnostic tools and debugging pods available in cluster
- [ ] Health checks and readiness probes configured properly

### HPA and Scaling Configuration Checklist
- [ ] Metrics-server installed and verified: `kubectl top nodes`
- [ ] Resource requests defined for all pods (required for HPA)
- [ ] HPA configured with appropriate min/max replicas
- [ ] CPU/memory utilization targets set appropriately (60-70% for CPU)
- [ ] Stabilization windows configured to prevent scaling flapping
- [ ] Scale-up policies configured for quick response to load increases
- [ ] Scale-down policies configured to prevent premature scale-down
- [ ] Multiple metrics configured for comprehensive scaling triggers
- [ ] Custom metrics configured for application-specific scaling
- [ ] HPA behavior policies tested under load conditions
- [ ] AI/ML workload metrics configured for specialized scaling (GPU, queue depth, etc.)
- [ ] Container resource metrics used for multi-container pods when needed
- [ ] HPA monitoring and alerting configured
- [ ] HPA performance tested under various load scenarios

### Health Probe Configuration Checklist
- [ ] Liveness probes configured to detect and restart unhealthy containers
- [ ] Readiness probes configured to remove unready containers from service
- [ ] Startup probes configured for applications with slow initialization (AI models, etc.)
- [ ] Initial delay settings appropriate for application startup time
- [ ] Timeout values sufficient for slow operations
- [ ] Failure thresholds set to balance responsiveness with resilience
- [ ] Period seconds optimized for checking frequency vs resource usage
- [ ] Success thresholds properly configured (1 for liveness/startup, adjustable for readiness)
- [ ] HTTP endpoints used for probes when possible (more informative than TCP)
- [ ] Exec-based probes used for complex health checks when HTTP not suitable
- [ ] gRPC probes configured for gRPC-based applications
- [ ] Probe configuration tested under load conditions
- [ ] Probe endpoints return appropriate HTTP status codes (200 for healthy)
- [ ] Applications implement fast health check endpoints (don't include expensive operations)

### Batch Workload Configuration Checklist
- [ ] Jobs configured with appropriate completions and parallelism values
- [ ] Backoff limits set appropriately for failure handling (default 6)
- [ ] Active deadline seconds configured to prevent indefinite running
- [ ] TTL seconds after finished configured for automatic cleanup
- [ ] Restart policies set correctly (Never, OnFailure) for batch workloads
- [ ] Resource requests and limits configured for batch processing requirements
- [ ] Indexed jobs used for ordered batch processing when needed
- [ ] Pod failure policies configured for custom failure handling
- [ ] Success policies defined for early job termination when applicable
- [ ] GPU resources properly requested for AI/ML workloads
- [ ] Node affinity configured for specialized hardware requirements
- [ ] Volume mounts configured for data input/output in batch jobs
- [ ] CronJobs configured with appropriate schedules using standard cron syntax
- [ ] Concurrency policies set appropriately (Allow/Forbid/Replace)
- [ ] Starting deadline seconds configured for missed schedules
- [ ] History limits set for successful and failed job retention
- [ ] Timezone configured correctly for scheduled jobs
- [ ] Suspend functionality tested for pausing scheduled jobs
- [ ] Job completion and success criteria verified
- [ ] Batch workload monitoring and alerting configured

### AI-Assisted Manifest Validation Checklist
- [ ] AI-generated manifests validated with kubeval for schema compliance
- [ ] Resource requests and limits verified for production appropriateness
- [ ] Security contexts properly configured (runAsNonRoot, capabilities, etc.)
- [ ] Health checks (liveness/readiness) properly configured
- [ ] Resource names and selectors consistently applied across related resources
- [ ] API versions current and not deprecated
- [ ] Labels follow organizational standards and conventions
- [ ] Annotations include appropriate metadata (description, version, etc.)
- [ ] Network policies defined for application communication
- [ ] Storage configurations properly specified with appropriate access modes
- [ ] Environment variables secured using ConfigMaps/Secrets instead of inline values
- [ ] Image pull secrets configured for private registries
- [ ] Pod disruption budgets defined for critical workloads
- [ ] Horizontal Pod Autoscaler configured for dynamic scaling
- [ ] Resource quotas enforced at namespace level
- [ ] AI-generated configurations tested with kubectl dry-run before application
- [ ] Security scanning performed on AI-generated manifests
- [ ] AI-generated code reviewed by human operators before production deployment
- [ ] Validation tools (kube-score, conftest, datree) run on AI-generated manifests
- [ ] Iterative refinement applied to improve AI-generated manifests

### RBAC Security and Permission Auditing Checklist
- [ ] Dedicated ServiceAccounts created for each application/service
- [ ] ServiceAccounts use principle of least privilege (minimal permissions)
- [ ] Roles defined with specific resource access (not wildcards)
- [ ] RoleBindings properly link ServiceAccounts to Roles
- [ ] Permissions verified using `kubectl auth can-i` commands
- [ ] Namespace-scoped Roles/RoleBindings used instead of ClusterRoles when possible
- [ ] Resource-specific permissions granted using resourceNames when needed
- [ ] Subresource permissions properly configured (pods/log, pods/exec, etc.)
- [ ] ServiceAccount tokens properly managed (automountServiceAccountToken settings)
- [ ] RBAC configurations audited regularly for unnecessary permissions
- [ ] Temporary elevated permissions properly revoked after use
- [ ] Administrative access limited to authorized personnel only
- [ ] RBAC policies tested in non-production environments first
- [ ] Permission audit logs monitored for suspicious activities

### Post-Deployment Checklist
- [ ] Verify cluster connectivity remains stable: `kubectl cluster-info`
- [ ] Check node status: `kubectl get nodes`
- [ ] Validate current context: `kubectl config current-context`
- [ ] Monitor resource utilization
- [ ] Verify autoscaling behavior
- [ ] Check for pod restarts: `kubectl get pods -l app=<app-name>`
- [ ] Validate monitoring metrics
- [ ] Test failover scenarios
- [ ] Verify backup functionality
- [ ] Conduct security audit
- [ ] Performance benchmarking
- [ ] Disaster recovery testing
- [ ] Reconciliation loop performance (watch events, state convergence)
- [ ] Control plane component health (API server, scheduler, controller manager)

## Reconciliation Loop Optimization for Production

### Watch Performance
For production environments, optimize watch mechanisms:

```yaml
# Configure efficient watches in controllers
apiVersion: apps/v1
kind: Deployment
metadata:
  name: controller-manager
spec:
  template:
    spec:
      containers:
      - name: controller-manager
        image: controller-manager:latest
        args:
        - --leader-elect=true
        - --sync-period=10s  # Balance between responsiveness and API load
        - --concurrent-goroutines=10  # Limit concurrent reconciliations
```

### Control Plane Resource Allocation
Ensure adequate resources for control plane components:

```yaml
# Example API server resource configuration
apiVersion: kubeadm.k8s.io/v1beta3
kind: ClusterConfiguration
apiServer:
  extraArgs:
    # Rate limiting to prevent API server overload
    max-requests-inflight: "400"
    max-mutating-requests-inflight: "200"
    # Watch cache configuration
    watch-cache: "true"
    watch-cache-sizes: "replicationcontrollers=500,pods=1000"
  extraVolumes:
  - name: audit-log
    hostPath: /var/log/kubernetes/audit
    mountPath: /var/log/kubernetes/audit
    pathType: DirectoryOrCreate
  resources:
    requests:
      cpu: 250m
      memory: 1Gi
    limits:
      cpu: 500m
      memory: 2Gi
```

### Controller Performance
Optimize controller behavior in production:

```yaml
# Example controller manager configuration
apiVersion: kubeadm.k8s.io/v1beta3
kind: ClusterConfiguration
controllerManager:
  extraArgs:
    # Concurrent workers for different resource types
    concurrent-deployment-syncs: "10"
    concurrent-endpoint-syncs: "10"
    concurrent-gc-syncs: "20"
    concurrent-namespace-syncs: "10"
    concurrent-replicaset-syncs: "10"
    concurrent-resource-quota-syncs: "10"
    concurrent-service-syncs: "2"
    concurrent-service-account-token-syncs: "4"
    # Leader election settings
    leader-elect: "true"
    leader-elect-retry-period: "2s"
    leader-elect-resource-lock: "leases"
  resources:
    requests:
      cpu: 200m
      memory: 512Mi
    limits:
      cpu: 500m
      memory: 1Gi
```

### Monitoring Reconciliation Loops
Track reconciliation performance:

```yaml
# Example ServiceMonitor for controller metrics
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: controller-manager-monitor
  labels:
    app: controller-manager
spec:
  selector:
    matchLabels:
      app: controller-manager
  endpoints:
  - port: https
    scheme: https
    interval: 30s
    path: /metrics
    bearerTokenFile: /var/run/secrets/kubernetes.io/serviceaccount/token
    tlsConfig:
      caFile: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
      serverName: kubernetes
---
# Example PrometheusRule for reconciliation alerts
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: reconciliation-alerts
spec:
  groups:
  - name: reconciliation.rules
    rules:
    - alert: HighReconciliationLatency
      expr: histogram_quantile(0.99, controller_runtime_reconcile_time_seconds_bucket) > 30
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: "High reconciliation latency in controller"
        description: "Controller reconcile time is high (99th percentile > 30s) for {{ $labels.controller }}"
    - alert: ControllerErrors
      expr: rate(controller_runtime_reconcile_errors_total[5m]) > 0.1
      for: 10m
      labels:
        severity: warning
      annotations:
        summary: "Controller experiencing errors"
        description: "Controller {{ $labels.controller }} is experiencing reconciliation errors"
```

These production best practices will help ensure your Kubernetes deployments are reliable, scalable, and maintainable.