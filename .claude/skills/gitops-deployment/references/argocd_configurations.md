# ArgoCD Configuration Reference

## Application CRD Examples

### Basic Application
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: guestbook
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/argoproj/argocd-example-apps.git
    targetRevision: HEAD
    path: guestbook
  destination:
    server: https://kubernetes.default.svc
    namespace: guestbook
  syncPolicy:
    automated:
      prune: false
      selfHeal: false
```

### Application with Helm
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: guestbook-helm
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/argoproj/argocd-example-apps.git
    targetRevision: HEAD
    path: helm-guestbook
    helm:
      valueFiles:
      - values.yaml
      - values-prod.yaml
      parameters:
      - name: "image.tag"
        value: "1.9.1"
      - name: "ingress.enabled"
        value: "true"
      - name: "ingress.hosts[0]"
        value: "mydomain.com"
  destination:
    server: https://kubernetes.default.svc
    namespace: guestbook
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

### Application with Kustomize
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: guestbook-kustomize
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/argoproj/argocd-example-apps.git
    targetRevision: HEAD
    path: kustomize-guestbook
    kustomize:
      namePrefix: prod-
      nameSuffix: -v1
      images:
      - gcr.io/heptio-images/ks-guestbook-demo:0.1
      replicas:
      - name: guestbook-ui
        count: 2
  destination:
    server: https://kubernetes.default.svc
    namespace: guestbook
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

### Multi-Source Application
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: multi-source-app
spec:
  project: default
  sources:
  - repoURL: https://github.com/argoproj/argocd-example-apps.git
    targetRevision: HEAD
    path: guestbook
  - repoURL: https://github.com/argoproj/argocd-example-apps.git
    targetRevision: HEAD
    path: kustomize-guestbook
    kustomize:
      namePrefix: prod-
  destination:
    server: https://kubernetes.default.svc
    namespace: guestbook
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

## AppProject CRD Examples

### Development Project
```yaml
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata:
  name: development
  namespace: argocd
spec:
  description: Development project
  sourceRepos:
  - '*'
  destinations:
  - namespace: dev-*
    server: https://kubernetes.default.svc
  clusterResourceWhitelist:
  - group: '*'
    kind: Namespace
  namespaceResourceBlacklist:
  - group: ''
    kind: ResourceQuota
  roles:
  - name: developers
    policies:
    - p, proj:development:developers, applications, *, development/*, allow
    groups:
    - developers@example.com
```

### Production Project
```yaml
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata:
  name: production
  namespace: argocd
spec:
  description: Production project
  sourceRepos:
  - https://github.com/mycompany/production-apps.git
  destinations:
  - namespace: production
    server: https://kubernetes.default.svc
  clusterResourceWhitelist:
  - group: ''
    kind: Namespace
  namespaceResourceWhitelist:
  - group: 'apps'
    kind: Deployment
  - group: 'apps'
    kind: StatefulSet
  - group: ''
    kind: Service
  - group: ''
    kind: ConfigMap
  roles:
  - name: ops-team
    policies:
    - p, proj:production:ops-team, applications, *, production/*, allow
    groups:
    - ops@example.com
  - name: ci-cd
    policies:
    - p, proj:production:ci-cd, applications, sync, production/*, allow
    - p, proj:production:ci-cd, applications, update, production/*, allow
    jwtTokens:
    - iat: 1620000000
      exp: 1620086400
```

## Repository and Cluster Configuration

### Repository with SSH Key
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: private-repo-ssh
  namespace: argocd
  labels:
    argocd.argoproj.io/secret-type: repository
stringData:
  type: git
  url: git@github.com:myorg/myapp.git
  sshPrivateKey: |
    -----BEGIN OPENSSH PRIVATE KEY-----
    ...
    -----END OPENSSH PRIVATE KEY-----
```

### Repository with TLS Certificate
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: private-repo-tls
  namespace: argocd
  labels:
    argocd.argoproj.io/secret-type: repository
stringData:
  type: git
  url: https://private-git.company.com/myorg/myapp.git
  tlsClientCertData: |
    -----BEGIN CERTIFICATE-----
    ...
    -----END CERTIFICATE-----
  tlsClientCertKey: |
    -----BEGIN RSA PRIVATE KEY-----
    ...
    -----END RSA PRIVATE KEY-----
```

### Cluster Configuration
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: my-cluster
  namespace: argocd
  labels:
    argocd.argoproj.io/secret-type: cluster
data:
  name: bXktY2x1c3Rlcg==
  server: aHR0cHM6Ly9rdWJlcm5ldGVzLWRlZmF1bHQuc3Zj
  config: |
    {
      "tlsClientConfig": {
        "insecure": false,
        "caData": "..."
      },
      "bearerToken": "..."
    }
```

## Sync Options and Policies

### Sync Options Reference
- **Prune=true/false**: Whether to delete resources that are no longer in Git
- **CreateNamespace=true/false**: Whether to create the destination namespace if it doesn't exist
- **Validate=true/false**: Whether to validate resources before applying
- **ServerSideApply=true/false**: Whether to use server-side apply for merging resources
- **ApplyOutOfSyncOnly=true/false**: Only apply resources that are out of sync
- **Replace=true/false**: Replace resources instead of applying
- **Force=true/false**: Force apply resources (equivalent to --force flag)
- **RespectIgnoreDifferences=true/false**: Respect ignore differences configuration

### Advanced Sync Policy
```yaml
spec:
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
      allowEmpty: false
    syncOptions:
    - CreateNamespace=true
    - PruneLast=true
    - RespectIgnoreDifferences=true
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m
```

## RBAC Configuration

### ArgoCD RBAC Configuration
```yaml
# argocd-rbac-cm.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-rbac-cm
  namespace: argocd
data:
  policy.csv: |
    # Grant all members of the group 'argocd-admins' admin privileges
    g, argocd-admins, role:admin
    # Grant all members of the group 'argocd-developers' read privileges to all applications
    g, argocd-developers, role:readonly
    # Grant specific user 'alice' admin privileges to applications in 'my-project'
    p, alice, applications, *, my-project/*, allow
  policy.default: role:readonly
  scopes: '[groups]'
```

### Built-in Roles
- **role:readonly**: Read-only access to all resources
- **role:admin**: Admin access to all resources
- **applications**: Application-specific permissions
- **projects**: Project-specific permissions
- **clusters**: Cluster-specific permissions
- **repositories**: Repository-specific permissions
- **certificates**: Certificate-specific permissions
- **accounts**: Account-specific permissions

## Quality Gate and Testing Configurations

### Custom Health Check Definitions
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-cm
  namespace: argocd
data:
  # Custom health check for custom resources
  resource.customizations.health.argoproj.io_Application: |
    hs = {}
    hs.status = "Progressing"
    hs.message = ""
    if obj.status ~= nil then
      if obj.status.health ~= nil then
        hs.status = obj.status.health.status
        if obj.status.health.message ~= nil then
          hs.message = obj.status.health.message
        end
      end
    end
    return hs

  # Custom health check for ingresses
  resource.customizations.health.networking.k8s.io_Ingress: |
    hs = {}
    if obj.status ~= nil then
      if obj.status.loadBalancer ~= nil then
        if obj.status.loadBalancer.ingress ~= nil then
          hs.status = "Healthy"
          hs.message = "Ingress has load balancer endpoints"
          return hs
        end
      end
    end
    hs.status = "Progressing"
    hs.message = "Waiting for load balancer to be available"
    return hs
```

### Sync Options for Quality Gates
```yaml
spec:
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
      allowEmpty: false
    syncOptions:
    - CreateNamespace=true
    - PruneLast=true
    - RespectIgnoreDifferences=true
    - Validate=false  # Set to false for CRDs that aren't available yet
    - ApplyOutOfSyncOnly=true
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m
```

## Rollback Configuration Examples

### Application with Rollback Configuration
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: rollback-ready-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/myorg/myapp.git
    targetRevision: HEAD
    path: manifests
    helm:
      valueFiles:
      - values.yaml
      parameters:
      - name: image.tag
        value: "v1.2.3"  # Versioned artifact
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    retry:
      limit: 3
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m
  ignoreDifferences:
  - group: apps
    kind: Deployment
    jsonPointers:
    - /status
  - group: ""
    kind: Service
    jsonPointers:
    - /metadata/annotations
```

### ApplicationSet with Progressive Rollout
```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: progressive-deployment
  namespace: argocd
spec:
  generators:
    - list:
        elements:
          - cluster: dev-cluster
            url: https://dev-k8s.example.com
            env: dev
          - cluster: staging-cluster
            url: https://staging-k8s.example.com
            env: staging
          - cluster: prod-cluster
            url: https://prod-k8s.example.com
            env: prod
  strategy:
    type: RollingSync
    rollingSync:
      steps:
        - matchExpressions:
            - key: env
              operator: In
              values:
                - dev
        - matchExpressions:
            - key: env
              operator: In
              values:
                - staging
          maxUpdate: 0  # Pause here for validation
        - matchExpressions:
            - key: env
              operator: In
              values:
                - prod
          maxUpdate: 1  # Update one at a time
  template:
    metadata:
      name: '{{cluster}}-app'
      labels:
        env: '{{env}}'
    spec:
      project: default
      source:
        repoURL: https://github.com/myorg/myapp.git
        targetRevision: HEAD
        path: 'manifests/{{env}}'
      destination:
        server: '{{url}}'
        namespace: myapp
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
        syncOptions:
        - CreateNamespace=true
```

## ArgoCD Server Configuration

### ArgoCD ConfigMap
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-cmd-params-cm
  namespace: argocd
data:
  # Server configuration
  server.insecure: "true"
  server.basehref: "/"
  server.rootpath: ""
  # Repository server configuration
  reposerver.parallelism.limit: "0"
  # Application controller configuration
  controller.operation.processors: "10"
  controller.repo.server.timeout.seconds: "60"
```

## Notifications Configuration

### ArgoCD Notifications
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-notifications-cm
  namespace: argocd
data:
  # Trigger definitions
  trigger.on-sync-status-unknown: |
    - when: app.status.sync.status == 'Unknown'
      send: [app-sync-failed]
  trigger.on-health-degraded: |
    - when: app.status.health.status == 'Degraded'
      send: [app-health-degraded]
  trigger.on-sync-failed: |
    - when: app.status.operationState.phase == 'Failed'
      send: [app-sync-failed]
  trigger.on-sync-succeeded: |
    - when: app.status.operationState.phase == 'Succeeded'
      send: [app-sync-success]

  # Template definitions
  template.app-sync-failed: |
    message: Application {{.app.metadata.name}} sync failed.
    slack:
      attachments: |
        [{
          "title": "{{.app.metadata.name}} sync failed",
          "color": "#FF0000",
          "fields": [
            {
              "title": "Error",
              "value": "{{.app.status.operationState.syncResult.revision}}"
            }
          ]
        }]
  template.app-health-degraded: |
    message: Application {{.app.metadata.name}} is degraded.
    slack:
      attachments: |
        [{
          "title": "{{.app.metadata.name}} is degraded",
          "color": "#FFCC00"
        }]
  template.app-sync-success: |
    message: Application {{.app.metadata.name}} sync succeeded.
    slack:
      attachments: |
        [{
          "title": "{{.app.metadata.name}} sync succeeded",
          "color": "#00FF00",
          "fields": [
            {
              "title": "Revision",
              "value": "{{.app.status.operationState.syncResult.revision}}"
            }
          ]
        }]
```