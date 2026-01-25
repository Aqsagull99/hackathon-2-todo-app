# Helm Chart Production Best Practices for Kubernetes Applications

This document covers production best practices for Helm charts in Kubernetes applications, focusing on reliability, scalability, and maintainability.

## Chart Structure Optimization

### 1. Proper Chart Versioning

Follow semantic versioning for charts:

```yaml
# Chart.yaml
apiVersion: v2
name: my-app
version: 1.2.3        # Chart version (increment for chart changes)
appVersion: "2.1.0"   # Application version (increment for app changes)
kubeVersion: ">=1.24.0"
```

### 2. Dependency Management

Manage dependencies properly:

```yaml
# Chart.yaml
dependencies:
  - name: postgresql
    version: "11.x.x"
    repository: https://charts.bitnami.com/bitnami
    condition: postgresql.enabled
    tags:
      - database
  - name: redis
    version: "^17.0.0"
    repository: https://charts.bitnami.com/bitnami
    tags:
      - cache
```

```bash
# Update dependencies
helm dependency update

# Vendor dependencies (for air-gapped environments)
helm dependency build
```

## Production-Ready Templates

### 1. Robust Template Functions

Use proper template functions and error handling:

```yaml
# templates/_helpers.tpl
{{/*
Expand the name of the chart with validation
*/}}
{{- define "my-app.name" -}}
{{- $name := default .Chart.Name .Values.nameOverride -}}
{{- if len $name | lt 63 -}}
{{- trunc 63 $name | trimSuffix "-" -}}
{{- else -}}
{{- $name | trunc 60 | trimSuffix "-" -}}{{- randAlphaNum 2 -}}
{{- end -}}
{{- end -}}

{{/*
Validate required values
*/}}
{{- define "my-app.validateValues" -}}
{{- if not .Values.image.repository -}}
{{- required "image.repository is required" .Values.image.repository -}}
{{- end -}}
{{- if not .Values.image.tag -}}
{{- required "image.tag is required" .Values.image.tag -}}
{{- end -}}
{{- end -}}
```

### 2. Advanced Deployment Configuration

Production-ready deployment with all features:

```yaml
# templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "my-app.fullname" . }}
  labels:
    {{- include "my-app.labels" . | nindent 4 }}
  {{- with .Values.deployment.annotations }}
  annotations:
    {{- toYaml . | nindent 4 }}
  {{- end }}
spec:
  {{- if not .Values.autoscaling.enabled }}
  replicas: {{ .Values.replicaCount }}
  {{- end }}
  {{- if .Values.deployment.strategy }}
  strategy: {{- toYaml .Values.deployment.strategy | nindent 4 }}
  {{- end }}
  selector:
    matchLabels:
      {{- include "my-app.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      {{- with .Values.podAnnotations }}
      annotations:
        {{- toYaml . | nindent 8 }}
        {{- if .Values.prometheus.enabled }}
        prometheus.io/scrape: "true"
        prometheus.io/port: "{{ .Values.service.port }}"
        prometheus.io/path: "/metrics"
        {{- end }}
      {{- end }}
      labels:
        {{- include "my-app.selectorLabels" . | nindent 8 }}
        {{- with .Values.podLabels }}
        {{- toYaml . | nindent 8 }}
        {{- end }}
    spec:
      {{- with .Values.imagePullSecrets }}
      imagePullSecrets:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      serviceAccountName: {{ include "my-app.serviceAccountName" . }}
      automountServiceAccountToken: {{ .Values.serviceAccount.automount }}
      {{- with .Values.podSecurityContext }}
      securityContext:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      containers:
        - name: {{ .Chart.Name }}
          {{- with .Values.securityContext }}
          securityContext:
            {{- toYaml . | nindent 12 }}
          {{- end }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          {{- if .Values.command }}
          command:
            {{- toYaml .Values.command | nindent 12 }}
          {{- end }}
          {{- if .Values.args }}
          args:
            {{- toYaml .Values.args | nindent 12 }}
          {{- end }}
          ports:
            - name: http
              containerPort: 80
              protocol: TCP
          {{- if .Values.livenessProbe.enabled }}
          livenessProbe:
            {{- toYaml .Values.livenessProbe.spec | nindent 12 }}
          {{- end }}
          {{- if .Values.readinessProbe.enabled }}
          readinessProbe:
            {{- toYaml .Values.readinessProbe.spec | nindent 12 }}
          {{- end }}
          {{- if .Values.startupProbe.enabled }}
          startupProbe:
            {{- toYaml .Values.startupProbe.spec | nindent 12 }}
          {{- end }}
          {{- with .Values.resources }}
          resources:
            {{- toYaml . | nindent 12 }}
          {{- end }}
          {{- with .Values.env }}
          env:
            {{- toYaml . | nindent 12 }}
          {{- end }}
          {{- with .Values.volumeMounts }}
          volumeMounts:
            {{- toYaml . | nindent 12 }}
          {{- end }}
      {{- with .Values.volumes }}
      volumes:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.nodeSelector }}
      nodeSelector:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.affinity }}
      affinity:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.tolerations }}
      tolerations:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- if .Values.priorityClassName }}
      priorityClassName: {{ .Values.priorityClassName }}
      {{- end }}
      {{- if .Values.schedulerName }}
      schedulerName: {{ .Values.schedulerName }}
      {{- end }}
```

## Production Values Configuration

### 1. Environment-Specific Values

Create different values files for different environments:

```yaml
# values-dev.yaml - Development environment
replicaCount: 1

image:
  repository: my-registry.com/my-app-dev
  pullPolicy: Always
  tag: "dev-latest"

resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 100m
    memory: 128Mi

service:
  type: ClusterIP
  port: 8080

ingress:
  enabled: true
  className: "nginx"
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
  hosts:
    - host: dev.my-app.local
      paths:
        - path: /
          pathType: ImplementationSpecific

env:
  - name: ENV
    value: "development"
  - name: LOG_LEVEL
    value: "debug"

livenessProbe:
  enabled: true
  path: "/health"
readinessProbe:
  enabled: true
  path: "/ready"

nodeSelector: {}
tolerations: []
affinity: {}
```

```yaml
# values-prod.yaml - Production environment
replicaCount: 3

image:
  repository: my-registry.com/my-app
  pullPolicy: IfNotPresent
  tag: "v1.2.3"  # Pin to specific version

imagePullSecrets:
  - name: production-registry-secret

resources:
  limits:
    cpu: 1000m
    memory: 1Gi
  requests:
    cpu: 500m
    memory: 512Mi

service:
  type: LoadBalancer
  port: 80

ingress:
  enabled: true
  className: "nginx"
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/force-ssl-redirect: "true"
  hosts:
    - host: my-app.example.com
      paths:
        - path: /
          pathType: ImplementationSpecific
  tls:
    - secretName: my-app-tls
      hosts:
        - my-app.example.com

autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70
  targetMemoryUtilizationPercentage: 80

env:
  - name: ENV
    value: "production"
  - name: LOG_LEVEL
    value: "info"

# Production security and performance configurations
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  runAsGroup: 3000
  readOnlyRootFilesystem: true
  allowPrivilegeEscalation: false
  capabilities:
    drop:
      - ALL

podSecurityContext:
  fsGroup: 2000

priorityClassName: "high-priority"

nodeSelector:
  node-type: production

tolerations:
  - key: node-type
    operator: Equal
    value: production
    effect: NoSchedule

affinity:
  podAntiAffinity:
    preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 100
        podAffinityTerm:
          labelSelector:
            matchExpressions:
              - key: app.kubernetes.io/name
                operator: In
                values:
                  - my-app
          topologyKey: kubernetes.io/hostname

# Production monitoring
livenessProbe:
  enabled: true
  spec:
    httpGet:
      path: /health
      port: 80
    initialDelaySeconds: 30
    periodSeconds: 10
    timeoutSeconds: 5
    failureThreshold: 6
readinessProbe:
  enabled: true
  spec:
    httpGet:
      path: /ready
      port: 80
    initialDelaySeconds: 5
    periodSeconds: 10
    timeoutSeconds: 5
    failureThreshold: 3

# Pod Disruption Budget for production
podDisruptionBudget:
  enabled: true
  minAvailable: 1
```

### 2. Deployment with Environment-Specific Values

Deploy with environment-specific configurations:

```bash
# Deploy to development
helm install my-app-dev . --values values-dev.yaml --namespace dev

# Deploy to staging
helm install my-app-staging . --values values-staging.yaml --namespace staging

# Deploy to production
helm install my-app-prod . --values values-prod.yaml --namespace production

# Upgrade with specific values
helm upgrade my-app-prod . --values values-prod.yaml --namespace production --reuse-values
```

### 2. Monitoring and Observability

Include monitoring configuration:

```yaml
# In values.yaml
prometheus:
  enabled: true
  serviceMonitor:
    enabled: true
    interval: 30s
    scrapeTimeout: 10s

logging:
  enabled: true
  sidecar:
    enabled: true
    image: fluent/fluent-bit:1.8
    config: |
      [INPUT]
          Name tail
          Path /var/log/app/*.log
      [OUTPUT]
          Name forward
          Match *

tracing:
  enabled: true
  endpoint: jaeger-collector.monitoring:14268
```

## Testing and Validation

### 1. Comprehensive Chart Testing

Create extensive test suite:

```yaml
# templates/tests/test-connection.yaml
apiVersion: v1
kind: Pod
metadata:
  name: "{{ include "my-app.fullname" . }}-test-connection"
  labels:
    {{- include "my-app.labels" . | nindent 4 }}
  annotations:
    "helm.sh/hook": test
spec:
  containers:
    - name: wget
      image: busybox
      command: ['wget']
      args: ['{{ include "my-app.fullname" . }}:{{ .Values.service.port }}']
  restartPolicy: Never
---
# templates/tests/test-health.yaml
apiVersion: v1
kind: Pod
metadata:
  name: "{{ include "my-app.fullname" . }}-test-health"
  labels:
    {{- include "my-app.labels" . | nindent 4 }}
  annotations:
    "helm.sh/hook": test
spec:
  containers:
    - name: curl
      image: curlimages/curl
      command: ['curl']
      args: ['-f', 'http://{{ include "my-app.fullname" . }}/health']
  restartPolicy: Never
```

### 2. Linting and Validation

Use comprehensive validation:

```bash
# Lint chart
helm lint

# Template validation
helm template test-release . --values values-prod.yaml

# Install dry-run
helm install test-release . --dry-run --debug

# Upgrade dry-run
helm upgrade test-release . --dry-run --debug
```

## Deployment Strategies

### 1. Blue-Green Deployment

Implement blue-green deployment patterns:

```yaml
# Use Argo Rollouts or Flagger for advanced deployments
# templates/rollout.yaml
{{- if .Values.rollout.enabled }}
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: {{ include "my-app.fullname" . }}
spec:
  replicas: {{ .Values.replicaCount }}
  strategy:
    blueGreen:
      activeService: {{ include "my-app.fullname" . }}-active
      previewService: {{ include "my-app.fullname" . }}-preview
  selector:
    matchLabels:
      {{- include "my-app.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      labels:
        {{- include "my-app.selectorLabels" . | nindent 8 }}
    spec:
      containers:
      - name: {{ .Chart.Name }}
        image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
{{- end }}
```

### 2. Canary Deployments

Implement canary deployment patterns:

```yaml
# templates/daemonset.yaml for infrastructure components
{{- if .Values.daemonset.enabled }}
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: {{ include "my-app.fullname" . }}
spec:
  selector:
    matchLabels:
      {{- include "my-app.selectorLabels" . | nindent 6 }}
  template:
    spec:
      containers:
      - name: {{ .Chart.Name }}
        image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
{{- end }}
```

## Production Deployment Process

### 1. CI/CD Pipeline

Implement proper CI/CD for chart deployment:

```yaml
# .github/workflows/deploy.yaml
name: Deploy Helm Chart

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Helm
        uses: azure/setup-helm@v3
        with:
          version: v3.10.0

      - name: Lint
        run: helm lint .

      - name: Package
        run: |
          VERSION=$(date +%Y%m%d-%H%M%S)
          helm package . --version $VERSION

      - name: Deploy to Production
        run: |
          helm upgrade --install my-app \
            . --namespace production \
            --values values-prod.yaml \
            --wait --timeout 10m
```

### 2. Monitoring and Observability

Include production monitoring:

```yaml
# templates/servicemonitor.yaml
{{- if and .Values.prometheus.enabled .Values.prometheus.serviceMonitor.enabled }}
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: {{ include "my-app.fullname" . }}
  labels:
    {{- include "my-app.labels" . | nindent 4 }}
spec:
  selector:
    matchLabels:
      {{- include "my-app.selectorLabels" . | nindent 6 }}
  endpoints:
  - port: http
    interval: {{ .Values.prometheus.serviceMonitor.interval }}
    scrapeTimeout: {{ .Values.prometheus.serviceMonitor.scrapeTimeout }}
{{- end }}
```

## Performance Optimization

### 1. Resource Optimization

Properly sized resources for production:

```yaml
# values-prod.yaml
resources:
  limits:
    cpu: 1000m
    memory: 1Gi
  requests:
    cpu: 500m
    memory: 512Mi

# Horizontal Pod Autoscaler
autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 20
  targetCPUUtilizationPercentage: 70
  targetMemoryUtilizationPercentage: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 10
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15
```

### 2. Pod Disruption Budget

Protect against involuntary disruptions:

```yaml
# templates/pdb.yaml
{{- if .Values.podDisruptionBudget.enabled }}
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: {{ include "my-app.fullname" . }}
  labels:
    {{- include "my-app.labels" . | nindent 4 }}
spec:
  {{- if .Values.podDisruptionBudget.minAvailable }}
  minAvailable: {{ .Values.podDisruptionBudget.minAvailable }}
  {{- end }}
  {{- if .Values.podDisruptionBudget.maxUnavailable }}
  maxUnavailable: {{ .Values.podDisruptionBudget.maxUnavailable }}
  {{- end }}
  selector:
    matchLabels:
      {{- include "my-app.selectorLabels" . | nindent 6 }}
{{- end }}
```

These production best practices will help you create robust, scalable, and maintainable Helm charts for Kubernetes applications.