---
name: todo
description: Manage tasks, todos, reminders, and chores. Use when the user wants to add a task, list their tasks, complete a task, delete a task, or set a reminder. Trigger words include todo, task, remind, reminder, add, list, done, complete, delete.
---

# Todo Skill

## When to use this skill

Use this skill when the user:
- Wants to add a new task or reminder ("add a task", "remind me to", "I need to")
- Wants to see their tasks ("show my tasks", "what are my todos", "list tasks")
- Wants to complete a task ("mark as done", "finished", "completed task 2")
- Wants to delete a task ("delete task", "remove todo")
- Mentions buying, doing, or remembering something as a future action

## Data storage

Tasks are stored in `data/todos.json` with this structure:
```json
{
  "todos": [
    {"id": 1, "content": "Buy groceries", "completed": false, "created_at": "2024-01-01T10:00:00"}
  ],
  "next_id": 2
}
```

## Actions

### Adding a task
1. Extract the task content from the user's message
2. Generate a new ID using `next_id`
3. Add the task with `completed: false` and current timestamp
4. Increment `next_id`
5. Confirm: "✅ Added task #[id]: [content]"

### Listing tasks
1. Read all tasks from the file
2. Format as a numbered list
3. Show completion status with ✅ (done) or ⬜ (pending)
4. If no tasks, say "No tasks yet! Add one with 'add a task...'"

### Completing a task
1. Find the task by ID
2. Set `completed: true`
3. Confirm: "✅ Completed: [content]"

### Deleting a task
1. Find the task by ID
2. Remove it from the list
3. Confirm: "🗑️ Deleted: [content]"

## Response format

When listing tasks:
```
📋 Your Tasks:
1. ⬜ Buy groceries
2. ✅ Call mom
3. ⬜ Fix the bug

Total: 3 tasks (1 completed)
```

## Examples

**User**: "add a task at 7pm to buy groceries"
**Response**: "✅ Added task #1: Buy groceries at 7pm"

**User**: "remind me to call mom tomorrow"
**Response**: "✅ Added task #2: Call mom tomorrow"

**User**: "show my todos"
**Response**: "📋 Your Tasks:
1. ⬜ Buy groceries at 7pm
2. ⬜ Call mom tomorrow"

**User**: "complete task 1"
**Response**: "✅ Completed: Buy groceries at 7pm"

**User**: "what do I need to do?"
**Response**: "📋 Your Tasks:
1. ⬜ Call mom tomorrow

You have 1 pending task."
