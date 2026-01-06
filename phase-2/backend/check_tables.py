#!/usr/bin/env python3
"""
Script to check the current state of the database tables
"""

import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel, select
from app.core.config import settings
from app.models.task import Task
from app.models.tag import Tag
from app.models.reminder import Reminder
from app.models.task_tag_link import TaskTagLink
from app.core.database import async_session_maker


async def check_database_state():
    print("Connecting to database...")

    # Create engine and session
    engine = create_async_engine(settings.DATABASE_URL)

    async with async_session_maker() as session:
        # Check tasks table
        tasks_count = await session.execute(select(Task))
        tasks = tasks_count.scalars().all()
        print(f"Tasks in database: {len(tasks)}")
        for i, task in enumerate(tasks):
            print(f"  Task {i+1}: {task.id} - {task.title} (user: {task.user_id})")

        # Check tags table
        tags_count = await session.execute(select(Tag))
        tags = tags_count.scalars().all()
        print(f"Tags in database: {len(tags)}")
        for i, tag in enumerate(tags):
            print(f"  Tag {i+1}: {tag.id} - {tag.name} (user: {tag.user_id})")

        # Check reminders table
        reminders_count = await session.execute(select(Reminder))
        reminders = reminders_count.scalars().all()
        print(f"Reminders in database: {len(reminders)}")
        for i, reminder in enumerate(reminders):
            print(f"  Reminder {i+1}: {reminder.id} - Task ID: {reminder.task_id}, Status: {reminder.status}")

        # Check task_tag_link table
        links_count = await session.execute(select(TaskTagLink))
        links = links_count.scalars().all()
        print(f"Task-Tag Links in database: {len(links)}")
        for i, link in enumerate(links):
            print(f"  Link {i+1}: Task ID: {link.task_id}, Tag ID: {link.tag_id}")

    print("Database check completed.")


if __name__ == "__main__":
    asyncio.run(check_database_state())