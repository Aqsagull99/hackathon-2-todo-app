#!/bin/bash
# Stop Context7 MCP Server
# Compiled skill script for Phase II

MCP_PORT=3001

echo "Stopping Context7 MCP server..."

# Kill by port
if command -v lsof &> /dev/null; then
    PID=$(lsof -ti:$MCP_PORT 2>/dev/null)
    if [ -n "$PID" ]; then
        kill $PID 2>/dev/null
        echo "Killed process on port $MCP_PORT (PID: $PID)"
    fi
fi

# Kill by process name
pkill -f "context7-mcp" 2>/dev/null
pkill -f "@upstash/context7-mcp" 2>/dev/null

# Kill Docker container
if command -v docker &> /dev/null; then
    docker stop context7-mcp 2>/dev/null
    docker rm context7-mcp 2>/dev/null
    echo "Stopped Docker container if existed"
fi

echo "Context7 MCP server stopped"
