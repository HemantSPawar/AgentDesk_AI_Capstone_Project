import json

from agentdesk_ai.tools import detect_intent, score_lead, decide_escalation


def build_agent_response(customer_message):
    intent = detect_intent(customer_message)
    lead_score = score_lead(customer_message)
    should_escalate = decide_escalation(customer_message)

    payload = {
        "intent": intent,
        "lead_score": lead_score,
        "customer_reply": "Thanks for reaching out. We will help you with this request.",
        "internal_summary": "Deterministic agent loop with rules only.",
        "should_escalate": should_escalate,
        "escalation_reason": "Sensitive issue detected." if should_escalate else "No escalation needed.",
        "next_action": "Move to RAG chapter for knowledge grounding.",
    }
    return json.dumps(payload, indent=2)
