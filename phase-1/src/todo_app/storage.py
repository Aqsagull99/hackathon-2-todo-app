"""In-memory task storage for the todo console application."""
from datetime import datetime
from typing import Dict, List, Optional, Set
from .models import Task, Priority, Recurrence
from .models import RecurrenceManager


class TaskList:
    """Manages in-memory storage of todo tasks.

    Provides CRUD operations for tasks with auto-incrementing IDs.
    All tasks are stored in memory and lost when the application exits.
    """

    def __init__(self) -> None:
        """Initialize an empty task list with ID counter."""
        self.tasks: Dict[int, Task] = {}
        self.next_id: int = 1

    def add(self, title: str, priority: Priority = None, tags: List[str] = None,
        due_date: datetime = None, recurrence: Recurrence = None) -> Task:
        """Create a new task with the given title and optional extended attributes.

        Args:
            title: The task description (must be non-empty)
            priority: Task priority level (optional)
            tags: List of tags (optional)
            due_date: Due date and time (optional)
            recurrence: Recurrence pattern (optional)

        Returns:
            The newly created Task
        """
        task = Task(
            id=self.next_id,
            title=title,
            completed=False,
            priority=priority if priority else Priority.MEDIUM,
            tags=tags if tags else [],
            due_date=due_date,
            recurrence=recurrence if recurrence else Recurrence.NONE
        )
        self.tasks[task.id] = task
        self.next_id += 1
        return task

    def get_all(self) -> List[Task]:
        """Return all tasks sorted by ID.

        Returns:
            List of all tasks ordered by ID
        """
        return [self.tasks[i] for i in sorted(self.tasks.keys())]

    def get_by_id(self, task_id: int) -> Optional[Task]:
        """Retrieve a task by its ID.

        Args:
            task_id: The ID of the task to find

        Returns:
            The Task if found, None otherwise
        """
        return self.tasks.get(task_id)

    def update_title(self, task_id: int, title: str) -> Optional[Task]:
        """Update the title of a task.

        Args:
            task_id: The ID of the task to update
            title: The new title (must be non-empty)

        Returns:
            The updated Task if found, None otherwise
        """
        task = self.tasks.get(task_id)
        if task:
            task.title = title
        return task

    def delete(self, task_id: int) -> bool:
        """Delete a task by its ID.

        Args:
            task_id: The ID of the task to delete

        Returns:
            True if the task was deleted, False if not found
        """
        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False

    def toggle_complete(self, task_id: int) -> Optional[Task]:
        """Toggle the completed status of a task.

        Args:
            task_id: The ID of the task to toggle

        Returns:
            The updated Task if found, None otherwise
        """
        task = self.tasks.get(task_id)
        if task:
            task.completed = not task.completed
            # If task is recurring and being completed, create next instance
            if task.completed and task.recurrence != Recurrence.NONE and task.due_date:
                new_task = self.create_recurring_instance(task)
                if new_task:
                    self.tasks[new_task.id] = new_task
        return task

    # Extended Methods

    def update_priority(self, task_id: int, priority: Priority) -> Optional[Task]:
        """Set or update priority of a task.

        Args:
            task_id: ID of task to update
            priority: New priority value

        Returns:
            Updated task if found, None otherwise
        """
        task = self.tasks.get(task_id)
        if task:
            task.priority = priority
        return task

    def add_tags(self, task_id: int, tags: List[str]) -> Optional[Task]:
        """Add tags to a task, avoiding duplicates.

        Args:
            task_id: ID of task
            tags: List of tags to add

        Returns:
            Updated task if found, None otherwise
        """
        task = self.tasks.get(task_id)
        if task:
            # Use set for deduplication, convert back to list
            existing_tags = set(task.tags)
            new_tags = set(tags)
            combined = existing_tags.union(new_tags)
            task.tags = list(combined)
        return task

    def remove_tags(self, task_id: int, tags: List[str]) -> Optional[Task]:
        """Remove tags from a task.

        Args:
            task_id: ID of task
            tags: List of tags to remove

        Returns:
            Updated task if found, None otherwise
        """
        task = self.tasks.get(task_id)
        if task:
            existing_tags = set(task.tags)
            tags_to_remove = set(tags)
            remaining = existing_tags - tags_to_remove
            task.tags = list(remaining)
        return task

    def set_due_date(self, task_id: int, due_date: datetime) -> Optional[Task]:
        """Set due date and time for a task.

        Args:
            task_id: ID of task to update
            due_date: Due date and time

        Returns:
            Updated task if found, None otherwise
        """
        task = self.tasks.get(task_id)
        if task:
            task.due_date = due_date
        return task

    def set_recurrence(self, task_id: int, recurrence: Recurrence) -> Optional[Task]:
        """Set or update recurrence pattern for a task.

        Args:
            task_id: ID of task to update
            recurrence: Recurrence pattern

        Returns:
            Updated task if found, None otherwise
        """
        task = self.tasks.get(task_id)
        if task:
            task.recurrence = recurrence
        return task

    def search(self, keyword: str) -> List[Task]:
        """Search for tasks by keyword in title or tags.

        Args:
            keyword: Search string

        Returns:
            List of matching tasks
        """
        keyword_lower = keyword.lower()
        matching_tasks = []

        for task in self.tasks.values():
            # Check title
            if keyword_lower in task.title.lower():
                matching_tasks.append(task)
                continue

            # Check tags
            for tag in task.tags:
                if keyword_lower in tag.lower():
                    matching_tasks.append(task)
                    break  # Avoid duplicates

        return matching_tasks

    def filter_by_status(self, status: bool) -> List[Task]:
        """Filter tasks by completion status.

        Args:
            status: True=completed, False=pending

        Returns:
            List of filtered tasks
        """
        return [task for task in self.tasks.values() if task.completed == status]

    def filter_by_priority(self, priority: Priority) -> List[Task]:
        """Filter tasks by priority level.

        Args:
            priority: Priority level to filter by

        Returns:
            List of filtered tasks
        """
        return [task for task in self.tasks.values() if task.priority == priority]

    def filter_by_due_date(self, start: Optional[datetime], end: Optional[datetime]) -> List[Task]:
        """Filter tasks by due date range.

        Args:
            start: Inclusive start date (None = no lower bound)
            end: Inclusive end date (None = no upper bound)

        Returns:
            List of filtered tasks
        """
        filtered_tasks = []

        for task in self.tasks.values():
            # Skip tasks without due dates
            if task.due_date is None:
                continue

            # Check start date
            if start is not None and task.due_date < start:
                continue

            # Check end date
            if end is not None and task.due_date > end:
                continue

            filtered_tasks.append(task)

        return filtered_tasks

    def sort_by_date(self, descending: bool = False) -> List[Task]:
        """Sort tasks by due date (tasks without due_date last).

        Args:
            descending: If True, highest dates first

        Returns:
            List of sorted tasks
        """
        tasks_with_dates = [t for t in self.tasks.values() if t.due_date is not None]
        tasks_without_dates = [t for t in self.tasks.values() if t.due_date is None]

        # Sort tasks with dates
        tasks_with_dates.sort(key=lambda t: t.due_date, reverse=descending)

        # Append tasks without dates at the end
        if descending:
            # Latest dates first, then tasks without dates
            return tasks_with_dates + tasks_without_dates
        else:
            # Earliest dates first, then tasks without dates
            return tasks_with_dates + tasks_without_dates

    def sort_by_priority(self, descending: bool = False) -> List[Task]:
        """Sort tasks by priority (High > Medium > Low).

        Args:
            descending: If True, lowest priorities first

        Returns:
            List of sorted tasks
        """
        priority_order = {Priority.HIGH: 0, Priority.MEDIUM: 1, Priority.LOW: 2}

        def priority_sort_key(task: Task) -> int:
            return priority_order.get(task.priority, 3)

        return sorted(self.tasks.values(), key=priority_sort_key, reverse=descending)

    def sort_by_name(self, descending: bool = False) -> List[Task]:
        """Sort tasks alphabetically by title.

        Args:
            descending: If True, Z to A

        Returns:
            List of sorted tasks
        """
        return sorted(self.tasks.values(), key=lambda t: t.title.lower(), reverse=descending)

    def create_recurring_instance(self, task: Task) -> Optional[Task]:
        """Create a new task instance for a completed recurring task.

        Args:
            task: The completed recurring task

        Returns:
            The new task instance, or None if task is not recurring
        """
        if task.recurrence == Recurrence.NONE or task.due_date is None:
            return None

        next_due = RecurrenceManager.calculate_next_due_date(
            task.due_date,
            task.recurrence
        )

        if next_due is None:
            return None

        new_task = Task(
            id=self.next_id,
            title=task.title,
            completed=False,
            priority=task.priority,
            tags=task.tags.copy(),
            due_date=next_due,
            recurrence=task.recurrence
        )

        self.tasks[new_task.id] = new_task
        self.next_id += 1
        return new_task

    def check_reminders(self, current_time: datetime) -> List[Task]:
        """Check for tasks with due dates that have been reached or passed.

        Args:
            current_time: Current datetime for comparison

        Returns:
            List of tasks needing reminders
        """
        overdue_tasks = []

        for task in self.tasks.values():
            # Skip completed tasks
            if task.completed:
                continue

            # Skip tasks without due dates
            if task.due_date is None:
                continue

            # Check if due date has passed or is now
            if task.due_date <= current_time:
                overdue_tasks.append(task)

        return overdue_tasks
