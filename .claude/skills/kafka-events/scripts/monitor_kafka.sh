#!/bin/bash
# Script to check Kafka cluster and consumer group status for decoupled architecture
# Usage: ./monitor_kafka.sh [consumer-group-name]
#
# This script monitors the health of your event-driven architecture,
# focusing on decoupling metrics like consumer lag and availability.
# It also provides insights into eventual consistency status.

set -e  # Exit on any error

CONSUMER_GROUP=${1:-""}

echo "Monitoring Kafka cluster for decoupled architecture health..."
echo "Checking broker status and API versions:"
bin/kafka-broker-api-versions.sh --bootstrap-server localhost:9092 2>/dev/null | head -10

echo ""
echo "Available topics (communication channels for decoupled services):"
bin/kafka-topics.sh --bootstrap-server localhost:9092 --list

if [ ! -z "$CONSUMER_GROUP" ]; then
    echo ""
    echo "Consumer group '$CONSUMER_GROUP' details (availability coupling monitoring):"
    bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group $CONSUMER_GROUP
else
    echo ""
    echo "Consumer groups (monitoring service availability):"
    bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --list
fi

echo ""
echo "Checking for under-replicated partitions (availability monitoring):"
bin/kafka-topics.sh --bootstrap-server localhost:9092 --describe --under-replicated-partitions

echo ""
echo "EDA Fundamentals Health Indicators:"
echo "Temporal Coupling Resolution:"
echo "- Low consumer lag indicates good temporal coupling (services process events timely)"
echo "- High lag suggests temporal coupling issues (consumers can't keep up)"
echo ""
echo "Availability Coupling Resolution:"
echo "- Stable consumer groups indicate good availability coupling"
echo "- Unstable groups suggest services going offline frequently"
echo ""
echo "Eventual Consistency Status:"
echo "- Consumer lag shows how far behind consumers are (consistency delay)"
echo "- Under-replicated partitions indicate potential data loss risks"
echo ""
echo "Behavioral Coupling Resolution:"
echo "- Healthy partition replication indicates system reliability"
echo "- Stable topic configurations support consistent event contracts"