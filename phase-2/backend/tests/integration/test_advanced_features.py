"""Integration tests for Phase V advanced features."""
import pytest
from datetime import datetime, timedelta
from app.models.task import Task, TaskPriority, RecurrencePattern

@pytest.mark.asyncio
async def test_create_task_with_priority(client, auth_headers):
    """Test creating task with priority."""
    response = await client.post(
        "/api/test-user/tasks",
        json={"title": "High priority task", "priority": "high"},
        headers=auth_headers
    )
    assert response.status_code == 201
    assert response.json()["priority"] == "high"

@pytest.mark.asyncio
async def test_create_task_with_due_date(client, auth_headers):
    """Test creating task with due date."""
    tomorrow = (datetime.utcnow() + timedelta(days=1)).isoformat()
    response = await client.post(
        "/api/test-user/tasks",
        json={"title": "Task due tomorrow", "due_date": tomorrow},
        headers=auth_headers
    )
    assert response.status_code == 201
    assert response.json()["due_date"] is not None

@pytest.mark.asyncio
async def test_filter_by_priority(client, auth_headers):
    """Test filtering tasks by priority."""
    response = await client.get(
        "/api/test-user/tasks?priority=high",
        headers=auth_headers
    )
    assert response.status_code == 200
    tasks = response.json()
    assert all(t["priority"] == "high" for t in tasks)

@pytest.mark.asyncio
async def test_search_tasks(client, auth_headers):
    """Test full-text search."""
    response = await client.get(
        "/api/test-user/tasks?search_query=meeting",
        headers=auth_headers
    )
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_recurring_task_spawn(db_session):
    """Test recurring task spawns next occurrence."""
    from app.services.recurring_tasks import spawn_next_occurrence
    
    task = Task(
        user_id="test-user",
        title="Weekly standup",
        recurrence_pattern=RecurrencePattern.weekly,
        due_date=datetime.utcnow()
    )
    db_session.add(task)
    await db_session.commit()
    
    next_task = await spawn_next_occurrence(db_session, task.id)
    assert next_task is not None
    assert next_task.recurrence_parent_id == task.id
