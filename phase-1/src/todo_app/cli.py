"""Command-line interface for the todo console application."""
import shlex
from typing import List, Optional, Tuple
from .storage import TaskList
from .models import Task


class CLI:
    """Handles command parsing and execution for the todo application."""

    def __init__(self, tasklist: TaskList) -> None:
        """Initialize CLI with a TaskList instance.

        Args:
            tasklist: The TaskList instance to operate on
        """
        self.tasklist = tasklist

    def parse_command(self, line: str) -> Tuple[Optional[str], List[str]]:
        """Parse a command line into command and arguments.

        Args:
            line: Raw command line input

        Returns:
            Tuple of (command, arguments list) or (None, []) for empty lines
        """
        line = line.strip()
        if not line:
            return None, []

        try:
            parts = shlex.split(line)
        except ValueError:
            # Handle unmatched quotes gracefully
            parts = line.split()

        if not parts:
            return None, []

        return parts[0].lower(), parts[1:]

    def run_command(self, command: str, args: List[str]) -> Optional[str]:
        """Execute a command and return the result message.

        Args:
            command: The command to execute
            args: Command arguments

        Returns:
            Result message to display, or None to continue
        """
        match command:
            case "add":
                return self.cmd_add(args)
            case "list":
                return self.cmd_list(args)
            case "view":
                return self.cmd_view(args)
            case "complete":
                return self.cmd_complete(args)
            case "update":
                return self.cmd_update(args)
            case "delete":
                return self.cmd_delete(args)
            case "help":
                return self.cmd_help()
            case "exit" | "quit":
                return "exit"
            case _:
                return f"Unknown command: {command}. Type 'help' for available commands."

    def cmd_add(self, args: List[str]) -> str:
        """Add a new task.

        Args:
            args: Command arguments (title)

        Returns:
            Result message
        """
        if not args:
            return "Error: 'add' requires a title. Usage: add \"task title\""

        title = " ".join(args)

        if not title.strip():
            return "Error: Task title cannot be empty."

        task = self.tasklist.add(title)
        return f"Task {task.id} created: \"{task.title}\""

    def cmd_list(self, args: List[str]) -> str:
        """List all tasks.

        Args:
            args: Command arguments (unused)

        Returns:
            Formatted task list
        """
        tasks = self.tasklist.get_all()

        if not tasks:
            return "No tasks yet. Add one with: add \"task title\""

        lines = []
        for task in tasks:
            status = "[x]" if task.completed else "[ ]"
            lines.append(f"{status} {task.id}. {task.title}")

        return "\n".join(lines)

    def cmd_view(self, args: List[str]) -> str:
        """View a specific task.

        Args:
            args: Command arguments (task_id)

        Returns:
            Task details or error
        """
        if not args:
            return "Error: 'view' requires a task ID. Usage: view <id>"

        try:
            task_id = int(args[0])
        except ValueError:
            return f"Error: Invalid task ID '{args[0]}'. Must be a number."

        task = self.tasklist.get_by_id(task_id)
        if not task:
            return f"Error: Task {task_id} not found."

        status = "Completed" if task.completed else "Pending"
        created = task.created_at.strftime("%Y-%m-%d %H:%M") if task.created_at else "Unknown"

        return f"Task {task.id}\n  Title: {task.title}\n  Status: {status}\n  Created: {created}"

    def cmd_complete(self, args: List[str]) -> str:
        """Mark a task as complete.

        Args:
            args: Command arguments (task_id)

        Returns:
            Result message
        """
        if not args:
            return "Error: 'complete' requires a task ID. Usage: complete <id>"

        try:
            task_id = int(args[0])
        except ValueError:
            return f"Error: Invalid task ID '{args[0]}'. Must be a number."

        task = self.tasklist.toggle_complete(task_id)
        if not task:
            return f"Error: Task {task_id} not found."

        return f"Task {task.id} marked as complete: \"{task.title}\""

    def cmd_update(self, args: List[str]) -> str:
        """Update a task's title.

        Args:
            args: Command arguments (task_id, new_title)

        Returns:
            Result message
        """
        if len(args) < 2:
            return "Error: 'update' requires ID and title. Usage: update <id> \"new title\""

        try:
            task_id = int(args[0])
        except ValueError:
            return f"Error: Invalid task ID '{args[0]}'. Must be a number."

        new_title = " ".join(args[1:])

        if not new_title.strip():
            return "Error: Task title cannot be empty."

        task = self.tasklist.update_title(task_id, new_title)
        if not task:
            return f"Error: Task {task_id} not found."

        return f"Task {task.id} updated: \"{task.title}\""

    def cmd_delete(self, args: List[str]) -> str:
        """Delete a task.

        Args:
            args: Command arguments (task_id)

        Returns:
            Result message
        """
        if not args:
            return "Error: 'delete' requires a task ID. Usage: delete <id>"

        try:
            task_id = int(args[0])
        except ValueError:
            return f"Error: Invalid task ID '{args[0]}'. Must be a number."

        success = self.tasklist.delete(task_id)
        if not success:
            return f"Error: Task {task_id} not found."

        return f"Task {task_id} deleted."

    def cmd_help(self) -> str:
        """Show help message.

        Returns:
            Help text
        """
        return """Available commands:
  add "title"       - Create a new task
  list              - Show all tasks
  view <id>         - Show task details
  complete <id>     - Mark task as complete
  update <id> "new title" - Update task title
  delete <id>       - Delete a task
  help              - Show this help message
  exit              - Quit the application"""
