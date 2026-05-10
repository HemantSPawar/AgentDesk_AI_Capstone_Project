from pydantic import BaseModel, Field


class GuardrailDecision(BaseModel):
    should_escalate: bool = False
    reason: str = "Safe for AI response"
    risk_flags: list[str] = Field(default_factory=list)


class AgentResponse(BaseModel):
    intent: str = Field(default="general_support")
    lead_score: int = Field(default=1, ge=1, le=10)
    customer_reply: str
    internal_summary: str
    should_escalate: bool = False
    escalation_reason: str = "Not required"
    next_action: str = "Send AI response"
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)


class TraceBundle(BaseModel):
    trace_id: str
    mode: str
    tools: dict
    guardrails: GuardrailDecision

