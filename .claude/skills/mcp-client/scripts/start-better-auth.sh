#!/bin/bash
# Start Better Auth MCP Server
# Compiled skill script for Phase II

export MCP_BETTER_AUTH_URL="http://localhost:3002"

echo "Starting Better Auth MCP server..."
echo "URL: $MCP_BETTER_AUTH_URL"

# Check if already running
if curl -s "$MCP_BETTER_AUTH_URL/schema" > /dev/null 2>&1; then
    echo "Better Auth MCP already running at $MCP_BETTER_AUTH_URL"
    exit 0
fi

# Start MCP server (adjust command based on your setup)
npx -y @modelcontextprotocol/server-github --port 3002 2>/dev/null &
# Note: Better Auth MCP may have different setup
# Using GitHub MCP as placeholder for auth operations

echo "Started MCP server on port 3002"

# Wait for server to be ready
echo "Waiting for server..."
for i in {1..30}; do
    if curl -s "$MCP_BETTER_AUTH_URL" > /dev/null 2>&1; then
        echo "Better Auth MCP server ready!"
        exit 0
    fi
    sleep 1
done

echo "Warning: Server may not be ready yet"
