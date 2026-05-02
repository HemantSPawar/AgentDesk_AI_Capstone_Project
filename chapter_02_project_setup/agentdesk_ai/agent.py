import json


def build_agent_response(customer_message):
    # TODO in later chapter: add intent detection, lead scoring, and escalation logic.
    payload = {
        "intent": "unknown",
        "lead_score": 1,
        "customer_reply": f"Thanks for your message: '{customer_message}'.",
        "internal_summary": "Project setup chapter placeholder response.",
        "should_escalate": False,
        "escalation_reason": "Not implemented yet.",
        "next_action": "Continue to chapter 03.",
    }
    return json.dumps(payload, indent=2)
