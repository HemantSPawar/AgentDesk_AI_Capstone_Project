from flask import Flask, jsonify, render_template, request

from agentdesk_ai.agent import run_agent
from agentdesk_ai.config import settings
from agentdesk_ai.ticketing import apply_ticket_action, clear_all_tickets, create_handoff_case, get_ticket, list_tickets

app = Flask(__name__)

DEMO_SCENARIOS = {
    "activation_failure": {
        "label": "Activation Failure",
        "message": "I paid yesterday but my account is still not activated. This is frustrating.",
        "expected_path": "Escalation expected -> ticket created -> assigned to human",
    },
    "refund_complaint": {
        "label": "Refund Complaint",
        "message": "I want a refund now. Your service failed and I am very angry.",
        "expected_path": "Escalation expected -> sensitive support handling",
    },
    "enterprise_pricing": {
        "label": "Enterprise Lead",
        "message": "We are a 120-person team and need enterprise pricing with CRM and WhatsApp integration.",
        "expected_path": "High lead score expected -> follow-up + potential sales handoff",
    },
    "duplicate_case": {
        "label": "Duplicate Case",
        "message": "I paid yesterday but my account is still not activated. This is frustrating.",
        "expected_path": "Second run should auto-mark duplicate if an open similar case exists",
    },
    "legal_security": {
        "label": "Legal/Security Escalation",
        "message": "We found a potential data breach and legal notice may follow. Escalate immediately.",
        "expected_path": "Guardrail escalation expected -> urgent human handoff",
    },
}


@app.get("/")
def index():
    tickets = list_tickets(limit=25)
    return render_template(
        "index.html",
        app_name=settings.app_name,
        tickets=tickets,
        demo_scenarios=DEMO_SCENARIOS,
        remote_url=settings.remote_mcp_url,
    )


@app.post("/chat")
def chat():
    customer_message = (request.form.get("customer_message") or "").strip()
    remote_url = (request.form.get("remote_url") or "").strip() or settings.remote_mcp_url

    if not customer_message:
        return render_template(
            "index.html",
            app_name=settings.app_name,
            tickets=list_tickets(limit=25),
            demo_scenarios=DEMO_SCENARIOS,
            error="Customer message is required.",
        )

    result, trace = run_agent(customer_message=customer_message, remote_url=remote_url)
    created_ticket = None
    if result.should_escalate:
        created_ticket = create_handoff_case(customer_message, result.model_dump(), trace.trace_id)

    return render_template(
        "index.html",
        app_name=settings.app_name,
        customer_message=customer_message,
        remote_url=remote_url,
        result=result.model_dump(),
        trace=trace.model_dump(),
        tickets=list_tickets(limit=25),
        demo_scenarios=DEMO_SCENARIOS,
        selected_ticket=created_ticket,
        expected_path=(request.form.get("expected_path") or "").strip(),
    )


@app.post("/api/chat")
def api_chat():
    payload = request.get_json(silent=True) or {}
    customer_message = (payload.get("customer_message") or "").strip()
    remote_url = (payload.get("remote_url") or "").strip() or settings.remote_mcp_url
    expected_path = (payload.get("expected_path") or "").strip()

    if not customer_message:
        return jsonify({"ok": False, "error": "Customer message is required."}), 400

    result, trace = run_agent(customer_message=customer_message, remote_url=remote_url)
    created_ticket = None
    if result.should_escalate:
        created_ticket = create_handoff_case(customer_message, result.model_dump(), trace.trace_id)

    return jsonify(
        {
            "ok": True,
            "customer_message": customer_message,
            "expected_path": expected_path,
            "result": result.model_dump(),
            "trace": trace.model_dump(),
            "selected_ticket": created_ticket,
            "tickets": list_tickets(limit=25),
        }
    )


@app.post("/ticket/action")
def ticket_action():
    ticket_id = (request.form.get("ticket_id") or "").strip()
    action = (request.form.get("action") or "").strip()
    note = (request.form.get("note") or "").strip()
    duplicate_of = (request.form.get("duplicate_of") or "").strip()
    selected_ticket = apply_ticket_action(ticket_id=ticket_id, action=action, note=note, duplicate_of=duplicate_of)

    return render_template(
        "index.html",
        app_name=settings.app_name,
        tickets=list_tickets(limit=25),
        demo_scenarios=DEMO_SCENARIOS,
        selected_ticket=selected_ticket or get_ticket(ticket_id),
        success=f"Action '{action}' applied to {ticket_id}" if selected_ticket else f"No changes applied for {ticket_id}",
    )


@app.post("/ticket/clear")
def ticket_clear():
    clear_all_tickets()
    return render_template(
        "index.html",
        app_name=settings.app_name,
        tickets=list_tickets(limit=25),
        demo_scenarios=DEMO_SCENARIOS,
        remote_url=settings.remote_mcp_url,
        success="All ticket data cleared.",
    )


if __name__ == "__main__":
    app.run(debug=True, port=5050)
