#!/usr/bin/env python3
"""
Script to add the missing 'reminder' column to the tasks table.
"""

import asyncio
import asyncpg
from app.core.config import settings


async def add_reminder_column():
    print("Connecting to database...")

    # Connect to the database
    conn = await asyncpg.connect(
        dsn=settings.DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")
    )

    try:
        print("Adding missing 'reminder' column to tasks table...")

        # Add the reminder column to the tasks table
        await conn.execute("""
            ALTER TABLE tasks
            ADD COLUMN IF NOT EXISTS reminder TIMESTAMP WITH TIME ZONE;
        """)

        print("Reminder column added successfully!")

        # Verify the changes
        print("\nVerifying changes...")

        # Check if reminder column exists
        result = await conn.fetch("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns
            WHERE table_name = 'tasks' AND column_name = 'reminder'
        """)
        print(f"Reminder column: {result}")

        # List all columns in tasks table
        result = await conn.fetch("""
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_name = 'tasks'
            ORDER BY ordinal_position
        """)
        print(f"Tasks table columns: {len(result)} total")
        for row in result:
            print(f"  - {row['column_name']}: {row['data_type']}")

    except Exception as e:
        print(f"Error adding reminder column: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        await conn.close()
        print("Database connection closed.")


if __name__ == "__main__":
    asyncio.run(add_reminder_column())