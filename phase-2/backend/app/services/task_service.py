"""Task service with CRUD operations."""

from typing import Optional
from datetime import datetime

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


async def create_task(
    db: AsyncSession,
    user_id: str,
    task_data: TaskCreate,
) -> Task:
    """Create a new task for a user.

    Args:
        db: Database session
        user_id: Owner's user ID
        task_data: Task creation data

    Returns:
        Created task
    """
    task = Task(
        user_id=user_id,
        title=task_data.title,
        description=task_data.description,
    )
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task


async def get_tasks(
    db: AsyncSession,
    user_id: str,
    skip: int = 0,
    limit: int = 10,
    status: Optional[str] = None,
) -> tuple[list[Task], int]:
    """Get paginated tasks for a user.

    Args:
        db: Database session
        user_id: Owner's user ID
        skip: Number of tasks to skip
        limit: Maximum number of tasks to return
        status: Filter by status (all, pending, completed)

    Returns:
        Tuple of (tasks list, total count)
    """
    # Base query
    query = select(Task).where(Task.user_id == user_id)

    # Apply status filter
    if status == "pending":
        query = query.where(Task.completed == False)
    elif status == "completed":
        query = query.where(Task.completed == True)

    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    # Apply pagination and ordering
    query = query.order_by(Task.created_at.desc()).offset(skip).limit(limit)

    result = await db.execute(query)
    tasks = list(result.scalars().all())

    return tasks, total


async def get_task(
    db: AsyncSession,
    task_id: int,
    user_id: str,
) -> Optional[Task]:
    """Get a specific task by ID for a user.

    Args:
        db: Database session
        task_id: Task ID
        user_id: Owner's user ID

    Returns:
        Task if found, None otherwise
    """
    result = await db.execute(
        select(Task)
        .where(Task.id == task_id)
        .where(Task.user_id == user_id)
    )
    return result.scalar_one_or_none()


async def update_task(
    db: AsyncSession,
    task: Task,
    task_data: TaskUpdate,
) -> Task:
    """Update an existing task.

    Args:
        db: Database session
        task: Task to update
        task_data: Update data

    Returns:
        Updated task
    """
    update_dict = task_data.model_dump(exclude_unset=True)

    for key, value in update_dict.items():
        setattr(task, key, value)

    task.updated_at = datetime.utcnow()

    await db.commit()
    await db.refresh(task)
    return task


async def delete_task(db: AsyncSession, task: Task) -> bool:
    """Delete a task.

    Args:
        db: Database session
        task: Task to delete

    Returns:
        True if deleted
    """
    await db.delete(task)
    await db.commit()
    return True


async def toggle_task_completion(db: AsyncSession, task: Task) -> Task:
    """Toggle task completion status.

    Args:
        db: Database session
        task: Task to toggle

    Returns:
        Updated task
    """
    task.completed = not task.completed
    task.updated_at = datetime.utcnow()

    await db.commit()
    await db.refresh(task)
    return task
