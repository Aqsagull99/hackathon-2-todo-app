# Implementation Guide: Task Field Parsing & Display

## Quick Start

The enhancement is fully implemented and ready to use. No additional setup required beyond what's already in place.

## How It Works

### 1. User Input
User provides task details in any format:
```
"Add morning walk - 30 minutes, Priority: high, Due: Monday, Recurring: daily, Reminder: 7am, Tags: exercise, health"
```

### 2. Backend Processing (chat_agent.py)

The `add` intent handler:
1. **Detects the `add` intent** from the message
2. **Parses individual fields** using regex patterns:
   - Title: Text before or after "Title:" marker
   - Description: Text after "Description:" marker
   - Priority: Keywords "high", "medium", "low"
   - Due Date: Day names (Monday-Sunday) or relative dates
   - Recurrence: Keywords "daily", "weekly", "monthly"
   - Reminder: Time specification after "Reminder:"
   - Tags: Comma-separated list after "Tags:"
3. **Creates task in DB** with all parsed fields via `TaskCreate`
4. **Formats response** with markdown to show all extracted details
5. **Returns tool_calls** with structured parameters

### 3. Frontend Display (TaskItem.tsx)

TaskItem component renders:
1. **Title**: Main task heading
2. **Description**: Full description text (not truncated)
3. **Field Badges**: Color-coded and icon-labeled badges for:
   - Priority (red/yellow/blue)
   - Due Date (green, calendar icon)
   - Recurrence (purple, refresh icon)
   - Reminder (orange, clock icon)
   - Tags (gray, tag icon)

### 4. User Sees
```
☑ Task Title
  Full description text

🚨 high | 📅 Jan 19 | 🔄 daily | ⏰ 6:30am | tag1 | tag2
```

## File Changes Summary

### Backend Files Modified

#### `/phase-2/backend/app/agents/chat_agent.py`
**Lines: add intent handler (now ~490-560)**

```python
if intent == "add":
    # Extract title
    title_match = re.search(r'(?:title|task):\s*([^,\n]+?)', user_message, re.IGNORECASE)
    title = title_match.group(1).strip() if title_match else user_message.strip()
    
    # Extract priority
    msg_lower = user_message.lower()
    priority = "high" if "high" in msg_lower else "medium"
    
    # Extract due_date, recurrence_pattern, reminder_time, tags, description
    # ... regex patterns ...
    
    # Create task in DB
    task = await create_task(db, user_identifier, task_payload)
    
    # Build formatted response with all fields
    details = [f"**Title:** {title}", f"**Priority:** {priority}", ...]
    
    # Return tool_calls with structured parameters
    return {"response": reply, "tool_calls": tool_calls, ...}
```

### Frontend Files Modified

#### `/phase-2/frontend/src/components/tasks/TaskItem.tsx`
**Lines: Task Content section (replaces old field display)**

```tsx
{/* Enhanced field badges */}
{task.priority && (
  <span className="...red badge...">🚨 {task.priority}</span>
)}
{task.due_date && (
  <span className="...green badge...">📅 {formatted_date}</span>
)}
{task.recurrence_pattern && (
  <span className="...purple badge...">🔄 {task.recurrence_pattern}</span>
)}
{task.reminder && (
  <span className="...orange badge...">⏰ {task.reminder}</span>
)}
{task.tags?.map(tag => (
  <span className="...gray badge...">{tag}</span>
))}
```

#### `/phase-2/frontend/src/types/index.ts`
**Lines: Task interface (added reminder field)**

```typescript
export interface Task {
  // ... existing fields ...
  reminder?: string | null;  // NEW FIELD
  // ... existing fields ...
}
```

## Configuration Files (No Changes Needed)

- `.env`: Already has all required API keys and DB config
- `pyproject.toml`: All dependencies already installed
- `package.json`: All frontend dependencies already present

## Testing the Implementation

### Test 1: Simple Task with All Fields
```bash
# User message with all details
Message: "Add Morning Walk - 30 min, high priority, Monday, daily, 7am, exercise, health"

Expected Response: 
- Task created in DB
- Response shows: **Title:** Morning Walk, **Priority:** high, **Due Date:** Jan 19, **Recurring:** daily, **Reminder:** 7am, **Tags:** exercise, health
- Frontend displays badges: 🚨 high | 📅 Jan 19 | 🔄 daily | ⏰ 7am | exercise | health
```

### Test 2: Minimal Task (Backward Compatibility)
```bash
# User message with title only
Message: "Add Buy groceries"

Expected Response:
- Task created in DB with just title
- Response shows: **Title:** Buy groceries
- Frontend displays with defaults (no badges for missing fields)
```

### Test 3: Urdu Input
```bash
# User message in Urdu
Message: "ap meri shopping ka task add krdo, high priority, monday ko"

Expected Response:
- Task created in DB
- Title and fields parsed correctly
- Works with Urdu keywords mixed with English field markers
```

## Feature Breakdown

### Priority Extraction
**Patterns recognized:**
- "Priority: high"
- "high priority"
- "High"
- "Priority: low"
- etc.

**Defaults to:** "medium"

### Date Parsing
**Patterns recognized:**
- "Monday", "Tuesday", etc. → Next occurrence of that day
- "Tomorrow" → Tomorrow's date
- "Today" → Today's date
- "Due: 2026-01-20" → Specific date
- Relative: "in 2 weeks", etc.

**Defaults to:** None (no due date)

### Recurrence Pattern
**Patterns recognized:**
- "daily"
- "weekly"
- "monthly"
- "recurring daily"
- etc.

**Defaults to:** None (one-time task)

### Tags Extraction
**Formats supported:**
- "Tags: work, urgent, project"
- "Tags: personal"
- Space-separated at end: "exercise health"

**Defaults to:** Empty array (no tags)

### Reminder Time
**Formats supported:**
- "Reminder: 9am"
- "Remind at 3:30pm"
- "7am reminder"

**Defaults to:** None (no reminder)

## API Integration

### Request Format
```json
{
  "message": "Add Morning Walk - 30 min, high priority, Monday, daily, 7am, exercise, health"
}
```

### Response Format
```json
{
  "response": "Naya task jor diya gaya! ✅\n\n**Title:** Morning Walk\n**Priority:** high\n**Due Date:** 2026-01-19\n**Recurring:** daily\n**Reminder:** 7am\n**Tags:** exercise, health",
  "tool_calls": [
    {
      "tool": "create_task",
      "parameters": {
        "title": "Morning Walk",
        "priority": "high",
        "due_date": "2026-01-19",
        "recurrence_pattern": "daily",
        "reminder_time": "7am",
        "tags": ["exercise", "health"]
      },
      "result": {
        "id": 123,
        "title": "Morning Walk",
        "local": false
      }
    }
  ]
}
```

## Styling Details (Frontend)

### Color Scheme
```css
/* Priority */
.priority-high { background: #FEE2E2; color: #991B1B; }     /* Red */
.priority-medium { background: #FEF3C7; color: #92400E; }   /* Yellow */
.priority-low { background: #DBEAFE; color: #1E3A8A; }      /* Blue */

/* Due Date */
.due-date { background: #F0FDF4; color: #15803D; }          /* Green */

/* Recurrence */
.recurrence { background: #F3E8FF; color: #6B21A8; }        /* Purple */

/* Reminder */
.reminder { background: #FEF3C7; color: #92400E; }          /* Orange */

/* Tags */
.tag { background: #F3F4F6; color: #374151; }               /* Gray */
```

### Layout
- Flex wrap with gap-2 spacing
- Icons included with semantic meaning
- Responsive on mobile (wraps naturally)
- Accessible with proper semantic HTML

## Debugging

### If fields not extracting:
1. Check regex patterns in chat_agent.py
2. Verify message format matches pattern
3. Add logging to `_detect_intent()` function
4. Check user_message encoding (for Urdu text)

### If frontend not displaying:
1. Verify Task type includes new fields
2. Check TaskItem imports and rendering logic
3. Inspect browser console for JS errors
4. Verify data returned from API has fields

### If DB not persisting:
1. Check DATABASE_URL in .env
2. Verify create_task service working (test via direct DB call)
3. Check task_payload has required fields
4. Review async session handling

## Future Enhancements

1. **Smarter NLP**: Use LLM to understand field boundaries
2. **Custom Parsing**: User-defined field markers
3. **Time Zones**: Support for different time zones
4. **Location Parsing**: Extract location for location-based reminders
5. **Duration Parsing**: "2 hours" becomes reminder offset
6. **Attachment Support**: Parse and attach files
7. **Collaboration**: Parse @ mentions for shared tasks

## Support

For issues or questions:
1. Check logs in `/phase-2/backend/logs/`
2. Review error in frontend browser console
3. Verify database connectivity
4. Test regex patterns independently
5. Check API response structure matches expected format

