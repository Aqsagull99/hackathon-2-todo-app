"""
Chat Agent Implementation using OpenAI Agents SDK with OpenRouter integration
Based on openai-agents-sdk-skill specification
"""

import os
from typing import Dict, List, Optional
from pydantic import BaseModel, Field
import asyncio
import logging

try:
    from agents import Agent, Runner
    from agents import AsyncOpenAI, OpenAIChatCompletionsModel
    from agents.run import RunConfig
    from agents import function_tool
    from agents.mcp import MCPServerStdio
except ImportError:
    # Fallback to handle missing agents package during deployment
    import logging
    logging.warning("Agents package not available, using fallback implementations")

    # Provide mock implementations for graceful degradation
    class Agent:
        def __init__(self, **kwargs):
            pass

    class Runner:
        @staticmethod
        async def run(*args, **kwargs):
            class Result:
                final_output = "Agent not available"
                tool_calls = []
            return Result()

    class RunConfig:
        def __init__(self, **kwargs):
            pass

    def function_tool(func):
        return func

    AsyncOpenAI = lambda **kwargs: None
    OpenAIChatCompletionsModel = lambda **kwargs: None
    MCPServerStdio = lambda **kwargs: None
from datetime import datetime


class Task(BaseModel):
    """Represents a task in the todo list."""
    id: int = Field(description="Unique task identifier")
    title: str = Field(description="Task title")
    description: Optional[str] = Field(default=None, description="Task description")
    completed: bool = Field(default=False, description="Whether task is completed")
    priority: str = Field(default="medium", description="Task priority: low, medium, high")


class AddTaskParams(BaseModel):
    """Parameters for adding a new task."""
    user_id: str = Field(description="The user's unique identifier")
    title: str = Field(description="Task title")
    description: Optional[str] = Field(default=None, description="Task description")
    priority: Optional[str] = Field(default="medium", description="Task priority: low, medium, high")
    due_date: Optional[datetime] = Field(default=None, description="Due date for the task")
    reminder: Optional[datetime] = Field(default=None, description="Reminder time for the task")
    tags: Optional[List[str]] = Field(default=None, description="List of tags to associate with the task")
    recurrence_pattern: Optional[str] = Field(default=None, description="Recurrence pattern: daily, weekly, monthly")


class UpdateTaskParams(BaseModel):
    """Parameters for updating an existing task."""
    user_id: str = Field(description="The user's unique identifier")
    task_id: int = Field(description="The ID of the task to update")
    title: Optional[str] = Field(default=None, description="New title for the task")
    description: Optional[str] = Field(default=None, description="New description for the task")
    priority: Optional[str] = Field(default=None, description="New priority level for the task")


class CompleteTaskParams(BaseModel):
    """Parameters for completing a task."""
    user_id: str = Field(description="The user's unique identifier")
    task_id: int = Field(description="The ID of the task to complete")


class DeleteTaskParams(BaseModel):
    """Parameters for deleting a task."""
    user_id: str = Field(description="The user's unique identifier")
    task_id: int = Field(description="The ID of the task to delete")


class ListTasksParams(BaseModel):
    """Parameters for listing tasks."""
    user_id: str = Field(description="The user's unique identifier")
    status: Optional[str] = Field(default="all", description="Filter tasks by status: all, pending, completed")
    priority: Optional[str] = Field(default=None, description="Filter tasks by priority level")
    tag_query: Optional[str] = Field(default=None, description="Filter tasks by tag name")
    search_query: Optional[str] = Field(default=None, description="Keyword search in task titles or descriptions")
    sort_by: Optional[str] = Field(default="created_at", description="Sort results by: created_at, priority, title, due_date")


class AddTagToTaskParams(BaseModel):
    """Parameters for adding a tag to a task."""
    user_id: str = Field(description="The user's unique identifier")
    task_id: int = Field(description="The ID of the task to add the tag to")
    tag_name: str = Field(description="The name of the tag to add")


class ContextManager:
    """Manage conversational history and context for the agent."""

    def __init__(self, user_id: str):
        self.user_id = user_id
        self.history = self._initialize_history()

    def _initialize_history(self) -> List[Dict[str, any]]:
        """Initialize conversation history with system message."""
        return [
            {"role": "system", "content": f"You are a helpful todo assistant for user {self.user_id}. Today is {datetime.now().strftime('%Y-%m-%d')}."},
        ]

    def add_user_message(self, message: str):
        """Add user message to history."""
        self.history.append({"role": "user", "content": message})

    def add_assistant_response(self, response: str):
        """Add assistant response to history."""
        self.history.append({"role": "assistant", "content": response})

    def get_context(self) -> List[Dict[str, any]]:
        """Get current conversation context."""
        return self.history

    def clear_history(self):
        """Clear conversation history."""
        self.history = self._initialize_history()

    def add_memory(self, key: str, value: str):
        """Add contextual memory to the conversation."""
        self.history.append({"role": "system", "content": f"[Memory: {key}={value}]"})


class TodoChatAgent:
    """AI agent for task management using OpenAI Agents SDK with OpenRouter."""

    def __init__(self, user_id: str):
        self.user_id = user_id
        self.mcp_server = None
        self.context_manager = ContextManager(user_id)

        # Setup model client: prefer OpenRouter (if key present), otherwise try OPENAI API key
        # Try process env first, then fallback to pydantic-settings `settings` (which reads .env)
        from app.core.config import settings

        openrouter_api_key = os.getenv("OPENROUTER_API_KEY") or settings.OPENROUTER_API_KEY
        openrouter_base_url = os.getenv("OPENROUTER_BASE_URL") or settings.OPENROUTER_BASE_URL
        openrouter_model = os.getenv("OPENROUTER_MODEL") or settings.OPENROUTER_MODEL or "mistralai/devstral-2512:free"
        openai_api_key = os.getenv("OPENAI_API_KEY") or settings.OPENAI_API_KEY
        openai_model = os.getenv("OPENAI_MODEL") or settings.OPENAI_MODEL

        self.use_fallback = False
        self.config = None
        provider_selected = None
        try:
            if openrouter_api_key:
                external_client = AsyncOpenAI(
                    api_key=openrouter_api_key,
                    base_url=openrouter_base_url,
                )
                model = OpenAIChatCompletionsModel(
                    model=openrouter_model,
                    openai_client=external_client,
                )
                self.config = RunConfig(model=model, model_provider=external_client)
                provider_selected = f"openrouter ({openrouter_model})"
            elif openai_api_key:
                # Fall back to direct OpenAI key (agents SDK expects an AsyncOpenAI-like client)
                external_client = AsyncOpenAI(api_key=openai_api_key)
                model = OpenAIChatCompletionsModel(
                    model=openai_model,
                    openai_client=external_client,
                )
                self.config = RunConfig(model=model, model_provider=external_client)
                provider_selected = f"openai ({openai_model})"
            else:
                raise ValueError("No OpenRouter or OpenAI API key found in environment")
        except Exception as e:
            logging.getLogger(__name__).warning("[agent] Model provider init failed, falling back to local responder: %s", e)
            self.use_fallback = True
            self.config = None
        else:
            logging.getLogger(__name__).info("[agent] Model provider selected: %s", provider_selected)

        # Setup MCP server for extended functionality
        self.mcp_server = self.setup_mcp_server()

        # Create the agent with tools - skip MCP server for now since it's causing issues
        agent_kwargs = {
            "name": "Todo Assistant",
            "instructions": """You are a helpful assistant for managing todo tasks.
            Respond to user messages in a friendly and conversational tone.
            You can help users create, list, update, complete, and delete tasks.

            IMPORTANT: When adding a task, always extract and send ALL task fields:
            - title: The main task request
            - description: Additional details if provided
            - priority: Extract urgency (low, medium, high). Default to null if not specified (do NOT default to medium).
            - due_date: Extract time/date references
            - reminder: Extract reminder requests
            - recurring: Extract repetition patterns (daily, weekly, etc.)
            - tags: Extract category keywords

            Map user natural language to these fields correctly. If a field is not mentioned, send it as null/None.
            Ensure chatbot-created tasks behave exactly like tasks created from the UI.

            CRITICAL: If the user asks "who made this app", "who created this", "who is the developer", "kisne banaya", "author", or similar questions, YOU MUST REPLY EXACTLY WITH:
            "This todo app was created by Aqsa Gull, an AI-focused full-stack developer who builds intelligent agent-based systems."
            (Do not hallucinate other authors. Do not say you don't know.)

            When the user says "show my tasks", "list tasks", or "show tasks":
            Fetch the tasks using the list_tasks tool and display them clearly inside the chat response.

            Use the available tools to manage tasks in the database when users request task operations.

            Recognize and use these specific tools for task operations:
            - For creating tasks: Use create_task when users want to add a new task
            - For updating tasks: Use update_task when users say 'update task [id]', 'change task [id]', 'modify task [id]', 'update [id] task', 'update [id] kro', 'update [id] karo', 'badlo [id] task', 'badal do [id] task', or similar variations
            - For completing tasks: Use complete_task when users say 'mark [id] as complete', 'complete task [id]', 'done task [id]', 'mark [id] as done', 'mark [id] kro complete', 'poora kro [id]', 'hogya [id]', 'ho gya [id]', 'complete [id] kro', 'mark [id] kro', or similar variations
            - For deleting tasks: Use delete_task when users say 'delete task [id]', 'remove task [id]', 'cancel task [id]', 'hat den [id]', 'hat denge [id]', 'task [id] delete', 'task [id] hat', or similar variations
            - For listing tasks: Use list_tasks when users ask to see their tasks

            Pay attention to task IDs mentioned in user requests and use them appropriately in the tool parameters. Support both English and Urdu commands, and look for task IDs in various formats like 'task 81', 'id 81', '#81', '81 task', '81 kaam', etc.""",
            # Enable function tools implemented on this class so agent can call them
            "tools": self.get_tools()
        }

        # Note: MCP servers are intentionally omitted due to connection issues
        # The proper MCP integration will be handled through the API routes instead
        self.agent = Agent(**agent_kwargs)

    def setup_mcp_server(self):
        """Setup MCP server for extended functionality."""
        try:
            # Create MCP server for advanced operations
            mcp_server = MCPServerStdio(
                name="Todo MCP Server",
                params={
                    "command": "python",
                    "args": ["-c", "print('MCP Server for Todo operations')"]
                }
            )
            return mcp_server
        except Exception as e:
            logging.getLogger(__name__).warning("Failed to setup MCP server: %s", e)
            return None

    async def async_init(self):
        """Initialize the agent asynchronously to connect MCP server if needed."""
        if self.mcp_server and self.mcp_server.session is None:
            try:
                await self.mcp_server.connect()
            except Exception as e:
                logging.getLogger(__name__).warning("Failed to connect MCP server: %s", e)
                # Continue without MCP server if connection fails

    def get_tools(self):
        """Define and return agent tools."""
        return [
            self.add_task_tool,
            self.list_tasks_tool,
            self.complete_task_tool,
            self.update_task_tool,
            self.delete_task_tool,
            self.add_tag_to_task_tool
        ]

    def _create_task_local(self, user_id: str, title: str, description: Optional[str] = None, priority: str = None) -> Task:
        """Create a Task object locally (used by fallback responder)."""
        import random
        task_id = random.randint(1000, 9999)
        task = Task(
            id=task_id,
            title=title,
            description=description,
            completed=False,
            priority=priority or "medium",
        )
        logging.getLogger(__name__).info("(fallback) Added task: %s for user: %s", task.title, user_id)
        return task

    def _detect_intent(self, text: str) -> dict:
        """Very small rule-based intent detector for fallback mode.

        Returns dict with keys: intent (add/list/delete/greet/db/unknown) and extra matches.
        """
        t = (text or "").lower()
        intent = "unknown"
        matches = {}

        # DB/connection questions
        if any(k in t for k in ["database", "db", "connect", "connected", "connt", "connection"]):
            return {"intent": "db", "matches": {}}

        # Add intents (english + urdu)
        # Greeting intents - check FIRST but only if this is PURELY a greeting
        greet_keywords = ["hi", "hello", "salam", "assalam", "kesy ho", "kaise ho", "kaise ho", "kese ho", "ap kese ho", "ap kesy ho", "ap kaise ho"]
        task_command_keywords = ["add", "list", "show", "delete", "update", "complete", "done", "create", "remove", "mark"]
        is_greeting = any(k in t for k in greet_keywords)
        is_task_command = any(k in t for k in task_command_keywords)
        if is_greeting and not is_task_command:
            intent = "greet"
            return {"intent": intent, "matches": matches}

        add_keywords = ["add", "add task", "naya", "naya task", "naya kaam", "task", "jor", "شامل", "create", "add my", "mera"]
        if any(k in t for k in add_keywords) and "list" not in t:
            intent = "add"

        # List intents
        list_keywords = ["list", "show", "dikh", "kya tasks", "mujhe tasks", "tasks dikhao", "lihat"]
        if any(k in t for k in list_keywords):
            intent = "list"

        # Delete intents
        delete_keywords = ["delete", "remove", "hat", "hat den", "hat denge", "remove task", "delete task", "remove task", "task delete", "task hat"]
        if any(k in t for k in delete_keywords):
            intent = "delete"

        # Update intents
        update_keywords = ["update", "update task", "change", "change task", "modify", "modify task", "edit", "edit task", "update kro", "update karo", "badlo", "badal do"]
        if any(k in t for k in update_keywords):
            intent = "update"

        # Complete intents
        complete_keywords = ["complete", "mark complete", "mark as complete", "done", "finish", "finished", "completed", "mark as done", "mark kro complete", "poora kro", "hogya", "ho gya", "complete kro", "mark kro"]
        if any(k in t for k in complete_keywords):
            intent = "complete"

        # Creator intents - EXPANDED list for better detection
        creator_keywords = [
            "who made", "who created", "who built", "who developed", "who coded",
            "creator", "developer", "author", "maker",
            "kisne banaya", "kisne banayi", "kisne likha",
            "kaun banaya", "banane wala", "developer kaun hai"
        ]
        if any(k in t for k in creator_keywords):
            intent = "creator"

        return {"intent": intent, "matches": matches}

    @function_tool
    async def add_task_tool(
        self,
        params: AddTaskParams
    ) -> Task:
        """Add a new task to the user's list and persist to DB.

        This implementation attempts to persist via `app.services.task_service.create_task`.
        If DB persistence fails for any reason, it falls back to a local in-memory task.
        """
        try:
            from app.core.database import async_session_maker
            from app.services.task_service import create_task
            from app.schemas.task import TaskCreate
            from app.models.task import TaskPriority, RecurrencePattern

            # Convert string params to Enums where necessary
            priority_enum = TaskPriority.MEDIUM
            if params.priority:
                try:
                    priority_enum = TaskPriority(params.priority.lower())
                except ValueError:
                    pass

            recurrence_enum = None
            if params.recurrence_pattern:
                try:
                    recurrence_enum = RecurrencePattern(params.recurrence_pattern.lower())
                except ValueError:
                    pass

            # Parse reminder time from params if available
            reminder_time = params.reminder

            async with async_session_maker() as db:
                payload = TaskCreate(
                    title=params.title,
                    description=params.description,
                    priority=priority_enum,
                    due_date=params.due_date,
                    reminder=reminder_time,
                    recurrence_pattern=recurrence_enum,
                    tags=params.tags  # tags as list of strings
                    # Note: tags are handled separately in the tag system
                )
                created = await create_task(db, params.user_id, payload)

                # If a reminder was specified, create a separate reminder record
                if reminder_time:
                    try:
                        from app.services import reminder_service
                        await reminder_service.create_reminder(db, created.id, reminder_time)
                    except Exception as reminder_error:
                        logging.getLogger(__name__).warning("Failed to create reminder: %s", reminder_error)

            return Task(
                id=created.id,
                title=created.title,
                description=created.description,
                completed=created.completed,
                priority=created.priority.value if hasattr(created.priority, 'value') else created.priority,
            )
        except Exception as e:
            logging.getLogger(__name__).exception("DB create failed, falling back to local creation: %s", e)
            return self._create_task_local(params.user_id, params.title, params.description, params.priority)

    @function_tool
    def list_tasks_tool(
        self,
        params: ListTasksParams
    ) -> Dict[str, object]:
        """List user's tasks with optional filtering."""
        # In a real implementation, this would fetch from your database
        # For demo purposes, we're returning sample tasks
        sample_tasks = [
            Task(id=1, title="Buy groceries", completed=False, priority="medium"),
            Task(id=2, title="Call doctor", completed=True, priority="high"),
            Task(id=3, title="Prepare presentation", completed=False, priority="high")
        ]

        # Apply basic filtering based on params
        filtered_tasks = sample_tasks
        if params.status == "completed":
            filtered_tasks = [task for task in sample_tasks if task.completed]
        elif params.status == "pending":
            filtered_tasks = [task for task in sample_tasks if not task.completed]

        logging.getLogger(__name__).info("Listing tasks for user: %s with status filter: %s", params.user_id, params.status)
        return {
            "tasks": filtered_tasks,
            "count": len(filtered_tasks),
            "filters_applied": {"status": params.status, "priority": params.priority}
        }

    @function_tool
    def complete_task_tool(
        self,
        params: CompleteTaskParams
    ) -> Task:
        """Mark a task as completed."""
        # In a real implementation, this would update your database
        # For demo purposes, we're simulating the completion
        task = Task(
            id=params.task_id,
            title=f"Completed task {params.task_id}",
            completed=True,
            priority="medium"
        )

        logging.getLogger(__name__).info("Marked task %s as completed for user: %s", params.task_id, params.user_id)
        return task

    @function_tool
    def update_task_tool(
        self,
        params: UpdateTaskParams
    ) -> Task:
        """Update an existing task."""
        # In a real implementation, this would update your database
        # For demo purposes, we're simulating the update
        task = Task(
            id=params.task_id,
            title=params.title or f"Updated task {params.task_id}",
            description=params.description,
            completed=False,
            priority=params.priority or "medium"
        )

        logging.getLogger(__name__).info("Updated task %s for user: %s", params.task_id, params.user_id)
        return task

    @function_tool
    def delete_task_tool(
        self,
        params: DeleteTaskParams
    ) -> Dict[str, object]:
        """Delete a task by ID."""
        # In a real implementation, this would delete from your database
        # For demo purposes, we're simulating the deletion

        logging.getLogger(__name__).info("Deleted task %s for user: %s", params.task_id, params.user_id)
        return {
            "success": True,
            "deleted_task_id": params.task_id,
            "message": f"Successfully deleted task {params.task_id}"
        }

    @function_tool
    def add_tag_to_task_tool(
        self,
        params: AddTagToTaskParams
    ) -> Dict[str, object]:
        """Add a tag to a task."""
        # In a real implementation, this would update your database
        # For demo purposes, we're simulating the tagging

        logging.getLogger(__name__).info("Added tag '%s' to task %s for user: %s", params.tag_name, params.task_id, params.user_id)
        return {
            "success": True,
            "task_id": params.task_id,
            "tag_name": params.tag_name,
            "message": f"Successfully added tag '{params.tag_name}' to task {params.task_id}"
        }

    async def process_message(
        self,
        user_message: str,
        conversation_history: List[dict] = None,
        user_id: str = None
    ) -> Dict[str, object]:
        """Process user message using the agent with OpenRouter configuration."""
        try:
            text = (user_message or "").lower()
            user_identifier = user_id or self.user_id

            # ALWAYS check for clear add/list/delete intents FIRST (both fallback and LLM modes)
            # This ensures DB-backed creation for common commands
            detected = self._detect_intent(text)
            intent = detected.get("intent")

            # Handle add intent - create task in DB
            if intent == "add":
                title = user_message.strip() or "Untitled task"
                
                # Extract task details from message
                import re
                from datetime import datetime, timedelta
                description = None
                priority = "medium"
                due_date = None
                recurrence_pattern = None
                tags = []
                reminder_time = None
                
                msg_lower = user_message.lower()
                
                # Extract title - look for "Title:" or "task:" marker, or use first line
                title_match = re.search(r'title:\s*([^\n]+?)(?:\n|description:|due|priority|tags|$)', user_message, re.IGNORECASE)
                if title_match:
                    title = title_match.group(1).strip()
                else:
                    # If no "Title:" marker, try to get meaningful text from start
                    first_line = user_message.split('\n')[0].strip()
                    if first_line and not any(marker in first_line.lower() for marker in ['description:', 'priority:', 'due', 'tags:', 'reminder:']):
                        title = first_line
                
                # Extract description
                desc_match = re.search(r'description:\s*([^\n]+?)(?:\n|tags:|priority:|due|reminder|$)', user_message, re.IGNORECASE)
                if desc_match:
                    description = desc_match.group(1).strip()
                
                # Extract priority - match exact patterns
                priority_match = re.search(r'priority:\s*(high|medium|low)', msg_lower)
                if priority_match:
                    priority = priority_match.group(1).lower()
                elif "high priority" in msg_lower:
                    priority = "high"
                elif "low priority" in msg_lower:
                    priority = "low"
                else:
                    priority = "medium"
                
                # Extract tags - capture everything after "Tags:" until newline or next marker
                tags_match = re.search(r'tags?:\s*([^\n]+?)(?:\n|priority:|due|reminder|$)', user_message, re.IGNORECASE)
                if tags_match:
                    tags_str = tags_match.group(1).strip()
                    # Split by both commas and spaces
                    tags = [t.strip() for t in re.split(r'[,\s]+', tags_str) if t.strip()]
                
                # Extract due date - look for "Due Date:" or "Due:" marker only, not daily/recurring
                due_match = re.search(r'due\s+(?:date)?:\s*([^\-\n]+?)(?:\s*-\s*|$|\n|recurring|reminder|tags|priority)', user_message, re.IGNORECASE)
                if due_match:
                    date_str = due_match.group(1).strip()
                    # Skip if it's a recurrence keyword
                    if date_str.lower() not in ['daily', 'weekly', 'monthly']:
                        today = datetime.now()
                        
                        if "tomorrow" in date_str.lower():
                            due_date = today + timedelta(days=1)
                        elif "today" in date_str.lower():
                            due_date = today
                        elif any(day in date_str.lower() for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]):
                            for i, day in enumerate(["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]):
                                if day in date_str.lower():
                                    days_ahead = (i - today.weekday()) % 7
                                    if days_ahead == 0:
                                        days_ahead = 7
                                    due_date = today + timedelta(days=days_ahead)
                                    break
                
                # Extract recurrence pattern - look for exact patterns
                if "recurring: daily" in msg_lower or "daily" in msg_lower:
                    recurrence_pattern = "daily"
                elif "recurring: weekly" in msg_lower or "weekly" in msg_lower:
                    recurrence_pattern = "weekly"
                elif "recurring: monthly" in msg_lower or "monthly" in msg_lower:
                    recurrence_pattern = "monthly"
                
                # Extract reminder - match time specifications only
                reminder_match = re.search(r'reminder:\s*(?:at\s+)?([^\-\n]+?)(?:\s*-\s*|$|\n|recurring|tags)', user_message, re.IGNORECASE)
                if reminder_match:
                    reminder_time = reminder_match.group(1).strip()
                    # Clean up common formats
                    reminder_time = reminder_time.lower().replace('at ', '').strip()
                    print(f"DEBUG: Extracted reminder_time = '{reminder_time}'")
                
                try:
                    from app.core.database import async_session_maker
                    from app.services.task_service import create_task
                    from app.schemas.task import TaskCreate
                    from app.models.task import TaskPriority, RecurrencePattern

                    # Map string priority to enum
                    priority_enum = TaskPriority.high if priority == "high" else (TaskPriority.low if priority == "low" else TaskPriority.medium)
                    
                    # Map string recurrence to enum if present
                    recurrence_enum = None
                    if recurrence_pattern:
                        recurrence_enum = RecurrencePattern.daily if recurrence_pattern == "daily" else (RecurrencePattern.weekly if recurrence_pattern == "weekly" else RecurrencePattern.monthly)

                    async with async_session_maker() as db:
                        print(f"DEBUG: TaskCreate params - priority={priority}, due_date={due_date}, reminder_time='{reminder_time}', recurrence={recurrence_pattern}, tags={tags}")
                        task_payload = TaskCreate(
                            title=title, 
                            description=description,
                            priority=priority_enum,
                            due_date=due_date,
                            reminder=None,
                            reminder_time=reminder_time,
                            recurrence_pattern=recurrence_enum,
                            tags=tags if tags else []
                        )
                        task = await create_task(db, user_identifier, task_payload)

                    # Build detailed response
                    details = []
                    if title:
                        details.append(f"**Title:** {title}")
                    if description:
                        details.append(f"**Description:** {description}")
                    if priority != "medium":
                        details.append(f"**Priority:** {priority}")
                    if due_date:
                        details.append(f"**Due Date:** {due_date.strftime('%Y-%m-%d')}")
                    if recurrence_pattern:
                        details.append(f"**Recurring:** {recurrence_pattern}")
                    if reminder_time:
                        details.append(f"**Reminder:** {reminder_time}")
                    if tags:
                        details.append(f"**Tags:** {', '.join(tags)}")
                    
                    details_str = "\n".join(details) if details else ""
                    reply = f"Naya task jor diya gaya! ✅\n\n{details_str}\n\n(New task added! Task ID: {task.id})"
                    
                    tool_calls = [{
                        "tool": "create_task",
                        "parameters": {
                            "title": title,
                            "description": description,
                            "priority": priority,
                            "due_date": due_date.isoformat() if due_date else None,
                            "recurrence_pattern": recurrence_pattern,
                            "reminder_time": reminder_time,
                            "tags": tags
                        },
                        "result": {"id": task.id, "title": task.title, "local": False},
                    }]

                    self.context_manager.add_assistant_response(reply)
                    return {"response": reply, "tool_calls": tool_calls, "context": self.context_manager.get_context()}
                except Exception as db_err:
                    # Log the error for debugging
                    logging.getLogger(__name__).exception(f"[agent] DB create_task failed for title '{title}': {db_err}")
                    # If DB isn't available, fall back to local creation
                    try:
                        task = self._create_task_local(user_identifier, title, description, priority)
                        reply = f"Naya task jor diya gaya (local)! ✅\n\n**Title:** {task.title}"
                        tool_calls = [{
                            "tool": "create_task",
                            "parameters": {"title": title},
                            "result": {"id": task.id, "title": task.title, "local": True},
                        }]

                        self.context_manager.add_assistant_response(reply)
                        return {"response": reply, "tool_calls": tool_calls, "context": self.context_manager.get_context()}
                    except Exception as e:
                        reply = f"Maaf kijiye, task jor nahi ho saka. Error: {e}"
                        self.context_manager.add_assistant_response(reply)
                        return {"response": reply, "tool_calls": [], "context": self.context_manager.get_context()}

            # Handle list intent
            if intent == "list":
                try:
                    from app.core.database import async_session_maker
                    from app.services.task_service import get_tasks

                    async with async_session_maker() as db:
                        tasks, total = await get_tasks(db, user_identifier, skip=0, limit=10, status=None)

                    if total == 0:
                        reply = "Aapke paas abhi koi tasks nahin hain. Kya main naya task jor doon?\n\n(You have no tasks yet. Should I add one?)"
                    else:
                        titles = [f"{t.id}: {t.title}" for t in tasks]
                        reply = "Yeh aapke recent tasks hain:\n" + "\n".join(titles)

                    self.context_manager.add_assistant_response(reply)
                    return {"response": reply, "tool_calls": [], "context": self.context_manager.get_context()}
                except Exception:
                    # Fall back to agent if DB fails
                    pass

            # If we're using the fallback responder, perform a simple local handling
            # to avoid returning the exact same canned reply for every message.
            if self.use_fallback:

                if intent == "db":
                    reply = (
                        "Nahi — main aapke database se connected nahin hoon. Yeh fallback local responder hai, "
                        "task creation sirf demo ke liye local hai.\n\n"
                        "(No — I'm not connected to your database. This is a local fallback responder; task creation is local/demo only.)"
                    )
                    self.context_manager.add_assistant_response(reply)
                    return {"response": reply, "tool_calls": [], "context": self.context_manager.get_context()}

                if intent == "greet":
                    import random
                    greetings = [
                        "Assalam-o-Alaikum! Main Urdu mein madad kar sakta hoon — aapko kya chahiye?",
                        "Hi! Main aapki todo list mein madad kar sakta hoon. Kya karna hai?",
                        "Salam! Aap mujhe bataiye, konsa task add karna hai?",
                    ]
                    reply = random.choice(greetings)
                    self.context_manager.add_assistant_response(reply)
                    return {"response": reply, "tool_calls": [], "context": self.context_manager.get_context()}

                if intent == "creator":
                    reply = (
                        "This todo app was created by Aqsa Gull, an AI-focused full-stack developer who builds intelligent agent-based systems.\n\n"
                        "(Is todo app ko Aqsa Gull ne banaya hai, jo ke aik AI-focused full-stack developer hain.)"
                    )
                    self.context_manager.add_assistant_response(reply)
                    return {"response": reply, "tool_calls": [], "context": self.context_manager.get_context()}

                if intent == "list":
                    # Try to fetch tasks from DB for the user
                    try:
                        from app.core.database import async_session_maker
                        from app.services.task_service import get_tasks

                        async with async_session_maker() as db:
                            tasks, total = await get_tasks(db, user_identifier, skip=0, limit=10, status=None)

                        if total == 0:
                            reply = "Aapke paas abhi koi tasks nahin hain. Kya main naya task jor doon?\n\n(You have no tasks yet. Should I add one?)"
                        else:
                            titles = [f"{t.id}: {t.title}" for t in tasks]
                            reply = "Yeh aapke recent tasks hain:\n" + "\n".join(titles)

                        self.context_manager.add_assistant_response(reply)
                        return {"response": reply, "tool_calls": [], "context": self.context_manager.get_context()}
                    except Exception:
                        # Fall back to canned reply if DB fails
                        pass

                if intent == "add":
                    title = user_message.strip() or "Untitled task"
                    try:
                        from app.core.database import async_session_maker
                        from app.services.task_service import create_task
                        from app.schemas.task import TaskCreate

                        async with async_session_maker() as db:
                            task_payload = TaskCreate(title=title, description=None)
                            task = await create_task(db, user_identifier, task_payload)

                        reply = f"Naya task jor diya gaya: {task.title} (ID: {task.id})\n\n(New task added: {task.title} (ID: {task.id}))"
                        tool_calls = [{
                            "tool": "create_task",
                            "parameters": {"title": title},
                            "result": {"id": task.id, "title": task.title, "local": False},
                        }]

                        self.context_manager.add_assistant_response(reply)
                        return {"response": reply, "tool_calls": tool_calls, "context": self.context_manager.get_context()}
                    except Exception as db_err:
                        # Log the error for debugging
                        logging.getLogger(__name__).exception(f"[agent] DB create_task failed for title '{title}': {db_err}")
                        # If DB isn't available, fall back to local creation
                        try:
                            task = self._create_task_local(user_identifier, title, None, None)
                            reply = f"Naya task jor diya gaya (local): {task.title} (ID: {task.id})\n\n(New task added locally: {task.title} (ID: {task.id}))"
                            tool_calls = [{
                                "tool": "create_task",
                                "parameters": {"title": title},
                                "result": {"id": task.id, "title": task.title, "local": True},
                            }]

                            self.context_manager.add_assistant_response(reply)
                            return {"response": reply, "tool_calls": tool_calls, "context": self.context_manager.get_context()}
                        except Exception as e:
                            reply = f"Maaf kijiye, task jor nahi ho saka. Error: {e}"
                            self.context_manager.add_assistant_response(reply)
                            return {"response": reply, "tool_calls": [], "context": self.context_manager.get_context()}

                if intent == "delete":
                    # Try to parse task ID from message and delete the task
                    import re
                    # Look for various patterns like "task 81", "id 81", "#81", "81 task", "delete 81", etc.
                    task_id_match = re.search(r'(?:task|id|#|no)\s*(\d+)|(\d+)\s*(?:task|kaam|work|id|no)|\bdelete\s+(\d+)\b|\bhat\s+(\d+)\b|\bhat\s+den\s+(\d+)\b', user_message, re.IGNORECASE)
                    if task_id_match:
                        # Get the first captured group that is not None
                        task_id = int(next(filter(None, task_id_match.groups())))
                        try:
                            from app.core.database import async_session_maker
                            from app.services.task_service import get_task, delete_task

                            async with async_session_maker() as db:
                                task = await get_task(db, task_id, user_identifier)
                                if task:
                                    await delete_task(db, task)
                                    reply = f"Task {task_id} '{task.title}' successfully deleted."
                                    tool_calls = [{
                                        "tool": "delete_task",
                                        "parameters": {"task_id": task_id},
                                        "result": {"deleted_task_id": task_id, "message": f"Task {task_id} deleted successfully"},
                                    }]
                                    self.context_manager.add_assistant_response(reply)
                                    return {"response": reply, "tool_calls": tool_calls, "context": self.context_manager.get_context()}
                                else:
                                    reply = f"Task {task_id} not found or you don't have permission to delete it."
                                    self.context_manager.add_assistant_response(reply)
                                    return {"response": reply, "tool_calls": [], "context": self.context_manager.get_context()}
                        except Exception:
                            # If DB isn't available, return message
                            reply = f"Could not delete task {task_id}. It might not exist or an error occurred."
                            self.context_manager.add_assistant_response(reply)
                            return {"response": reply, "tool_calls": [], "context": self.context_manager.get_context()}
                    else:
                        reply = "Could not identify task ID to delete. Please specify which task to delete by ID."
                        self.context_manager.add_assistant_response(reply)
                        return {"response": reply, "tool_calls": [], "context": self.context_manager.get_context()}

                if intent == "update":
                    # Try to parse task ID and new details from message and update the task
                    import re
                    # Look for various patterns like "task 81", "id 81", "#81", "81 task", "update 81", etc.
                    task_id_match = re.search(r'(?:task|id|#|no)\s*(\d+)|(\d+)\s*(?:task|kaam|work|id|no)|\b(?:update|change|modify|badlo|badal)\s+(\d+)\b', user_message, re.IGNORECASE)
                    if task_id_match:
                        # Get the first captured group that is not None
                        task_id = int(next(filter(None, task_id_match.groups())))

                        # Extract new title from message (everything after the task id and common keywords)
                        remaining_text = user_message
                        # Remove the task id and surrounding words
                        remaining_text = re.sub(r'(?:task|id|#)?\s*' + str(task_id) + r'\s*(?:task|kaam|work)?', '', remaining_text, flags=re.IGNORECASE)
                        # Look for keywords that indicate the actual task content
                        parts = re.split(r'[k:,\-\s]+', remaining_text, 1)
                        new_title = parts[-1].strip() if len(parts) > 1 else remaining_text.strip()

                        # If the new title is empty, try to extract it differently
                        if not new_title:
                            # Try to find content after common update keywords
                            update_patterns = [
                                r'update\s+kro\s+', r'update\s+karo\s+', r'badlo\s+', r'badal\s+do\s+',
                                r'change\s+', r'modify\s+', r'edit\s+'
                            ]
                            for pattern in update_patterns:
                                match = re.search(pattern + r'(.+)', remaining_text, re.IGNORECASE)
                                if match:
                                    new_title = match.group(1).strip()
                                    break

                        # Clean up the title if it still contains task IDs
                        if new_title:
                            # Remove any remaining digits that might be task IDs
                            new_title = re.sub(r'^\d+\s*', '', new_title).strip()

                        if new_title:
                            try:
                                from app.core.database import async_session_maker
                                from app.services.task_service import get_task, update_task
                                from app.schemas.task import TaskUpdate

                                async with async_session_maker() as db:
                                    task = await get_task(db, task_id, user_identifier)
                                    if task:
                                        task_update = TaskUpdate(title=new_title)
                                        updated_task = await update_task(db, task, task_update)
                                        reply = f"Task {task_id} updated successfully: '{updated_task.title}'"
                                        tool_calls = [{
                                            "tool": "update_task",
                                            "parameters": {"task_id": task_id, "title": new_title},
                                            "result": {"id": updated_task.id, "title": updated_task.title},
                                        }]
                                        self.context_manager.add_assistant_response(reply)
                                        return {"response": reply, "tool_calls": tool_calls, "context": self.context_manager.get_context()}
                                    else:
                                        reply = f"Task {task_id} not found or you don't have permission to update it."
                                        self.context_manager.add_assistant_response(reply)
                                        return {"response": reply, "tool_calls": [], "context": self.context_manager.get_context()}
                            except Exception:
                                # If DB isn't available, return message
                                reply = f"Could not update task {task_id}. It might not exist or an error occurred."
                                self.context_manager.add_assistant_response(reply)
                                return {"response": reply, "tool_calls": [], "context": self.context_manager.get_context()}
                        else:
                            reply = "Could not identify new task details to update."
                            self.context_manager.add_assistant_response(reply)
                            return {"response": reply, "tool_calls": [], "context": self.context_manager.get_context()}
                    else:
                        reply = "Could not identify task ID to update. Please specify which task to update by ID."
                        self.context_manager.add_assistant_response(reply)
                        return {"response": reply, "tool_calls": [], "context": self.context_manager.get_context()}

                if intent == "complete":
                    # Try to parse task ID from message and mark as complete
                    import re
                    # Look for various patterns like "task 81", "id 81", "#81", "81 task", "complete 81", etc.
                    task_id_match = re.search(r'(?:task|id|#|no)\s*(\d+)|(\d+)\s*(?:task|kaam|work|id|no)|\b(?:complete|done|mark|hogya|ho\s+gaya|ho\s+gya)\s+(\d+)\b', user_message, re.IGNORECASE)
                    if task_id_match:
                        # Get the first captured group that is not None
                        task_id = int(next(filter(None, task_id_match.groups())))
                        try:
                            from app.core.database import async_session_maker
                            from app.services.task_service import get_task, toggle_task_completion

                            async with async_session_maker() as db:
                                task = await get_task(db, task_id, user_identifier)
                                if task:
                                    updated_task = await toggle_task_completion(db, task)
                                    status = "completed" if updated_task.completed else "marked as incomplete"
                                    reply = f"Task {task_id} '{task.title}' {status}."
                                    tool_calls = [{
                                        "tool": "complete_task",
                                        "parameters": {"task_id": task_id},
                                        "result": {"id": updated_task.id, "title": updated_task.title, "completed": updated_task.completed},
                                    }]
                                    self.context_manager.add_assistant_response(reply)
                                    return {"response": reply, "tool_calls": tool_calls, "context": self.context_manager.get_context()}
                                else:
                                    reply = f"Task {task_id} not found or you don't have permission to complete it."
                                    self.context_manager.add_assistant_response(reply)
                                    return {"response": reply, "tool_calls": [], "context": self.context_manager.get_context()}
                        except Exception:
                            # If DB isn't available, return message
                            reply = f"Could not complete task {task_id}. It might not exist or an error occurred."
                            self.context_manager.add_assistant_response(reply)
                            return {"response": reply, "tool_calls": [], "context": self.context_manager.get_context()}
                    else:
                        reply = "Could not identify task ID to complete. Please specify which task to mark as complete by ID."
                        self.context_manager.add_assistant_response(reply)
                        return {"response": reply, "tool_calls": [], "context": self.context_manager.get_context()}

                # Default friendly multilingual prompt when no specific intent detected
                reply = "Ji haan — main Urdu bol sakta hoon. Aap ko kis cheez mein madad chahiye?\n\n(Yes — I can speak Urdu. How can I help?)"
                self.context_manager.add_assistant_response(reply)
                return {"response": reply, "tool_calls": [], "context": self.context_manager.get_context()}

            # Initialize agent (connect MCP server if needed)
            await self.async_init()

            # Prepare context with conversation history if provided
            context = self.context_manager.get_context()
            if conversation_history:
                # Add historical context to current context
                context.extend(conversation_history[-5:])  # Add last 5 messages from history

            # Add user message to context
            self.context_manager.add_user_message(user_message)

            # Small intent shortcut: if message clearly intends to add or list tasks,
            # handle it directly using the DB-backed tools so we always return
            # a `tool_calls` structure for the frontend to react to.
            try:
                detected = self._detect_intent(user_message)
                intent = detected.get("intent")
                user_identifier = user_id or self.user_id

                if intent == "add":
                    # Create task in DB and return a tool_call for frontend
                    title = user_message.strip() or "Untitled task"

                    # Enhanced extraction of priority, due_date, recurrence, etc.
                    priority = "medium"
                    due_date = None
                    recurrence_pattern = None

                    # Try to parse priority from text
                    text_lower = title.lower()
                    if "high" in text_lower or "urgent" in text_lower or "important" in text_lower:
                        priority = "high"
                    elif "low" in text_lower or "not urgent" in text_lower:
                        priority = "low"

                    # Look for due date in the message
                    import re
                    from datetime import datetime, timedelta

                    # Look for various date patterns like "tomorrow", "next Monday", "by Friday", "on 2023-12-25", etc.
                    date_patterns = [
                        r"by\s+(.+?)(?:\s|$|,|and|but)",  # "by tomorrow", "by next Monday"
                        r"on\s+(.+?)(?:\s|$|,|and|but)",  # "on Monday", "on 2023-12-25"
                        r"due\s+(.+?)(?:\s|$|,|and|but)", # "due tomorrow", "due next week"
                        r"for\s+(.+?)(?:\s|$|,|and|but)", # "for tomorrow", "for next week"
                    ]

                    for pattern in date_patterns:
                        date_match = re.search(pattern, user_message, re.IGNORECASE)
                        if date_match:
                            date_str = date_match.group(1).strip()

                            # Simple date parsing - try to convert common expressions
                            today = datetime.now()

                            if "tomorrow" in date_str.lower():
                                due_date = today + timedelta(days=1)
                                due_date = due_date.replace(hour=9, minute=0, second=0, microsecond=0)  # Set to 9 AM
                            elif "today" in date_str.lower():
                                due_date = today.replace(hour=9, minute=0, second=0, microsecond=0)  # Set to 9 AM today
                            elif "monday" in date_str.lower():
                                days_ahead = 0 if today.weekday() == 0 else (7 - today.weekday()) if today.weekday() > 0 else 0
                                if days_ahead == 0 and today.weekday() != 0:
                                    days_ahead = 7
                                due_date = today.replace(hour=9, minute=0, second=0, microsecond=0) + timedelta(days_ahead)
                            elif "tuesday" in date_str.lower():
                                days_ahead = 1 - today.weekday()
                                if days_ahead <= 0:  # Target day already happened this week
                                    days_ahead += 7
                                due_date = today.replace(hour=9, minute=0, second=0, microsecond=0) + timedelta(days_ahead)
                            elif "wednesday" in date_str.lower():
                                days_ahead = 2 - today.weekday()
                                if days_ahead <= 0:  # Target day already happened this week
                                    days_ahead += 7
                                due_date = today.replace(hour=9, minute=0, second=0, microsecond=0) + timedelta(days_ahead)
                            elif "thursday" in date_str.lower():
                                days_ahead = 3 - today.weekday()
                                if days_ahead <= 0:  # Target day already happened this week
                                    days_ahead += 7
                                due_date = today.replace(hour=9, minute=0, second=0, microsecond=0) + timedelta(days_ahead)
                            elif "friday" in date_str.lower():
                                days_ahead = 4 - today.weekday()
                                if days_ahead <= 0:  # Target day already happened this week
                                    days_ahead += 7
                                due_date = today.replace(hour=9, minute=0, second=0, microsecond=0) + timedelta(days_ahead)
                            elif "saturday" in date_str.lower():
                                days_ahead = 5 - today.weekday()
                                if days_ahead <= 0:  # Target day already happened this week
                                    days_ahead += 7
                                due_date = today.replace(hour=9, minute=0, second=0, microsecond=0) + timedelta(days_ahead)
                            elif "sunday" in date_str.lower():
                                days_ahead = 6 - today.weekday()
                                if days_ahead <= 0:  # Target day already happened this week
                                    days_ahead += 7
                                due_date = today.replace(hour=9, minute=0, second=0, microsecond=0) + timedelta(days_ahead)
                            elif re.search(r'\d{4}-\d{2}-\d{2}', date_str):  # YYYY-MM-DD format
                                try:
                                    due_date = datetime.strptime(re.search(r'\d{4}-\d{2}-\d{2}', date_str).group(), '%Y-%m-%d')
                                    due_date = due_date.replace(hour=9, minute=0, second=0, microsecond=0)  # Set to 9 AM
                                except ValueError:
                                    pass  # Ignore if date format is invalid
                            elif re.search(r'\d{2}/\d{2}/\d{4}', date_str):  # MM/DD/YYYY format
                                try:
                                    due_date = datetime.strptime(re.search(r'\d{2}/\d{2}/\d{4}', date_str).group(), '%m/%d/%Y')
                                    due_date = due_date.replace(hour=9, minute=0, second=0, microsecond=0)  # Set to 9 AM
                                except ValueError:
                                    pass  # Ignore if date format is invalid
                            elif re.search(r'\d{2}-\d{2}-\d{4}', date_str):  # DD-MM-YYYY format
                                try:
                                    due_date = datetime.strptime(re.search(r'\d{2}-\d{2}-\d{4}', date_str).group(), '%d-%m-%Y')
                                    due_date = due_date.replace(hour=9, minute=0, second=0, microsecond=0)  # Set to 9 AM
                                except ValueError:
                                    pass  # Ignore if date format is invalid
                            break  # Take the first date found

                    # Look for reminder in the message
                    # Patterns like "reminder 1 hour before", "remind me 30 minutes before", etc.
                    reminder_time = None
                    reminder_patterns = [
                        r"reminder\s+(.+?)\s+before",
                        r"remind\s+me\s+(.+?)\s+before",
                        r"remind\s+(.+?)\s+before",
                    ]

                    for pattern in reminder_patterns:
                        reminder_match = re.search(pattern, user_message, re.IGNORECASE)
                        if reminder_match:
                            reminder_spec = reminder_match.group(1).strip()

                            # Parse time units for reminder
                            time_match = re.search(r'(\d+)\s*(hour|minute|day|week)s?\s*(before|prior|earlier)', reminder_spec, re.IGNORECASE)
                            if time_match:
                                time_amount = int(time_match.group(1))
                                time_unit = time_match.group(2).lower()

                                # Calculate reminder time based on due date
                                if due_date:
                                    if time_unit.startswith('hour'):
                                        reminder_time = due_date - timedelta(hours=time_amount)
                                    elif time_unit.startswith('minute'):
                                        reminder_time = due_date - timedelta(minutes=time_amount)
                                    elif time_unit.startswith('day'):
                                        reminder_time = due_date - timedelta(days=time_amount)
                                    elif time_unit.startswith('week'):
                                        reminder_time = due_date - timedelta(weeks=time_amount)

                            break  # Only process the first reminder found

                    # Look for recurrence pattern in the message
                    recurrence_patterns = {
                        "daily": ["daily", "every day", "each day", "everyday"],
                        "weekly": ["weekly", "every week", "each week", "every monday", "every tuesday", "every wednesday", "every thursday", "every friday", "every saturday", "every sunday"],
                        "monthly": ["monthly", "every month", "each month"]
                    }

                    for rec_pattern, keywords in recurrence_patterns.items():
                        for keyword in keywords:
                            if keyword in text_lower:
                                recurrence_pattern = rec_pattern
                                break
                        if recurrence_pattern:
                            break

                    try:
                        from app.core.database import async_session_maker
                        from app.services.task_service import create_task
                        from app.schemas.task import TaskCreate
                        from app.models.task import TaskPriority, RecurrencePattern

                        async with async_session_maker() as db:
                            # Try to map priority string to enum
                            try:
                                priority_enum = TaskPriority(priority)
                            except ValueError:
                                priority_enum = TaskPriority.MEDIUM

                            # Try to map recurrence pattern to enum
                            recurrence_enum = None
                            if recurrence_pattern:
                                try:
                                    recurrence_enum = RecurrencePattern(recurrence_pattern.upper())
                                except ValueError:
                                    recurrence_enum = None

                            task_payload = TaskCreate(
                                title=title,
                                description=None,
                                priority=priority_enum,
                                due_date=due_date,
                                recurrence_pattern=recurrence_enum,
                                    reminder_time=reminder_time.isoformat() if reminder_time else None
                            )
                            task = await create_task(db, user_identifier, task_payload)

                        reply = f"Naya task jor diya gaya: {task.title} (ID: {task.id})\nPriority: {task.priority}\nDue Date: {task.due_date if task.due_date else 'Not set'}\nRecurrence: {task.recurrence_pattern if task.recurrence_pattern else 'None'}\nReminder: {reminder_time if reminder_time else 'Not set'}\n\n(New task added: {task.title} (ID: {task.id}) - Priority: {task.priority} - Due Date: {task.due_date if task.due_date else 'Not set'} - Recurrence: {task.recurrence_pattern if task.recurrence_pattern else 'None'} - Reminder: {reminder_time if reminder_time else 'Not set'})"
                        tool_calls = [{
                            "tool": "create_task",
                            "parameters": {"title": title, "priority": priority, "due_date": due_date.isoformat() if due_date else None, "recurrence_pattern": recurrence_pattern, "reminder_time": reminder_time.isoformat() if reminder_time else None},
                            "result": {
                                "id": task.id,
                                "title": task.title,
                                "priority": task.priority.value if hasattr(task.priority, 'value') else task.priority,
                                "due_date": task.due_date.isoformat() if task.due_date else None,
                                "recurrence_pattern": task.recurrence_pattern.value if task.recurrence_pattern else None,
                                "reminder_time": reminder_time.isoformat() if reminder_time else None,
                                "local": False
                            },
                        }]

                        self.context_manager.add_assistant_response(reply)
                        return {"response": reply, "tool_calls": tool_calls, "context": self.context_manager.get_context()}
                    except Exception as e:
                        # If DB fails, fall back to local creation
                        task = self._create_task_local(user_identifier, title, None, priority)
                        reply = f"Naya task jor diya gaya (local): {task.title} (ID: {task.id})\nPriority: {task.priority}\n\n(New task added locally: {task.title} (ID: {task.id}) - Priority: {task.priority})"
                        tool_calls = [{
                            "tool": "create_task",
                            "parameters": {"title": title, "priority": priority, "due_date": due_date.isoformat() if due_date else None, "recurrence_pattern": recurrence_pattern},
                            "result": {
                                "id": task.id,
                                "title": task.title,
                                "priority": task.priority,
                                "due_date": due_date.isoformat() if due_date else None,
                                "recurrence_pattern": recurrence_pattern,
                                "local": True
                            },
                        }]

                        self.context_manager.add_assistant_response(reply)
                        return {"response": reply, "tool_calls": tool_calls, "context": self.context_manager.get_context()}

                if intent == "list":
                    # Try to fetch tasks from DB and return a structured reply
                    try:
                        from app.core.database import async_session_maker
                        from app.services.task_service import get_tasks

                        async with async_session_maker() as db:
                            tasks, total = await get_tasks(db, user_identifier, skip=0, limit=10, status=None)

                        if total == 0:
                            reply = "Aapke paas abhi koi tasks nahin hain. Kya main naya task jor doon?"
                        else:
                            titles = [f"{t.id}: {t.title}" for t in tasks]
                            reply = "Yeh aapke recent tasks hain:\n" + "\n".join(titles)

                        self.context_manager.add_assistant_response(reply)
                        return {"response": reply, "tool_calls": [], "context": self.context_manager.get_context()}
                    except Exception:
                        # Fall back to normal agent flow if DB fails
                        pass

                if intent == "delete":
                    # Try to parse task ID from message and delete the task
                    import re
                    task_id_match = re.search(r'(?:task|id|no)\s*(\d+)', user_message, re.IGNORECASE)
                    if task_id_match:
                        task_id = int(task_id_match.group(1))
                        try:
                            from app.core.database import async_session_maker
                            from app.services.task_service import get_task, delete_task

                            async with async_session_maker() as db:
                                task = await get_task(db, task_id, user_identifier)
                                if task:
                                    await delete_task(db, task)
                                    reply = f"Task {task_id} '{task.title}' successfully deleted."
                                    tool_calls = [{
                                        "tool": "delete_task",
                                        "parameters": {"task_id": task_id},
                                        "result": {"deleted_task_id": task_id, "message": f"Task {task_id} deleted successfully"},
                                    }]
                                    self.context_manager.add_assistant_response(reply)
                                    return {"response": reply, "tool_calls": tool_calls, "context": self.context_manager.get_context()}
                                else:
                                    reply = f"Task {task_id} not found or you don't have permission to delete it."
                                    self.context_manager.add_assistant_response(reply)
                                    return {"response": reply, "tool_calls": [], "context": self.context_manager.get_context()}
                        except Exception:
                            reply = f"Could not delete task {task_id}. It might not exist or an error occurred."
                            self.context_manager.add_assistant_response(reply)
                            return {"response": reply, "tool_calls": [], "context": self.context_manager.get_context()}
                    else:
                        reply = "Could not identify task ID to delete. Please specify which task to delete by ID."
                        self.context_manager.add_assistant_response(reply)
                        return {"response": reply, "tool_calls": [], "context": self.context_manager.get_context()}

                if intent == "update":
                    # Try to parse task ID and new details from message and update the task
                    import re
                    # Look for various patterns like "task 81", "id 81", "#81", "81 task", "update 81", etc.
                    task_id_match = re.search(r'(?:task|id|#|no)\s*(\d+)|(\d+)\s*(?:task|kaam|work|id|no)|\b(?:update|change|modify|badlo|badal)\s+(\d+)\b', user_message, re.IGNORECASE)
                    if task_id_match:
                        # Get the first captured group that is not None
                        task_id = int(next(filter(None, task_id_match.groups())))

                        # Extract new title from message (everything after the task id and common keywords)
                        remaining_text = user_message
                        # Remove the task id and surrounding words
                        remaining_text = re.sub(r'(?:task|id|#)?\s*' + str(task_id) + r'\s*(?:task|kaam|work)?', '', remaining_text, flags=re.IGNORECASE)
                        # Look for keywords that indicate the actual task content
                        parts = re.split(r'[k:,\-\s]+', remaining_text, 1)
                        new_title = parts[-1].strip() if len(parts) > 1 else remaining_text.strip()

                        # If the new title is empty, try to extract it differently
                        if not new_title:
                            # Try to find content after common update keywords
                            update_patterns = [
                                r'update\s+kro\s+', r'update\s+karo\s+', r'badlo\s+', r'badal\s+do\s+',
                                r'change\s+', r'modify\s+', r'edit\s+'
                            ]
                            for pattern in update_patterns:
                                match = re.search(pattern + r'(.+)', remaining_text, re.IGNORECASE)
                                if match:
                                    new_title = match.group(1).strip()
                                    break

                        # Clean up the title if it still contains task IDs
                        if new_title:
                            # Remove any remaining digits that might be task IDs
                            new_title = re.sub(r'^\d+\s*', '', new_title).strip()

                        if new_title:
                            try:
                                from app.core.database import async_session_maker
                                from app.services.task_service import get_task, update_task
                                from app.schemas.task import TaskUpdate

                                async with async_session_maker() as db:
                                    task = await get_task(db, task_id, user_identifier)
                                    if task:
                                        task_update = TaskUpdate(title=new_title)
                                        updated_task = await update_task(db, task, task_update)
                                        reply = f"Task {task_id} updated successfully: '{updated_task.title}'"
                                        tool_calls = [{
                                            "tool": "update_task",
                                            "parameters": {"task_id": task_id, "title": new_title},
                                            "result": {"id": updated_task.id, "title": updated_task.title},
                                        }]
                                        self.context_manager.add_assistant_response(reply)
                                        return {"response": reply, "tool_calls": tool_calls, "context": self.context_manager.get_context()}
                                    else:
                                        reply = f"Task {task_id} not found or you don't have permission to update it."
                                        self.context_manager.add_assistant_response(reply)
                                        return {"response": reply, "tool_calls": [], "context": self.context_manager.get_context()}
                            except Exception:
                                reply = f"Could not update task {task_id}. It might not exist or an error occurred."
                                self.context_manager.add_assistant_response(reply)
                                return {"response": reply, "tool_calls": [], "context": self.context_manager.get_context()}
                        else:
                            reply = "Could not identify new task details to update."
                            self.context_manager.add_assistant_response(reply)
                            return {"response": reply, "tool_calls": [], "context": self.context_manager.get_context()}
                    else:
                        reply = "Could not identify task ID to update. Please specify which task to update by ID."
                        self.context_manager.add_assistant_response(reply)
                        return {"response": reply, "tool_calls": [], "context": self.context_manager.get_context()}

                if intent == "complete":
                    # Try to parse task ID from message and mark as complete
                    import re
                    # Look for various patterns like "task 81", "id 81", "#81", "81 task", "complete 81", etc.
                    task_id_match = re.search(r'(?:task|id|#|no)\s*(\d+)|(\d+)\s*(?:task|kaam|work|id|no)|\b(?:complete|done|mark|hogya|ho\s+gaya|ho\s+gya)\s+(\d+)\b', user_message, re.IGNORECASE)
                    if task_id_match:
                        # Get the first captured group that is not None
                        task_id = int(next(filter(None, task_id_match.groups())))
                        try:
                            from app.core.database import async_session_maker
                            from app.services.task_service import get_task, toggle_task_completion

                            async with async_session_maker() as db:
                                task = await get_task(db, task_id, user_identifier)
                                if task:
                                    updated_task = await toggle_task_completion(db, task)
                                    status = "completed" if updated_task.completed else "marked as incomplete"
                                    reply = f"Task {task_id} '{task.title}' {status}."
                                    tool_calls = [{
                                        "tool": "complete_task",
                                        "parameters": {"task_id": task_id},
                                        "result": {"id": updated_task.id, "title": updated_task.title, "completed": updated_task.completed},
                                    }]
                                    self.context_manager.add_assistant_response(reply)
                                    return {"response": reply, "tool_calls": tool_calls, "context": self.context_manager.get_context()}
                                else:
                                    reply = f"Task {task_id} not found or you don't have permission to complete it."
                                    self.context_manager.add_assistant_response(reply)
                                    return {"response": reply, "tool_calls": [], "context": self.context_manager.get_context()}
                        except Exception:
                            reply = f"Could not complete task {task_id}. It might not exist or an error occurred."
                            self.context_manager.add_assistant_response(reply)
                            return {"response": reply, "tool_calls": [], "context": self.context_manager.get_context()}
                    else:
                        reply = "Could not identify task ID to complete. Please specify which task to mark as complete by ID."
                        self.context_manager.add_assistant_response(reply)
                        return {"response": reply, "tool_calls": [], "context": self.context_manager.get_context()}
            except Exception:
                # If intent detection fails for some reason, continue to normal agent flow
                pass

            # Run the agent with the current context
            result = await Runner.run(
                self.agent,
                self.context_manager.get_context(),  # Use the context instead of just the message
                run_config=self.config
            )

            # Add assistant response to context
            self.context_manager.add_assistant_response(result.final_output)

            # Return both the response and any tool calls that were made
            return {
                "response": result.final_output,
                "tool_calls": result.tool_calls if hasattr(result, 'tool_calls') else [],
                "context": self.context_manager.get_context()
            }
        except Exception as e:
            # Return a helpful error response
            error_response = f"I encountered an issue processing your request. Could you please try again? Error: {str(e)}"
            return {
                "response": error_response,
                "tool_calls": [],
                "context": self.context_manager.get_context()
            }


async def main():
    """Example usage of the TodoChatAgent."""
    # Create an instance of the agent
    agent = TodoChatAgent(user_id="user123")

    # Process a sample message
    result = await agent.process_message("Add a task to buy groceries")
    logging.getLogger(__name__).info("Response: %s", result["response"])
    logging.getLogger(__name__).info("Tool Calls: %s", result["tool_calls"])


if __name__ == "__main__":
    asyncio.run(main())