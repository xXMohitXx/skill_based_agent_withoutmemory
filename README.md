# Skill-Based Personal Assistant

A personal assistant built with **LangChain** and **LangGraph** that uses the **AgentSkills.io** specification for dynamic skill loading.

## How It Works

This agent follows the [AgentSkills.io](https://agentskills.io) specification:

1. **Discovery**: At startup, the agent loads only the `name` and `description` from each skill's `SKILL.md`
2. **Activation**: When a user's message matches a skill's description, the full instructions are loaded
3. **Execution**: The agent follows the skill's instructions to help the user

## Project Structure

```
skillbased_agent/
├── main.py              # Entry point
├── agent/
│   ├── core.py          # LangGraph agent
│   ├── skill_loader.py  # AgentSkills.io compatible loader
│   └── state.py         # Agent state
├── skills/              # AgentSkills.io format skills
│   ├── chat/
│   │   └── SKILL.md
│   ├── todo/
│   │   └── SKILL.md
│   ├── profile/
│   │   └── SKILL.md
│   └── math/
│       └── SKILL.md
├── data/                # Persistent storage
├── requirements.txt
└── .env
```

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Add your Groq API key
echo "GROQ_API_KEY=your_key_here" > .env

# Run the assistant
python main.py
```

## Skills

| Skill | Description |
|-------|-------------|
| **chat** | General conversation, greetings, time queries |
| **todo** | Task and reminder management |
| **profile** | Remember user information |
| **math** | Calculations and conversions |

## Adding New Skills

Create a new folder in `skills/` with a `SKILL.md` file:

```yaml
---
name: my-skill
description: What this skill does and when to use it.
---

# My Skill

## When to use
Describe when this skill should be activated.

## Instructions
Step-by-step instructions for the agent.
```

## License

MIT
