import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from agentdesk_ai.tools import score_lead, decide_escalation

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = os.getenv("MODEL", "gpt-4o-mini")

SYSTEM_PROMPT = """
You are AgentDesk AI, a business agent for customer support and lead follow-up.
Return structured JSON only.
"""


def build_agent_response(customer_message):
    lead_score = score_lead(customer_message)
    should_escalate = decide_escalation(customer_message, lead_score)

    context = {
        "customer_message": customer_message,
        "lead_score": lead_score,
        "should_escalate": should_escalate,
        # TODO in later chapter: include knowledge-base retrieval context (RAG).
    }

    user_prompt = f"""
Generate a structured business response from this context:
{json.dumps(context, indent=2)}

Return JSON with keys:
intent, lead_score, customer_reply, internal_summary, should_escalate, escalation_reason, next_action
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
