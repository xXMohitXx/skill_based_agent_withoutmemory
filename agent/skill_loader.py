"""
Skill Loader
=============
AgentSkills.io compatible loader for discovering and loading skills.
"""

import os
import re
import yaml
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class SkillMetadata:
    """Metadata extracted from a skill's SKILL.md frontmatter."""
    name: str
    description: str
    path: Path
    
    def to_xml(self) -> str:
        """Convert to XML format for prompt injection."""
        return f"""<skill>
  <name>{self.name}</name>
  <description>{self.description}</description>
  <location>{self.path}</location>
</skill>"""


class SkillLoader:
    """
    AgentSkills.io compatible skill loader.
    
    Follows the specification:
    1. Discovery: At startup, load only name and description
    2. Activation: Load full SKILL.md when needed
    3. Execution: Agent follows the instructions
    """
    
    def __init__(self, skills_dir: str = "skills"):
        """
        Initialize the skill loader.
        
        Args:
            skills_dir: Path to the skills directory
        """
        self.skills_dir = Path(skills_dir)
        self.available_skills: Dict[str, SkillMetadata] = {}
        self.active_skills: Dict[str, str] = {}  # name -> full content
        
        # Discover all skills on init
        self._discover_skills()
    
    def _discover_skills(self) -> None:
        """
        Discover all skills in the skills directory.
        Load only metadata (name and description) for each.
        """
        if not self.skills_dir.exists():
            print(f"⚠️ Skills directory not found: {self.skills_dir}")
            return
        
        for skill_folder in self.skills_dir.iterdir():
            if skill_folder.is_dir():
                skill_file = skill_folder / "SKILL.md"
                if skill_file.exists():
                    metadata = self._parse_metadata(skill_file)
                    if metadata:
                        self.available_skills[metadata.name] = metadata
                        print(f"📝 Discovered skill: {metadata.name}")
    
    def _parse_metadata(self, skill_path: Path) -> Optional[SkillMetadata]:
        """
        Parse the YAML frontmatter from a SKILL.md file.
        
        Args:
            skill_path: Path to the SKILL.md file
            
        Returns:
            SkillMetadata or None if parsing fails
        """
        try:
            content = skill_path.read_text(encoding='utf-8')
            
            # Extract YAML frontmatter (between --- markers)
            frontmatter_match = re.match(
                r'^---\s*\n(.*?)\n---\s*\n',
                content,
                re.DOTALL
            )
            
            if not frontmatter_match:
                print(f"⚠️ No frontmatter in {skill_path}")
                return None
            
            frontmatter = yaml.safe_load(frontmatter_match.group(1))
            
            if not frontmatter or 'name' not in frontmatter or 'description' not in frontmatter:
                print(f"⚠️ Missing required fields in {skill_path}")
                return None
            
            return SkillMetadata(
                name=frontmatter['name'],
                description=frontmatter['description'],
                path=skill_path
            )
            
        except Exception as e:
            print(f"⚠️ Error parsing {skill_path}: {e}")
            return None
    
    def get_available_skills_xml(self) -> str:
        """
        Get all available skills as XML for prompt injection.
        This follows the AgentSkills.io format.
        """
        if not self.available_skills:
            return "<available_skills></available_skills>"
        
        skills_xml = "\n".join(
            skill.to_xml() for skill in self.available_skills.values()
        )
        
        return f"<available_skills>\n{skills_xml}\n</available_skills>"
    
    def get_skill_list(self) -> List[Dict[str, str]]:
        """Get list of available skills as dictionaries."""
        return [
            {"name": s.name, "description": s.description}
            for s in self.available_skills.values()
        ]
    
    def activate_skill(self, skill_name: str) -> Optional[str]:
        """
        Activate a skill by loading its full SKILL.md content.
        
        Args:
            skill_name: Name of the skill to activate
            
        Returns:
            Full skill content or None if not found
        """
        if skill_name in self.active_skills:
            return self.active_skills[skill_name]
        
        if skill_name not in self.available_skills:
            print(f"⚠️ Skill not found: {skill_name}")
            return None
        
        try:
            skill = self.available_skills[skill_name]
            content = skill.path.read_text(encoding='utf-8')
            
            # Remove frontmatter, keep only the body
            body_match = re.sub(
                r'^---\s*\n.*?\n---\s*\n',
                '',
                content,
                flags=re.DOTALL
            )
            
            self.active_skills[skill_name] = body_match.strip()
            print(f"✓ Activated skill: {skill_name}")
            return self.active_skills[skill_name]
            
        except Exception as e:
            print(f"⚠️ Error loading skill {skill_name}: {e}")
            return None
    
    def deactivate_skill(self, skill_name: str) -> bool:
        """
        Deactivate a skill to free up context.
        
        Args:
            skill_name: Name of the skill to deactivate
            
        Returns:
            True if deactivated, False if wasn't active
        """
        if skill_name in self.active_skills:
            del self.active_skills[skill_name]
            print(f"✓ Deactivated skill: {skill_name}")
            return True
        return False
    
    def get_active_skills_content(self) -> str:
        """
        Get the combined content of all active skills.
        This is injected into the agent's context.
        """
        if not self.active_skills:
            return ""
        
        sections = []
        for name, content in self.active_skills.items():
            sections.append(f"<active_skill name=\"{name}\">\n{content}\n</active_skill>")
        
        return "\n\n".join(sections)
    
    def list_available(self) -> List[str]:
        """Get names of all available skills."""
        return list(self.available_skills.keys())
    
    def list_active(self) -> List[str]:
        """Get names of currently active skills."""
        return list(self.active_skills.keys())
    
    def is_active(self, skill_name: str) -> bool:
        """Check if a skill is currently active."""
        return skill_name in self.active_skills
