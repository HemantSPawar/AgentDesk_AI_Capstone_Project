def detect_intent(customer_message):
    text = customer_message.lower()
    if any(word in text for word in ["price", "pricing", "cost"]):
        return "pricing_inquiry"
    if any(word in text for word in ["paid", "refund", "not activated", "frustrating"]):
        return "support_issue"
    if any(word in text for word in ["demo", "integrate", "integration", "whatsapp"]):
        return "product_fit_inquiry"
    return "general_question"


def score_lead(customer_message):
    text = customer_message.lower()
    score = 3
    if any(word in text for word in ["pricing", "demo", "buy", "business"]):
        score += 3
    if any(word in text for word in ["enterprise", "crm", "integration"]):
        score += 2
    return min(score, 10)


def decide_escalation(customer_message):
    text = customer_message.lower()
    escalation_keywords = ["paid", "refund", "legal", "frustrating", "angry", "cancel"]
    return any(keyword in text for keyword in escalation_keywords)
