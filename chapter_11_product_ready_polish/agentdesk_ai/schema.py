from pydantic import BaseModel, Field


class AgentResponse(BaseModel):
    intent: str = Field(default="general_question")
    lead_score: int = Field(default=1, ge=1, le=10)
    customer_reply: str
    internal_summary: str
    should_escalate: bool = False
    escalation_reason: str
    next_action: str
