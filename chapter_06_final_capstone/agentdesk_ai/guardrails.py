from agentdesk_ai.schema import GuardrailDecision


def evaluate_guardrails(customer_message: str, tool_escalation: dict) -> GuardrailDecision:
    text = customer_message.lower()
    flags: list[str] = []

    if any(token in text for token in ["password", "otp", "credit card", "ssn", "cvv"]):
        flags.append("sensitive_information")
    if any(token in text for token in ["lawsuit", "legal notice", "regulator"]):
        flags.append("legal_risk")
    if any(token in text for token in ["hack", "breach", "data leak"]):
        flags.append("security_risk")

    should_escalate = bool(flags) or bool(tool_escalation.get("should_escalate", False))
    if flags:
        reason = f"Policy escalation due to: {', '.join(flags)}"
    else:
        reason = tool_escalation.get("reason", "Safe for AI response")

    return GuardrailDecision(should_escalate=should_escalate, reason=reason, risk_flags=flags)

