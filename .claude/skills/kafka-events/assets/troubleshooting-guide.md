# Kafka Health Probes Troubleshooting Guide

## Common Health Probe Issues and Solutions

### 1. Liveness Probe Failures

#### Symptoms
- Pod restarts due to liveness probe failures
- Application appears healthy but probe endpoint returns errors

#### Diagnosis Commands
```bash
# Check liveness probe failures in events
kubectl get events --field-selector involvedObject.kind=Pod,reason=Unhealthy -n <namespace>

# Check pod status and events
kubectl describe pod <pod-name> -n <namespace>

# Check application logs around restart times
kubectl logs <pod-name> -n <namespace> --previous

# Test the health endpoint directly
kubectl port-forward <pod-name> 8080:8080 -n <namespace>
curl http://localhost:8080/healthz
```

#### Solutions
1. **Increase probe timeouts for AI applications with slow initialization:**
```yaml
livenessProbe:
  httpGet:
    path: /healthz
    port: 8080
  initialDelaySeconds: 180  # Increased for AI model loading
  periodSeconds: 30
  timeoutSeconds: 15        # Increased for slow AI operations
  failureThreshold: 5       # Increased to prevent false positives
```

2. **Implement proper health check logic:**
```java
@GetMapping("/healthz")
public ResponseEntity<Map<String, Object>> healthCheck() {
    Map<String, Object> health = new HashMap<>();

    try {
        // Check Kafka connectivity
        kafkaTemplate.send("health-check-topic", "health-ping");

        // For AI applications, check model availability
        if (isAIModelReady()) {
            health.put("status", "UP");
            health.put("kafka", "CONNECTED");
            health.put("ai_model", "LOADED");
            return ResponseEntity.ok(health);
        } else {
            health.put("status", "PARTIAL");
            health.put("kafka", "CONNECTED");
            health.put("ai_model", "LOADING");
            return ResponseEntity.status(HttpStatus.SERVICE_UNAVAILABLE).body(health);
        }
    } catch (Exception e) {
        health.put("status", "DOWN");
        health.put("error", e.getMessage());
        return ResponseEntity.status(HttpStatus.SERVICE_UNAVAILABLE).body(health);
    }
}
```

### 2. Readiness Probe Failures

#### Symptoms
- Pod not receiving traffic despite being healthy
- Service endpoints not including the pod

#### Diagnosis Commands
```bash
# Check readiness status
kubectl get pods -n <namespace> -o jsonpath='{.items[*].status.conditions[?(@.type=="Ready")]}'

# Check service endpoints
kubectl get endpoints <service-name> -n <namespace>

# Test readiness endpoint
kubectl exec <pod-name> -n <namespace> -- curl -s http://localhost:8080/readyz
```

#### Solutions
1. **Adjust readiness probe for AI model loading:**
```yaml
readinessProbe:
  httpGet:
    path: /readyz
    port: 8080
  initialDelaySeconds: 120  # Allow for AI model loading
  periodSeconds: 10
  timeoutSeconds: 10
  failureThreshold: 3
  successThreshold: 1
```

2. **Implement comprehensive readiness checks:**
```java
@GetMapping("/readyz")
public ResponseEntity<Map<String, Object>> readinessCheck() {
    Map<String, Object> readiness = new HashMap<>();

    try {
        // Check Kafka connectivity
        boolean kafkaReady = checkKafkaConnectivity();

        // For AI applications, check model readiness
        boolean aiReady = isAIModelReady();

        // Check other dependencies
        boolean dbReady = checkDatabaseConnection();

        if (kafkaReady && aiReady && dbReady) {
            readiness.put("status", "READY");
            readiness.put("kafka", "READY");
            readiness.put("ai_model", "READY");
            readiness.put("database", "READY");
            return ResponseEntity.ok(readiness);
        } else {
            readiness.put("status", "NOT_READY");
            readiness.put("kafka", kafkaReady);
            readiness.put("ai_model", aiReady);
            readiness.put("database", dbReady);
            return ResponseEntity.status(HttpStatus.SERVICE_UNAVAILABLE).body(readiness);
        }
    } catch (Exception e) {
        readiness.put("status", "ERROR");
        readiness.put("error", e.getMessage());
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(readiness);
    }
}
```

### 3. Startup Probe Issues

#### Symptoms
- Pod fails to start within the default timeout
- AI applications with slow model loading fail to become ready

#### Diagnosis Commands
```bash
# Check startup probe failures
kubectl describe pod <pod-name> -n <namespace> | grep -A 10 -B 10 "Startup"

# Check startup times
kubectl get pod <pod-name> -n <namespace> -o jsonpath='{.status.containerStatuses[0].state}'

# Monitor startup progress
kubectl logs <pod-name> -n <namespace> | head -50
```

#### Solutions
1. **Configure appropriate startup probe for AI applications:**
```yaml
startupProbe:
  httpGet:
    path: /startup
    port: 8080
  initialDelaySeconds: 30
  periodSeconds: 15           # Check every 15 seconds
  timeoutSeconds: 10
  failureThreshold: 40        # Allow up to 10 minutes (40 * 15s) for startup
  successThreshold: 1
```

2. **Implement startup endpoint for AI applications:**
```java
@GetMapping("/startup")
public ResponseEntity<Map<String, Object>> startupCheck() {
    Map<String, Object> startup = new HashMap<>();

    try {
        // Check if AI model is loaded
        if (isAIModelLoaded() && isKafkaConnected()) {
            startup.put("status", "STARTED");
            startup.put("ai_model", "LOADED");
            startup.put("kafka", "CONNECTED");
            return ResponseEntity.ok(startup);
        } else {
            startup.put("status", "STARTING");
            startup.put("ai_model_loaded", isAIModelLoaded());
            startup.put("kafka_connected", isKafkaConnected());
            return ResponseEntity.status(HttpStatus.SERVICE_UNAVAILABLE).body(startup);
        }
    } catch (Exception e) {
        startup.put("status", "ERROR");
        startup.put("error", e.getMessage());
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(startup);
    }
}
```

## Kafka-Specific Health Checks

### Consumer Lag Monitoring
Monitor consumer lag in health endpoints:

```java
@Component
public class ConsumerLagHealthIndicator implements HealthIndicator {

    private final KafkaConsumer<String, String> consumer;

    @Override
    public Health health() {
        try {
            // Get consumer lag metrics
            Map<TopicPartition, Long> endOffsets = consumer.endOffsets(consumer.assignment());
            Map<TopicPartition, OffsetAndMetadata> committedOffsets = consumer.committed(consumer.assignment());

            long maxLag = 0;
            for (TopicPartition tp : consumer.assignment()) {
                long endOffset = endOffsets.get(tp);
                OffsetAndMetadata committedOffset = committedOffsets.get(tp);

                if (committedOffset != null) {
                    long lag = endOffset - committedOffset.offset();
                    maxLag = Math.max(maxLag, lag);
                }
            }

            if (maxLag > 1000) { // Threshold for lag
                return Health.outOfService()
                    .withDetail("status", "LAG_TOO_HIGH")
                    .withDetail("max_lag", maxLag)
                    .build();
            }

            return Health.up()
                .withDetail("status", "LAG_ACCEPTABLE")
                .withDetail("max_lag", maxLag)
                .build();
        } catch (Exception e) {
            return Health.down()
                .withDetail("status", "CHECK_FAILED")
                .withDetail("error", e.getMessage())
                .build();
        }
    }
}
```

### Topic and Partition Health Checks
Verify topic and partition availability:

```java
@GetMapping("/topic-health")
public ResponseEntity<Map<String, Object>> topicHealthCheck(@RequestParam String topicName) {
    Map<String, Object> health = new HashMap<>();

    try {
        // Check if topic exists and get metadata
        DescribeTopicsResult topicsResult = adminClient.describeTopics(Collections.singletonList(topicName));
        TopicDescription topicDescription = topicsResult.values().get(topicName).get();

        // Check partition count and leader availability
        int partitionCount = topicDescription.partitions().size();
        boolean allLeadersAvailable = topicDescription.partitions().stream()
            .allMatch(info -> info.leader() != null && !info.leader().isEmpty());

        health.put("topic_exists", true);
        health.put("partition_count", partitionCount);
        health.put("all_leaders_available", allLeadersAvailable);
        health.put("status", "HEALTHY");

        return ResponseEntity.ok(health);
    } catch (Exception e) {
        health.put("topic_exists", false);
        health.put("error", e.getMessage());
        health.put("status", "UNHEALTHY");
        return ResponseEntity.status(HttpStatus.SERVICE_UNAVAILABLE).body(health);
    }
}
```

## Advanced Troubleshooting Commands

### Kafka-Specific Diagnostics
```bash
# Check consumer group lag
kubectl exec -it <kafka-pod> -- bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group <consumer-group>

# Check topic details
kubectl exec -it <kafka-pod> -- bin/kafka-topics.sh --bootstrap-server localhost:9092 --describe --topic <topic-name>

# Monitor consumer group status
kubectl exec -it <kafka-pod> -- bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --list

# Check broker logs for issues
kubectl logs <kafka-pod> | grep -i "error\|warn\|exception"

# Check for under-replicated partitions
kubectl exec -it <kafka-pod> -- bin/kafka-topics.sh --bootstrap-server localhost:9092 --describe --under-replicated-partitions

# Check for unavailable partitions
kubectl exec -it <kafka-pod> -- bin/kafka-topics.sh --bootstrap-server localhost:9092 --describe --unavailable-partitions
```

### Network Connectivity Diagnostics
```bash
# Test connectivity to Kafka from application pod
kubectl exec -it <app-pod> -- telnet <kafka-service> 9092

# Check DNS resolution
kubectl exec -it <app-pod> -- nslookup <kafka-service>.<namespace>.svc.cluster.local

# Test Kafka connectivity with netcat
kubectl exec -it <app-pod> -- nc -zv <kafka-service> 9092

# Check service endpoints
kubectl get endpoints <kafka-service> -n <namespace>
```

### Resource-Related Troubleshooting
```bash
# Check pod resource usage during probe failures
kubectl top pod <pod-name> -n <namespace>

# Check node resource availability
kubectl top nodes

# Check pod resource limits
kubectl describe pod <pod-name> -n <namespace> | grep -A 10 -B 10 "Limits\|Requests"

# Check for resource pressure events
kubectl get events -n <namespace> --sort-by='.lastTimestamp' | grep -i "insufficient\|evicted\|oom"
```

## AI-Agent Specific Considerations

For AI applications with slow initialization, consider these patterns:

### AI Model Loading Health Checks
```java
@RestController
public class AIHealthController {

    @Autowired
    private AIModelService aiModelService;

    @GetMapping("/ai-model-health")
    public ResponseEntity<Map<String, Object>> aiModelHealth() {
        Map<String, Object> health = new HashMap<>();

        try {
            AIModelStatus status = aiModelService.getModelStatus();

            if (status.isLoaded()) {
                health.put("status", "READY");
                health.put("model_loaded", true);
                health.put("model_version", status.getVersion());
                health.put("loading_time", status.getLoadingTime());
                return ResponseEntity.ok(health);
            } else if (status.isLoading()) {
                health.put("status", "LOADING");
                health.put("model_loaded", false);
                health.put("progress", status.getProgress());
                return ResponseEntity.status(HttpStatus.ACCEPTED).body(health);
            } else {
                health.put("status", "NOT_LOADED");
                health.put("model_loaded", false);
                return ResponseEntity.status(HttpStatus.SERVICE_UNAVAILABLE).body(health);
            }
        } catch (Exception e) {
            health.put("status", "ERROR");
            health.put("error", e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(health);
        }
    }
}
```

### Slow Startup Configuration
```yaml
# For AI applications with slow model loading
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-kafka-app
spec:
  template:
    spec:
      containers:
      - name: ai-app
        image: ai-kafka-app:latest
        # Extended startup probe for AI model loading
        startupProbe:
          httpGet:
            path: /ai-startup
            port: 8080
          initialDelaySeconds: 60
          periodSeconds: 30        # Longer intervals for slow startups
          timeoutSeconds: 20       # Longer timeouts for AI operations
          failureThreshold: 20     # Allow up to 10 minutes for model loading
        # Normal liveness probe after startup
        livenessProbe:
          httpGet:
            path: /healthz
            port: 8080
          initialDelaySeconds: 300 # Start after model is loaded
          periodSeconds: 60
          timeoutSeconds: 15
        # Normal readiness probe after startup
        readinessProbe:
          httpGet:
            path: /readyz
            port: 8080
          initialDelaySeconds: 240 # Start after model is loaded
          periodSeconds: 15
          timeoutSeconds: 10
```

## Diagnostic Scripts

### Comprehensive Kafka Health Check Script
```bash
#!/bin/bash
# kafka-health-check.sh - Comprehensive Kafka health verification

NAMESPACE=${1:-default}
APP_POD=${2:-$(kubectl get pods -n $NAMESPACE -l app=kafka-app -o jsonpath='{.items[0].metadata.name}')}

echo "=== Kafka Application Health Check ==="
echo "Namespace: $NAMESPACE"
echo "Pod: $APP_POD"
echo "Timestamp: $(date)"
echo

echo "1. Pod Status:"
kubectl get pod $APP_POD -n $NAMESPACE
echo

echo "2. Pod Events:"
kubectl describe pod $APP_POD -n $NAMESPACE | grep -A 10 -B 10 "Events:"
echo

echo "3. Application Logs (last 50 lines):"
kubectl logs $APP_POD -n $NAMESPACE --tail=50
echo

echo "4. Health Endpoint Check:"
kubectl exec $APP_POD -n $NAMESPACE -- curl -s -o /dev/null -w "HTTP Status: %{http_code}\n" http://localhost:8080/healthz
echo

echo "5. Resource Usage:"
kubectl top pod $APP_POD -n $NAMESPACE
echo

echo "6. Kafka Connectivity Test:"
kubectl exec $APP_POD -n $NAMESPACE -- timeout 10 bash -c "</dev/tcp/kafka-service/9092 && echo 'Kafka connection: SUCCESS' || echo 'Kafka connection: FAILED'"
echo

echo "7. Consumer Group Status (if applicable):"
kubectl exec $APP_POD -n $NAMESPACE -- timeout 15 bash -c "echo dump | nc kafka-service 9092 | grep -q 'Connected' && echo 'Connection: SUCCESS' || echo 'Connection: FAILED'"
echo

echo "=== Health Check Complete ==="
```

This troubleshooting guide provides comprehensive patterns for diagnosing and resolving health probe issues in Kafka applications, with special attention to AI applications that may have slow initialization times.