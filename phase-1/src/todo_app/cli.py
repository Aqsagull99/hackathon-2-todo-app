"""Command-line interface for the todo console application."""
import shlex
from datetime import datetime
from typing import List, Optional, Tuple
from .storage import TaskList
from .models import Task, Priority, Recurrence
from .notifications import NotificationManager


class CLI:
    """Handles command parsing and execution for the todo application."""

    def __init__(self, tasklist: TaskList) -> None:
        """Initialize CLI with a TaskList instance.

        Args:
            tasklist: The TaskList instance to operate on
        """
        self.tasklist = tasklist
        self.notification_manager = NotificationManager()

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
            case "priority":
                return self.cmd_priority(args)
            case "tag":
                return self.cmd_tag(args)
            case "untag":
                return self.cmd_untag(args)
            case "due":
                return self.cmd_due(args)
            case "recurring":
                return self.cmd_recurring(args)
            case "search":
                return self.cmd_search(args)
            case "filter":
                return self.cmd_filter(args)
            case "sort":
                return self.cmd_sort(args)
            case "check-reminders":
                return self.cmd_check_reminders(args)
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
        return f"✅ Your task '{task.title}' was added successfully!"

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
            priority = f"[{task.priority.value[0]}]" if task.priority else "[ ]"
            tags_str = f" #{','.join(task.tags)}" if task.tags else ""
            due_str = f" Due: {task.due_date.strftime('%Y-%m-%d')}" if task.due_date else ""
            lines.append(f"{status} {priority} {task.id}. {task.title}{tags_str}{due_str}")

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
        priority_str = task.priority.value if task.priority else "Medium"
        tags_str = ", ".join(task.tags) if task.tags else "None"
        due_str = task.due_date.strftime("%Y-%m-%d %H:%M") if task.due_date else "None"
        recur_str = task.recurrence.value if task.recurrence else "None"

        return f"""Task {task.id}
  Title: {task.title}
  Status: {status}
  Created: {created}
  Priority: {priority_str}
  Tags: {tags_str}
  Due: {due_str}
  Recurrence: {recur_str}"""

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

        return f"✅ Task '{task.title}' marked as complete!"

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

        return f"✏️ Task '{task.title}' updated successfully."

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

        # Get task before deleting to show name in message
        task = self.tasklist.get_by_id(task_id)
        if not task:
            return f"Error: Task {task_id} not found."

        task_title = task.title
        success = self.tasklist.delete(task_id)

        return f"🗑️ Task '{task_title}' deleted successfully."

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

  Extended commands:
  priority <id> <High|Medium|Low> - Set task priority
  tag <id> <tag1,tag2,...>        - Add tags to task
  untag <id> <tag1,tag2,...>      - Remove tags from task
  due <id> "YYYY-MM-DD HH:MM"     - Set due date/time
  recurring <id> <None|Daily|Weekly|Monthly> - Set recurrence
  search "<keyword>"               - Search tasks
  filter [--status|--priority|--start-date|--end-date] - Filter tasks
  sort --by <date|priority|name> [--order <asc|desc>]  - Sort tasks
  check-reminders                  - Check for overdue tasks

  help              - Show this help message
  exit              - Quit the application"""

    # Extended command handlers

    def cmd_priority(self, args: List[str]) -> str:
        """Set or update priority of a task."""
        if len(args) < 2:
            return "Error: 'priority' requires task ID and priority level. Usage: priority <id> <High|Medium|Low>"

        try:
            task_id = int(args[0])
        except ValueError:
            return f"Error: Invalid task ID '{args[0]}'. Must be a number."

        priority_str = args[1].capitalize()
        try:
            priority = Priority[priority_str.upper()]
        except KeyError:
            return f"Error: Invalid priority '{args[1]}'. Use High, Medium, or Low."

        task = self.tasklist.update_priority(task_id, priority)
        if not task:
            return f"Error: Task {task_id} not found."

        return f"⚡ Priority for '{task.title}' set to {priority.value}."

    def cmd_tag(self, args: List[str]) -> str:
        """Add tags to a task."""
        if len(args) < 2:
            return "Error: 'tag' requires task ID and tags. Usage: tag <id> <tag1,tag2,...>"

        try:
            task_id = int(args[0])
        except ValueError:
            return f"Error: Invalid task ID '{args[0]}'. Must be a number."

        tags_str = " ".join(args[1:])
        tags = [tag.strip() for tag in tags_str.split(",") if tag.strip()]

        if not tags:
            return "Error: At least one tag is required."

        task = self.tasklist.add_tags(task_id, tags)
        if not task:
            return f"Error: Task {task_id} not found."

        all_tags_display = ", ".join(task.tags)
        return f"🏷️ Tags for '{task.title}' updated: {all_tags_display}."

    def cmd_untag(self, args: List[str]) -> str:
        """Remove tags from a task."""
        if len(args) < 2:
            return "Error: 'untag' requires task ID and tags. Usage: untag <id> <tag1,tag2,...>"

        try:
            task_id = int(args[0])
        except ValueError:
            return f"Error: Invalid task ID '{args[0]}'. Must be a number."

        tags_str = " ".join(args[1:])
        tags = [tag.strip() for tag in tags_str.split(",") if tag.strip()]

        if not tags:
            return "Error: At least one tag is required."

        task = self.tasklist.remove_tags(task_id, tags)
        if not task:
            return f"Error: Task {task_id} not found."

        remaining_tags = ", ".join(task.tags) if task.tags else "none"
        return f"🏷️ Tags for '{task.title}' updated: {remaining_tags}."

    def cmd_due(self, args: List[str]) -> str:
        """Set due date and time for a task."""
        if len(args) < 2:
            return "Error: 'due' requires task ID and datetime. Usage: due <id> \"YYYY-MM-DD HH:MM\""

        try:
            task_id = int(args[0])
        except ValueError:
            return f"Error: Invalid task ID '{args[0]}'. Must be a number."

        datetime_str = " ".join(args[1:])
        due_date = None

        # Try parsing with time (YYYY-MM-DD HH:MM)
        try:
            due_date = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
        except ValueError:
            # Try parsing date only (YYYY-MM-DD)
            try:
                due_date = datetime.strptime(datetime_str, "%Y-%m-%d")
            except ValueError:
                return f"Error: Invalid date format. Use YYYY-MM-DD or YYYY-MM-DD HH:MM"

        task = self.tasklist.set_due_date(task_id, due_date)
        if not task:
            return f"Error: Task {task_id} not found."

        due_str = due_date.strftime("%Y-%m-%d %H:%M")
        return f"Task {task_id} due date set to: {due_str}"

    def cmd_recurring(self, args: List[str]) -> str:
        """Set or update recurrence pattern for a task."""
        if len(args) < 2:
            return "Error: 'recurring' requires task ID and pattern. Usage: recurring <id> <None|Daily|Weekly|Monthly>"

        try:
            task_id = int(args[0])
        except ValueError:
            return f"Error: Invalid task ID '{args[0]}'. Must be a number."

        recurrence_str = args[1].capitalize()
        try:
            recurrence = Recurrence[recurrence_str.upper()]
        except KeyError:
            return f"Error: Invalid recurrence '{args[1]}'. Use None, Daily, Weekly, or Monthly."

        task = self.tasklist.set_recurrence(task_id, recurrence)
        if not task:
            return f"Error: Task {task_id} not found."

        return f"Task {task_id} recurrence set to: {recurrence.value}"

    def cmd_search(self, args: List[str]) -> str:
        """Search for tasks by keyword."""
        if len(args) < 1:
            return "Error: 'search' requires a keyword. Usage: search \"keyword\""

        keyword = " ".join(args)
        matching_tasks = self.tasklist.search(keyword)

        if not matching_tasks:
            return "🔍 No tasks match your search."

        result_lines = ["🔍 Here are the tasks matching your search:"]
        for task in matching_tasks:
            status = "[x]" if task.completed else "[ ]"
            result_lines.append(f"{status} {task.id}. {task.title}")

        return "\n".join(result_lines)

    def cmd_filter(self, args: List[str]) -> str:
        """Filter tasks by status, priority, or due date range."""
        filtered_tasks = self.tasklist.get_all()
        filters_applied = []

        i = 0
        while i < len(args):
            arg = args[i].lower()

            if arg == "--status" and i + 1 < len(args):
                status_str = args[i + 1].lower()
                if status_str == "pending":
                    filtered_tasks = [t for t in filtered_tasks if not t.completed]
                    filters_applied.append("status=pending")
                elif status_str == "completed":
                    filtered_tasks = [t for t in filtered_tasks if t.completed]
                    filters_applied.append("status=completed")
                else:
                    return f"Error: Invalid status '{args[i+1]}'. Use pending or completed."
                i += 2

            elif arg == "--priority" and i + 1 < len(args):
                priority_str = args[i + 1].capitalize()
                try:
                    priority = Priority[priority_str.upper()]
                    filtered_tasks = [t for t in filtered_tasks if t.priority == priority]
                    filters_applied.append(f"priority={priority.value}")
                except KeyError:
                    return f"Error: Invalid priority '{args[i+1]}'. Use High, Medium, or Low."
                i += 2

            elif arg == "--start-date" and i + 1 < len(args):
                try:
                    start_date = datetime.strptime(args[i + 1], "%Y-%m-%d")
                    filtered_tasks = [t for t in filtered_tasks if t.due_date and t.due_date >= start_date]
                    filters_applied.append(f"start-date={args[i+1]}")
                except ValueError:
                    return f"Error: Invalid date format '{args[i+1]}'. Use YYYY-MM-DD."
                i += 2

            elif arg == "--end-date" and i + 1 < len(args):
                try:
                    end_date = datetime.strptime(args[i + 1], "%Y-%m-%d")
                    filtered_tasks = [t for t in filtered_tasks if t.due_date and t.due_date <= end_date]
                    filters_applied.append(f"end-date={args[i+1]}")
                except ValueError:
                    return f"Error: Invalid date format '{args[i+1]}'. Use YYYY-MM-DD."
                i += 2
            else:
                i += 1

        if not filters_applied:
            return "Error: No filters specified. Use --status, --priority, --start-date, or --end-date"

        if not filtered_tasks:
            return "No matching tasks found."

        filter_str = ", ".join(filters_applied)
        result_lines = [f"Filtered tasks ({filter_str}):"]
        for task in filtered_tasks:
            status = "[x]" if task.completed else "[ ]"
            result_lines.append(f"{status} {task.id}. {task.title}")

        return "\n".join(result_lines)

    def cmd_sort(self, args: List[str]) -> str:
        """Sort tasks by date, priority, or name."""
        sort_by = None
        order = "asc"

        i = 0
        while i < len(args):
            arg = args[i].lower()
            if arg == "--by" and i + 1 < len(args):
                sort_by = args[i + 1].lower()
                if sort_by not in ["date", "priority", "name"]:
                    return f"Error: Invalid sort criteria '{sort_by}'. Use date, priority, or name."
                i += 2
            elif arg == "--order" and i + 1 < len(args):
                order = args[i + 1].lower()
                if order not in ["asc", "desc"]:
                    return f"Error: Invalid order '{order}'. Use asc or desc."
                i += 2
            else:
                i += 1

        if not sort_by:
            return "Error: --by must be specified. Usage: sort --by <date|priority|name> [--order <asc|desc>]"

        # Sort tasks
        if sort_by == "date":
            sorted_tasks = self.tasklist.sort_by_date(descending=(order == "desc"))
        elif sort_by == "priority":
            sorted_tasks = self.tasklist.sort_by_priority(descending=(order == "desc"))
        elif sort_by == "name":
            sorted_tasks = self.tasklist.sort_by_name(descending=(order == "desc"))

        result_lines = [f"Tasks sorted by {sort_by} ({order}):"]
        for task in sorted_tasks:
            status = "[x]" if task.completed else "[ ]"
            result_lines.append(f"{status} {task.id}. {task.title}")

        return "\n".join(result_lines)

    def cmd_check_reminders(self, args: List[str]) -> str:
        """Check for overdue tasks and trigger notifications."""
        current_time = datetime.now()
        overdue_tasks = self.tasklist.check_reminders(current_time)

        if not overdue_tasks:
            return "⏰ No upcoming reminders."

        # Trigger notifications for each overdue task
        for task in overdue_tasks:
            self.notification_manager.send_notification(
                title=task.title,
                message=f"Due: {task.due_date.strftime('%Y-%m-%d %H:%M')}"
            )

        result_lines = [f"⏰ You have {len(overdue_tasks)} upcoming reminder{'s' if len(overdue_tasks) > 1 else ''}."]
        for task in overdue_tasks:
            due_str = task.due_date.strftime('%Y-%m-%d %H:%M') if task.due_date else "No date"
            result_lines.append(f"  • {task.title} (Due: {due_str})")

        return "\n".join(result_lines)
