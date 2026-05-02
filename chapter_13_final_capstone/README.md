# Chapter 13 - Final Capstone

## What This Chapter Teaches

This is the final, complete AgentDesk AI implementation.

## Which Files To Open

- `app.py`
- `agentdesk_ai/agent.py`
- `agentdesk_ai/tools.py`
- `agentdesk_ai/rag.py`
- `agentdesk_ai/mcp_server.py`

## What Command To Run

```bash
pip install -r requirements.txt
python app.py
```

Optional:

```bash
python scripts/test_mcp_tools.py
```

## What Student Should Observe

- Full workflow: RAG + lead scoring + escalation + structured reply.
- Reusable MCP tools for integration-ready architecture.

## Common Mistakes

- Running without `OPENAI_API_KEY`.
- Returning free-form model text instead of JSON-compatible output.

## Connection Beyond Course

Use this folder as your base for deployment, UI integration, and portfolio demos.
