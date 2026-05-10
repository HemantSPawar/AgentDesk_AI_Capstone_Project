from agentdesk_ai.rag import simple_rag_search


def search_knowledge_base(customer_message: str) -> dict:
    return {"tool": "search_knowledge_base", "results": simple_rag_search(customer_message)}


def score_lead(customer_message: str) -> dict:
    text = customer_message.lower()
    score = 3
    if any(word in text for word in ["pricing", "price", "cost", "demo", "buy", "business", "quote"]):
        score += 3
    if any(word in text for word in ["team", "crm", "integration", "enterprise", "api"]):
        score += 2
    if any(word in text for word in ["urgent", "today", "immediately", "decision"]):
        score += 1
    return {"tool": "score_lead", "lead_score": min(score, 10)}


def decide_escalation(customer_message: str, lead_score: int) -> dict:
    text = customer_message.lower()
    escalation_keywords = ["paid", "refund", "legal", "angry", "frustrating", "cancel", "breach", "invoice error"]
    should_escalate = any(keyword in text for keyword in escalation_keywords) or lead_score >= 9
    return {
        "tool": "decide_escalation",
        "should_escalate": should_escalate,
        "reason": "High urgency or sensitive customer issue" if should_escalate else "Safe for AI response",
    }

