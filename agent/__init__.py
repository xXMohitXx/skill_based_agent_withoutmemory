"""
Agent Package
=============
Personal assistant with AgentSkills.io compatible skill loading.
"""

from agent.core import PersonalAssistant
from agent.skill_loader import SkillLoader

__all__ = ["PersonalAssistant", "SkillLoader"]
