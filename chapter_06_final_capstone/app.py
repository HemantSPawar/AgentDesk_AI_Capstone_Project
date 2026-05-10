from flask import Flask, render_template, request

from agentdesk_ai.agent import run_agent
from agentdesk_ai.config import settings
from agentdesk_ai.ticketing import apply_ticket_action, create_handoff_case, get_ticket, list_tickets

app = Flask(__name__)


@app.get("/")
def index():
    tickets = list_tickets(limit=25)
    return render_template("index.html", app_name=settings.app_name, tickets=tickets)


@app.post("/chat")
def chat():
    customer_message = (request.form.get("customer_message") or "").strip()

    if not customer_message:
        return render_template(
            "index.html",
            app_name=settings.app_name,
            tickets=list_tickets(limit=25),
            error="Customer message is required.",
        )

    result, trace = run_agent(customer_message=customer_message, mode="local")
    created_ticket = None
    if result.should_escalate:
        created_ticket = create_handoff_case(customer_message, result.model_dump(), trace.trace_id)

    return render_template(
        "index.html",
        app_name=settings.app_name,
        customer_message=customer_message,
        result=result.model_dump(),
        trace=trace.model_dump(),
        tickets=list_tickets(limit=25),
        selected_ticket=created_ticket,
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
        selected_ticket=selected_ticket or get_ticket(ticket_id),
        success=f"Action '{action}' applied to {ticket_id}" if selected_ticket else f"No changes applied for {ticket_id}",
    )


if __name__ == "__main__":
    app.run(debug=True, port=5050)
