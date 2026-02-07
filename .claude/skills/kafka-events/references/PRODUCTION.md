# Kafka Production Best Practices

## Configuration Management

### Topic Configuration Checklist
- [ ] Partition count appropriate for expected throughput (typically 1 partition per 1000-10000 msg/sec)
- [ ] Replication factor set to 3 for production (higher for critical data)
- [ ] min.insync.replicas set to 2 for durability
- [ ] Log retention configured appropriately (time or size based)
- [ ] Cleanup policy set correctly (delete vs compact vs delete+compact)
- [ ] Message size limits configured for expected payloads
- [ ] Topic-level quotas configured if needed
- [ ] Topic naming follows organizational conventions
- [ ] Topic labels/annotations include business context

### Consumer Configuration Checklist
- [ ] Consumer group ID follows naming convention
- [ ] Offset management strategy configured (manual vs auto-commit)
- [ ] Session and heartbeat timeouts properly balanced
- [ ] Max poll records set appropriately (avoid timeouts)
- [ ] Consumer lag monitoring configured
- [ ] Deserialization error handling implemented
- [ ] Consumer rebalancing handled gracefully
- [ ] Consumer fetch size tuned for expected message sizes
- [ ] Consumer connection pooling configured properly

### Producer Configuration Checklist
- [ ] Acknowledgment level set appropriately (acks=all for durability)
- [ ] Idempotent producer enabled for exactly-once semantics
- [ ] Retry configuration with exponential backoff
- [ ] Batch size and linger time tuned for throughput
- [ ] Message serialization format optimized
- [ ] Producer compression enabled (snappy/lz4/zstd)
- [ ] Connection pooling configured properly
- [ ] Producer error handling and retry logic implemented
- [ ] Producer metrics collection enabled

## Health Probes and Monitoring

### Kafka Application Health Probes Checklist
- [ ] Liveness probe configured with appropriate timeouts for AI workloads
- [ ] Readiness probe verifies Kafka connectivity before accepting traffic
- [ ] Startup probe accounts for slow AI model initialization (up to 10 minutes if needed)
- [ ] Health endpoints return broker connectivity status
- [ ] Consumer lag monitored and reported in health checks
- [ ] Topic existence verified in readiness checks
- [ ] Partition assignment health checked
- [ ] Consumer group status monitored
- [ ] Producer connection health verified

### Monitoring Configuration Checklist
- [ ] JMX metrics enabled for broker monitoring
- [ ] Consumer lag metrics collected and alerted
- [ ] Broker resource utilization monitored (CPU, memory, disk)
- [ ] Network throughput and latency metrics collected
- [ ] Topic-specific metrics monitored (messages in/out rates)
- [ ] Partition leader distribution monitored
- [ ] Under-replicated partition count tracked
- [ ] Broker restart frequency monitored
- [ ] Consumer group rebalancing frequency tracked
- [ ] Message processing latency measured
- [ ] Error rate monitoring implemented
- [ ] Dead letter queue monitoring configured if applicable

## Security Configuration

### Authentication and Authorization Checklist
- [ ] SSL/TLS enabled for all communications
- [ ] SASL authentication configured (SCRAM, PLAIN, or OAUTHBEARER)
- [ ] Client certificates properly managed
- [ ] Principal-to-identity mapping configured
- [ ] ACLs defined for all topics and consumer groups
- [ ] Network policies configured to restrict access
- [ ] Encryption at rest enabled if required
- [ ] Audit logging configured for security events
- [ ] Certificate rotation strategy implemented
- [ ] Security configurations tested in non-production environments

### Network Security Checklist
- [ ] Firewall rules restrict access to Kafka brokers
- [ ] VPN/VPC access for external connections
- [ ] Network segmentation between components
- [ ] TLS termination handled properly at load balancers
- [ ] Certificate validation enabled
- [ ] Mutual TLS authentication configured
- [ ] Network traffic encryption enforced
- [ ] Access logs collected and analyzed
- [ ] Intrusion detection systems configured if applicable

## Performance Optimization

### Performance Tuning Checklist
- [ ] Broker heap size configured appropriately (usually 6GB max)
- [ ] Garbage collection tuned for low latency (G1GC recommended)
- [ ] Disk I/O optimized with proper storage configuration
- [ ] Network buffer sizes tuned for throughput
- [ ] Replication settings optimized for consistency vs availability
- [ ] Consumer fetch sizes optimized for message size
- [ ] Producer batching tuned for throughput
- [ ] Compression enabled and tuned (snappy for balance)
- [ ] Topic partitioning aligned with consumer parallelism
- [ ] Consumer group scaling configured appropriately

### Resource Management Checklist
- [ ] CPU and memory requests/limits configured for containers
- [ ] Storage configured with appropriate IOPS for throughput
- [ ] Node affinity/anti-affinity configured for brokers
- [ ] Pod disruption budgets configured for availability
- [ ] Horizontal pod autoscaling configured for consumers if needed
- [ ] Resource quotas enforced at namespace level
- [ ] Node resource allocation planned for peak loads
- [ ] Storage growth monitored and planned for
- [ ] Backup storage resources allocated
- [ ] Monitoring agent resources configured appropriately

## Disaster Recovery

### Backup and Recovery Checklist
- [ ] Offsets periodically exported for critical consumer groups
- [ ] Topic data backup strategy implemented (incremental/differential)
- [ ] Broker metadata backup configured
- [ ] Recovery procedures documented and tested
- [ ] Cross-cluster mirroring configured for disaster recovery
- [ ] Backup retention policies defined
- [ ] Backup verification procedures implemented
- [ ] Recovery time objectives (RTO) defined and tested
- [ ] Recovery point objectives (RPO) defined and verified
- [ ] Failover procedures documented and rehearsed
- [ ] Data consistency verification after recovery
- [ ] Business continuity procedures validated

### High Availability Checklist
- [ ] Multi-AZ deployment for broker distribution
- [ ] Rack awareness configured for replication
- [ ] Quorum size appropriate for cluster (majority of brokers)
- [ ] Load balancer health checks configured
- [ ] Automatic failover procedures tested
- [ ] Manual failover procedures documented
- [ ] Cluster monitoring includes availability metrics
- [ ] Backup cluster configured and synchronized
- [ ] Network redundancy implemented
- [ ] Hardware failure scenarios tested
- [ ] Data center failover procedures validated

## Operational Procedures

### Deployment Checklist
- [ ] Configuration management follows Infrastructure as Code
- [ ] Secrets managed through secure vault/secret store
- [ ] Blue-green or rolling deployment strategy configured
- [ ] Pre-deployment health checks implemented
- [ ] Post-deployment validation procedures defined
- [ ] Rollback procedures documented and tested
- [ ] Traffic shifting strategy configured
- [ ] Canary deployment approach implemented if needed
- [ ] Configuration validation performed before deployment
- [ ] Resource allocation verified before deployment
- [ ] Security scans performed on images/configurations
- [ ] Compliance checks validated before deployment

### Maintenance Checklist
- [ ] Regular security patching schedule defined
- [ ] Kafka version upgrade procedures documented
- [ ] Topic cleanup and archival procedures defined
- [ ] Consumer group cleanup procedures implemented
- [ ] Log rotation configured and monitored
- [ ] Performance tuning reviews scheduled regularly
- [ ] Capacity planning performed quarterly
- [ ] Configuration drift detection implemented
- [ ] Backup verification performed regularly
- [ ] Disaster recovery tests conducted periodically
- [ ] Security audit procedures implemented
- [ ] Performance baseline updates scheduled

## AI/ML Workload Specific Considerations

### AI/ML Pipeline Integration Checklist
- [ ] Topic partitioning aligned with ML model parallelism
- [ ] Consumer group scaling configured for batch processing
- [ ] Message schema evolution strategy defined
- [ ] Data lineage tracking implemented
- [ ] Model version metadata included in messages
- [ ] Feature store integration considered
- [ ] Real-time inference pipeline configured
- [ ] Batch processing pipeline integrated
- [ ] Model retraining triggers configured
- [ ] Data quality monitoring implemented
- [ ] Prediction drift detection configured
- [ ] Model performance metrics collected