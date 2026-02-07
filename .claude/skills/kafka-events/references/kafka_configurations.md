# Apache Kafka Configuration Reference

## KRaft Mode Configuration

### Essential Server Properties
```properties
# KRaft mode configuration (replaces ZooKeeper)
process.roles=broker,controller
node.id=1
controller.quorum.bootstrap.servers=localhost:9093

# Network listeners
listeners=PLAINTEXT://:9092,CONTROLLER://:9093
advertised.listeners=PLAINTEXT://localhost:9092
inter.broker.listener.name=PLAINTEXT
controller.listener.names=CONTROLLER
listener.security.protocol.map=CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT,SSL:SSL,SASL_PLAINTEXT:SASL_PLAINTEXT,SASL_SSL:SASL_SSL

# Threading configuration
num.network.threads=3
num.io.threads=8
socket.send.buffer.bytes=102400
socket.receive.buffer.bytes=102400
socket.request.max.bytes=104857600

# Log storage
log.dirs=/tmp/kraft-combined-logs
num.partitions=1
num.recovery.threads.per.data.dir=2

# Replication
offsets.topic.replication.factor=3
transaction.state.log.replication.factor=3
transaction.state.log.min.isr=2
default.replication.factor=3
min.insync.replicas=2

# Log retention
log.retention.hours=168
log.segment.bytes=1073741824
log.retention.check.interval.ms=300000

# Log cleanup policy
log.cleanup.policy=delete
log.cleaner.enable=true

# Compression
compression.type=producer
```

## Producer Configuration Best Practices

### High Throughput Settings
```properties
acks=all
retries=2147483647
max.in.flight.requests.per.connection=5
enable.idempotence=true
batch.size=16384
linger.ms=5
buffer.memory=33554432
compression.type=snappy
```

### Low Latency Settings
```properties
acks=1
retries=0
max.in.flight.requests.per.connection=1
batch.size=16
linger.ms=0
compression.type=none
```

## Consumer Configuration Best Practices

### Low Latency Consumer
```properties
fetch.min.bytes=1
fetch.max.wait.ms=500
max.partition.fetch.bytes=1048576
max.poll.records=100
```

### High Throughput Consumer
```properties
fetch.min.bytes=5242880  # 5MB
fetch.max.wait.ms=500
max.partition.fetch.bytes=10485760  # 10MB
max.poll.records=1000
```

## Security Configuration

### SSL Configuration
```properties
security.protocol=SSL
ssl.truststore.location=/path/to/kafka.client.truststore.jks
ssl.truststore.password=test1234
ssl.keystore.location=/path/to/kafka.client.keystore.jks
ssl.keystore.password=test1234
ssl.key.password=test1234
```

### SASL/SCRAM Configuration
```properties
security.protocol=SASL_SSL
sasl.mechanism=SCRAM-SHA-256
sasl.jaas.config=org.apache.kafka.common.security.scram.ScramLoginModule required \
  username="client" \
  password="client-secret";
```

## Kafka Streams Configuration

### Basic Streams Configuration
```properties
application.id=my-streams-application
bootstrap.servers=localhost:9092
key.serde=org.apache.kafka.common.serialization.Serdes$StringSerde
value.serde=org.apache.kafka.common.serialization.Serdes$StringSerde
auto.offset.reset=earliest
```

### Production Streams Configuration
```properties
application.id=my-streams-application
bootstrap.servers=localhost:9092
acks=all
replication.factor=3
num.standby.replicas=1
state.dir=/path/to/state/dir
processing.guarantee=exactly_once_v2
```

## Event-Driven Architecture and Decoupling Patterns

### Addressing Coupling Types with Kafka Events

#### 1. Temporal Coupling Resolution
Kafka eliminates temporal coupling by allowing asynchronous communication between services:
- Producers publish events without waiting for consumer acknowledgment
- Consumers process events at their own pace
- Applications can continue processing without blocking on other services

#### 2. Availability Coupling Resolution
Kafka acts as a buffer to resolve availability coupling:
- Events persist in topics even when consumers are offline
- Consumers can process historical events when they become available
- System remains functional despite individual component failures

#### 3. Behavioral Coupling Resolution
Well-defined event schemas reduce behavioral coupling:
- Clear contracts between services using Avro or JSON Schema
- Support for schema evolution with backward/forward compatibility
- Services can evolve independently while maintaining interoperability

## Event-Driven Architecture Fundamentals Reference

### Producer Configuration for Different Consistency Needs

#### At-Most-Once Delivery (Fastest, Less Reliable)
```properties
# Auto commit enabled - fastest but risk of message loss
enable.auto.commit=true
auto.commit.interval.ms=1000
acks=1
```

#### At-Least-Once Delivery (Recommended for Most Cases)
```properties
# Manual commit after processing - ensures no message loss
enable.auto.commit=false
acks=all
retries=2147483647
max.in.flight.requests.per.connection=5
```

#### Exactly-Once Delivery (Strongest Guarantee)
```properties
# Idempotent producer with transactions
enable.idempotence=true
acks=all
retries=2147483647
max.in.flight.requests.per.connection=5
transactional.id=my-transactional-id
isolation.level=read_committed
```

### Consumer Configuration for Different Scenarios

#### High Throughput Consumer
```properties
fetch.min.bytes=5242880  # 5MB
fetch.max.wait.ms=500
max.partition.fetch.bytes=10485760  # 10MB
max.poll.records=1000
```

#### Low Latency Consumer
```properties
fetch.min.bytes=1
fetch.max.wait.ms=500
max.partition.fetch.bytes=1048576
max.poll.records=100
```

#### Exactly-Once Consumer
```properties
isolation.level=read_committed
enable.auto.commit=false
auto.offset.reset=earliest
```

### When to Use Event-Driven Architecture

#### Choose EDA When:
- Need loose coupling between services
- Require high scalability and resilience
- Need real-time processing capabilities
- Integrating heterogeneous systems
- Audit trail is required
- Partial system failures should not stop the entire system

#### Avoid EDA When:
- Strong consistency is required immediately
- Simple request-response patterns are sufficient
- Cannot tolerate asynchronous processing latency
- Team lacks experience with distributed systems

### Eventual Consistency Management Patterns

#### CQRS (Command Query Responsibility Segregation)
Separate read and write models to handle eventual consistency:
- Commands modify the write model
- Queries read from the read model
- Events synchronize the models over time

#### SAGA Pattern
Coordinate distributed transactions using sequences of local transactions:
- Each step has a compensating action
- Rollback is achieved by executing compensating actions in reverse order
- Maintains data consistency across services

#### Compensating Actions
Implement undo operations for failed business processes:
- Each action has a corresponding compensation
- Used when a multi-step process fails partway through
- Helps maintain business-level consistency