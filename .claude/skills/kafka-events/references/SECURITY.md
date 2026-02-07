# Kafka Security Best Practices

## Authentication and Authorization

### SASL/SCRAM Configuration
Secure authentication using SCRAM:

```yaml
# Kafka broker configuration for SASL/SCRAM
listeners=SASL_SSL://:9093
security.inter.broker.protocol=SASL_SSL
sasl.mechanism.inter.broker.protocol=SCRAM-SHA-256
sasl.enabled.mechanisms=SCRAM-SHA-256,SCRAM-SHA-512

# Add SCRAM credentials in server.properties or via admin client
# bin/kafka-configs.sh --zookeeper localhost:2181 --alter --add-config 'SCRAM-SHA-256=[iterations=8192,password=alice-secret],SCRAM-SHA-512=[password=alice-secret2]' --entity-type users --entity-name alice
```

### SSL/TLS Configuration
Secure transport layer encryption:

```yaml
# Broker SSL configuration
listeners=SSL://:9093
ssl.keystore.location=/path/to/keystore.jks
ssl.keystore.password=keystore_password
ssl.key.password=key_password
ssl.truststore.location=/path/to/truststore.jks
ssl.truststore.password=truststore_password
ssl.client.auth=required
ssl.enabled.protocols=TLSv1.2,TLSv1.3
ssl.cipher.suites=TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384,TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256
```

### ACL Configuration
Implement fine-grained access control:

```bash
# Create ACL for a specific topic
bin/kafka-acls.sh --bootstrap-server localhost:9092 \
  --add \
  --allow-principal User:myuser \
  --operation Read \
  --topic my-topic

# Create ACL for consumer group
bin/kafka-acls.sh --bootstrap-server localhost:9092 \
  --add \
  --allow-principal User:myuser \
  --operation Read \
  --consumer-group my-consumer-group

# Create ACL for producing to topic
bin/kafka-acls.sh --bootstrap-server localhost:9092 \
  --add \
  --allow-principal User:producer \
  --operation Write \
  --topic my-topic

# List all ACLs
bin/kafka-acls.sh --bootstrap-server localhost:9092 --list
```

## Network Security

### Network Policies
Implement network-level access control:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: kafka-broker-policy
  namespace: kafka
spec:
  podSelector:
    matchLabels:
      app: kafka-broker
  policyTypes:
  - Ingress
  - Egress
  ingress:
  # Allow connections from Kafka clients
  - from:
    - podSelector:
        matchLabels:
          role: kafka-client
    ports:
    - protocol: TCP
      port: 9092
  # Allow connections from other brokers for replication
  - from:
    - podSelector:
        matchLabels:
          app: kafka-broker
    ports:
    - protocol: TCP
      port: 9092
  egress:
  # Allow outbound connections to other brokers
  - to:
    - podSelector:
        matchLabels:
          app: kafka-broker
    ports:
    - protocol: TCP
      port: 9092
```

### Service Security Configuration
Secure service configurations:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: kafka-service
  namespace: kafka
  annotations:
    # Security annotations for service
    service.alpha.kubernetes.io/tolerate-unready-endpoints: "false"
spec:
  type: ClusterIP
  ports:
  - name: plaintext
    port: 9092
    targetPort: 9092
    protocol: TCP
  selector:
    app: kafka-broker
  # Only expose to internal cluster traffic
  clusterIP: None  # For headless service if needed for direct broker access
```

## Data Protection

### Encryption at Rest
Configure encryption for stored data:

```properties
# Enable encryption at rest (requires additional configuration)
# This is typically handled at the storage layer (disk encryption)
# But Kafka can be configured to work with encrypted storage

log.dirs=/encrypted/kafka/logs
# Ensure underlying storage is encrypted
```

### Data Classification and Handling
Implement proper data handling practices:

```java
// Example of secure data processing in Kafka Streams
StreamsBuilder builder = new StreamsBuilder();

KStream<String, String> secureStream = builder.stream("input-topic")
    .mapValues(value -> {
        // Sanitize sensitive data
        String sanitized = sanitizePIIData(value);

        // Encrypt sensitive fields if needed
        String encrypted = encryptSensitiveData(sanitized);

        return encrypted;
    });

// Ensure output to secure topic
secureStream.to("secure-output-topic", Produced.with(Serdes.String(), Serdes.String()));
```

## Security Monitoring

### Audit Logging Configuration
Enable comprehensive audit logging:

```properties
# Enable controller request logging
log4j.logger.kafka.controller=TRACE, controllerAppender
log4j.additivity.kafka.controller=false

# Enable authorizer logging for ACLs
log4j.logger.kafka.authorizer.logger=INFO, authorizerAppender
log4j.additivity.kafka.authorizer.logger=false

# Enable request logging
log4j.logger.kafka.request.logger=WARN, requestAppender
log4j.additivity.kafka.request.logger=false
```

### Security Event Detection
Monitor for security events:

```bash
# Monitor for authentication failures
kubectl logs -f kafka-broker-pod | grep -i "authentication failed\|authorization denied"

# Check for unauthorized access attempts
bin/kafka-acls.sh --bootstrap-server localhost:9092 --list | grep -i suspicious-user

# Monitor for configuration changes
kubectl get events --field-selector involvedObject.kind=Kafka --sort-by='.lastTimestamp'
```

## Secure Configuration Patterns

### Minimal Permissions Pattern
Implement principle of least privilege:

```yaml
# Role for Kafka application with minimal permissions
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: kafka
  name: kafka-app-role
rules:
# Only allow access to specific topics
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list", "watch"]
# Allow access to configmaps for configuration
- apiGroups: [""]
  resources: ["configmaps"]
  resourceNames: ["kafka-config"]  # Specific configmap only
  verbs: ["get"]
# Allow access to secrets for credentials
- apiGroups: [""]
  resources: ["secrets"]
  resourceNames: ["kafka-credentials"]  # Specific secret only
  verbs: ["get"]
---
# RoleBinding with minimal scope
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: kafka-app-rolebinding
  namespace: kafka
subjects:
- kind: ServiceAccount
  name: kafka-app-sa
  namespace: kafka
roleRef:
  kind: Role
  name: kafka-app-role
  apiGroup: rbac.authorization.k8s.io
```

### Secure Client Configuration
Configure clients with security in mind:

```java
// Secure consumer configuration
Properties props = new Properties();
props.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, "kafka-cluster:9093"); // SSL port
props.put(ConsumerConfig.GROUP_ID_CONFIG, "secure-consumer-group");
props.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, "org.apache.kafka.common.serialization.StringDeserializer");
props.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, "org.apache.kafka.common.serialization.StringDeserializer");

// Security configuration
props.put(CommonClientConfigs.SECURITY_PROTOCOL_CONFIG, "SASL_SSL");
props.put(SaslConfigs.SASL_MECHANISM, "SCRAM-SHA-256");
props.put(SaslConfigs.SASL_JAAS_CONFIG,
    "org.apache.kafka.common.security.scram.ScramLoginModule required " +
    "username=\"secure-user\" " +
    "password=\"${SECRET_PASSWORD}\";");

// Additional security settings
props.put(ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG, false);
props.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");
props.put(ConsumerConfig.MAX_POLL_RECORDS_CONFIG, 100);
```

### Vulnerability Management
Regular security maintenance procedures:

```bash
# Check for known vulnerabilities in Kafka images
trivy image confluentinc/cp-kafka:latest

# Verify Kafka version security patches
bin/kafka-topics.sh --bootstrap-server localhost:9092 --describe --topic __consumer_offsets

# Monitor for security advisories
# Subscribe to Kafka security mailing list
# Check Confluent/CVE databases regularly

# Verify certificate expiration
openssl x509 -in /path/to/broker-cert.pem -text -noout | grep -A 2 "Validity"
```

## Health Check Security Considerations

### Secure Health Endpoint Implementation
Implement secure health checks:

```java
@RestController
public class SecureHealthController {

    @Autowired
    private KafkaTemplate<String, String> kafkaTemplate;

    @Value("${security.health.check.enabled:true}")
    private boolean healthCheckEnabled;

    @GetMapping(path = "/healthz", produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<Map<String, Object>> secureHealthCheck() {
        if (!healthCheckEnabled) {
            return ResponseEntity.status(HttpStatus.FORBIDDEN).build();
        }

        Map<String, Object> health = new HashMap<>();

        try {
            // Perform minimal security-safe checks
            // Don't expose sensitive information

            // Test basic Kafka connectivity
            kafkaTemplate.send("health-test", "ping");

            health.put("status", "UP");
            health.put("kafka", "CONNECTED");
            health.put("timestamp", Instant.now().toString());

            // Don't include detailed broker information in health check
            return ResponseEntity.ok(health);
        } catch (Exception e) {
            health.put("status", "DOWN");
            health.put("kafka", "DISCONNECTED");
            // Don't expose error details in production
            return ResponseEntity.status(HttpStatus.SERVICE_UNAVAILABLE).body(health);
        }
    }
}
```

### Probe Security Configuration
Secure configuration for Kubernetes probes:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: secure-kafka-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: secure-kafka-app
  template:
    metadata:
      labels:
        app: secure-kafka-app
    spec:
      containers:
      - name: app
        image: secure-kafka-app:latest
        # Secure probe configuration
        livenessProbe:
          httpGet:
            path: /healthz
            port: 8080
            scheme: HTTPS  # Use HTTPS for health checks
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /readyz
            port: 8080
            scheme: HTTPS
          initialDelaySeconds: 10
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
        # Security context for the container
        securityContext:
          runAsNonRoot: true
          runAsUser: 1000
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          capabilities:
            drop:
            - ALL
        env:
        - name: KAFKA_SECURITY_PROTOCOL
          value: "SASL_SSL"
        - name: KAFKA_SASL_MECHANISM
          value: "SCRAM-SHA-256"
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
```

Following these security practices will significantly improve the security posture of your Kafka deployments.