#!/bin/bash
# Script to set up a Kafka cluster in KRaft mode for event-driven architecture
# Usage: ./setup_kafka_cluster.sh
#
# This sets up a Kafka cluster that enables:
# - Temporal decoupling: Asynchronous event processing
# - Availability decoupling: Buffer between services during downtime
# - Behavioral decoupling: Well-defined event contracts

set -e  # Exit on any error

echo "Setting up Kafka cluster in KRaft mode for decoupled event-driven architecture..."

# Generate cluster ID if not provided
if [ -z "$CLUSTER_ID" ]; then
    export CLUSTER_ID=$(bin/kafka-storage.sh random-uuid)
    echo "Generated Cluster ID: $CLUSTER_ID"
else
    echo "Using provided Cluster ID: $CLUSTER_ID"
fi

# Format storage (only needed on first run)
if [ ! -d "/tmp/kraft-combined-logs" ] || [ -z "$(ls -A /tmp/kraft-combined-logs)" ]; then
    echo "Formatting storage for KRaft mode..."
    bin/kafka-storage.sh format --standalone -t $CLUSTER_ID -c config/kraft/server.properties
    echo "Storage formatted successfully."
else
    echo "Storage already exists, skipping format."
fi

echo ""
echo "Kafka cluster setup complete for decoupled architecture!"
echo "This cluster enables:"
echo "  - Temporal decoupling: Services don't need to be synchronized"
echo "  - Availability decoupling: Services can operate independently when others are down"
echo "  - Behavioral decoupling: Services can evolve independently with event contracts"
echo ""
echo "To start the broker, run: bin/kafka-server-start.sh config/kraft/server.properties"