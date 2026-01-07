#!/bin/bash
# Start Playwright MCP Server
# Compiled skill script for Phase II

export MCP_PLAYWRIGHT_URL="http://localhost:8808"

echo "Starting Playwright MCP server..."
echo "URL: $MCP_PLAYWRIGHT_URL"

# Check if already running
if curl -s "$MCP_PLAYWRIGHT_URL/tools" > /dev/null 2>&1; then
    echo "Playwright MCP already running at $MCP_PLAYWRIGHT_URL"
    exit 0
fi

# Start Playwright MCP
npx -y @playwright/mcp@latest --port 8808 &
echo "Started @playwright/mcp on port 8808"

# Wait for server to be ready
echo "Waiting for server..."
for i in {1..30}; do
    if curl -s "$MCP_PLAYWRIGHT_URL/tools" > /dev/null 2>&1; then
        echo "Playwright MCP server ready!"
        exit 0
    fi
    sleep 1
done

echo "Warning: Server may not be ready yet"
