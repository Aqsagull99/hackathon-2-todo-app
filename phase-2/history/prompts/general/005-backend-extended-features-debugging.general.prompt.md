---
ID: 005
TITLE: Backend Extended Features Debugging & Fix Session
STAGE: general
DATE_ISO: 2026-01-07
SURFACE: agent
MODEL: claude-opus-4-5-20251101
FEATURE: "none"
BRANCH: phase-two
USER: aqsagulllinux
COMMAND: "continue (resumed from previous context)"
LABELS: ["debugging", "backend", "fastapi", "sqlalchemy", "database", "extended-features"]
LINKS:
  SPEC: null
  TICKET: null
  ADR: null
  PR: null
FILES_YAML: |
  - app/schemas/extended.py
  - app/models/reminder.py
  - app/services/reminder_service.py
  - app/api/routes/tasks_extended.py
TESTS_YAML: |
  - bash /tmp/test_extended_features.sh (verified all endpoints)
  - Manual curl tests for task creation with timezone
  - Manual curl tests for reminder creation
---

## Summary

Fixed critical backend bugs preventing extended features (tags, reminders, recurring tasks) from being stored in Neon PostgreSQL database. All extended features now working end-to-end.

## Bugs Fixed

### Bug 1: Timezone Mismatch on `due_date` (CRITICAL)
**Error**: `can't subtract offset-naive and offset-aware datetimes`
- **Root Cause**: Frontend sends ISO 8601 datetimes with timezone (e.g., "2026-01-15T18:00:00Z"), but database column is `TIMESTAMP WITHOUT TIME ZONE`
- **Solution**: Added Pydantic field validators to strip timezone info from `due_date` and `due_time` fields before storing
- **Files Modified**:
  - `app/schemas/extended.py` - Added `@field_validator('due_date')` and `@field_validator('due_time')` methods
  - `app/api/routes/tasks_extended.py` - Removed redundant timezone stripping code

### Bug 2: PostgreSQL Enum Value Mismatch (CRITICAL)
**Error**: `invalid input value for enum reminderstatus: "pending"`
- **Root Cause**: PostgreSQL enum `reminderstatus` was created with uppercase values (`PENDING`, `SENT`, `SNOOZED`, `DISMISSED`), but Python enum had lowercase values
- **Solution**: Updated ReminderStatus enum to use uppercase values to match database
- **Files Modified**:
  - `app/models/reminder.py` - Changed enum values from "pending"/"sent"/etc. to "PENDING"/"SENT"/etc.
  - `app/schemas/extended.py` - Same enum value changes in schema definition

### Bug 3: SQLAlchemy Lazy-Load Exception in Async Context
**Error**: `sqlalchemy.exc.MissingGreenlet: greenlet_spawn has not been called`
- **Root Cause**: Accessing `task.tags` relationship after async query triggered lazy-loading in non-greenlet context
- **Solution**: Manually loaded tags using service and built response dict without accessing lazy-loaded relationship
- **Files Modified**:
  - `app/api/routes/tasks_extended.py` - Changed create_task_extended to manually build response dict

### Bug 4: Variable Name Error in Tag Assignment
**Error**: `NameError: name 'user_id' is not defined`
- **Root Cause**: Used undefined variable `user_id` instead of parameter `current_user_id`
- **Solution**: Corrected variable reference in loop
- **Files Modified**: `app/api/routes/tasks_extended.py` line ~129

## Test Results

All extended features now working:

✅ **Tags**: Created tag "Work" (ID: 9)
✅ **Task with Tags**: Task created with tag attached (ID: 42, includes "Work" tag in response)
✅ **Reminders**: Reminder created for task (ID: 2, status: "PENDING")
✅ **Recurring Tasks**: Daily recurring task created (ID: 43, recurrence_pattern: "daily")

Response from test script:
```json
{
  "id": 42,
  "title": "Complete project documentation",
  "priority": "high",
  "due_date": "2026-01-15T18:00:00Z",
  "tags": [{"id": 9, "name": "Work", "color": "#FF6EC7"}],
  "created_at": "2026-01-07T06:27:00.403196"
}
```

## Implementation Details

### Timezone Handling Strategy
- All datetimes sent by frontend with timezone info (ISO 8601 with Z suffix)
- Database schema uses `TIMESTAMP WITHOUT TIME ZONE` (naive datetimes)
- Solution: Strip timezone in Pydantic validators before database operations
- Timezone info stored separately in `due_date_tz` field for client reference

### Enum Value Consistency
- PostgreSQL enum `reminderstatus` has uppercase values in database
- Python enums must match exactly: `"PENDING"` not `"pending"`
- Verified via query: `SELECT enumlabel FROM pg_enum WHERE enumtypid = (SELECT oid FROM pg_type WHERE typname='reminderstatus')`
- Result: `[('PENDING',), ('SENT',), ('SNOOZED',), ('DISMISSED',)]`

### Async/Await Pattern
- SQLModel relationships are lazy-loaded by default in async context
- Accessing relationship attributes (`task.tags`) after async query breaks greenlet context
- Solution: Explicitly load relationships in service layer, pass data to response serializer

## Files Changed Summary

1. **app/models/reminder.py**
   - Line 16-19: Updated ReminderStatus enum values to uppercase
   - Line 32: Corrected enum type name to "reminderstatus"

2. **app/schemas/extended.py**
   - Added import: `from pydantic import field_validator`
   - TaskCreateExtended: Added `strip_timezone_from_due_date` validator
   - TaskUpdateExtended: Added `strip_timezone_from_due_date` validator
   - ReminderCreate: Added `strip_timezone_from_due_time` validator
   - ReminderStatus: Changed enum values to uppercase (lines 26-29)

3. **app/api/routes/tasks_extended.py**
   - Lines 111-120: Removed redundant timezone stripping (now handled in schema validator)
   - Lines 146-161: Changed response building to manually construct dict (avoid lazy-load)
   - Line 138: Fixed variable name from `user_id` to `current_user_id`

4. **app/services/reminder_service.py**
   - Updated status assignments to use ReminderStatus enum (already correct)

## Database Verification

Confirmed that all records are now being stored in Neon PostgreSQL:
- **tags table**: New tags persisting with ID, name, color, user_id, created_at
- **task_tag_link table**: Task-tag relationships properly stored
- **reminders table**: Reminders storing with task_id, due_time, status (enum), timestamps
- **tasks table**: Extended task data (priority, due_date, recurrence_pattern) all storing correctly

## Lessons Learned

1. **Timezone Handling**: ISO 8601 strings with 'Z' suffix parse to timezone-aware datetimes in Python. Database-level timezone management requires explicit handling in ORM layer.

2. **PostgreSQL Enums**: Enum values must match exactly (case-sensitive). Verify database enum values with system queries when debugging mismatches.

3. **SQLAlchemy Async**: Lazy-loaded relationships in async context cause greenlet issues. Always explicitly load relationships in service layer for async operations.

4. **Testing Strategy**: Test end-to-end with realistic client data (timezone-aware datetimes) not just happy-path naive datetimes.

## Outcome

✅ All extended features (tags, reminders, recurring tasks) now fully functional
✅ Data persisting correctly to Neon PostgreSQL
✅ CORS working, requests returning proper status codes and headers
✅ Frontend can now complete end-to-end workflows with extended features

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
