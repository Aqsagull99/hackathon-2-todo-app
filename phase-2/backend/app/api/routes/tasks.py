"""Task CRUD API routes."""

from typing import Optional

from fastapi import APIRouter, HTTPException, Query, Path, status

from app.api.deps import DBSession, VerifiedUserId
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskListResponse
from app.services import task_service


router = APIRouter(prefix="/api", tags=["tasks"])


@router.get("/{user_id}/tasks", response_model=TaskListResponse)
async def list_tasks(
    user_id: VerifiedUserId,
    db: DBSession,
    skip: int = Query(0, ge=0, description="Number of tasks to skip"),
    limit: int = Query(10, ge=1, le=100, description="Max tasks to return"),
    status: Optional[str] = Query(
        None,
        pattern="^(all|pending|completed)$",
        description="Filter by status",
    ),
) -> TaskListResponse:
    """List all tasks for a user with pagination.

    - **user_id**: Owner's user ID
    - **skip**: Number of tasks to skip (default: 0)
    - **limit**: Maximum tasks to return (default: 10, max: 100)
    - **status**: Filter by status (all, pending, completed)
    """
    tasks, total = await task_service.get_tasks(
        db, user_id, skip=skip, limit=limit, status=status
    )
    return TaskListResponse(
        tasks=[TaskResponse.model_validate(t) for t in tasks],
        total=total,
        skip=skip,
        limit=limit,
    )


@router.post(
    "/{user_id}/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_task(
    user_id: VerifiedUserId,
    task_data: TaskCreate,
    db: DBSession,
) -> TaskResponse:
    """Create a new task.

    - **user_id**: Owner's user ID
    - **title**: Task title (required, 1-200 chars)
    - **description**: Task description (optional, max 1000 chars)
    """
    task = await task_service.create_task(db, user_id, task_data)
    return TaskResponse.model_validate(task)


@router.get("/{user_id}/tasks/{task_id}", response_model=TaskResponse)
async def get_task(
    user_id: VerifiedUserId,
    task_id: int = Path(..., ge=1, description="Task ID"),
    db: DBSession = None,
) -> TaskResponse:
    """Get a specific task by ID.

    - **user_id**: Owner's user ID
    - **task_id**: Task ID
    """
    task = await task_service.get_task(db, task_id, user_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found",
        )
    return TaskResponse.model_validate(task)


@router.put("/{user_id}/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    user_id: VerifiedUserId,
    task_data: TaskUpdate,
    task_id: int = Path(..., ge=1, description="Task ID"),
    db: DBSession = None,
) -> TaskResponse:
    """Update an existing task.

    - **user_id**: Owner's user ID
    - **task_id**: Task ID
    - **title**: New title (optional)
    - **description**: New description (optional)
    - **completed**: New completion status (optional)
    """
    task = await task_service.get_task(db, task_id, user_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found",
        )

    updated_task = await task_service.update_task(db, task, task_data)
    return TaskResponse.model_validate(updated_task)


@router.delete(
    "/{user_id}/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_task(
    user_id: VerifiedUserId,
    task_id: int = Path(..., ge=1, description="Task ID"),
    db: DBSession = None,
) -> None:
    """Delete a task.

    - **user_id**: Owner's user ID
    - **task_id**: Task ID
    """
    task = await task_service.get_task(db, task_id, user_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found",
        )

    await task_service.delete_task(db, task)


@router.patch(
    "/{user_id}/tasks/{task_id}/complete",
    response_model=TaskResponse,
)
async def toggle_task_completion(
    user_id: VerifiedUserId,
    task_id: int = Path(..., ge=1, description="Task ID"),
    db: DBSession = None,
) -> TaskResponse:
    """Toggle task completion status.

    - **user_id**: Owner's user ID
    - **task_id**: Task ID
    """
    task = await task_service.get_task(db, task_id, user_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found",
        )

    updated_task = await task_service.toggle_task_completion(db, task)
    return TaskResponse.model_validate(updated_task)
