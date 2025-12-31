"""In-memory task storage for the todo console application."""
from typing import Dict, List, Optional
from .models import Task


class TaskList:
    """Manages in-memory storage of todo tasks.

    Provides CRUD operations for tasks with auto-incrementing IDs.
    All tasks are stored in memory and lost when the application exits.
    """

    def __init__(self) -> None:
        """Initialize an empty task list with ID counter."""
        self.tasks: Dict[int, Task] = {}
        self.next_id: int = 1

    def add(self, title: str) -> Task:
        """Create a new task with the given title.

        Args:
            title: The task description (must be non-empty)

        Returns:
            The newly created Task
        """
        task = Task(
            id=self.next_id,
            title=title,
            completed=False
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
        return task
