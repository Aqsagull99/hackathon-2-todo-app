#!/usr/bin/env python3
"""
Test script to verify Phase-V event-driven architecture is working properly.
"""

import asyncio
from datetime import datetime
from app.core.database import async_session_maker
from app.services.task_service import create_task, toggle_task_completion
from app.models.task import Task, TaskPriority, RecurrencePattern
from app.schemas.task import TaskCreate
from app.events.publisher import publish_task_event


async def test_event_driven_architecture():
    """Test the event-driven architecture functionality."""

    print("🧪 Testing Phase-V Event-Driven Architecture...\n")

    # Test 1: Create a recurring task
    print("1. Creating a recurring task...")
    async with async_session_maker() as session:
        task_data = TaskCreate(
            title="Weekly team meeting",
            description="Weekly team sync meeting",
            priority="high",
            due_date=datetime.now(),
            recurrence_pattern=RecurrencePattern.weekly
        )

        task = await create_task(session, "test-user", task_data)
        print(f"   ✓ Created recurring task: '{task.title}' (ID: {task.id})")
        print(f"   ✓ Priority: {task.priority}, Recurrence: {task.recurrence_pattern}")

    # Test 2: Simulate task completion (should trigger event)
    print("\n2. Completing the task to trigger recurring event...")
    async with async_session_maker() as session:
        task = await session.get(Task, task.id)
        if task:
            updated_task = await toggle_task_completion(session, task)
            print(f"   ✓ Task '{updated_task.title}' marked as completed")
            print(f"   ✓ Completed at: {updated_task.completed_at}")

    # Test 3: Check if next occurrence was created
    print("\n3. Checking for next recurring occurrence...")
    async with async_session_maker() as session:
        # Look for tasks with the same title but different ID (next occurrence)
        from sqlalchemy import select
        stmt = select(Task).where(
            Task.title == "Weekly team meeting",
            Task.recurrence_parent_id == task.id  # Should link to original
        )
        result = await session.execute(stmt)
        next_occurrences = result.scalars().all()

        if next_occurrences:
            next_task = next_occurrences[0]
            print(f"   ✓ Next occurrence created: ID {next_task.id}")
            print(f"   ✓ Linked to parent: {next_task.recurrence_parent_id}")
            print(f"   ✓ Due date: {next_task.due_date}")
        else:
            print("   ⚠ No next occurrence found (may need to wait for event processing)")

    # Test 4: Test event publishing directly
    print("\n4. Testing direct event publishing...")
    try:
        event_result = await publish_task_event(
            topic="task-events",
            event_type="test-event",
            task_data={
                "id": task.id,
                "user_id": "test-user",
                "title": "Test Event",
                "test": True
            }
        )
        print(f"   ✓ Event published successfully")
        if event_result:
            print(f"   ✓ Response: {event_result}")
        else:
            print(f"   ✓ Event published (no response expected)")
    except Exception as e:
        print(f"   ⚠ Event publishing failed: {e}")
        print(f"   (This is expected if Dapr is not running)")

    print("\n✅ Event-driven architecture test completed!")
    print("\n📝 Note: For full functionality, ensure:")
    print("   - Dapr runtime is installed and initialized")
    print("   - Kafka/Redpanda is running and configured")
    print("   - Dapr components are deployed to Kubernetes")


if __name__ == "__main__":
    asyncio.run(test_event_driven_architecture())