"""Tag service for tag management."""

from typing import Optional, List

from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tag import Tag
from app.models.task_tag_link import TaskTagLink


async def get_user_tags(
    db: AsyncSession,
    user_id: str,
) -> List[Tag]:
    """Get all tags for a user with task counts.

    Args:
        db: Database session
        user_id: Owner's user ID

    Returns:
        List of tags
    """
    result = await db.execute(
        select(Tag)
        .where(Tag.user_id == user_id)
        .order_by(Tag.name)
    )
    return list(result.scalars().all())


async def get_tag(
    db: AsyncSession,
    tag_id: int,
    user_id: str,
) -> Optional[Tag]:
    """Get a specific tag by ID for a user.

    Args:
        db: Database session
        tag_id: Tag ID
        user_id: Owner's user ID

    Returns:
        Tag if found, None otherwise
    """
    result = await db.execute(
        select(Tag)
        .where(Tag.id == tag_id)
        .where(Tag.user_id == user_id)
    )
    return result.scalar_one_or_none()


async def create_tag(
    db: AsyncSession,
    user_id: str,
    name: str,
    color: str = "#EC4899",
) -> Tag:
    """Create a new tag for a user.

    Args:
        db: Database session
        user_id: Owner's user ID
        name: Tag name
        color: Tag color (hex)

    Returns:
        Created tag
    """
    tag = Tag(
        user_id=user_id,
        name=name,
        color=color,
    )
    db.add(tag)
    await db.commit()
    await db.refresh(tag)
    return tag


async def update_tag(
    db: AsyncSession,
    tag_id: int,
    user_id: str,
    name: Optional[str] = None,
    color: Optional[str] = None,
) -> Tag:
    """Update an existing tag.

    Args:
        db: Database session
        tag_id: Tag ID
        user_id: Owner's user ID
        name: New name (optional)
        color: New color (optional)

    Returns:
        Updated tag
    """
    tag = await get_tag(db, tag_id, user_id)
    if not tag:
        return None

    if name is not None:
        tag.name = name
    if color is not None:
        tag.color = color

    await db.commit()
    await db.refresh(tag)
    return tag


async def delete_tag(
    db: AsyncSession,
    tag_id: int,
    user_id: str,
) -> List[int]:
    """Delete a tag and return affected task IDs.

    Args:
        db: Database session
        tag_id: Tag ID
        user_id: Owner's user ID

    Returns:
        List of affected task IDs
    """
    # Get affected task IDs before deletion
    result = await db.execute(
        select(TaskTagLink.task_id)
        .where(TaskTagLink.tag_id == tag_id)
    )
    affected_task_ids = list(result.scalars().all())

    # Delete tag (cascade will handle task_tag_link)
    tag = await get_tag(db, tag_id, user_id)
    if tag:
        await db.delete(tag)
        await db.commit()

    return affected_task_ids


async def get_tag_for_task(
    db: AsyncSession,
    task_id: int,
) -> List[Tag]:
    """Get all tags for a task.

    Args:
        db: Database session
        task_id: Task ID

    Returns:
        List of tags
    """
    result = await db.execute(
        select(Tag)
        .join(TaskTagLink, Tag.id == TaskTagLink.tag_id)
        .where(TaskTagLink.task_id == task_id)
        .order_by(Tag.name)
    )
    return list(result.scalars().all())


async def add_tag_to_task(
    db: AsyncSession,
    task_id: int,
    tag_id: int,
) -> None:
    """Add a tag to a task.

    Args:
        db: Database session
        task_id: Task ID
        tag_id: Tag ID
    """
    link = TaskTagLink(
        task_id=task_id,
        tag_id=tag_id,
    )
    db.add(link)
    await db.commit()


async def remove_tag_from_task(
    db: AsyncSession,
    task_id: int,
    tag_id: int,
) -> None:
    """Remove a tag from a task.

    Args:
        db: Database session
        task_id: Task ID
        tag_id: Tag ID
    """
    result = await db.execute(
        select(TaskTagLink)
        .where(TaskTagLink.task_id == task_id)
        .where(TaskTagLink.tag_id == tag_id)
    )
    link = result.scalar_one_or_none()
    if link:
        await db.delete(link)
        await db.commit()


async def bulk_assign_tags(
    db: AsyncSession,
    task_id: int,
    tag_ids: List[int],
) -> None:
    """Replace all tags on a task with new set.

    Args:
        db: Database session
        task_id: Task ID
        tag_ids: List of tag IDs to assign
    """
    # Delete existing tags
    await db.execute(
        select(TaskTagLink)
        .where(TaskTagLink.task_id == task_id)
    )
    result = await db.execute(
        select(TaskTagLink).where(TaskTagLink.task_id == task_id)
    )
    existing_links = result.scalars().all()
    for link in existing_links:
        await db.delete(link)

    # Add new tags
    for tag_id in tag_ids:
        link = TaskTagLink(
            task_id=task_id,
            tag_id=tag_id,
        )
        db.add(link)

    await db.commit()


async def get_or_create_tag(
    db: AsyncSession,
    user_id: str,
    name: str,
    color: str = "#EC4899",
) -> Tag:
    """Get existing tag or create new one.

    Args:
        db: Database session
        user_id: Owner's user ID
        name: Tag name
        color: Tag color (hex)

    Returns:
        Existing or newly created tag
    """
    result = await db.execute(
        select(Tag)
        .where(Tag.user_id == user_id)
        .where(Tag.name == name)
    )
    tag = result.scalar_one_or_none()

    if tag:
        return tag

    return await create_tag(db, user_id, name, color)
