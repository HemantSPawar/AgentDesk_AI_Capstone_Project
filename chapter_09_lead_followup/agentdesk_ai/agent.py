import json
import os
from dotenv import load_dotenv
from openai import OpenAI

from agentdesk_ai.tools import search_knowledge_base, score_lead, decide_escalation, draft_follow_up

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = os.getenv("MODEL", "gpt-4o-mini")

SYSTEM_PROMPT = """
You are AgentDesk AI, a business agent for customer support and lead follow-up.
Your job:
1. Understand customer intent.
2. Use company knowledge.
3. Draft a helpful customer reply.
4. Score the lead from 1 to 10.
5. Decide whether human escalation is required.
6. Return structured JSON only.

Safety rules:
- Do not invent pricing numbers not present in the knowledge base.
- Escalate payment, refund, legal, account access, and angry customer issues.
- Keep the customer reply polite, clear, and business-friendly.
"""


def build_agent_response(customer_message):
    kb_result = search_knowledge_base(customer_message)
    lead_result = score_lead(customer_message)
    escalation_result = decide_escalation(customer_message, lead_result["lead_score"])
    follow_up_result = draft_follow_up(
        customer_message,
        lead_result["lead_score"],
        escalation_result["should_escalate"],
    )

    context = {
        "customer_message": customer_message,
        "knowledge_base_results": kb_result["results"],
        "lead_score": lead_result["lead_score"],
        "escalation": escalation_result,
        "follow_up_plan": follow_up_result,
    }

    user_prompt = f"""
Analyze this customer message and produce a final AgentDesk AI response.

Context:
{json.dumps(context, indent=2)}

Return JSON with these keys:
- intent
- lead_score
- customer_reply
- internal_summary
- should_escalate
- escalation_reason
- next_action
- lead_followup_plan
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content
