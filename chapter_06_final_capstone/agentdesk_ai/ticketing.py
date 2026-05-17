import json
from datetime import datetime, timezone
from pathlib import Path

from agentdesk_ai.config import BASE_DIR

TICKET_STORE = BASE_DIR / "data" / "tickets.json"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _ensure_store() -> None:
    if not TICKET_STORE.exists():
        TICKET_STORE.parent.mkdir(parents=True, exist_ok=True)
        with open(TICKET_STORE, "w", encoding="utf-8") as f:
            json.dump({"counter": 0, "tickets": []}, f, indent=2)


def _load_store() -> dict:
    _ensure_store()
    with open(TICKET_STORE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_store(data: dict) -> None:
    with open(TICKET_STORE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def _event(step: str, note: str, actor: str) -> dict:
    return {"step": step, "note": note, "actor": actor, "ts": _now_iso()}


def _next_ticket_id(data: dict) -> str:
    data["counter"] += 1
    today = datetime.now().strftime("%Y%m%d")
    return f"CASE-{today}-{data['counter']:04d}"


def _normalize_message(text: str) -> str:
    return " ".join(text.lower().split())


def list_tickets(limit: int = 20) -> list[dict]:
    data = _load_store()
    return list(reversed(data["tickets"]))[:limit]


def get_ticket(ticket_id: str) -> dict | None:
    data = _load_store()
    for ticket in data["tickets"]:
        if ticket["ticket_id"] == ticket_id:
            return ticket
    return None


def _find_duplicate_open_case(data: dict, customer_message: str) -> str | None:
    normalized = _normalize_message(customer_message)
    for ticket in reversed(data["tickets"]):
        if ticket.get("normalized_message") == normalized and ticket.get("status") not in {"CASE_CLOSED", "DUPLICATE"}:
            return ticket["ticket_id"]
    return None


def create_handoff_case(customer_message: str, agent_result: dict, trace_id: str) -> dict:
    data = _load_store()
    duplicate_of = _find_duplicate_open_case(data, customer_message)
    ticket_id = _next_ticket_id(data)

    status = "DUPLICATE" if duplicate_of else "TICKET_CREATED"
    timeline = [
        _event("AI_DECISION_COMPLETE", f"AI marked escalation=True for trace {trace_id}", "ai_agent"),
    ]
    if duplicate_of:
        timeline.append(_event("DUPLICATE", f"Marked as duplicate of {duplicate_of}", "workflow_engine"))
    else:
        timeline.append(_event("TICKET_CREATED", "Case created in human support queue", "workflow_engine"))
        timeline.append(_event("ASSIGNED_TO_HUMAN", "Assigned to L2 support queue", "workflow_engine"))
        status = "ASSIGNED_TO_HUMAN"

    ticket = {
        "ticket_id": ticket_id,
        "status": status,
        "created_at": _now_iso(),
        "updated_at": _now_iso(),
        "customer_message": customer_message,
        "normalized_message": _normalize_message(customer_message),
        "intent": agent_result.get("intent"),
        "lead_score": agent_result.get("lead_score"),
        "escalation_reason": agent_result.get("escalation_reason"),
        "next_action": agent_result.get("next_action"),
        "duplicate_of": duplicate_of,
        "assignee": "L2_SUPPORT_QUEUE" if not duplicate_of else None,
        "timeline": timeline,
    }
    data["tickets"].append(ticket)
    _save_store(data)
    return ticket


def apply_ticket_action(ticket_id: str, action: str, note: str = "", duplicate_of: str = "") -> dict | None:
    data = _load_store()
    for ticket in data["tickets"]:
        if ticket["ticket_id"] != ticket_id:
            continue

        if action == "human_action":
            ticket["status"] = "HUMAN_ACTION_TAKEN"
            ticket["timeline"].append(_event("HUMAN_ACTION_TAKEN", note or "Human triage completed", "human_agent"))
        elif action == "notify_customer":
            ticket["status"] = "CUSTOMER_NOTIFIED"
            ticket["timeline"].append(_event("CUSTOMER_NOTIFIED", note or "Customer notified with update", "human_agent"))
        elif action == "close_case":
            ticket["status"] = "CASE_CLOSED"
            ticket["timeline"].append(_event("CASE_CLOSED", note or "Case closed after resolution", "human_agent"))
        elif action == "mark_duplicate":
            ticket["status"] = "DUPLICATE"
            ticket["duplicate_of"] = duplicate_of or ticket.get("duplicate_of")
            ticket["timeline"].append(
                _event("DUPLICATE", note or f"Marked duplicate of {ticket.get('duplicate_of', 'another case')}", "human_agent")
            )
        else:
            return ticket

        ticket["updated_at"] = _now_iso()
        _save_store(data)
        return ticket
    return None


def clear_all_tickets() -> None:
    _save_store({"counter": 0, "tickets": []})
