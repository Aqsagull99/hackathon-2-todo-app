# Dapr Configuration Reference

## Component Types

### State Store Components

#### Redis State Store
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: redis-statestore
spec:
  type: state.redis
  version: v1
  metadata:
  - name: redisHost
    value: redis-master:6379
  - name: redisPassword
    secretKeyRef:
      name: redis-password
      key: redis-password
  - name: actorStateStore
    value: "true"
  - name: keyPrefix
    value: "myapp"
```

#### Azure Cosmos DB State Store
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: cosmosdb-statestore
spec:
  type: state.azure.cosmosdb
  version: v1
  metadata:
  - name: url
    value: "[your cosmos db url]"
  - name: masterKey
    value: "[your master key]"
  - name: database
    value: "[your database name]"
  - name: collection
    value: "[your collection name]"
```

### Pub/Sub Components

#### Redis Pub/Sub
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: redis-pubsub
spec:
  type: pubsub.redis
  version: v1
  metadata:
  - name: redisHost
    value: localhost:6379
  - name: redisPassword
    value: ""
  - name: consumerID
    value: "myapp"
```

#### Apache Kafka Pub/Sub
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kafka-pubsub
spec:
  type: pubsub.kafka
  version: v1
  metadata:
  - name: brokers
    value: "localhost:9092"
  - name: consumerGroup
    value: "myapp"
  - name: clientID
    value: "myapp"
  - name: authRequired
    value: "false"
```

### Secret Store Components

#### Azure Key Vault
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: azure-keyvault
spec:
  type: secretstores.azure.keyvault
  version: v1
  metadata:
  - name: vaultName
    value: "[your-vault-name]"
  - name: tenantId
    value: "[your-tenant-id]"
  - name: spnClientId
    value: "[your-service-principal-client-id]"
  - name: spnClientSecret
    value: "[your-service-principal-client-secret]"
```

#### HashiCorp Vault
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: hashicorp-vault
spec:
  type: secretstores.hashicorp.vault
  version: v1
  metadata:
  - name: vaultAddr
    value: "https://localhost:8200"
  - name: skipVerify
    value: "false"
  - name: scheme
    value: "https"
  - name: mountPath
    value: "secret"
  - name: keyPrefix
    value: "dapr"
```

## Configuration Options

### Dapr Configuration File
```yaml
apiVersion: dapr.io/v1alpha1
kind: Configuration
metadata:
  name: appconfig
spec:
  tracing:
    samplingRate: "1"
    zipkin:
      endpointAddress: "http://zipkin.default.svc.cluster.local:9411/api/v2/spans"
  metric:
    enabled: true
  httpPipeline:
    handlers:
    - name: uppercase
      type: middleware.http.uppercase
  accessControl:
    defaultAction: allow
    trustDomain: "pubdomain"
    policies:
    - appId: app1
      defaultAction: allow
      trustDomain: "pubdomain"
      namespace: "default"
  features:
  - name: AppHealthCheck
    enabled: true
  - name: InputBindingInvocation
    enabled: true
```

## Dapr Runtime Configuration

### Actor Configuration
```yaml
apiVersion: dapr.io/v1alpha1
kind: Configuration
metadata:
  name: actor-config
spec:
  actors:
    actorIdleTimeout: 1h
    actorScanInterval: 30s
    drainOngoingCallTimeout: 1m
    drainRebalancedActors: true
    reentrancy:
      enabled: true
      maxStackDepth: 32
    remindersStoragePartitions: 0
```

## Environment-Specific Deployments

### Kubernetes Annotations

#### Essential Dapr Annotations
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  template:
    metadata:
      annotations:
        dapr.io/enabled: "true"          # Required: Enables Dapr sidecar injection
        dapr.io/app-id: "myapp"          # Required: Unique application ID for service discovery
        dapr.io/app-port: "3000"         # Required: Port where your app is listening
        dapr.io/config: "appconfig"      # Optional: Dapr configuration to use
        dapr.io/enable-metrics: "true"   # Optional: Enable Prometheus metrics
        dapr.io/metrics-port: "9090"     # Optional: Metrics port
```

#### Advanced Dapr Annotations
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  template:
    metadata:
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "myapp"
        dapr.io/app-port: "3000"
        # Port configurations
        dapr.io/grpc-port: "50001"                      # Dapr gRPC API port
        dapr.io/http-port: "3500"                       # Dapr HTTP API port (deprecated, use resource limits instead)

        # Resource limits
        dapr.io/sidecar-cpu-limit: "4.0"
        dapr.io/sidecar-cpu-request: "0.1"
        dapr.io/sidecar-memory-limit: "512Mi"
        dapr.io/sidecar-memory-request: "256Mi"

        # Logging and debugging
        dapr.io/log-as-json: "true"
        dapr.io/enable-debug: "true"
        dapr.io/debug-port: "40000"
        dapr.io/enable-api-logging: "true"

        # Security
        dapr.io/disable-builtin-k8s-secret-store: "false"
        dapr.io/api-token-secret: "dapr-api-token"
        dapr.io/app-token-secret: "dapr-app-token"

        # Networking
        dapr.io/sidecar-listen-addresses: "127.0.0.1"
        dapr.io/unix-domain-socket-path: "/tmp/dapr-sockets"

        # Probes
        dapr.io/sidecar-liveness-probe-delay-seconds: "3"
        dapr.io/sidecar-liveness-probe-timeout-seconds: "3"
        dapr.io/sidecar-liveness-probe-period-seconds: "6"
        dapr.io/sidecar-readiness-probe-delay-seconds: "3"
        dapr.io/sidecar-readiness-probe-timeout-seconds: "3"
        dapr.io/sidecar-readiness-probe-period-seconds: "6"
```

### Dapr Sidecar Ports Reference

#### Standard Dapr Ports
- **HTTP API Port**: 3500 (default) - For HTTP API calls to Dapr
- **gRPC API Port**: 50001 (default) - For gRPC API calls to Dapr
- **Internal gRPC Port**: 50002 (default) - For internal Dapr-to-Dapr communication
- **Metrics Port**: 9090 (default) - For Prometheus metrics
- **Debug Port**: 40000 (default) - For debugging

#### Custom Port Configuration
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  template:
    metadata:
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "myapp"
        dapr.io/app-port: "3000"
        # Custom port assignments
        dapr.io/grpc-port: "50003"       # Custom gRPC API port
        dapr.io/internal-grpc-port: "50004"  # Custom internal gRPC port
        dapr.io/metrics-port: "9091"     # Custom metrics port
```

### Container Mode vs Process Mode Configuration

#### Process Mode (Self-Hosted)
```bash
# Running in process mode with Dapr CLI
dapr run --app-id myapp --app-port 3000 --dapr-http-port 3500 --dapr-grpc-port 50001 node app.js

# Or with Docker container for Dapr sidecar, host process for app
docker run --net="host" --mount type=bind,source="$(pwd)"/components,target=/components \
  daprio/daprd:edge ./daprd -app-id myapp -app-port 3000
```

#### Container Mode (Kubernetes)
```yaml
# In Kubernetes, the sidecar is automatically injected as a container
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "myapp"
        dapr.io/app-port: "3000"
    spec:
      containers:
      - name: myapp           # Your application container
        image: myapp:latest
        ports:
        - containerPort: 3000
      # Dapr sidecar container is automatically injected by the Dapr operator
      # No need to define it explicitly
```

### Resource Limits for Dapr Sidecar
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  template:
    spec:
      containers:
      - name: myapp
        image: myapp:latest
      # The Dapr sidecar container is injected automatically
      # Resource limits are applied via annotations
      # No need to define the daprd container explicitly

## Production Deployment Patterns

### Multi-App Run Configuration
```yaml
# apps.yaml
version: 1
apps:
- appDirPath: app1
  appPort: 3000
  appProtocol: http
  appID: app1
  daprHTTPPort: 3501
  daprGRPCPort: 50001
  command: ["node", "app.js"]
- appDirPath: app2
  appPort: 4000
  appProtocol: http
  appID: app2
  daprHTTPPort: 3502
  daprGRPCPort: 50002
  command: ["python", "app.py"]
```

### Dapr Placement Service Configuration (for Actors)
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: dapr-placement
spec:
  replicas: 3
  selector:
    matchLabels:
      app: dapr-placement
  template:
    metadata:
      labels:
        app: dapr-placement
    spec:
      containers:
      - name: placement
        image: daprio/placement:1.12.0
        ports:
        - containerPort: 50005
        - containerPort: 8080
        resources:
          limits:
            cpu: "1000m"
            memory: "256Mi"
          requests:
            cpu: "100m"
            memory: "128Mi"
```