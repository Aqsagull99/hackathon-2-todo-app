"""Tag management API routes."""

from typing import List

from fastapi import APIRouter, HTTPException, Query, Path, status

from app.api.deps import DBSession, VerifiedUserId
from app.schemas.extended import (
    TagCreate,
    TagUpdate,
    TagResponse,
    TagWithTaskCount,
)
from app.services import tag_service


router = APIRouter(prefix="/api", tags=["tags"])


@router.get("/{user_id}/tags", response_model=dict)
async def list_tags(
    user_id: VerifiedUserId,
    db: DBSession,
) -> dict:
    """List all tags for a user with task counts.

    - **user_id**: Owner's user ID
    """
    from sqlalchemy import func
    from app.models.task_tag_link import TaskTagLink

    tags = await tag_service.get_user_tags(db, user_id)

    # Count tasks per tag
    tags_with_counts = []
    for tag in tags:
        result = await db.execute(
            select(func.count()).select_from(
                select(TaskTagLink.task_id).where(TaskTagLink.tag_id == tag.id)
            )
        )
        task_count = result.scalar() or 0

        tags_with_counts.append({
            **tag.__dict__,
            "task_count": task_count,
        })

    return {"tags": tags_with_counts}


@router.post(
    "/{user_id}/tags",
    response_model=TagResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_tag(
    user_id: VerifiedUserId,
    tag_data: TagCreate,
    db: DBSession,
) -> TagResponse:
    """Create a new tag for a user.

    - **user_id**: Owner's user ID
    - **name**: Tag name (required, 1-50 chars)
    - **color**: Tag color (optional, hex format)
    """
    tag = await tag_service.create_tag(
        db,
        user_id=user_id,
        name=tag_data.name,
        color=tag_data.color,
    )
    return TagResponse.model_validate(tag)


@router.get("/{user_id}/tags/{tag_id}", response_model=TagResponse)
async def get_tag(
    user_id: VerifiedUserId,
    tag_id: int = Path(..., ge=1, description="Tag ID"),
    db: DBSession = None,
) -> TagResponse:
    """Get a specific tag by ID.

    - **user_id**: Owner's user ID
    - **tag_id**: Tag ID
    """
    tag = await tag_service.get_tag(db, tag_id, user_id)
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tag {tag_id} not found",
        )
    return TagResponse.model_validate(tag)


@router.patch("/{user_id}/tags/{tag_id}", response_model=TagResponse)
async def update_tag(
    user_id: VerifiedUserId,
    tag_data: TagUpdate,
    tag_id: int = Path(..., ge=1, description="Tag ID"),
    db: DBSession = None,
) -> TagResponse:
    """Update an existing tag.

    - **user_id**: Owner's user ID
    - **tag_id**: Tag ID
    - **name**: New name (optional, 1-50 chars)
    - **color**: New color (optional, hex format)
    """
    tag = await tag_service.update_tag(
        db,
        tag_id=tag_id,
        user_id=user_id,
        name=tag_data.name,
        color=tag_data.color,
    )

    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tag {tag_id} not found",
        )

    return TagResponse.model_validate(tag)


@router.delete("/{user_id}/tags/{tag_id}")
async def delete_tag(
    user_id: VerifiedUserId,
    tag_id: int = Path(..., ge=1, description="Tag ID"),
    db: DBSession = None,
) -> dict:
    """Delete a tag and return affected task IDs.

    - **user_id**: Owner's user ID
    - **tag_id**: Tag ID
    """
    # Get affected task IDs before deletion
    affected_task_ids = await tag_service.delete_tag(db, tag_id, user_id)

    return {
        "message": "Tag deleted successfully",
        "affected_task_ids": affected_task_ids,
    }
