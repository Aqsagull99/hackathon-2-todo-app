#!/bin/bash
# Script to check the health of Dapr applications and components
# Usage: ./check_dapr_health.sh
#
# This script checks the health of Dapr sidecars and verifies:
# - Standard Dapr ports (HTTP:3500, gRPC:50001, Internal gRPC:50002)
# - Dapr runtime status
# - Running applications
# - Sidecar accessibility

set -e  # Exit on any error

echo "Checking Dapr health and status..."

# Check if Dapr is initialized
echo "Checking Dapr installation..."
if command -v dapr &> /dev/null; then
    echo "✓ Dapr CLI version: $(dapr --version)"
else
    echo "✗ Dapr CLI not found"
    exit 1
fi

# Check Dapr runtime status
echo ""
echo "Checking Dapr runtime status..."
if dapr status -k &> /dev/null; then
    echo "✓ Dapr runtime is running"
    dapr status -k
else
    echo "⚠ Dapr runtime is not running in Kubernetes"
fi

# List running Dapr applications
echo ""
echo "Running Dapr applications:"
dapr list || echo "No Dapr applications currently running"

# Check if Dapr sidecar is accessible on standard ports
echo ""
echo "Testing Dapr sidecar accessibility..."
echo "Standard Dapr ports:"
echo "  - HTTP: 3500 (default) - For HTTP API calls to Dapr"
echo "  - gRPC: 50001 (default) - For gRPC API calls to Dapr"
echo "  - Internal gRPC: 50002 (default) - For internal Dapr-to-Dapr communication"

if curl -sf http://localhost:3500/v1.0/healthz &> /dev/null; then
    echo "✓ Dapr sidecar is accessible on HTTP port 3500"
else
    echo "⚠ Dapr sidecar may not be accessible on HTTP port 3500"
    echo "  This is expected if no Dapr application is currently running"
fi

if curl -sf http://localhost:50001/v1.0/healthz &> /dev/null; then
    echo "✓ Dapr sidecar is accessible on gRPC port 50001 (via HTTP test)"
else
    echo "⚠ Dapr sidecar may not be accessible on gRPC port 50001"
fi

# Check common Dapr ports
echo ""
echo "Checking common Dapr ports..."
for port in 3500 50001 3501 50002; do
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        case $port in
            3500)
                echo "✓ Port $port is in use (Dapr HTTP API)"
                ;;
            50001)
                echo "✓ Port $port is in use (Dapr gRPC API)"
                ;;
            50002)
                echo "✓ Port $port is in use (Dapr Internal gRPC)"
                ;;
            *)
                echo "✓ Port $port is in use (possibly Dapr sidecar)"
                ;;
        esac
    else
        echo "○ Port $port is available"
    fi
done

echo ""
echo "Dapr health check completed."
echo ""
echo "Sidecar Architecture Info:"
echo "- Dapr runs as a sidecar process/container alongside your application"
echo "- Standard ports: HTTP:3500, gRPC:50001, Internal gRPC:50002"
echo "- Communication happens via localhost between app and sidecar"
echo ""
echo "Tips:"
echo "- To start a Dapr application: dapr run --app-id <id> --app-port <port> <command>"
echo "- To check all Dapr logs: dapr logs -k"
echo "- To stop all Dapr apps: dapr stop --all"
echo "- For Kubernetes: dapr status -k, kubectl get pods -n dapr-system"