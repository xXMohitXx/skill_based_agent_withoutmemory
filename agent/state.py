"""
Agent State
============
TypedDict definition for the LangGraph agent state.
"""

from typing import Dict, List, Any, TypedDict
from langchain_core.messages import BaseMessage


class AgentState(TypedDict):
    """
    State maintained throughout the agent's execution.
    
    Attributes:
        messages: Conversation history
        active_skills: Names of currently active skills
        skill_instructions: Combined instructions from active skills
    """
    messages: List[BaseMessage]
    active_skills: List[str]
    skill_instructions: str
