from agentdesk_ai.rag import simple_rag_search


def search_knowledge_base(customer_message):
    results = simple_rag_search(customer_message)
    return {
        "tool": "search_knowledge_base",
        "results": results,
    }


def score_lead(customer_message):
    text = customer_message.lower()
    score = 3
    if any(word in text for word in ["pricing", "price", "cost", "demo", "buy", "website", "business"]):
        score += 3
    if any(word in text for word in ["urgent", "today", "immediately", "paid", "frustrating"]):
        score += 2
    if any(word in text for word in ["enterprise", "team", "crm", "whatsapp", "integration"]):
        score += 2
    return {
        "tool": "score_lead",
        "lead_score": min(score, 10),
    }


def decide_escalation(customer_message, lead_score):
    text = customer_message.lower()
    escalation_keywords = [
        "paid",
        "refund",
        "angry",
        "frustrating",
        "not activated",
        "legal",
        "cancel",
        "chargeback",
        "lawsuit",
        "compliance",
        "breach",
        "urgent",
    ]
    should_escalate = any(keyword in text for keyword in escalation_keywords) or lead_score >= 8
    reason = "Guardrail triggered: urgency, payment risk, legal risk, or account access issue." if should_escalate else "Safe for AI draft response"
    return {
        "tool": "decide_escalation",
        "should_escalate": should_escalate,
        "reason": reason,
    }
