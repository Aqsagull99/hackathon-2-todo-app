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

### Post-Deployment Checklist
- [ ] Monitor resource utilization
- [ ] Verify autoscaling behavior
- [ ] Check for pod restarts
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