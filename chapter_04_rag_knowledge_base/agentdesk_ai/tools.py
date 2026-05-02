from agentdesk_ai.rag import simple_rag_search


def search_knowledge_base(customer_message):
    return simple_rag_search(customer_message)


def score_lead(customer_message):
    text = customer_message.lower()
    score = 3
    if any(word in text for word in ["pricing", "demo", "buy", "business"]):
        score += 3
    return min(score, 10)


def decide_escalation(customer_message):
    text = customer_message.lower()
    escalation_keywords = ["paid", "refund", "legal", "frustrating", "angry", "cancel"]
    return any(keyword in text for keyword in escalation_keywords)
