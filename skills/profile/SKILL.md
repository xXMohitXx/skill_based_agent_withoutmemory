---
name: profile
description: Remember and recall user information like name, job, email, preferences, and personal details. Use when the user shares information about themselves or asks what you know about them.
---

# Profile Skill

## When to use this skill

Use this skill when the user:
- Shares their name ("I'm John", "My name is Sarah", "Call me Mike")
- Shares their job ("I work as a developer", "I'm a teacher")
- Shares contact info ("My email is...", "My phone is...")
- Shares preferences ("I prefer dark mode", "I like coffee")
- Shares location ("I live in New York", "I'm from London")
- Asks what you know about them ("What's my name?", "What do you know about me?")

## Data storage

Profile data is stored in `data/profile.json`:
```json
{
  "name": "John Doe",
  "job": "Software Developer",
  "email": "john@example.com",
  "location": "New York",
  "preferences": {
    "theme": "dark",
    "language": "English"
  },
  "custom": {
    "favorite_color": "blue"
  }
}
```

## Actions

### Saving information
1. Identify the type of information (name, job, email, etc.)
2. Extract the value from the user's message
3. Update the profile file
4. Confirm: "Got it! I'll remember that your [field] is [value]."

### Retrieving information
1. Read the profile file
2. Return the requested field(s)
3. If not found: "I don't have that information yet. Would you like to tell me?"

### Show all profile
When asked "what do you know about me":
1. List all stored information
2. Format nicely with emojis

## Response format

When showing profile:
```
👤 Your Profile:
• Name: John Doe
• Job: Software Developer
• Email: john@example.com
• Location: New York
• Preferences: Dark mode, English

Is there anything you'd like to update?
```

## Examples

**User**: "My name is Sarah"
**Response**: "Nice to meet you, Sarah! 👋 I'll remember that."

**User**: "I work as a graphic designer"
**Response**: "Got it! I'll remember that you work as a graphic designer. 🎨"

**User**: "What's my name?"
**Response**: "Your name is Sarah! 😊"

**User**: "I prefer dark mode and I like tea over coffee"
**Response**: "Noted! I'll remember your preference for dark mode and that you prefer tea. ☕"

**User**: "What do you know about me?"
**Response**: "👤 Here's what I know about you:
• Name: Sarah
• Job: Graphic Designer  
• Preferences: Dark mode, Tea over coffee

Would you like to add or update anything?"
