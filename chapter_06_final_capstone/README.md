# Chapter 6 Final Capstone (Chapters 6-13 Unified)

This capstone combines all subchapters from 6 to 13 into one enterprise-style implementation:

- Agent brain and response orchestration
- Retrieval-augmented context
- Real MCP tool execution (tool discovery + calls over protocol)
- Guardrails and escalation policy
- Lead scoring and follow-up logic
- Human handoff lifecycle with case operations
- Demo/evaluation scripts
- Bootstrap web UI for teaching and walkthroughs

## Folder Structure

- `app.py` - Flask app with Bootstrap UI
- `agentdesk_ai/agent.py` - end-to-end agent orchestration
- `agentdesk_ai/mcp_client.py` - remote MCP client flow
- `agentdesk_ai/tools.py` - tool business logic
- `agentdesk_ai/rag.py` - embeddings retrieval
- `agentdesk_ai/guardrails.py` - policy checks and escalation overrides
- `agentdesk_ai/ticketing.py` - case lifecycle engine (`AI_DECISION_COMPLETE -> CASE_CLOSED`)
- `agentdesk_ai/schema.py` - response schemas
- `templates/index.html` - Bootstrap UI
- `scripts/test_remote_mcp.py` - remote capstone test
- `scripts/run_demo_cases.py` - batch demo/eval runner

## Setup

From root folder:

```bash
pip install -r requirements.txt
```

Create/update `.env` in root:

```env
OPENAI_API_KEY=your_key_here
MODEL=gpt-4o-mini
EMBEDDING_MODEL=text-embedding-3-small
REMOTE_MCP_URL=http://127.0.0.1:3010/mcp
```

## Run Remote MCP Capstone

From chapter folder:

```bash
python scripts/test_remote_mcp.py http://127.0.0.1:3010/mcp
```

## Run Bootstrap UI

From chapter folder:

```bash
python app.py
```

Open:

- `http://127.0.0.1:5050`

## Run Demo Cases (evaluation-style output)

```bash
python scripts/run_demo_cases.py
```

This saves a report JSON inside `outputs/`.

## Notes

- This capstone is branch-safe and does not require any push to `main`.
- Retrieval uses OpenAI embeddings directly (no fallback path).
- UI now includes end-to-end ticket lifecycle controls:
  - `TICKET_CREATED`
  - `ASSIGNED_TO_HUMAN`
  - `HUMAN_ACTION_TAKEN`
  - `CUSTOMER_NOTIFIED`
  - `CASE_CLOSED`
  - `DUPLICATE`

## Deployment Guide

See:

- `DEPLOYMENT_FREE_GUIDE.md`
