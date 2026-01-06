#!/usr/bin/env python3
"""
Script to fix the enum name mismatch in the database.
"""

import asyncio
import asyncpg
from app.core.config import settings


async def fix_enum_names():
    print("Connecting to database...")

    # Connect to the database
    conn = await asyncpg.connect(
        dsn=settings.DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")
    )

    try:
        print("Fixing enum name mismatch...")

        # Check current enum names
        result = await conn.fetch("""
            SELECT t.typname AS enum_name, e.enumlabel AS enum_value
            FROM pg_type t
            JOIN pg_enum e ON t.oid = e.enumtypid
            WHERE t.typname IN ('taskpriority', 'task_priority', 'recurrencepattern', 'recurrence_pattern')
            ORDER BY t.typname, e.enumsortorder;
        """)

        print("Current enum names and values:")
        for row in result:
            print(f"  {row['enum_name']}: {row['enum_value']}")

        # Check what enum the priority column is using
        result = await conn.fetch("""
            SELECT column_name, data_type, udt_name
            FROM information_schema.columns
            WHERE table_name = 'tasks' AND column_name = 'priority';
        """)
        print(f"\nPriority column info: {result}")

        # Check for both enum types
        result = await conn.fetch("""
            SELECT t.typname AS enum_name
            FROM pg_type t
            JOIN pg_namespace n ON t.typnamespace = n.oid
            WHERE t.typname IN ('taskpriority', 'task_priority');
        """)
        print(f"\nExisting enum types: {[row['enum_name'] for row in result]}")

        # If both exist, we need to update the column to use the correct one
        if 'task_priority' in [row['enum_name'] for row in result] and 'taskpriority' in [row['enum_name'] for row in result]:
            print("\nRenaming the incorrect enum type...")
            # Drop the incorrect enum type and rename the correct one if needed
            # Or update the column to use the correct enum
            await conn.execute("ALTER TABLE tasks ALTER COLUMN priority TYPE task_priority USING priority::text::task_priority;")
            print("Updated priority column to use correct enum type")
        elif 'taskpriority' in [row['enum_name'] for row in result] and 'task_priority' not in [row['enum_name'] for row in result]:
            # The enum is named taskpriority, but we need task_priority
            print("\nRenaming enum from taskpriority to task_priority...")
            await conn.execute("ALTER TYPE taskpriority RENAME TO task_priority;")
            print("Renamed enum type")

            # Update the column type
            await conn.execute("ALTER TABLE tasks ALTER COLUMN priority TYPE task_priority USING priority::text::task_priority;")
        elif 'task_priority' in [row['enum_name'] for row in result]:
            # Check if the column is using the right type
            print("\nChecking if column uses correct enum type...")
            # Update the column to use the correct enum
            try:
                await conn.execute("ALTER TABLE tasks ALTER COLUMN priority TYPE task_priority USING priority::text::task_priority;")
                print("Updated priority column to use correct enum type")
            except Exception as e:
                print(f"Column might already be correct: {e}")

        # Also fix the recurrence pattern enum if needed
        result = await conn.fetch("""
            SELECT t.typname AS enum_name
            FROM pg_type t
            JOIN pg_namespace n ON t.typnamespace = n.oid
            WHERE t.typname IN ('recurrencepattern', 'recurrence_pattern');
        """)
        if 'recurrencepattern' in [row['enum_name'] for row in result] and 'recurrence_pattern' not in [row['enum_name'] for row in result]:
            print("Renaming recurrencepattern to recurrence_pattern...")
            await conn.execute("ALTER TYPE recurrencepattern RENAME TO recurrence_pattern;")
            print("Renamed recurrence pattern enum type")

            # Update any columns that use it
            try:
                await conn.execute("ALTER TABLE tasks ALTER COLUMN recurrence_pattern TYPE recurrence_pattern USING recurrence_pattern::text::recurrence_pattern;")
            except Exception as e:
                print(f"Recurrence pattern column update: {e}")

        # Check if enum values are correct case
        result = await conn.fetch("""
            SELECT t.typname AS enum_name, e.enumlabel AS enum_value
            FROM pg_type t
            JOIN pg_enum e ON t.oid = e.enumtypid
            WHERE t.typname = 'task_priority'
            ORDER BY e.enumsortorder;
        """)

        values = [row['enum_value'] for row in result]
        print(f"\nTask priority enum values: {values}")

        # If values are lowercase, we may need to handle the mapping in the application
        # But first, let's make sure the column type is correct

        print("\nVerifying fixes...")
        result = await conn.fetch("""
            SELECT column_name, data_type, udt_name
            FROM information_schema.columns
            WHERE table_name = 'tasks' AND column_name = 'priority';
        """)
        print(f"Priority column after fix: {result}")

        print("\nEnum names and values after fix:")
        result = await conn.fetch("""
            SELECT t.typname AS enum_name, e.enumlabel AS enum_value
            FROM pg_type t
            JOIN pg_enum e ON t.oid = e.enumtypid
            WHERE t.typname = 'task_priority'
            ORDER BY e.enumsortorder;
        """)
        for row in result:
            print(f"  {row['enum_name']}: {row['enum_value']}")

        print("Enum name fixes applied successfully!")

    except Exception as e:
        print(f"Error fixing enum names: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        await conn.close()
        print("Database connection closed.")


if __name__ == "__main__":
    asyncio.run(fix_enum_names())