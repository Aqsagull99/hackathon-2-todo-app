"""Extended Task CRUD API routes with search, filter, and recurring support."""

from typing import Optional, List
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, Query, Path, status
from sqlalchemy.orm.attributes import set_committed_value

from app.api.deps import DBSession, VerifiedUserId, VerifiedUserIdFromToken
from app.schemas.extended import (
    TaskCreateExtended,
    TaskUpdateExtended,
    TaskResponseExtended,
    TaskListResponseExtended,
    TaskSearchParams,
    TaskPriority,
    RecurringCompleteResponse,
)
from app.models.task import Task
from app.services import task_service, recurring_service, search_service, tag_service


router = APIRouter(prefix="/api", tags=["tasks"])


@router.get("/tasks", response_model=TaskListResponseExtended)
async def list_tasks_extended(
    current_user_id: VerifiedUserIdFromToken,
    db: DBSession,
    search: Optional[str] = Query(None, description="Keyword search"),
    status: Optional[str] = Query(
        None,
        pattern="^(all|pending|completed)$",
        description="Filter by status",
    ),
    priority: Optional[str] = Query(None, description="Filter by priority"),
    due_date_from: Optional[str] = Query(None, description="Filter due date >= this date"),
    due_date_to: Optional[str] = Query(None, description="Filter due date <= this date"),
    tag_ids: Optional[str] = Query(None, description="Filter by tag IDs (comma-separated)"),
    sort_by: str = Query("created_at", description="Sort field"),
    sort_order: str = Query("desc", pattern="^(asc|desc)$", description="Sort direction"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
) -> TaskListResponseExtended:
    """List all tasks for a user with search, filter, and sort support.

    - **user_id**: Owner's user ID
    - **search**: Keyword to search in title/description
    - **status**: Filter by status (all, pending, completed)
    - **priority**: Filter by priority (high, medium, low)
    - **due_date_from**: Filter due date >= this date (ISO 8601)
    - **due_date_to**: Filter due date <= this date (ISO 8601)
    - **tag_ids**: Filter by tag IDs (comma-separated)
    - **sort_by**: Sort field (created_at, due_date, priority, title)
    - **sort_order**: Sort direction (asc, desc)
    - **page**: Page number (1-indexed)
    - **page_size**: Items per page (default: 20, max: 100)
    """
    params = TaskSearchParams(
        search=search,
        status=status,
        priority=TaskPriority(priority) if priority else None,
        due_date_from=due_date_from,
        due_date_to=due_date_to,
        tag_ids=[int(t) for t in tag_ids.split(",")] if tag_ids else None,
        sort_by=sort_by,
        sort_order=sort_order,
        page=page,
        page_size=page_size,
    )

    result = await search_service.search_tasks(
        db=db,
        user_id=current_user_id,
        search=params.search,
        status=params.status,
        priority=params.priority.value if params.priority else None,
        due_date_from=params.due_date_from,
        due_date_to=params.due_date_to,
        tag_ids=params.tag_ids,
        sort_by=params.sort_by,
        sort_order=params.sort_order,
        page=params.page,
        page_size=params.page_size,
    )

    return TaskListResponseExtended(**result)


@router.post(
    "/tasks",
    response_model=TaskResponseExtended,
    status_code=status.HTTP_201_CREATED,
)
async def create_task_extended(
    current_user_id: VerifiedUserIdFromToken,
    task_data: TaskCreateExtended,
    db: DBSession,
) -> TaskResponseExtended:
    """Create a new task with extended features.

    - **user_id**: Owner's user ID
    - **title**: Task title (required, 1-200 chars)
    - **description**: Task description (optional, max 1000 chars)
    - **priority**: Task priority (high, medium, low)
    - **due_date**: Due date (ISO 8601)
    - **due_date_tz**: Timezone for due date (e.g., America/New_York)
    - **recurrence_pattern**: Recurrence pattern (daily, weekly, monthly)
    - **tag_ids**: List of tag IDs to assign
    """
    # Create base task
    task = Task(
        user_id=current_user_id,
        title=task_data.title,
        description=task_data.description,
        priority=task_data.priority.value,
        due_date=task_data.due_date,
        due_date_tz=task_data.due_date_tz,
        recurrence_pattern=task_data.recurrence_pattern.value if task_data.recurrence_pattern else None,
    )

    db.add(task)
    await db.commit()
    await db.refresh(task)

    # Assign tags if provided
    if task_data.tag_ids:
        for tag_id in task_data.tag_ids:
            # Verify tag belongs to user
            tag = await tag_service.get_tag(db, tag_id, current_user_id)
            if tag:
                await tag_service.add_tag_to_task(db, task.id, tag_id)

    # Load tags for response and build dict manually to avoid lazy-load issues
    tags = await tag_service.get_tag_for_task(db, task.id)

    # Manually build response dict instead of using task_to_dict which accesses task.tags
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
        "tags": [{"id": t.id, "name": t.name, "color": t.color, "created_at": t.created_at.isoformat(), "user_id": t.user_id} for t in tags],
    }


@router.get("/tasks/{task_id}", response_model=TaskResponseExtended)
async def get_task_extended(
    current_user_id: VerifiedUserIdFromToken,
    task_id: int = Path(..., ge=1, description="Task ID"),
    db: DBSession = None,
) -> TaskResponseExtended:
    """Get a specific task by ID with extended fields.

    - **user_id**: Owner's user ID
    - **task_id**: Task ID
    """
    task = await task_service.get_task(db, task_id, current_user_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found",
        )

    # Load tags for response
    task.tags = await tag_service.get_tag_for_task(db, task_id)

    return search_service.task_to_dict(task)


@router.put("/tasks/{task_id}", response_model=TaskResponseExtended)
async def update_task_extended(
    current_user_id: VerifiedUserIdFromToken,
    task_data: TaskUpdateExtended,
    task_id: int = Path(..., ge=1, description="Task ID"),
    db: DBSession = None,
) -> TaskResponseExtended:
    """Update an existing task with extended fields.

    - **user_id**: Owner's user ID
    - **task_id**: Task ID
    - **title**: New title (optional)
    - **description**: New description (optional)
    - **completed**: New completion status (optional)
    - **priority**: New priority (optional)
    - **due_date**: New due date (optional)
    - **due_date_tz**: New timezone (optional)
    - **recurrence_pattern**: New recurrence pattern (optional)
    - **tag_ids**: Replace all tags with this list (optional)
    """
    task = await task_service.get_task(db, task_id, current_user_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found",
        )

    update_dict = task_data.model_dump(exclude_unset=True, exclude={"tag_ids"})

    for key, value in update_dict.items():
        if value is not None:
            if hasattr(value, "value"):  # Handle enum values
                setattr(task, key, value.value)
            else:
                setattr(task, key, value)

    task.mark_updated()

    # Update tags if provided
    if task_data.tag_ids is not None:
        await tag_service.bulk_assign_tags(db, task_id, task_data.tag_ids)

    await db.commit()
    await db.refresh(task)

    # Load tags for response
    task.tags = await tag_service.get_tag_for_task(db, task_id)

    return search_service.task_to_dict(task)


@router.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_task_extended(
    current_user_id: VerifiedUserIdFromToken,
    task_id: int = Path(..., ge=1, description="Task ID"),
    db: DBSession = None,
) -> None:
    """Delete a task.

    - **user_id**: Owner's user ID
    - **task_id**: Task ID
    """
    task = await task_service.get_task(db, task_id, current_user_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found",
        )

    await task_service.delete_task(db, task)


@router.patch(
    "/tasks/{task_id}/complete",
    response_model=RecurringCompleteResponse,
)
async def complete_task_with_recurring(
    current_user_id: VerifiedUserIdFromToken,
    task_id: int = Path(..., ge=1, description="Task ID"),
    db: DBSession = None,
) -> RecurringCompleteResponse:
    """Complete task and create new instance if recurring.

    - **user_id**: Owner's user ID
    - **task_id**: Task ID
    """
    task = await task_service.get_task(db, task_id, current_user_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found",
        )

    # Load tags before completing
    task.tags = await tag_service.get_tag_for_task(db, task_id)

    # Complete task
    completed_task = await task_service.toggle_task_completion(db, task)

    # Handle recurring task
    new_instance = None
    if task.recurrence_pattern:
        new_instance = await recurring_service.complete_recurring_task(db, task)

    # Load tags for responses
    completed_task.tags = await tag_service.get_tag_for_task(db, task_id)
    if new_instance:
        new_instance.tags = await tag_service.get_tag_for_task(db, new_instance.id)

    return RecurringCompleteResponse(
        completed_task=search_service.task_to_dict(completed_task),
        new_instance=search_service.task_to_dict(new_instance) if new_instance else None,
    )


@router.post(
    "/tasks/{task_id}/skip",
    response_model=RecurringCompleteResponse,
)
async def skip_task_instance(
    current_user_id: VerifiedUserIdFromToken,
    task_id: int = Path(..., ge=1, description="Task ID"),
    db: DBSession = None,
) -> RecurringCompleteResponse:
    """Skip a recurring task instance and create next one.

    - **user_id**: Owner's user ID
    - **task_id**: Task ID
    """
    task = await task_service.get_task(db, task_id, current_user_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found",
        )

    # Skip recurring task
    new_instance = await recurring_service.skip_task_instance(db, task)

    # Load tags for responses
    task.tags = await tag_service.get_tag_for_task(db, task_id)
    if new_instance:
        new_instance.tags = await tag_service.get_tag_for_task(db, new_instance.id)

    return RecurringCompleteResponse(
        completed_task=search_service.task_to_dict(task),
        new_instance=search_service.task_to_dict(new_instance) if new_instance else None,
    )


@router.delete("/{user_id}/tasks/{task_id}/recurrence", response_model=TaskResponseExtended)
async def cancel_recurrence(
    user_id: VerifiedUserId,
    task_id: int = Path(..., ge=1, description="Task ID"),
    db: DBSession = None,
) -> TaskResponseExtended:
    """Cancel recurrence pattern on a task.

    - **user_id**: Owner's user ID
    - **task_id**: Task ID
    """
    task = await task_service.get_task(db, task_id, user_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found",
        )

    await recurring_service.cancel_recurrence(db, task)

    # Load tags for response
    task.tags = await tag_service.get_tag_for_task(db, task_id)

    return search_service.task_to_dict(task)


