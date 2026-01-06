"""Search and filter service for tasks."""

from datetime import datetime
from typing import Optional, List, Tuple

from sqlalchemy import select, and_, or_, func
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task, TaskPriority
from app.models.tag import Tag


async def search_tasks(
    db: AsyncSession,
    user_id: str,
    search: Optional[str] = None,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    due_date_from: Optional[str] = None,
    due_date_to: Optional[str] = None,
    tag_ids: Optional[List[int]] = None,
    sort_by: str = "created_at",
    sort_order: str = "desc",
    page: int = 1,
    page_size: int = 20,
) -> dict:
    """Build and execute search query with filters.

    Args:
        db: Database session
        user_id: Owner's user ID
        search: Keyword to search in title/description
        status: Filter by status (all, pending, completed)
        priority: Filter by priority (high, medium, low)
        due_date_from: Filter due date >= this date
        due_date_to: Filter due date <= this date
        tag_ids: Filter by tag IDs
        sort_by: Sort field (created_at, due_date, priority, title)
        sort_order: Sort direction (asc, desc)
        page: Page number (1-indexed)
        page_size: Items per page

    Returns:
        Dict with tasks, total, page, page_size, total_pages
    """
    # Base query with user isolation
    query = select(Task).where(Task.user_id == user_id)

    # Apply search filter (full-text search)
    if search:
        query = query.where(
            Task.search_vector.op("@@")(func.plainto_tsquery(search))
        )

    # Apply status filter
    if status == "pending":
        query = query.where(Task.completed == False)
    elif status == "completed":
        query = query.where(Task.completed == True)

    # Apply priority filter
    if priority and priority != "all":
        query = query.where(Task.priority == TaskPriority(priority))

    # Apply due date range filter
    if due_date_from:
        try:
            from_date = datetime.fromisoformat(due_date_from)
            query = query.where(Task.due_date >= from_date)
        except ValueError:
            pass  # Invalid date format, skip filter

    if due_date_to:
        try:
            to_date = datetime.fromisoformat(due_date_to)
            query = query.where(Task.due_date <= to_date)
        except ValueError:
            pass  # Invalid date format, skip filter

    # Apply tag filter (requires JOIN with task_tag_link)
    if tag_ids:
        # Subquery to find tasks with specified tags
        from app.models.task_tag_link import TaskTagLink

        tag_subquery = select(TaskTagLink.task_id).where(
            TaskTagLink.tag_id.in_(tag_ids)
        ).distinct()

        query = query.where(Task.id.in_(tag_subquery))

    # Get total count before pagination
    count_query = select(func.count()).select_from(query.subquery())
    count_result = await db.execute(count_query)
    total = count_result.scalar() or 0

    # Apply sorting
    sort_column = getattr(Task, sort_by, Task.created_at)
    if sort_order == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    # Apply pagination
    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)

    # Execute with tags loaded (eager loading for performance)
    query = query.options(selectinload(Task.tags))
    result = await db.execute(query)
    tasks = list(result.scalars().all())

    total_pages = (total + page_size - 1) // page_size if total > 0 else 0

    return {
        "tasks": [task_to_dict(t) for t in tasks],
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
    }


def task_to_dict(task: Task) -> dict:
    """Convert Task model to dict with all fields.

    Args:
        task: Task model instance

    Returns:
        Dictionary representation
    """
    return {
        "id": task.id,
        "user_id": task.user_id,
        "title": task.title,
        "description": task.description,
        "completed": task.completed,
        "priority": task.priority.value if task.priority else None,
        "due_date": task.due_date.isoformat() if task.due_date else None,
        "due_date_tz": task.due_date_tz,
        "recurrence_pattern": task.recurrence_pattern.value if task.recurrence_pattern else None,
        "recurrence_parent_id": task.recurrence_parent_id,
        "created_at": task.created_at.isoformat(),
        "updated_at": task.updated_at.isoformat(),
        "completed_at": task.completed_at.isoformat() if task.completed_at else None,
        "tags": [tag_to_dict(tag) for tag in task.tags] if task.tags else [],
    }


def tag_to_dict(tag: Tag) -> dict:
    """Convert Tag model to dict.

    Args:
        tag: Tag model instance

    Returns:
        Dictionary representation
    """
    return {
        "id": tag.id,
        "name": tag.name,
        "color": tag.color,
        "created_at": tag.created_at.isoformat(),
    }


async def get_filtered_tasks_by_due_date(
    db: AsyncSession,
    user_id: str,
    filter_type: str = "today",
) -> List[Task]:
    """Get tasks filtered by due date category.

    Args:
        db: Database session
        user_id: Owner's user ID
        filter_type: today, thisWeek, thisMonth, overdue

    Returns:
        List of tasks
    """
    from datetime import timedelta, date

    query = select(Task).where(Task.user_id == user_id).where(Task.due_date.isnot(None))

    today = date.today()

    if filter_type == "today":
        # Tasks due today
        start = datetime.combine(today, datetime.min.time())
        end = datetime.combine(today, datetime.max.time())
        query = query.where(and_(Task.due_date >= start, Task.due_date <= end))

    elif filter_type == "thisWeek":
        # Tasks due this week (next 7 days)
        start = datetime.combine(today, datetime.min.time())
        end = start + timedelta(days=7)
        query = query.where(and_(Task.due_date >= start, Task.due_date <= end))

    elif filter_type == "thisMonth":
        # Tasks due this month
        start = datetime.combine(today.replace(day=1), datetime.min.time())
        # First day of next month
        if today.month == 12:
            next_month = start.replace(year=today.year + 1, month=1)
        else:
            next_month = start.replace(month=today.month + 1)
        query = query.where(and_(Task.due_date >= start, Task.due_date < next_month))

    elif filter_type == "overdue":
        # Tasks overdue (due date in the past, not completed)
        now = datetime.utcnow()
        query = query.where(and_(Task.due_date < now, Task.completed == False))

    query = query.order_by(Task.due_date.asc())

    result = await db.execute(query)
    return list(result.scalars().all())
