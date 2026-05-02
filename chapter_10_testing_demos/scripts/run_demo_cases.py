import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from agentdesk_ai.agent import build_agent_response

demo_messages = [
    "Hi, I run a coaching business. I need an AI chatbot for my website. What is your pricing?",
    "I paid yesterday but my account is still not activated. This is very frustrating.",
    "Can this integrate with WhatsApp and my website?",
]

for index, message in enumerate(demo_messages, start=1):
    print(f"\nDemo Case {index}")
    print(f"Input: {message}\n")
    print(build_agent_response(message))
    print("\n" + "=" * 100)
