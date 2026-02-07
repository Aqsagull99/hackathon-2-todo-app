#!/bin/bash
# Script to deploy a Dapr-enabled application in process mode
# Usage: ./deploy_dapr_app.sh <app-id> <app-port> <command>
#
# This script deploys a Dapr application in process mode where:
# - Your application runs as a separate process
# - Dapr sidecar (daprd) runs as a separate process alongside
# - Communication happens via localhost using standard Dapr ports:
#   - HTTP: 3500 (default) - For HTTP API calls to Dapr
#   - gRPC: 50001 (default) - For gRPC API calls to Dapr

set -e  # Exit on any error

APP_ID=${1:-"myapp"}
APP_PORT=${2:-"3000"}
COMMAND=${3:-"node app.js"}

echo "Deploying Dapr application: $APP_ID"
echo "Application port: $APP_PORT"
echo "Command: $COMMAND"
echo "Mode: Process mode (Dapr sidecar runs as separate process)"

# Validate inputs
if [[ -z "$APP_ID" ]]; then
    echo "Error: App ID cannot be empty"
    exit 1
fi

if ! [[ "$APP_PORT" =~ ^[0-9]+$ ]] || [ "$APP_PORT" -lt 1 ] || [ "$APP_PORT" -gt 65535 ]; then
    echo "Error: Invalid port number"
    exit 1
fi

# Calculate Dapr ports based on app port
DAPR_HTTP_PORT=3500  # Default Dapr HTTP API port
DAPR_GRPC_PORT=50001  # Default Dapr gRPC API port

echo "Starting Dapr application with ID: $APP_ID"
echo "App port: $APP_PORT"
echo "Dapr ports - HTTP: $DAPR_HTTP_PORT, gRPC: $DAPR_GRPC_PORT"
echo ""
echo "Architecture: Process mode"
echo "- Your application runs as a separate process"
echo "- Dapr sidecar (daprd) runs as a separate process"
echo "- Communication via localhost using standard Dapr APIs"

# Run the application with Dapr sidecar
dapr run \
    --app-id "$APP_ID" \
    --app-port "$APP_PORT" \
    --dapr-http-port "$DAPR_HTTP_PORT" \
    --dapr-grpc-port "$DAPR_GRPC_PORT" \
    --log-level info \
    -- "$COMMAND"

echo "Dapr application $APP_ID stopped."
echo "Process mode deployment completed."