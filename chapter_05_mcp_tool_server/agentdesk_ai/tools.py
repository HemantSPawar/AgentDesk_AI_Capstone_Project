from agentdesk_ai.rag import simple_rag_search


def search_knowledge_base(customer_message):
    return {
        "tool": "search_knowledge_base",
        "results": simple_rag_search(customer_message),
    }


def score_lead(customer_message):
    text = customer_message.lower()
    score = 3
    if any(word in text for word in ["pricing", "demo", "buy", "business", "website"]):
        score += 3
    if any(word in text for word in ["enterprise", "crm", "whatsapp", "integration"]):
        score += 2
    return {"tool": "score_lead", "lead_score": min(score, 10)}


def decide_escalation(customer_message, lead_score):
    text = customer_message.lower()
    escalation_keywords = ["paid", "refund", "legal", "frustrating", "angry", "cancel"]
    should_escalate = any(keyword in text for keyword in escalation_keywords) or lead_score >= 9
    return {
        "tool": "decide_escalation",
        "should_escalate": should_escalate,
        "reason": "High urgency or sensitive customer issue" if should_escalate else "Safe for AI draft response",
    }
