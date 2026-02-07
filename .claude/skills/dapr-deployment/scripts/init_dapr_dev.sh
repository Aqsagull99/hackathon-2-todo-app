#!/bin/bash
# Script to initialize Dapr environment for development
# Usage: ./init_dapr_dev.sh
#
# This script initializes Dapr in process mode for development:
# - Dapr runtime runs as a separate process (daprd)
# - Your applications will run as separate processes
# - Communication happens via localhost using standard Dapr ports:
#   - HTTP: 3500 (default) - For HTTP API calls to Dapr
#   - gRPC: 50001 (default) - For gRPC API calls to Dapr

set -e  # Exit on any error

echo "Initializing Dapr development environment..."
echo "Mode: Process mode (Dapr sidecar runs as separate process)"

# Check if Dapr CLI is installed
if ! command -v dapr &> /dev/null; then
    echo "Dapr CLI not found. Installing Dapr CLI..."
    wget -q https://raw.githubusercontent.com/dapr/cli/master/install/install.sh -O - | /bin/bash
fi

# Initialize Dapr runtime
echo "Initializing Dapr runtime in process mode..."
echo "Dapr will run as a separate process alongside your applications"
dapr init

# Wait for Dapr to be ready
sleep 10

# Check Dapr status
echo "Checking Dapr status..."
dapr status -k

echo ""
echo "Dapr development environment initialized successfully!"
echo ""
echo "Architecture: Process mode"
echo "- Dapr sidecar (daprd) runs as a separate process"
echo "- Your applications run as separate processes"
echo "- Communication via localhost using standard Dapr APIs"
echo "- Standard ports: HTTP:3500, gRPC:50001, Internal gRPC:50002"
echo ""
echo "You can now run your applications with 'dapr run --app-id <app-id> --app-port <port> <command>'"
echo "Example: dapr run --app-id myapp --app-port 3000 node app.js"