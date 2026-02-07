"""
Search Service - Phase V
Provides full-text search across tasks.

[Task]: T013
[From]: phase-5/specs/007-phase-v-cloud-deployment/plan.md §3.1
"""

from typing import List, Optional, Dict
from sqlmodel import Session, select, or_
from app.models.task import Task


async def search_tasks(
    session: Session,
    user_id: str,
    query: str,
    filters: Optional[Dict] = None
) -> List[Task]:
    """
    Full-text search across task titles and descriptions.

    Args:
        session: Database session
        user_id: User identifier
        query: Search query string
        filters: Additional filters (priority, tags, status)

    Returns:
        List of matching tasks

    Process:
    1. Build base query with user_id filter
    2. Add ILIKE conditions for title and description
    3. Apply additional filters if provided
    4. Return sorted by relevance (title matches first)
    """
    if not query or not query.strip():
        # Empty query returns all tasks
        statement = select(Task).where(Task.user_id == user_id)
        result = await session.execute(statement)
        return result.scalars().all()

    # Clean query
    search_term = f"%{query.strip()}%"

    # Build search query
    statement = select(Task).where(
        Task.user_id == user_id,
        or_(
            Task.title.ilike(search_term),
            Task.description.ilike(search_term)
        )
    )

    # Apply additional filters if provided
    if filters:
        if filters.get("priority"):
            statement = statement.where(Task.priority == filters["priority"])

        if filters.get("completed") is not None:
            statement = statement.where(Task.completed == filters["completed"])

        if filters.get("has_due_date"):
            statement = statement.where(Task.due_date.is_not(None))

    # Execute query
    result = await session.execute(statement)
    tasks = result.scalars().all()

    # Sort by relevance (title matches first, then description matches)
    return sort_by_relevance(tasks, query)


def sort_by_relevance(tasks: List[Task], query: str) -> List[Task]:
    """
    Sort tasks by search relevance.

    Args:
        tasks: List of tasks
        query: Original search query

    Returns:
        Tasks sorted by relevance

    Relevance rules:
    1. Title exact match (highest)
    2. Title contains (case-insensitive)
    3. Description contains
    4. Tag match (via task.tags)
    """
    query_lower = query.lower()

    def relevance_score(task: Task) -> int:
        score = 0

        # Title exact match
        if task.title.lower() == query_lower:
            score += 100

        # Title contains query
        elif query_lower in task.title.lower():
            score += 50

        # Description contains query
        if task.description and query_lower in task.description.lower():
            score += 25

        # Tag match
        if task.tags:
            for tag in task.tags:
                if query_lower in tag.name.lower():
                    score += 10

        return score

    # Sort by score (descending)
    return sorted(tasks, key=relevance_score, reverse=True)


async def search_by_tags(
    session: Session,
    user_id: str,
    tag_names: List[str]
) -> List[Task]:
    """
    Search tasks by tag names.

    Args:
        session: Database session
        user_id: User identifier
        tag_names: List of tag names to search

    Returns:
        Tasks that have any of the specified tags
    """
    from app.models.tag import Tag
    from app.models.task_tag_link import TaskTagLink

    # Query tasks through the many-to-many relationship
    statement = (
        select(Task)
        .join(TaskTagLink, Task.id == TaskTagLink.task_id)
        .join(Tag, TaskTagLink.tag_id == Tag.id)
        .where(
            Task.user_id == user_id,
            Tag.name.in_(tag_names)
        )
        .distinct()
    )

    result = await session.execute(statement)
    return result.scalars().all()


async def advanced_search(
    session: Session,
    user_id: str,
    query: Optional[str] = None,
    priority: Optional[str] = None,
    tags: Optional[List[str]] = None,
    status: Optional[str] = "all",
    has_due_date: Optional[bool] = None,
    overdue_only: bool = False
) -> List[Task]:
    """
    Advanced search with multiple criteria.

    Args:
        session: Database session
        user_id: User identifier
        query: Text search query
        priority: Filter by priority
        tags: Filter by tags
        status: Filter by status
        has_due_date: Filter tasks with/without due dates
        overdue_only: Show only overdue tasks

    Returns:
        List of matching tasks
    """
    from datetime import datetime

    # Start with base query
    statement = select(Task).where(Task.user_id == user_id)

    # Text search
    if query:
        search_term = f"%{query}%"
        statement = statement.where(
            or_(
                Task.title.ilike(search_term),
                Task.description.ilike(search_term)
            )
        )

    # Priority filter
    if priority:
        statement = statement.where(Task.priority == priority)

    # Status filter
    if status == "completed":
        statement = statement.where(Task.completed == True)
    elif status == "pending":
        statement = statement.where(Task.completed == False)

    # Due date filters
    if has_due_date is not None:
        if has_due_date:
            statement = statement.where(Task.due_date.is_not(None))
        else:
            statement = statement.where(Task.due_date.is_(None))

    if overdue_only:
        now = datetime.utcnow()
        statement = statement.where(
            Task.due_date < now,
            Task.completed == False
        )

    # Execute base query
    result = await session.execute(statement)
    tasks = result.scalars().all()

    # Apply tag filter (requires loading relationships)
    if tags:
        from app.services.task_utils import filter_by_tags
        tasks = filter_by_tags(tasks, tags)

    return tasks
