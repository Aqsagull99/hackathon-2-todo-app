#!/bin/bash
# Start Context7 MCP Server
# Compiled skill script for Phase II

export MCP_CONTEXT7_URL="http://localhost:3001"

echo "Starting Context7 MCP server..."
echo "URL: $MCP_CONTEXT7_URL"

# Check if already running
if curl -s "$MCP_CONTEXT7_URL/tools" > /dev/null 2>&1; then
    echo "Context7 MCP already running at $MCP_CONTEXT7_URL"
    exit 0
fi

# Start MCP server (adjust command based on your setup)
# Option 1: Using npx
if command -v npx &> /dev/null; then
    npx -y @upstash/context7-mcp --port 3001 &
    echo "Started via npx @upstash/context7-mcp on port 3001"
# Option 2: Using Docker
elif command -v docker &> /dev/null; then
    docker run -d -p 3001:3000 --name context7-mcp upstash/context7-mcp
    echo "Started via Docker on port 3001"
else
    echo "Warning: Neither npx nor Docker available"
    echo "Please start Context7 MCP server manually"
fi

# Wait for server to be ready
echo "Waiting for server..."
for i in {1..30}; do
    if curl -s "$MCP_CONTEXT7_URL/tools" > /dev/null 2>&1; then
        echo "Context7 MCP server ready!"
        exit 0
    fi
    sleep 1
done

echo "Warning: Server may not be ready yet"
