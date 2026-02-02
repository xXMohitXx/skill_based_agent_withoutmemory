"""
Skill-Based Personal Assistant
==============================
Uses the AgentSkills.io specification for dynamic skill loading.

Run this file to start the interactive assistant.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Verify API key is set
if not os.getenv("GROQ_API_KEY"):
    print("❌ Error: GROQ_API_KEY not found in environment.")
    print("   Please create a .env file with your Groq API key.")
    sys.exit(1)

from agent.core import PersonalAssistant


def print_banner():
    """Print the welcome banner."""
    banner = """
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║   🤖  SKILL-BASED PERSONAL ASSISTANT                              ║
║                                                                   ║
║   Built with LangChain & LangGraph                                ║
║   📚 Using AgentSkills.io specification                           ║
║                                                                   ║
║   Type /help for commands or just chat naturally!                 ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
    """.strip()
    print(banner)
    print()


def format_skills_table(skill_info: dict) -> str:
    """Format skill information as a table."""
    lines = [
        "╔════════════╦════════════════════════════════════════════╦══════════╗",
        "║   Skill    ║ Description                                ║  Status  ║",
        "╠════════════╬════════════════════════════════════════════╬══════════╣",
    ]
    
    for name, info in skill_info.items():
        status = "🟢 Active" if info["active"] else "⚪ Ready"
        desc = info["description"][:40] + "..." if len(info["description"]) > 40 else info["description"]
        desc = desc.ljust(40)
        name_fmt = name.ljust(10)
        lines.append(f"║ {name_fmt} ║ {desc} ║ {status.ljust(8)} ║")
    
    lines.append("╚════════════╩════════════════════════════════════════════╩══════════╝")
    return "\n".join(lines)


def print_help():
    """Print help text."""
    help_text = """
╔═══════════════════════════════════════════════════════════════════╗
║  📖 COMMANDS                                                      ║
╠═══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║  /skills         - Show all available skills and their status     ║
║  /activate <name> - Manually activate a skill                     ║
║  /deactivate <name> - Manually deactivate a skill                 ║
║  /help           - Show this help message                         ║
║  /quit           - Exit the assistant                             ║
║                                                                   ║
║  Just type naturally to chat! Skills are activated automatically. ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
    """.strip()
    print(help_text)


def main():
    """Main entry point for the assistant."""
    print_banner()
    
    # Initialize the assistant
    print("🔧 Initializing skill-based assistant...")
    print("-" * 50)
    
    assistant = PersonalAssistant(skills_dir="skills")
    
    print("-" * 50)
    print("\n✨ Ready! Skills are loaded automatically based on your messages.\n")
    
    # Main conversation loop
    while True:
        try:
            # Get user input
            user_input = input("👤 You: ").strip()
            
            if not user_input:
                continue
            
            # Check for commands
            if user_input.startswith("/"):
                parts = user_input[1:].split(maxsplit=1)
                command = parts[0].lower()
                argument = parts[1] if len(parts) > 1 else None
                
                if command == "quit" or command == "exit":
                    print("\n👋 Goodbye! Have a great day!")
                    break
                
                elif command == "help":
                    print_help()
                
                elif command == "skills":
                    print("\n" + format_skills_table(assistant.get_skill_info()))
                
                elif command == "activate":
                    if not argument:
                        print("⚠️  Usage: /activate <skill_name>")
                        print("   Available:", ", ".join(assistant.list_available_skills()))
                    elif assistant.activate_skill(argument):
                        print(f"   Active skills: {', '.join(assistant.list_active_skills())}")
                    else:
                        print(f"⚠️  Could not activate '{argument}'")
                
                elif command == "deactivate":
                    if not argument:
                        print("⚠️  Usage: /deactivate <skill_name>")
                        print("   Active:", ", ".join(assistant.list_active_skills()))
                    elif assistant.deactivate_skill(argument):
                        active = assistant.list_active_skills()
                        if active:
                            print(f"   Active skills: {', '.join(active)}")
                        else:
                            print("   No skills active")
                    else:
                        print(f"⚠️  Skill '{argument}' is not active")
                
                else:
                    print(f"⚠️  Unknown command: /{command}")
                    print("   Type /help for available commands")
            
            else:
                # Regular conversation
                response = assistant.chat(user_input)
                
                # Show which skills are active
                active = assistant.list_active_skills()
                if active:
                    print(f"   [Skills: {', '.join(active)}]")
                
                print(f"\n🤖 Assistant: {response}\n")
        
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Have a great day!")
            break
        
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
            print("   Please try again or type /help for commands.\n")


if __name__ == "__main__":
    main()
