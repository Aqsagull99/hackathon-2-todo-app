-- Migration: Add Extended Features to Tasks
-- Feature: Task Organization & Intelligence (004)
-- Created: 2026-01-03

-- 1. Create priority enum type if not exists
DO $$ BEGIN
    CREATE TYPE task_priority AS ENUM ('high', 'medium', 'low');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- 2. Create recurrence_pattern enum type if not exists
DO $$ BEGIN
    CREATE TYPE recurrence_pattern AS ENUM ('daily', 'weekly', 'monthly');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- 3. Create reminder_status enum type if not exists
DO $$ BEGIN
    CREATE TYPE reminder_status AS ENUM ('pending', 'sent', 'snoozed', 'dismissed');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- 4. Add new columns to tasks table
ALTER TABLE tasks
ADD COLUMN IF NOT EXISTS priority task_priority DEFAULT 'medium' NOT NULL,
ADD COLUMN IF NOT EXISTS due_date TIMESTAMP WITH TIME ZONE,
ADD COLUMN IF NOT EXISTS due_date_tz VARCHAR(50) DEFAULT 'UTC',
ADD COLUMN IF NOT EXISTS recurrence_pattern recurrence_pattern,
ADD COLUMN IF NOT EXISTS recurrence_parent_id INTEGER REFERENCES tasks(id);

-- 5. Create tags table
CREATE TABLE IF NOT EXISTS tags (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(50) NOT NULL,
    color VARCHAR(7) DEFAULT '#EC4899',
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(name, user_id)
);

-- 6. Create task_tag_link table for many-to-many relationship
CREATE TABLE IF NOT EXISTS task_tag_link (
    task_id INTEGER NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
    tag_id INTEGER NOT NULL REFERENCES tags(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (task_id, tag_id)
);

-- 7. Create reminders table
CREATE TABLE IF NOT EXISTS reminders (
    id SERIAL PRIMARY KEY,
    task_id INTEGER NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
    due_time TIMESTAMP NOT NULL,
    status reminder_status DEFAULT 'pending',
    snoozed_until TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 8. Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_tasks_priority ON tasks(priority);
CREATE INDEX IF NOT EXISTS idx_tasks_due_date ON tasks(due_date);
CREATE INDEX IF NOT EXISTS idx_tasks_user_priority ON tasks(user_id, priority);
CREATE INDEX IF NOT EXISTS idx_tasks_user_due_date ON tasks(user_id, due_date);
CREATE INDEX IF NOT EXISTS idx_tags_user_id ON tags(user_id);
CREATE INDEX IF NOT EXISTS idx_reminders_task_id ON reminders(task_id);
CREATE INDEX IF NOT EXISTS idx_reminders_due_time ON reminders(due_time) WHERE status = 'pending';

-- 9. Create full-text search vector column
ALTER TABLE tasks ADD COLUMN IF NOT EXISTS search_vector TSVECTOR;

-- 10. Create function to update search vector
CREATE OR REPLACE FUNCTION update_task_search_vector()
RETURNS TRIGGER AS $$
BEGIN
    NEW.search_vector :=
        setweight(to_tsvector('english', COALESCE(NEW.title, '')), 'A') ||
        setweight(to_tsvector('english', COALESCE(NEW.description, '')), 'B');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 11. Create trigger to auto-update search vector
DROP TRIGGER IF EXISTS task_search_vector_update ON tasks;
CREATE TRIGGER task_search_vector_update
    BEFORE INSERT OR UPDATE OF title, description
    ON tasks
    FOR EACH ROW
    EXECUTE FUNCTION update_task_search_vector();

-- 12. Create GIN index for full-text search
CREATE INDEX IF NOT EXISTS idx_tasks_search_vector ON tasks USING GIN(search_vector);

-- Verification query (run after migration):
-- SELECT column_name, data_type FROM information_schema.columns
-- WHERE table_name = 'tasks' ORDER BY ordinal_position;

-- SELECT tablename FROM pg_tables WHERE schemaname = 'public'
-- AND tablename IN ('tasks', 'tags', 'task_tag_link', 'reminders');
