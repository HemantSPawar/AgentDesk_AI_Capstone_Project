def score_lead(customer_message):
    text = customer_message.lower()
    score = 3
    if any(word in text for word in ["pricing", "price", "cost", "demo", "buy", "business"]):
        score += 3
    if any(word in text for word in ["urgent", "today", "immediately", "paid", "frustrating"]):
        score += 2
    if any(word in text for word in ["enterprise", "team", "crm", "whatsapp", "integration"]):
        score += 2
    return min(score, 10)


def decide_escalation(customer_message, lead_score):
    text = customer_message.lower()
    escalation_keywords = ["paid", "refund", "angry", "frustrating", "not activated", "legal", "cancel"]
    return any(keyword in text for keyword in escalation_keywords) or lead_score >= 9
