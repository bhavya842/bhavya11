"""
Main entry point — Mental Health Awareness & Suicide Prevention Agent
Run with: python main.py
"""
import sys
import textwrap
from agent.mental_health_agent import MentalHealthAgent
from agent.resources import GROUNDING_EXERCISES

BANNER = """
╔══════════════════════════════════════════════════════════════════════╗
║          🌿  Aria — Mental Health Support Companion  🌿              ║
║          Powered by IBM WatsonX AI (Llama 3.3 70B)                  ║
╠══════════════════════════════════════════════════════════════════════╣
║  I'm here to listen, support, and help you find resources.           ║
║  You are not alone.                                                  ║
║                                                                      ║
║  Type your message and press Enter.                                  ║
║  Commands: /help  /hotlines [country]  /breathe  /ground  /quit     ║
╚══════════════════════════════════════════════════════════════════════╝
"""

HELP_TEXT = """
Available commands:
  /help                  — Show this help message
  /hotlines              — Show international crisis hotlines
  /hotlines [country]    — Show hotlines for a specific country
                           (USA, UK, India, Australia, Canada, Germany)
  /breathe               — Box breathing grounding exercise
  /ground                — 5-4-3-2-1 sensory grounding exercise
  /tip                   — Receive a mental health tip
  /new                   — Start a new conversation session
  /quit or /exit         — Exit the program

If you are in immediate danger, please call:
  Emergency services: 911 (US) · 999 (UK) · 112 (EU)
  988 Suicide & Crisis Lifeline (US): Call or text 988
"""


def print_wrapped(text: str, width: int = 80, prefix: str = ""):
    """Pretty-print agent responses with word wrapping."""
    lines = text.split("\n")
    for line in lines:
        if len(line) > width:
            wrapped = textwrap.fill(line, width=width, subsequent_indent="  ")
            print(prefix + wrapped)
        else:
            print(prefix + line)


def handle_command(cmd: str, agent: MentalHealthAgent) -> bool:
    """
    Process slash commands.
    Returns True if the loop should continue, False to quit.
    """
    parts = cmd.strip().split()
    command = parts[0].lower()

    if command in ("/quit", "/exit"):
        print("\n🌿 Take care of yourself. Remember — help is always available.\n")
        return False

    elif command == "/help":
        print(HELP_TEXT)

    elif command == "/hotlines":
        country = parts[1].capitalize() if len(parts) > 1 else "International"
        print(agent.get_hotlines(country))

    elif command == "/breathe":
        print("\n" + GROUNDING_EXERCISES["box_breathing"] + "\n")

    elif command == "/ground":
        print("\n" + GROUNDING_EXERCISES["5-4-3-2-1"] + "\n")

    elif command == "/tip":
        import random
        from agent.resources import MENTAL_HEALTH_TIPS
        print(f"\n💚 Tip: {random.choice(MENTAL_HEALTH_TIPS)}\n")

    elif command == "/new":
        agent.reset()
        print("\n✨ New session started. How are you feeling today?\n")

    else:
        print(f"Unknown command: {command}. Type /help for available commands.")

    return True


def main():
    agent = MentalHealthAgent()
    print(BANNER)
    print("Aria: Hello. I'm Aria, your mental health companion. How are you feeling today?\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\n🌿 Take care of yourself. Goodbye.\n")
            sys.exit(0)

        if not user_input:
            continue

        # Handle slash commands
        if user_input.startswith("/"):
            should_continue = handle_command(user_input, agent)
            if not should_continue:
                break
            continue

        # Send message to agent
        print("\nAria: ", end="", flush=True)
        try:
            response = agent.respond(user_input)
            print_wrapped(response)
            print()
        except Exception as e:
            print(f"\n⚠️  I'm having trouble connecting right now. Please try again.")
            print(f"    If you are in crisis, please call 988 (US) or your local emergency line.\n")
            if "--debug" in sys.argv:
                raise e


if __name__ == "__main__":
    main()
