import json

from agentdesk_ai.tools import search_knowledge_base, score_lead, decide_escalation


def build_agent_response(customer_message):
    kb_results = search_knowledge_base(customer_message)
    lead_score = score_lead(customer_message)
    should_escalate = decide_escalation(customer_message)

    # TODO in later chapter: replace this deterministic reply with LLM synthesis.
    reply = "Thanks for your message. Based on our policy, here is what we can do next."

    payload = {
        "intent": "kb_grounded_response",
        "lead_score": lead_score,
        "customer_reply": reply,
        "internal_summary": f"Top KB hits: {[doc['title'] for doc in kb_results]}",
        "should_escalate": should_escalate,
        "escalation_reason": "Sensitive issue detected." if should_escalate else "No escalation needed.",
        "next_action": "Move to MCP tool server chapter.",
    }
    return json.dumps(payload, indent=2)
