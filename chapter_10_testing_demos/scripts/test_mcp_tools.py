import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from agentdesk_ai.tools import search_knowledge_base, score_lead, decide_escalation

message = "I paid yesterday but my account is still not activated. This is frustrating."

kb = search_knowledge_base(message)
lead = score_lead(message)
escalation = decide_escalation(message, lead["lead_score"])

print("Knowledge Base Result:")
print(kb)
print("\nLead Score Result:")
print(lead)
print("\nEscalation Result:")
print(escalation)
