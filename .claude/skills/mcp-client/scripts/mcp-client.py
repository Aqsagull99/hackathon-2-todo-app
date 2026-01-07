#!/usr/bin/env python3
"""
Universal MCP Client - Compiled for Skills
Connects to MCP servers via HTTP transport and executes tool calls.

Usage:
    python mcp-client.py --server <name> --tool <name> --args <json>

Environment:
    MCP_SERVER_URL: URL of MCP server (default: http://localhost:3000)
    MCP_SERVER_NAME: Name identifier for logging
"""

import argparse
import json
import os
import sys
import time
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

# Default MCP server URLs
SERVER_URLS = {
    "context7": "http://localhost:3001",
    "better-auth": "http://localhost:3002",
    "neon": "http://localhost:3003",
    "playwright": "http://localhost:8808",
}


def call_mcp_tool(server_name: str, tool_name: str, args: dict) -> dict:
    """Execute a tool call on an MCP server."""
    server_url = os.environ.get(f"MCP_{server_name.upper()}_URL") or SERVER_URLS.get(
        server_name.lower()
    )

    if not server_url:
        return {"error": f"Unknown server: {server_name}", "available": list(SERVER_URLS.keys())}

    # Ensure trailing slash
    if not server_url.endswith("/"):
        server_url += "/"

    endpoint = f"{server_url}tools/{tool_name}"

    payload = {"arguments": args}

    try:
        req = Request(
            endpoint,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))

        # Filter result to reduce tokens
        return filter_result(result, tool_name)

    except HTTPError as e:
        error_body = e.read().decode("utf-8") if e.code < 500 else {}
        return {
            "error": f"HTTP {e.code}: {str(e)}",
            "details": error_body,
            "tool": tool_name,
        }
    except URLError as e:
        return {"error": f"Connection failed: {e.reason}", "server": server_name}
    except json.JSONDecodeError:
        return {"error": "Invalid JSON response", "server": server_name}
    except Exception as e:
        return {"error": str(e), "type": type(e).__name__}


def filter_result(result: dict, tool_name: str) -> dict:
    """Filter results to reduce token size."""
    if isinstance(result, dict):
        # Keep structure but trim large fields
        filtered = {}
        for key, value in result.items():
            if key in ("content", "text", "result", "response"):
                # Truncate long text
                if isinstance(value, str) and len(value) > 5000:
                    filtered[key] = value[:5000] + "... [truncated]"
                else:
                    filtered[key] = value
            elif key in ("success", "error", "status", "tool", "server"):
                filtered[key] = value
        return filtered if filtered else {"status": "processed"}
    return result


def list_tools(server_name: str) -> dict:
    """List available tools on an MCP server."""
    server_url = os.environ.get(f"MCP_{server_name.upper()}_URL") or SERVER_URLS.get(
        server_name.lower()
    )

    if not server_url:
        return {"error": f"Unknown server: {server_name}"}

    if not server_url.endswith("/"):
        server_url += "/"

    # List tools endpoint varies by server
    # Try common patterns
    endpoints = [
        f"{server_url}tools",
        f"{server_url}schema/tools",
        f"{server_url}",
    ]

    for endpoint in endpoints:
        try:
            req = Request(endpoint, headers={"Accept": "application/json"})
            with urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode("utf-8"))
                if isinstance(data, dict) and ("tools" in data or "functions" in data):
                    return data
        except Exception:
            continue

    return {"error": "Could not list tools", "server": server_name}


def main():
    parser = argparse.ArgumentParser(description="Universal MCP Client")
    parser.add_argument("--server", "-s", required=True, help="MCP server name")
    parser.add_argument("--tool", "-t", required=True, help="Tool name to call")
    parser.add_argument(
        "--args", "-a", default="{}", help="Tool arguments as JSON string"
    )
    parser.add_argument(
        "--list", "-l", action="store_true", help="List available tools"
    )

    args = parser.parse_args()

    if args.list:
        result = list_tools(args.server)
    else:
        try:
            args_dict = json.loads(args.args) if args.args else {}
        except json.JSONDecodeError:
            print(json.dumps({"error": f"Invalid JSON args: {args.args}"}))
            sys.exit(1)

        result = call_mcp_tool(args.server, args.tool, args_dict)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
