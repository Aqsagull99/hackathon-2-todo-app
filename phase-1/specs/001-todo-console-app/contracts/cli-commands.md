# CLI Command Contracts

## Command Reference

### add

Create a new task.

**Format**: `add "title"`

**Input**:
- title: string (quoted, 1-200 characters)

**Output**:
- Success: `Created task [id]: "title"`
- Error: `Error: Title cannot be empty` or `Error: Title must be under 200 characters`

**Example**:
```
> add "Buy groceries"
Created task 1: "Buy groceries"
```

---

### list

Display all tasks.

**Format**: `list`

**Output**: Formatted list showing ID, status, and title

**Example**:
```
> list
[ ] 1. Buy groceries
[ ] 2. Call mom
[✓] 3. Finish project
```

---

### view

Show detailed task information.

**Format**: `view <id>`

**Input**:
- id: integer (task ID)

**Output**:
- Success: Task details (id, title, status, created)
- Error: `Error: Task [id] not found`

**Example**:
```
> view 1
Task #1
-------
Title: Buy groceries
Status: Pending
```

---

### complete

Mark a task as complete.

**Format**: `complete <id>`

**Input**:
- id: integer (task ID)

**Output**:
- Success: `Task [id] marked as complete`
- Error: `Error: Task [id] not found`

**Example**:
```
> complete 1
Task 1 marked as complete
```

---

### update

Update a task's title.

**Format**: `update <id> "new title"`

**Input**:
- id: integer (task ID)
- new_title: string (quoted, 1-200 characters)

**Output**:
- Success: `Task [id] updated to: "new title"`
- Error: `Error: Task [id] not found`
- Error: `Error: Title cannot be empty`

**Example**:
```
> update 1 "Buy groceries and fruits"
Task 1 updated to: "Buy groceries and fruits"
```

---

### delete

Delete a task.

**Format**: `delete <id>`

**Input**:
- id: integer (task ID)

**Output**:
- Success: `Task [id] deleted`
- Error: `Error: Task [id] not found`

**Example**:
```
> delete 1
Task 1 deleted
```

---

### help

Display available commands.

**Format**: `help`

**Output**: List of all commands with descriptions

---

### exit

Exit the application.

**Format**: `exit`

**Output**: `Goodbye!`

## Error Handling

All errors follow this pattern:

1. Invalid ID (non-numeric, negative, too large):
   ```
   Error: Task [id] not found
   ```

2. Empty/whitespace title:
   ```
   Error: Title cannot be empty
   ```

3. Title too long:
   ```
   Error: Title must be under 200 characters
   ```

4. No tasks exist:
   ```
   Error: No tasks found. Add a task first!
   ```
