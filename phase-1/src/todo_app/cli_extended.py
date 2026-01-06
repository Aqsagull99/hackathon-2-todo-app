"""Extended command handlers for todo application with new features."""
from datetime import datetime
from typing import List, Optional, Tuple
from .storage import TaskList
from .models import Task, Priority, Recurrence
from .notifications import NotificationManager


class ExtendedCLI:
    """Extended CLI handlers for priority, tags, search, filter, sort, recurring, reminders."""

    def __init__(self, tasklist: TaskList, notification_manager: NotificationManager) -> None:
        """Initialize extended CLI with tasklist and notification manager.

        Args:
            tasklist: TaskList instance
            notification_manager: NotificationManager for reminders
        """
        self.tasklist = tasklist
        self.notification_manager = notification_manager

    def cmd_priority(self, args: List[str]) -> str:
        """Set or update priority of a task.

        Args:
            args: [task_id, priority]

        Returns:
            Result message
        """
        if len(args) < 2:
            return "Error: 'priority' requires task ID and priority level. Usage: priority <id> <High|Medium|Low>"
        if len(args) > 2:
            return "Error: 'priority' accepts only 2 arguments (id and priority)."

        try:
            task_id = int(args[0])
        except ValueError:
            return f"Error: Invalid task ID '{args[0]}'. Must be a number."

        priority_str = args[1].lower()
        try:
            priority = Priority(priority_str.upper())
        except ValueError:
            return f"Error: Invalid priority '{args[1]}'. Use High, Medium, or Low."

        task = self.tasklist.update_priority(task_id, priority)
        if not task:
            return f"Error: Task {task_id} not found."

        return f"Task {task_id} priority updated to: {priority.value}"

    def cmd_tag(self, args: List[str]) -> str:
        """Add tags to a task.

        Args:
            args: [task_id, tags...]

        Returns:
            Result message
        """
        if len(args) < 2:
            return "Error: 'tag' requires task ID and tags. Usage: tag <id> <tag1,tag2,...>"
        if len(args) < 2:
            return "Error: 'tag' requires at least one tag."

        try:
            task_id = int(args[0])
        except ValueError:
            return f"Error: Invalid task ID '{args[0]}'. Must be a number."

        tags_str = " ".join(args[1:])
        tags = [tag.strip() for tag in tags_str.split(",") if tag.strip()]

        task = self.tasklist.add_tags(task_id, tags)
        if not task:
            return f"Error: Task {task_id} not found."

        tags_display = ", ".join(tags)
        return f"Task {task_id} tags updated: {tags_display}"

    def cmd_untag(self, args: List[str]) -> str:
        """Remove tags from a task.

        Args:
            args: [task_id, tags...]

        Returns:
            Result message
        """
        if len(args) < 2:
            return "Error: 'untag' requires task ID and tags. Usage: untag <id> <tag1,tag2,...>"
        if len(args) < 2:
            return "Error: 'untag' requires at least one tag."

        try:
            task_id = int(args[0])
        except ValueError:
            return f"Error: Invalid task ID '{args[0]}'. Must be a number."

        tags_str = " ".join(args[1:])
        tags = [tag.strip() for tag in tags_str.split(",") if tag.strip()]

        task = self.tasklist.remove_tags(task_id, tags)
        if not task:
            return f"Error: Task {task_id} not found."

        return f"Task {task_id} tags removed"

    def cmd_due(self, args: List[str]) -> str:
        """Set due date and time for a task.

        Args:
            args: [task_id, datetime]

        Returns:
            Result message
        """
        if len(args) < 2:
            return "Error: 'due' requires task ID and datetime. Usage: due <id> \"YYYY-MM-DD HH:MM\""

        try:
            task_id = int(args[0])
        except ValueError:
            return f"Error: Invalid task ID '{args[0]}'. Must be a number."

        datetime_str = args[1]

        # Try parsing date only (YYYY-MM-DD)
        try:
            due_date = datetime.strptime(datetime_str, "%Y-%m-%d")
        except ValueError:
            pass

        # Try parsing with time (YYYY-MM-DD HH:MM)
        try:
            due_date = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
        except ValueError:
            pass

        if due_date is None:
            return f"Error: Invalid date format. Use YYYY-MM-DD or YYYY-MM-DD HH:MM"

        task = self.tasklist.set_due_date(task_id, due_date)
        if not task:
            return f"Error: Task {task_id} not found."

        due_str = due_date.strftime("%Y-%m-%d %H:%M")
        return f"Task {task_id} due date set to: {due_str}"

    def cmd_recurring(self, args: List[str]) -> str:
        """Set or update recurrence pattern for a task.

        Args:
            args: [task_id, recurrence]

        Returns:
            Result message
        """
        if len(args) < 2:
            return "Error: 'recurring' requires task ID and pattern. Usage: recurring <id> <None|Daily|Weekly>"

        try:
            task_id = int(args[0])
        except ValueError:
            return f"Error: Invalid task ID '{args[0]}'. Must be a number."

        recurrence_str = args[1]
        try:
            recurrence = Recurrence(recurrence_str)
        except ValueError:
            return f"Error: Invalid recurrence '{args[1]}'. Use None, Daily, or Weekly."

        task = self.tasklist.set_recurrence(task_id, recurrence)
        if not task:
            return f"Error: Task {task_id} not found."

        return f"Task {task_id} recurrence set to: {recurrence.value}"

    def cmd_search(self, args: List[str]) -> str:
        """Search for tasks by keyword.

        Args:
            args: [keyword]

        Returns:
            Result message with matching tasks
        """
        if len(args) < 1:
            return "Error: 'search' requires a keyword. Usage: search \"keyword\""

        keyword = args[0]
        matching_tasks = self.tasklist.search(keyword)

        if not matching_tasks:
            return f"No matching tasks found for keyword: {keyword}"

        result_lines = [f"Search results for \"{keyword}\":"]
        for task in matching_tasks:
            status = "[X]" if task.completed else "[ ]"
            result_lines.append(f"  {status} {task.id}. {task.title}")

        return "\n".join(result_lines)

    def cmd_filter(self, args: List[str]) -> str:
        """Filter tasks by status, priority, or due date range.

        Args:
            args: [--status, --priority, --start-date, --end-date]

        Returns:
            Result message with filtered tasks
        """
        status = None
        priority = None
        start_date = None
        end_date = None

        i = 0
        while i < len(args):
            arg = args[i].lower()
            if arg == "--status":
                i += 1
                if i + 1 >= len(args):
                    return "Error: --status requires a value (pending or completed)."
                status = args[i + 1].lower() == "completed"
                if status not in ["pending", "completed"]:
                    return f"Error: Invalid status '{args[i+1]}'. Use pending or completed."

            elif arg == "--priority":
                i += 1
                if i + 1 >= len(args):
                    return "Error: --priority requires a value (High, Medium, Low)."
                priority_str = args[i + 1]
                try:
                    priority = Priority(priority_str.upper())
                except ValueError:
                    return f"Error: Invalid priority '{priority_str}'. Use High, Medium, or Low."

            elif arg == "--start-date":
                i += 1
                if i + 1 >= len(args):
                    return "Error: --start-date requires a date (YYYY-MM-DD)."
                try:
                    start_date = datetime.strptime(args[i + 1], "%Y-%m-%d")
                except ValueError:
                    return f"Error: Invalid date format '{args[i+1]}'. Use YYYY-MM-DD."

            elif arg == "--end-date":
                i += 1
                if i + 1 >= len(args):
                    return "Error: --end-date requires a date (YYYY-MM-DD)."
                try:
                    end_date = datetime.strptime(args[i + 1], "%Y-%m-%d")
                except ValueError:
                    return f"Error: Invalid date format '{args[i+1]}'. Use YYYY-MM-DD."

        # Apply filters
        filtered_tasks = self.tasklist.get_all()
        if status is not None:
            filtered_tasks = [t for t in filtered_tasks if t.completed == (status == "completed")]
        if priority is not None:
            filtered_tasks = [t for t in filtered_tasks if t.priority == priority]
        if start_date is not None or end_date is not None:
            filtered_tasks = self.tasklist.filter_by_due_date(start_date, end_date)

        if not filtered_tasks:
            return "No matching tasks found."

        result_lines = [f"Filtered tasks ({len(filtered_tasks)} found):"]
        for task in filtered_tasks:
            status = "[X]" if task.completed else "[ ]"
            priority_disp = f"[{task.priority.value[0]}]" if task.priority else "[ ]"
            due_str = task.due_date.strftime("%Y-%m-%d") if task.due_date else "No date"
            result_lines.append(f"  {status} {task.id}. {task.title} | {priority_disp} | Due: {due_str}")

        return "\n".join(result_lines)

    def cmd_sort(self, args: List[str]) -> str:
        """Sort tasks by date, priority, or name.

        Args:
            args: [--by, --order]

        Returns:
            Result message with sorted tasks
        """
        sort_by = None
        order = "asc"

        i = 0
        while i < len(args):
            arg = args[i].lower()
            if arg == "--by":
                i += 1
                if i + 1 >= len(args):
                    return "Error: --by requires a value (date, priority, name)."
                sort_by = args[i + 1].lower()
                if sort_by not in ["date", "priority", "name"]:
                    return f"Error: Invalid sort criteria '{sort_by}'. Use date, priority, or name."
            elif arg == "--order":
                i += 1
                if i + 1 >= len(args):
                    return "Error: --order requires a value (asc or desc)."
                order = args[i + 1].lower()
                if order not in ["asc", "desc"]:
                    return f"Error: Invalid order '{order}'. Use asc or desc."

        # Sort tasks
        if sort_by == "date":
            sorted_tasks = self.tasklist.sort_by_date(descending=(order == "desc"))
        elif sort_by == "priority":
            sorted_tasks = self.tasklist.sort_by_priority(descending=(order == "desc"))
        elif sort_by == "name":
            sorted_tasks = self.tasklist.sort_by_name(descending=(order == "desc"))
        else:
            return "Error: --by must be specified."

        result_lines = [f"Tasks sorted by {sort_by} ({order}):"]
        for task in sorted_tasks:
            status = "[X]" if task.completed else "[ ]"
            result_lines.append(f"  {status} {task.id}. {task.title}")

        return "\n".join(result_lines)

    def cmd_check_reminders(self, args: List[str]) -> str:
        """Check for overdue tasks and trigger notifications.

        Args:
            args: [] (no arguments needed)

        Returns:
            Result message with overdue tasks
        """
        current_time = datetime.now()
        overdue_tasks = self.tasklist.check_reminders(current_time)

        if not overdue_tasks:
            return "No overdue tasks found."

        # Trigger notifications for each overdue task
        for task in overdue_tasks:
            self.notification_manager.send_notification(
                title=task.title,
                message=f"Due: {task.due_date.strftime('%Y-%m-%d %H:%M')}"
            )

        result_lines = [f"Overdue tasks ({len(overdue_tasks)}):"]
        for task in overdue_tasks:
            result_lines.append(f"  {task.title} (Due: {task.due_date.strftime('%Y-%m-%d %H:%M')})")

        return "\n".join(result_lines)
