#!/usr/bin/env python3
"""
Script to apply the 004_extended_features migration directly to the database.
"""

import asyncio
import asyncpg
import os
from app.core.config import settings


async def apply_migration():
    print("Connecting to database...")

    # Connect to the database
    conn = await asyncpg.connect(
        dsn=settings.DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")
    )

    try:
        print("Applying migration: Add Extended Features to Tasks")

        # 1. Create priority enum type if not exists
        print("Creating priority enum type...")
        await conn.execute("""
            DO $$ BEGIN
                CREATE TYPE task_priority AS ENUM ('high', 'medium', 'low');
            EXCEPTION
                WHEN duplicate_object THEN null;
            END $$;
        """)

        # 2. Create recurrence_pattern enum type if not exists
        print("Creating recurrence_pattern enum type...")
        await conn.execute("""
            DO $$ BEGIN
                CREATE TYPE recurrence_pattern AS ENUM ('daily', 'weekly', 'monthly');
            EXCEPTION
                WHEN duplicate_object THEN null;
            END $$;
        """)

        # 3. Create reminder_status enum type if not exists
        print("Creating reminder_status enum type...")
        await conn.execute("""
            DO $$ BEGIN
                CREATE TYPE reminder_status AS ENUM ('pending', 'sent', 'snoozed', 'dismissed');
            EXCEPTION
                WHEN duplicate_object THEN null;
            END $$;
        """)

        # 4. Add new columns to tasks table
        print("Adding new columns to tasks table...")
        await conn.execute("""
            ALTER TABLE tasks
            ADD COLUMN IF NOT EXISTS priority task_priority DEFAULT 'medium' NOT NULL,
            ADD COLUMN IF NOT EXISTS due_date TIMESTAMP WITH TIME ZONE,
            ADD COLUMN IF NOT EXISTS due_date_tz VARCHAR(50) DEFAULT 'UTC',
            ADD COLUMN IF NOT EXISTS recurrence_pattern recurrence_pattern,
            ADD COLUMN IF NOT EXISTS recurrence_parent_id INTEGER REFERENCES tasks(id),
            ADD COLUMN IF NOT EXISTS completed_at TIMESTAMP WITHOUT TIME ZONE;
        """)

        # 5. Create tags table
        print("Creating tags table...")
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS tags (
                id SERIAL PRIMARY KEY,
                user_id VARCHAR(255) NOT NULL, -- Will add FK reference later if needed
                name VARCHAR(50) NOT NULL,
                color VARCHAR(7) DEFAULT '#EC4899',
                created_at TIMESTAMP DEFAULT NOW(),
                UNIQUE(name, user_id)
            );
        """)

        # 6. Create task_tag_link table for many-to-many relationship
        print("Creating task_tag_link table...")
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS task_tag_link (
                task_id INTEGER NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
                tag_id INTEGER NOT NULL REFERENCES tags(id) ON DELETE CASCADE,
                created_at TIMESTAMP DEFAULT NOW(),
                PRIMARY KEY (task_id, tag_id)
            );
        """)

        # 7. Create reminders table
        print("Creating reminders table...")
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS reminders (
                id SERIAL PRIMARY KEY,
                task_id INTEGER NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
                due_time TIMESTAMP NOT NULL,
                status reminder_status,
                snoozed_until TIMESTAMP,
                created_at TIMESTAMP DEFAULT NOW(),
                updated_at TIMESTAMP DEFAULT NOW()
            );
        """)

        # Set default after table creation to avoid enum issues
        try:
            await conn.execute("ALTER TABLE reminders ALTER COLUMN status SET DEFAULT 'pending';")
        except Exception as e:
            print(f"Warning: Could not set default for reminders.status: {e}")
            pass

        # 8. Create indexes for performance
        print("Creating indexes...")
        await conn.execute("CREATE INDEX IF NOT EXISTS idx_tasks_priority ON tasks(priority);")
        await conn.execute("CREATE INDEX IF NOT EXISTS idx_tasks_due_date ON tasks(due_date);")
        await conn.execute("CREATE INDEX IF NOT EXISTS idx_tasks_user_priority ON tasks(user_id, priority);")
        await conn.execute("CREATE INDEX IF NOT EXISTS idx_tasks_user_due_date ON tasks(user_id, due_date);")
        await conn.execute("CREATE INDEX IF NOT EXISTS idx_tags_user_id ON tags(user_id);")
        await conn.execute("CREATE INDEX IF NOT EXISTS idx_reminders_task_id ON reminders(task_id);")
        # Skip the partial index that uses enum value to avoid issues
        # await conn.execute("CREATE INDEX IF NOT EXISTS idx_reminders_due_time ON reminders(due_time) WHERE status = 'pending';")

        # 9. Create full-text search vector column
        print("Adding search vector column...")
        await conn.execute("ALTER TABLE tasks ADD COLUMN IF NOT EXISTS search_vector TSVECTOR;")

        # 10. Create function to update search vector
        print("Creating search vector function...")
        await conn.execute("""
            CREATE OR REPLACE FUNCTION update_task_search_vector()
            RETURNS TRIGGER AS $$
            BEGIN
                NEW.search_vector :=
                    setweight(to_tsvector('english', COALESCE(NEW.title, '')), 'A') ||
                    setweight(to_tsvector('english', COALESCE(NEW.description, '')), 'B');
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
        """)

        # 11. Create trigger to auto-update search vector
        print("Creating search vector trigger...")
        await conn.execute("DROP TRIGGER IF EXISTS task_search_vector_update ON tasks;")
        await conn.execute("""
            CREATE TRIGGER task_search_vector_update
                BEFORE INSERT OR UPDATE OF title, description
                ON tasks
                FOR EACH ROW
                EXECUTE FUNCTION update_task_search_vector();
        """)

        # 12. Create GIN index for full-text search
        print("Creating search vector index...")
        await conn.execute("CREATE INDEX IF NOT EXISTS idx_tasks_search_vector ON tasks USING GIN(search_vector);")

        print("Migration applied successfully!")

        # Verify the changes
        print("\nVerifying changes...")

        # Check if priority column exists
        result = await conn.fetch("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns
            WHERE table_name = 'tasks' AND column_name = 'priority'
        """)
        print(f"Priority column: {result}")

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

        # Check if other extended tables exist
        result = await conn.fetch("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_name IN ('tags', 'task_tag_link', 'reminders')
        """)
        print(f"Extended tables created: {[row['table_name'] for row in result]}")

    except Exception as e:
        print(f"Error applying migration: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        await conn.close()
        print("Database connection closed.")


if __name__ == "__main__":
    asyncio.run(apply_migration())