---
name: helm-charts
description: Comprehensive Helm chart creation and management for Kubernetes applications, from simple hello-world charts to production-ready deployments with security, testing, and packaging best practices. Use when creating, packaging, testing, or deploying Helm charts for Kubernetes applications, including chart scaffolding, template development, dependency management, security scanning, and production deployment.
---

# Helm Charts for Kubernetes Applications

This skill provides comprehensive support for creating, packaging, and managing Helm charts for Kubernetes applications, from simple hello-world examples to production-ready deployments with security and testing best practices.

## When to Use This Skill

Use this skill when you need to:
1. Create Helm charts for Kubernetes applications from scratch
2. Package applications for distribution and deployment
3. Manage chart dependencies and versions
4. Implement security best practices and provenance
5. Test charts before production deployment
6. Deploy production-ready charts with proper configuration
7. Publish charts to repositories or OCI registries

## Prerequisites Validation

Before using this skill, verify your Helm installation:

```bash
# Check Helm version
helm version

# Verify Helm functionality
helm list --help

# Check for Kubernetes cluster access
kubectl cluster-info
```

## Quick Start

### Create a New Helm Chart
```bash
# Scaffold a new chart
helm create my-app

# The generated chart structure:
my-app/
  Chart.yaml          # Chart metadata
  values.yaml         # Default configuration values
  charts/             # Chart dependencies
  templates/          # Kubernetes manifest templates
    NOTES.txt         # Post-installation notes
    _helpers.tpl      # Template helpers
    deployment.yaml
    service.yaml
    serviceaccount.yaml
    hpa.yaml
    ingress.yaml
    tests/
      test-connection.yaml
  .helmignore         # Files to ignore during packaging
```

### Chart Metadata (Chart.yaml)
```yaml
apiVersion: v2
name: my-app
version: 0.1.0
appVersion: "1.0.0"
kubeVersion: ">=1.24.0"
description: A Helm chart for my application
type: application
keywords:
  - web
  - frontend
home: https://example.com
sources:
  - https://github.com/example/my-app
maintainers:
  - name: Your Name
    email: your.email@example.com
icon: https://example.com/icon.png
dependencies:
  - name: postgresql
    version: "11.x.x"
    repository: https://charts.bitnami.com/bitnami
    condition: postgresql.enabled
annotations:
  artifacthub.io/license: Apache-2.0
  artifacthub.io/links: |
    - name: Documentation
      url: https://example.com/docs
  artifacthub.io/operator: "false"
  artifacthub.io/prerelease: "false"
  artifacthub.io/containsSecurityUpdates: "false"
  artifacthub.io/deprecated: "false"
  artifacthub.io/alternativeLocations: |
    - oci://registry.example.com/charts/my-app
  artifacthub.io/images: |
    - name: my-app
      image: nginx:latest
```

### Default Values (values.yaml)
```yaml
# Default values for my-app
replicaCount: 1

image:
  repository: nginx
  pullPolicy: IfNotPresent
  tag: "1.21.0"

imagePullSecrets: []
nameOverride: ""
fullnameOverride: ""

serviceAccount:
  create: true
  annotations: {}
  name: ""

podAnnotations: {}

podSecurityContext: {}
  # fsGroup: 2000

securityContext: {}
  # capabilities:
  #   drop:
  #   - ALL
  # readOnlyRootFilesystem: true
  # runAsNonRoot: true
  # runAsUser: 1000

service:
  type: ClusterIP
  port: 80

ingress:
  enabled: false
  className: ""
  annotations: {}
    # kubernetes.io/ingress.class: nginx
    # kubernetes.io/tls-acme: "true"
  hosts:
    - host: chart-example.local
      paths:
        - path: /
          pathType: ImplementationSpecific
  tls: []
  #  - secretName: chart-example-tls
  #    hosts:
  #      - chart-example.local

resources:
  # We usually recommend not to specify default resources and to leave this as a conscious
  # choice for the user. This also increases chances charts run on environments with little
  # resources, such as Minikube. If you do want to specify resources, uncomment the following
  # lines, adjust them as necessary, and remove the curly braces after 'resources:'.
  limits:
    cpu: 100m
    memory: 128Mi
  requests:
    cpu: 100m
    memory: 128Mi

autoscaling:
  enabled: false
  minReplicas: 1
  maxReplicas: 100
  targetCPUUtilizationPercentage: 80
  # targetMemoryUtilizationPercentage: 80

nodeSelector: {}

tolerations: []

affinity: {}
```

## Production Best Practices

### Template Development

Use helper templates for consistent naming and labels:

```yaml
# templates/_helpers.tpl
{{/*
Expand the name of the chart.
*/}}
{{- define "my-app.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "my-app.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "my-app.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "my-app.labels" -}}
helm.sh/chart: {{ include "my-app.chart" . }}
{{ include "my-app.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "my-app.selectorLabels" -}}
app.kubernetes.io/name: {{ include "my-app.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
```

### Deployment Template with Best Practices
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
  {{- with .Values.deployment.strategy }}
  strategy:
    {{- toYaml . | nindent 4 }}
  {{- end }}
  selector:
    matchLabels:
      {{- include "my-app.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      {{- with .Values.podAnnotations }}
      annotations:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      labels:
        {{- include "my-app.selectorLabels" . | nindent 8 }}
    spec:
      {{- with .Values.imagePullSecrets }}
      imagePullSecrets:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      serviceAccountName: {{ include "my-app.serviceAccountName" . }}
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
              containerPort: {{ .Values.service.targetPort | default 80 }}
              protocol: TCP
          {{- if .Values.livenessProbe.enabled }}
          livenessProbe:
            {{- toYaml .Values.livenessProbe.spec | nindent 12 }}
          {{- else if .Values.livenessProbe }}
          livenessProbe:
            httpGet:
              path: {{ .Values.livenessProbe.path | default "/" }}
              port: {{ .Values.service.port }}
          {{- end }}
          {{- if .Values.readinessProbe.enabled }}
          readinessProbe:
            {{- toYaml .Values.readinessProbe.spec | nindent 12 }}
          {{- else if .Values.readinessProbe }}
          readinessProbe:
            httpGet:
              path: {{ .Values.readinessProbe.path | default "/" }}
              port: {{ .Values.service.port }}
          {{- end }}
          {{- if .Values.startupProbe.enabled }}
          startupProbe:
            {{- toYaml .Values.startupProbe.spec | nindent 12 }}
          {{- end }}
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
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

### Service Template with Best Practices
```yaml
# templates/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: {{ include "my-app.fullname" . }}
  labels:
    {{- include "my-app.labels" . | nindent 4 }}
  {{- with .Values.service.annotations }}
  annotations:
    {{- toYaml . | nindent 4 }}
  {{- end }}
spec:
  type: {{ .Values.service.type }}
  {{- with .Values.service.clusterIP }}
  clusterIP: {{ . }}
  {{- end }}
  {{- if .Values.service.loadBalancerIP }}
  loadBalancerIP: {{ .Values.service.loadBalancerIP }}
  {{- end }}
  {{- with .Values.service.loadBalancerSourceRanges }}
  loadBalancerSourceRanges:
    {{- toYaml . | nindent 4 }}
  {{- end }}
  ports:
    - name: http
      port: {{ .Values.service.port }}
      targetPort: {{ .Values.service.targetPort | default 80 }}
      protocol: TCP
      {{- if and (eq .Values.service.type "NodePort") .Values.service.nodePort }}
      nodePort: {{ .Values.service.nodePort }}
      {{- end }}
  selector:
    {{- include "my-app.selectorLabels" . | nindent 4 }}
```

## Environment-Specific Configuration

### Development Values (values-dev.yaml)
```yaml
# Development environment specific values
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

nodeSelector: {}
tolerations: []
affinity: {}

# Development-specific configurations
livenessProbe:
  enabled: true
  path: "/health"
readinessProbe:
  enabled: true
  path: "/ready"
```

### Production Values (values-prod.yaml)
```yaml
# Production environment specific values
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

## Chart Testing and Validation

### Linting
```bash
# Lint the chart for best practices
helm lint

# Lint with specific values
helm lint --values values-prod.yaml
```

### Template Rendering
```bash
# Render templates locally without installing
helm template my-release .

# Render with custom values
helm template my-release . --values values-prod.yaml

# Render specific templates only
helm template my-release . --show-only templates/deployment.yaml
```

### Testing
```bash
# Run built-in tests
helm test my-release

# Create test templates in templates/tests/
# templates/tests/test-connection.yaml
apiVersion: v1
kind: Pod
metadata:
  name: "{{ include \"my-app.fullname\" . }}-test-connection"
  labels:
    {{- include \"my-app.labels\" . | nindent 4 }}
  annotations:
    "helm.sh/hook": test
spec:
  containers:
    - name: wget
      image: busybox
      command: ['wget']
      args: ['{{ include \"my-app.fullname\" . }}:{{ .Values.service.port }}']
  restartPolicy: Never
```

## Security and Provenance

### Chart Signing
```bash
# Generate a key pair for signing
helm repo add keybase https://keybase.io/charts
helm plugin install https://github.com/technosophos/helm-keybase

# Sign a chart
helm package my-app
helm sign my-app-0.1.0.tgz --keyring ~/.gnupg/secring.gpg

# Verify a signed chart
helm verify my-app-0.1.0.tgz --keyring ~/.gnupg/pubring.gpg
```

### Installation with Verification
```bash
# Install with verification
helm install my-release my-app-0.1.0.tgz --verify
```

## Production Deployment

### Dependency Management
```bash
# Add repositories
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update

# Update dependencies
helm dependency update

# Vendor dependencies
helm dependency build
```

### Deployment Commands
```bash
# Install to specific namespace with creation
helm install my-release . \
  --namespace production \
  --create-namespace

# Install with custom values
helm install my-release . \
  --values values-prod.yaml

# Install with inline value overrides
helm install my-release . \
  --set replicaCount=3 \
  --set image.tag=1.21.0 \
  --set-string nodeSelector.disktype=ssd

# Upgrade release
helm upgrade my-release . \
  --reuse-values \
  --atomic

# Rollback release
helm rollback my-release 1
```

## Publishing Charts

### To Chart Repository
```bash
# Package chart
helm package my-app

# Index repository
helm repo index . --url https://repo.example.com

# Push to repository
# (Implementation depends on repository hosting)
```

### To OCI Registry
```bash
# Enable OCI support
export HELM_EXPERIMENTAL_OCI=1

# Push to OCI registry
helm chart save . my-registry.example.com/my-org/my-app:0.1.0
helm chart push my-registry.example.com/my-org/my-app:0.1.0

# Pull from OCI registry
helm chart pull my-registry.example.com/my-org/my-app:0.1.0

# Install from OCI registry
helm install my-release oci://my-registry.example.com/my-org/my-app --version 0.1.0
```

## Scripts Available

See [HELMT-SCRIPTS.md](references/HELMT-SCRIPTS.md) for automated chart creation and management scripts.

## Security Considerations

See [SECURITY.md](references/SECURITY.md) for detailed security best practices and production hardening techniques.

## Production Best Practices

See [PRODUCTION.md](references/PRODUCTION.md) for production deployment guidelines and optimization strategies.