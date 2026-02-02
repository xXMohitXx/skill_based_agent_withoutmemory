"""
Personal Assistant Agent
========================
LangGraph agent with AgentSkills.io compatible skill loading.
The agent dynamically loads skills based on the conversation context.
"""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from agent.state import AgentState
from agent.skill_loader import SkillLoader


class PersonalAssistant:
    """
    Personal assistant with AgentSkills.io compatible skill loading.
    
    The agent:
    1. Discovers all skills at startup (loads only metadata)
    2. Analyzes user messages to determine which skills are needed
    3. Activates relevant skills by loading their full instructions
    4. Uses skill instructions to help the user
    """
    
    SYSTEM_PROMPT = """You are a helpful personal assistant.

## Current Time
{current_time}

## Available Skills
You have access to these skills that can be activated when needed:
{available_skills}

## Active Skills
{active_skills_section}

## Your Capabilities

### Data Operations
You can read and write JSON files in the `data/` directory to persist information:
- `data/todos.json` - Task list storage
- `data/profile.json` - User profile storage

When a skill instructs you to store data, use Python-style JSON operations mentally and describe the result.

## Instructions

1. **Analyze the user's request** to understand what they need
2. **Follow the instructions from active skills** to help them
3. **Be conversational and friendly** in your responses
4. **Use emojis** to make responses more engaging
5. **Persist important data** when skills instruct you to

## Important
- Follow skill instructions exactly as written
- If no skill is active for a request, have a natural conversation
- Be helpful, concise, and accurate
"""

    def __init__(self, skills_dir: str = "skills"):
        """
        Initialize the personal assistant.
        
        Args:
            skills_dir: Path to the skills directory
        """
        self.skill_loader = SkillLoader(skills_dir)
        self.memory = MemorySaver()
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)
        
        # Initialize LLM
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.7,
        )
        
        # Build the graph
        self._build_graph()
    
    def _build_graph(self) -> None:
        """Build the LangGraph workflow."""
        graph = StateGraph(AgentState)
        
        # Single node that handles the conversation
        graph.add_node("agent", self._agent_node)
        
        # Set entry point and edge to end
        graph.set_entry_point("agent")
        graph.add_edge("agent", END)
        
        # Compile with memory
        self.graph = graph.compile(checkpointer=self.memory)
    
    def _get_system_prompt(self) -> str:
        """Generate the current system prompt with active skills."""
        # Current time
        current_time = datetime.now().strftime("%A, %B %d, %Y at %I:%M %p")
        
        # Available skills
        available_skills = self.skill_loader.get_available_skills_xml()
        
        # Active skills section
        active_skills = self.skill_loader.list_active()
        if active_skills:
            active_content = self.skill_loader.get_active_skills_content()
            active_skills_section = f"""The following skills are currently active. Follow their instructions:

{active_content}"""
        else:
            active_skills_section = "No skills are currently active. Have a natural conversation."
        
        return self.SYSTEM_PROMPT.format(
            current_time=current_time,
            available_skills=available_skills,
            active_skills_section=active_skills_section
        )
    
    def _agent_node(self, state: AgentState) -> Dict[str, Any]:
        """
        Main agent node that processes user messages.
        """
        # Build messages with current system prompt
        system_msg = SystemMessage(content=self._get_system_prompt())
        messages = [system_msg] + state["messages"]
        
        # Get response from LLM
        response = self.llm.invoke(messages)
        
        return {"messages": [response]}
    
    def _determine_skills_needed(self, message: str) -> List[str]:
        """
        Analyze the message to determine which skills should be active.
        Uses keyword matching based on skill descriptions.
        """
        message_lower = message.lower()
        skills_needed = []
        
        # Define trigger patterns for each skill
        skill_triggers = {
            "chat": [
                "hello", "hi", "hey", "good morning", "good afternoon", "good evening",
                "bye", "goodbye", "see you", "what time", "what's the time", "current time",
                "what can you do", "who are you", "help me"
            ],
            "todo": [
                "todo", "task", "remind", "reminder", "add a task", "add task",
                "my tasks", "my todos", "list task", "show task", "complete task",
                "done", "finished", "delete task", "remove task", "buy", "need to",
                "don't forget", "remember to", "chore", "errand"
            ],
            "profile": [
                "my name is", "i'm", "i am", "call me", "my job", "i work",
                "my email", "my phone", "i live", "i prefer", "my favorite",
                "what's my name", "what do you know about me", "who am i"
            ],
            "math": [
                "calculate", "what is", "how much", "plus", "minus", "times",
                "divided", "multiply", "add", "subtract", "percent", "%",
                "convert", "celsius", "fahrenheit", "square root", "√"
            ]
        }
        
        # Check each skill
        for skill_name, triggers in skill_triggers.items():
            if skill_name in self.skill_loader.list_available():
                for trigger in triggers:
                    if trigger in message_lower:
                        if skill_name not in skills_needed:
                            skills_needed.append(skill_name)
                        break
        
        # Default to chat if no specific skill matched
        if not skills_needed:
            skills_needed = ["chat"]
        
        return skills_needed
    
    def chat(self, message: str, thread_id: str = "default") -> str:
        """
        Send a message to the assistant and get a response.
        
        Args:
            message: User message
            thread_id: Conversation thread ID for memory
            
        Returns:
            Assistant's response
        """
        # Determine and activate needed skills
        needed_skills = self._determine_skills_needed(message)
        
        # Activate needed skills
        for skill_name in needed_skills:
            if not self.skill_loader.is_active(skill_name):
                self.skill_loader.activate_skill(skill_name)
        
        # Prepare state
        initial_state = {
            "messages": [HumanMessage(content=message)],
            "active_skills": self.skill_loader.list_active(),
            "skill_instructions": self.skill_loader.get_active_skills_content()
        }
        
        config = {"configurable": {"thread_id": thread_id}}
        
        # Run the graph
        result = self.graph.invoke(initial_state, config)
        
        # Extract response
        for msg in reversed(result["messages"]):
            if isinstance(msg, AIMessage) and msg.content:
                return msg.content
        
        return "I'm having trouble responding right now."
    
    def activate_skill(self, skill_name: str) -> bool:
        """Manually activate a skill."""
        return self.skill_loader.activate_skill(skill_name) is not None
    
    def deactivate_skill(self, skill_name: str) -> bool:
        """Manually deactivate a skill."""
        return self.skill_loader.deactivate_skill(skill_name)
    
    def get_skill_info(self) -> Dict[str, Dict]:
        """Get information about all skills."""
        info = {}
        for skill in self.skill_loader.get_skill_list():
            info[skill["name"]] = {
                "description": skill["description"],
                "active": self.skill_loader.is_active(skill["name"])
            }
        return info
    
    def list_available_skills(self) -> List[str]:
        """Get list of available skill names."""
        return self.skill_loader.list_available()
    
    def list_active_skills(self) -> List[str]:
        """Get list of active skill names."""
        return self.skill_loader.list_active()
