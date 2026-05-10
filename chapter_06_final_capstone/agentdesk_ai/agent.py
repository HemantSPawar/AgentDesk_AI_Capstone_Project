import json
import uuid

from openai import OpenAI
from pydantic import ValidationError

from agentdesk_ai.config import settings
from agentdesk_ai.guardrails import evaluate_guardrails
from agentdesk_ai.mcp_client import call_capstone_tools
from agentdesk_ai.schema import AgentResponse, TraceBundle

SYSTEM_PROMPT = """
You are AgentDesk AI, an enterprise support and lead-follow-up assistant.
Return valid JSON only with keys:
intent, lead_score, customer_reply, internal_summary, should_escalate, escalation_reason, next_action, confidence.

Rules:
- Never invent pricing or policy facts.
- Use provided tool context.
- If issue is sensitive or risky, prefer escalation.
- Keep reply polite, concise, and actionable.
"""


def _fallback_response(customer_message: str, lead_score: int, escalate: bool, reason: str) -> AgentResponse:
    return AgentResponse(
        intent="customer_support",
        lead_score=lead_score,
        customer_reply=(
            "Thanks for reaching out. We reviewed your request and will help you promptly. "
            "A support specialist will follow up where needed."
        ),
        internal_summary=f"Fallback response used for message: {customer_message[:120]}",
        should_escalate=escalate,
        escalation_reason=reason if escalate else "No policy escalation required",
        next_action="Escalate to human queue" if escalate else "Send AI response and monitor",
        confidence=0.55,
    )


def _generate_llm_response(customer_message: str, tools_payload: dict, escalate: bool, reason: str) -> AgentResponse:
    client = OpenAI(api_key=settings.openai_api_key)
    user_prompt = f"""
Customer message:
{customer_message}

Tool payload:
{json.dumps(tools_payload, indent=2)}

Policy escalation:
{json.dumps({"should_escalate": escalate, "reason": reason}, indent=2)}

Return JSON only.
"""
    response = client.chat.completions.create(
        model=settings.model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
    )
    raw = (response.choices[0].message.content or "{}").strip()
    if raw.startswith("```"):
        raw = raw.replace("```json", "").replace("```", "").strip()
    if "{" in raw and "}" in raw and not raw.strip().startswith("{"):
        raw = raw[raw.find("{") : raw.rfind("}") + 1]
    parsed = AgentResponse.model_validate_json(raw)
    return parsed


def run_agent(customer_message: str, remote_url: str | None = None) -> tuple[AgentResponse, TraceBundle]:
    trace_id = str(uuid.uuid4())
    try:
        tools_payload = call_capstone_tools(customer_message, remote_url=remote_url)
    except Exception as exc:
        tools_payload = {
            "mode": "remote_degraded",
            "knowledge_base": {"tool": "search_knowledge_base", "results": []},
            "lead_score": {"tool": "score_lead", "lead_score": 1},
            "escalation": {
                "tool": "decide_escalation",
                "should_escalate": True,
                "reason": f"Tooling failure: {type(exc).__name__}",
            },
            "error": str(exc),
        }

    lead_score = int(tools_payload.get("lead_score", {}).get("lead_score", 1))
    escalation_payload = tools_payload.get("escalation", {})
    guardrail_decision = evaluate_guardrails(customer_message, escalation_payload)

    try:
        if not settings.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY missing for LLM generation")
        agent_response = _generate_llm_response(
            customer_message=customer_message,
            tools_payload=tools_payload,
            escalate=guardrail_decision.should_escalate,
            reason=guardrail_decision.reason,
        )
    except (ValidationError, RuntimeError, Exception):
        agent_response = _fallback_response(
            customer_message=customer_message,
            lead_score=lead_score,
            escalate=guardrail_decision.should_escalate,
            reason=guardrail_decision.reason,
        )

    if guardrail_decision.should_escalate:
        agent_response.should_escalate = True
        agent_response.escalation_reason = guardrail_decision.reason
        agent_response.next_action = "Escalate to human queue"

    trace = TraceBundle(
        trace_id=trace_id,
        mode=tools_payload.get("mode", "remote_mcp_http"),
        tools=tools_payload,
        guardrails=guardrail_decision,
    )
    return agent_response, trace
