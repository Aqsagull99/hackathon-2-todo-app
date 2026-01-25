# Helm Chart Security Best Practices for Kubernetes Applications

This document outlines security best practices for Helm charts in Kubernetes applications, particularly for production deployments.

## Security Hardening Techniques

### 1. Secure Pod Security Context

Always define security contexts to limit container privileges:

```yaml
# In values.yaml
podSecurityContext:
  fsGroup: 2000

securityContext:
  capabilities:
    drop:
    - ALL
  readOnlyRootFilesystem: true
  runAsNonRoot: true
  runAsUser: 1000
  runAsGroup: 3000
```

```yaml
# In deployment template
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "my-app.fullname" . }}
spec:
  template:
    spec:
      securityContext:
        {{- toYaml .Values.podSecurityContext | nindent 8 }}
      containers:
        - name: {{ .Chart.Name }}
          securityContext:
            {{- toYaml .Values.securityContext | nindent 12 }}
```

### 2. Image Security

Use verified and trusted base images:

```yaml
# In values.yaml
image:
  repository: nginx
  pullPolicy: IfNotPresent
  tag: "1.21.6-alpine"  # Pin to specific version
  pullSecrets:
    - name: regcred  # Use image pull secrets
```

### 3. Resource Limits

Define resource quotas to prevent resource exhaustion:

```yaml
# In values.yaml
resources:
  limits:
    cpu: 100m
    memory: 128Mi
  requests:
    cpu: 50m
    memory: 64Mi
```

### 4. Network Policies

Implement network policies for traffic control:

```yaml
# templates/networkpolicy.yaml
{{- if .Values.networkPolicy.enabled }}
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: {{ include "my-app.fullname" . }}
spec:
  podSelector:
    matchLabels:
      {{- include "my-app.selectorLabels" . | nindent 6 }}
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          {{- include "my-app.selectorLabels" . | nindent 10 }}
    ports:
    - protocol: TCP
      port: 80
  egress:
  - to: []
    ports:
    - protocol: UDP
      port: 53
    - protocol: TCP
      port: 53
{{- end }}
```

## Chart Signing and Verification

### 1. Provenance Files

Sign charts to ensure integrity:

```bash
# Generate GPG key for signing
gpg --gen-key

# Package and sign chart
helm package my-chart
helm sign my-chart-0.1.0.tgz

# Verify signed chart
helm verify my-chart-0.1.0.tgz
```

### 2. Install with Verification

Always verify charts before installation:

```bash
# Install with verification
helm install my-release my-chart-0.1.0.tgz --verify

# Verify chart from repository
helm install my-release my-repo/my-chart --verify
```

## Security Scanning

### 1. Template Security Analysis

Check templates for security issues:

```bash
# Use conftest for policy validation
# Install conftest
go install github.com/open-policy-agent/conftest/cmd/conftest@latest

# Create policy file (policy/rendered.rego)
package main

deny[msg] {
  input.kind == "Deployment"
  some i
  input.spec.template.spec.containers[i].securityContext.privileged == true
  msg := "privileged containers are not allowed"
}

# Test chart templates
helm template . | conftest test -
```

### 2. Static Analysis

Use tools like Kubesec or Datree for security analysis:

```bash
# Install kubesec scanner
npm install -g kubesec

# Scan rendered templates
helm template my-release . | kubesec scan -
```

## Production Security Configuration

### Complete Secure Deployment Template

```yaml
# templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "my-app.fullname" . }}
  labels:
    {{- include "my-app.labels" . | nindent 4 }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      {{- include "my-app.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      labels:
        {{- include "my-app.selectorLabels" . | nindent 8 }}
      {{- with .Values.podAnnotations }}
      annotations:
        {{- toYaml . | nindent 8 }}
      {{- end }}
    spec:
      {{- with .Values.imagePullSecrets }}
      imagePullSecrets:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      serviceAccountName: {{ include "my-app.serviceAccountName" . }}
      automountServiceAccountToken: false  # Disable SA token auto-mount
      securityContext:
        {{- toYaml .Values.podSecurityContext | nindent 8 }}
      containers:
        - name: {{ .Chart.Name }}
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            runAsNonRoot: true
            runAsUser: 1000
            runAsGroup: 3000
            capabilities:
              drop:
              - ALL
              add:
              - NET_BIND_SERVICE  # Only add required capabilities
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          ports:
            - name: http
              containerPort: 80
              protocol: TCP
          livenessProbe:
            httpGet:
              path: /
              port: http
          readinessProbe:
            httpGet:
              path: /
              port: http
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
          {{- with .Values.env }}
          env:
            {{- toYaml . | nindent 12 }}
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
```

### Service Account with Minimal Permissions

```yaml
# templates/serviceaccount.yaml
{{- if .Values.serviceAccount.create -}}
apiVersion: v1
kind: ServiceAccount
metadata:
  name: {{ include "my-app.serviceAccountName" . }}
  labels:
    {{- include "my-app.labels" . | nindent 4 }}
  {{- with .Values.serviceAccount.annotations }}
  annotations:
    {{- toYaml . | nindent 4 }}
  {{- end }}
automountServiceAccountToken: {{ .Values.serviceAccount.automount }}
{{- end }}
```

## Additional Security Measures

### 1. RBAC Configuration

Define minimal required permissions:

```yaml
# templates/rbac.yaml
{{- if .Values.rbac.create }}
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: {{ include "my-app.fullname" . }}
rules:
- apiGroups: [""]
  resources: ["pods", "services"]
  verbs: ["get", "list"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: {{ include "my-app.fullname" . }}
subjects:
- kind: ServiceAccount
  name: {{ include "my-app.serviceAccountName" . }}
roleRef:
  kind: Role
  name: {{ include "my-app.fullname" . }}
  apiGroup: rbac.authorization.k8s.io
{{- end }}
```

### 2. Secrets Management

Securely manage secrets:

```yaml
# Use external secrets managers like External Secrets or HashiCorp Vault
# templates/externalsecret.yaml
{{- if .Values.externalSecrets.enabled }}
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: {{ include "my-app.fullname" . }}
spec:
  provider:
    aws:
      service: SecretsManager
      region: {{ .Values.aws.region }}
{{- end }}
```

### 3. Admission Controllers

Use OPA Gatekeeper or Kyverno for policy enforcement:

```yaml
# Example constraint template
apiVersion: templates.gatekeeper.sh/v1beta1
kind: ConstraintTemplate
metadata:
  name: k8srequiredlabels
spec:
  crd:
    spec:
      names:
        kind: K8sRequiredLabels
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8srequiredlabels

        violation[{"msg": msg, "details": {"missing_labels": missing}}] {
          provided := {label | input.review.object.metadata.labels[label]}
          required := {label | label := input.parameters.labels[_]}
          missing := required - provided
          count(missing) > 0
          msg := sprintf("you must provide labels: %v", [missing])
        }
```

Following these security practices will significantly improve the security posture of your Helm chart deployments.