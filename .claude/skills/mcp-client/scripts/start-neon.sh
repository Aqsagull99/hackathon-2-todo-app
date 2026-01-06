#!/bin/bash
# Start Neon MCP Server
# Compiled skill script for Phase II

export MCP_NEON_URL="http://localhost:3003"

echo "Starting Neon MCP server..."
echo "URL: $MCP_NEON_URL"

# Check if already running
if curl -s "$MCP_NEON_URL" > /dev/null 2>&1; then
    echo "Neon MCP already running at $MCP_NEON_URL"
    exit 0
fi

# Neon MCP typically requires authentication
# Use environment variables for credentials
export NEON_API_KEY="${NEON_API_KEY:-your-api-key}"

# Start MCP server
if command -v npx &> /dev/null; then
    # Check for official Neon MCP or use custom
    echo "Note: Configure NEON_API_KEY environment variable"
    npx -y neon-mcp-server --port 3003 2>/dev/null &
    echo "Started MCP server on port 3003"
else
    echo "npx not available. Please start Neon MCP manually."
fi

# Wait for server to be ready
echo "Waiting for server..."
for i in {1..30}; do
    if curl -s "$MCP_NEON_URL" > /dev/null 2>&1; then
        echo "Neon MCP server ready!"
        exit 0
    fi
    sleep 1
done

echo "Warning: Server may not be ready yet"
