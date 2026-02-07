#!/bin/bash
# Script to create a Kafka topic with custom configurations for decoupled event-driven architecture
# Usage: ./create_topic.sh <topic-name> [partitions] [replication-factor]
#
# This script creates topics that support decoupling patterns:
# - Temporal: Asynchronous event processing
# - Availability: Buffer between services
# - Behavioral: Well-defined event contracts
# - Eventual Consistency: Support for different consistency models

set -e  # Exit on any error

TOPIC_NAME=${1:-"default-topic"}
PARTITIONS=${2:-1}
REPLICATION_FACTOR=${3:-1}

echo "Creating Kafka topic: $TOPIC_NAME"
echo "Partitions: $PARTITIONS"
echo "Replication Factor: $REPLICATION_FACTOR"
echo ""
echo "This topic will support decoupling patterns:"
echo "  - Temporal: Enables asynchronous communication between services"
echo "  - Availability: Acts as a buffer when services are unavailable"
echo "  - Behavioral: Provides contract for event-based interactions"
echo "  - Eventual Consistency: Supports various consistency models"
echo ""
echo "EDA Fundamentals:"
echo "  - Producers can publish events without waiting for consumers"
echo "  - Consumers process events at their own pace"
echo "  - System state converges over time (eventual consistency)"

# Create the topic with specified configurations
bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic $TOPIC_NAME \
  --partitions $PARTITIONS --replication-factor $REPLICATION_FACTOR

echo ""
echo "Topic $TOPIC_NAME created successfully!"
echo "Services can now publish and consume events asynchronously for loose coupling."
echo "This enables event-driven architecture with eventual consistency."