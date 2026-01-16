"""MCP tool implementations for Phase III AI Chatbot."""

import json
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from sqlmodel import select, Session
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.database import async_session_maker
from app.models.task import Task, TaskPriority
from app.models.tag import Tag
from app.models.task_tag_link import TaskTagLink


async def add_task_impl(
    user_id: str,
    title: str,
    description: Optional[str] = None,
    priority: str = "medium",
    due_date: Optional[datetime] = None,
    reminder: Optional[datetime] = None,
    recurrence_pattern: Optional[str] = None,
    tag_ids: Optional[List[int]] = None
) -> Dict[str, Any]:
    """
    Create a new task (stateless MCP tool)

    Returns:
        {"task_id": int, "status": "created", "title": str, "tags": list[str]}
    """
    from app.core.database import async_session_maker
    from app.models.task import RecurrencePattern

    # Input validation
    if not title or len(title) > 200:
        return {"error": "Title must be 1-200 characters", "status": "failed"}

    if priority not in ["high", "medium", "low"]:
        return {"error": "Priority must be high, medium, or low", "status": "failed"}

    async with async_session_maker() as session:
        # Create task
        task = Task(
            user_id=user_id,
            title=title,
            description=description,
            priority=TaskPriority(priority) if priority in ["high", "medium", "low"] else TaskPriority.medium,
            due_date=due_date,
            reminder=reminder,
            recurrence_pattern=RecurrencePattern(recurrence_pattern) if recurrence_pattern in ["daily", "weekly", "monthly", "yearly"] else None,
            completed=False
        )
        session.add(task)
        await session.flush()  # Get task.id before adding tags

        # Add tags if provided
        tag_names = []
        if tag_ids:
            for tag_id in tag_ids:
                # Verify tag belongs to user
                tag_stmt = select(Tag).where(
                    Tag.id == tag_id,
                    Tag.user_id == user_id
                )
                tag_result = await session.execute(tag_stmt)
                tag = tag_result.scalar_one_or_none()

                if tag:
                    task_tag = TaskTagLink(task_id=task.id, tag_id=tag.id)
                    session.add(task_tag)
                    tag_names.append(tag.name)

        await session.commit()

        return {
            "task_id": task.id,
            "status": "created",
            "title": task.title,
            "tags": tag_names,
            "priority": task.priority.value,
            "due_date": task.due_date.isoformat() if task.due_date else None,
            "reminder": task.reminder.isoformat() if task.reminder else None,
            "recurring": task.recurrence_pattern.value if task.recurrence_pattern else None
        }


async def list_tasks_impl(
    user_id: str,
    status: str = "all",
    priority: Optional[str] = None,
    tag_query: Optional[str] = None,
    search_query: Optional[str] = None,
    sort_by: str = "created_at"
) -> Dict[str, Any]:
    """List tasks for a user with optional filters."""
    from app.core.database import async_session_maker

    async with async_session_maker() as session:
        # Build query
        stmt = select(Task).where(Task.user_id == user_id)

        # Apply status filter
        if status == "pending":
            stmt = stmt.where(Task.completed == False)
        elif status == "completed":
            stmt = stmt.where(Task.completed == True)

        # Apply priority filter
        if priority:
            stmt = stmt.where(Task.priority == TaskPriority(priority))

        # Apply search query
        if search_query:
            from sqlalchemy import or_
            stmt = stmt.where(
                Task.title.ilike(f"%{search_query}%") |
                Task.description.ilike(f"%{search_query}%")
            )

        # Apply sorting
        if sort_by == "priority":
            stmt = stmt.order_by(Task.priority.desc())
        elif sort_by == "title":
            stmt = stmt.order_by(Task.title.asc())
        elif sort_by == "due_date":
            stmt = stmt.order_by(Task.due_date.asc())
        else:
            stmt = stmt.order_by(Task.created_at.desc())

        result = await session.execute(stmt)
        tasks = result.scalars().all()

        # Format response
        task_list = []
        for task in tasks:
            task_dict = {
                "id": task.id,
                "title": task.title,
                "completed": task.completed,
                "priority": task.priority.value,
                "description": task.description,
                "created_at": task.created_at.isoformat() if task.created_at else None,
                "due_date": task.due_date.isoformat() if task.due_date else None,
                "tags": []  # Will populate separately if needed
            }

            # Add tags if they exist
            if hasattr(task, 'tags'):
                task_dict["tags"] = [tag.name for tag in task.tags]

            task_list.append(task_dict)

        return {
            "tasks": task_list,
            "count": len(task_list)
        }


async def complete_task_impl(
    user_id: str,
    task_id: int
) -> Dict[str, Any]:
    """Mark task as complete with proper error handling."""
    from app.core.database import async_session_maker

    async with async_session_maker() as session:
        # Verify task exists and belongs to user
        stmt = select(Task).where(
            Task.id == task_id,
            Task.user_id == user_id
        )
        result = await session.execute(stmt)
        task = result.scalar_one_or_none()

        if not task:
            return {"error": f"Task {task_id} not found", "status": "failed"}

        if task.completed:
            return {"error": "Task already completed", "status": "failed"}

        # Update task
        task.completed = True
        task.completed_at = datetime.utcnow()
        await session.commit()

        return {
            "task_id": task.id,
            "status": "completed",
            "title": task.title
        }


async def delete_task_impl(
    user_id: str,
    task_id: int
) -> Dict[str, Any]:
    """Delete task from database."""
    from app.core.database import async_session_maker

    async with async_session_maker() as session:
        # Verify task exists and belongs to user
        stmt = select(Task).where(
            Task.id == task_id,
            Task.user_id == user_id
        )
        result = await session.execute(stmt)
        task = result.scalar_one_or_none()

        if not task:
            return {"error": f"Task {task_id} not found", "status": "failed"}

        # Delete task
        await session.delete(task)
        await session.commit()

        return {
            "task_id": task_id,
            "status": "deleted",
            "title": task.title
        }


async def update_task_impl(
    user_id: str,
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    priority: Optional[str] = None
) -> Dict[str, Any]:
    """Update task fields."""
    from app.core.database import async_session_maker

    async with async_session_maker() as session:
        # Verify task exists and belongs to user
        stmt = select(Task).where(
            Task.id == task_id,
            Task.user_id == user_id
        )
        result = await session.execute(stmt)
        task = result.scalar_one_or_none()

        if not task:
            return {"error": f"Task {task_id} not found", "status": "failed"}

        # Update fields if provided
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if priority is not None and priority in ["high", "medium", "low"]:
            task.priority = TaskPriority(priority)

        task.mark_updated()  # Update updated_at timestamp
        await session.commit()

        return {
            "task_id": task.id,
            "status": "updated",
            "title": task.title
        }


async def add_tag_to_task_impl(
    user_id: str,
    task_id: int,
    tag_name: str
) -> Dict[str, Any]:
    """Add or create a tag and associate it with a task."""
    from app.core.database import async_session_maker

    async with async_session_maker() as session:
        # Verify task exists and belongs to user
        task_stmt = select(Task).where(
            Task.id == task_id,
            Task.user_id == user_id
        )
        task_result = await session.execute(task_stmt)
        task = task_result.scalar_one_or_none()

        if not task:
            return {"error": f"Task {task_id} not found", "status": "failed"}

        # Find or create tag
        tag_stmt = select(Tag).where(
            Tag.name == tag_name,
            Tag.user_id == user_id
        )
        tag_result = await session.execute(tag_stmt)
        tag = tag_result.scalar_one_or_none()

        if not tag:
            # Create new tag
            tag = Tag(
                user_id=user_id,
                name=tag_name
            )
            session.add(tag)
            await session.flush()  # Get tag.id

        # Check if association already exists
        assoc_stmt = select(TaskTagLink).where(
            TaskTagLink.task_id == task_id,
            TaskTagLink.tag_id == tag.id
        )
        assoc_result = await session.execute(assoc_stmt)
        existing_assoc = assoc_result.scalar_one_or_none()

        if existing_assoc:
            return {
                "task_id": task_id,
                "tag_name": tag_name,
                "status": "already_tagged"
            }

        # Create association
        task_tag = TaskTagLink(
            task_id=task.id,
            tag_id=tag.id
        )
        session.add(task_tag)
        await session.commit()

        return {
            "task_id": task_id,
            "tag_name": tag_name,
            "status": "tagged"
        }