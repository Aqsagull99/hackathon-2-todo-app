"""Official MCP server for Phase III AI Chatbot."""

import asyncio
import json
import logging
from typing import Dict, List

from mcp.server import Server
from mcp.types import Tool, TextContent
from sqlmodel import select

from app.mcp.schemas import (
    AddTaskParams,
    ListTasksParams,
    CompleteTaskParams,
    DeleteTaskParams,
    UpdateTaskParams,
    AddTagToTaskParams,
)

# Initialize Official MCP server
server = Server("todo-mcp-server")

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/mcp_tools.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("mcp_tools")


@server.list_tools()
async def list_tools() -> List[Tool]:
    """List all available MCP tools."""
    return [
        Tool(
            name="add_task",
            description="Create a new task for the user",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "format": "uuid", "description": "User identifier"},
                    "title": {"type": "string", "minLength": 1, "maxLength": 200, "description": "Task title"},
                    "description": {"type": "string", "maxLength": 1000, "description": "Optional task description"},
                    "priority": {"type": "string", "enum": ["high", "medium", "low"], "default": "medium", "description": "Task priority level"},
                    "tag_ids": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "description": "Optional list of tag IDs"
                    }
                },
                "required": ["user_id", "title"]
            }
        ),
        Tool(
            name="list_tasks",
            description="Retrieve user's tasks with optional filters",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "format": "uuid"},
                    "status": {
                        "type": "string",
                        "enum": ["all", "pending", "completed"],
                        "default": "all"
                    },
                    "priority": {
                        "type": "string",
                        "enum": ["high", "medium", "low"]
                    },
                    "tag_query": {
                        "type": "string",
                        "description": "Filter by tag name"
                    },
                    "search_query": {
                        "type": "string",
                        "description": "Keyword search in title/description"
                    },
                    "sort_by": {
                        "type": "string",
                        "enum": ["priority", "due_date", "title", "created_at"],
                        "default": "created_at"
                    }
                },
                "required": ["user_id"]
            }
        ),
        Tool(
            name="complete_task",
            description="Mark a task as complete",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "format": "uuid"},
                    "task_id": {"type": "integer"}
                },
                "required": ["user_id", "task_id"]
            }
        ),
        Tool(
            name="delete_task",
            description="Permanently delete a task",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "format": "uuid"},
                    "task_id": {"type": "integer"}
                },
                "required": ["user_id", "task_id"]
            }
        ),
        Tool(
            name="update_task",
            description="Update task fields",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "format": "uuid"},
                    "task_id": {"type": "integer"},
                    "title": {"type": "string"},
                    "description": {"type": "string"},
                    "priority": {"type": "string", "enum": ["high", "medium", "low"]}
                },
                "required": ["user_id", "task_id"]
            }
        ),
        Tool(
            name="add_tag_to_task",
            description="Add or create a tag and associate with task",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "format": "uuid"},
                    "task_id": {"type": "integer"},
                    "tag_name": {"type": "string"}
                },
                "required": ["user_id", "task_id", "tag_name"]
            }
        )
    ]


# Tool implementation mapping
tool_implementations: Dict[str, callable] = {}

# We'll populate this after defining the tools in tools.py
# For now, we'll implement a placeholder that loads implementations dynamically


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> List[TextContent]:
    """Handle tool execution requests."""
    logger.info(f"MCP Tool Called: {name} with args: {arguments}")

    # Import tool implementations here to avoid circular imports
    from app.mcp.tools import (
        add_task_impl,
        list_tasks_impl,
        complete_task_impl,
        delete_task_impl,
        update_task_impl,
        add_tag_to_task_impl
    )

    # Map tool names to implementations
    tool_map = {
        "add_task": add_task_impl,
        "list_tasks": list_tasks_impl,
        "complete_task": complete_task_impl,
        "delete_task": delete_task_impl,
        "update_task": update_task_impl,
        "add_tag_to_task": add_tag_to_task_impl
    }

    if name not in tool_map:
        error_result = {"error": f"Unknown tool: {name}", "status": "failed"}
        logger.error(f"Unknown tool: {name}")
        return [TextContent(type="text", text=json.dumps(error_result))]

    try:
        # Execute the tool
        result = await tool_map[name](**arguments)
        logger.info(f"MCP Tool Result: {name} -> {result}")

        # Return result as TextContent
        return [TextContent(type="text", text=json.dumps(result))]
    except Exception as e:
        error_result = {"error": str(e), "status": "failed"}
        logger.error(f"Tool execution error: {name} -> {str(e)}")
        return [TextContent(type="text", text=json.dumps(error_result))]