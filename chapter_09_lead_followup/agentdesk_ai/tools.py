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
    escalation_keywords = ["paid", "refund", "angry", "frustrating", "not activated", "legal", "cancel"]
    should_escalate = any(keyword in text for keyword in escalation_keywords) or lead_score >= 9
    reason = "High urgency or sensitive customer issue" if should_escalate else "Safe for AI draft response"
    return {
        "tool": "decide_escalation",
        "should_escalate": should_escalate,
        "reason": reason,
    }


def draft_follow_up(customer_message, lead_score, should_escalate):
    if should_escalate:
        return {
            "cadence": "Immediate human handoff",
            "owner": "Support specialist",
            "next_step": "Collect payment email and transaction ID; resolve and confirm by email.",
        }

    text = customer_message.lower()
    if lead_score >= 7:
        return {
            "cadence": "Within 24 hours",
            "owner": "Sales rep",
            "next_step": "Invite to 30-minute demo and collect company size, use case, and preferred channel.",
        }

    if "pricing" in text or "cost" in text:
        return {
            "cadence": "Within 1 business day",
            "owner": "Inside sales",
            "next_step": "Share plan options and qualify expected monthly conversation volume.",
        }

    return {
        "cadence": "No follow-up needed",
        "owner": "AI assistant",
        "next_step": "Close with helpful response and wait for next customer message.",
    }
