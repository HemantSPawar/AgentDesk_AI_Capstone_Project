# Portfolio Notes - AgentDesk AI

## Project Pitch

AgentDesk AI is an AI business agent that handles customer support and lead follow-up using:
- retrieval over company policies
- lead qualification heuristics
- escalation guardrails
- structured JSON outputs for workflow automation

## Architecture Summary

1. Input arrives from CLI (`app.py`).
2. Tool layer runs:
- RAG search (`rag.py`)
- lead scoring (`tools.py`)
- escalation decision (`tools.py`)
3. Agent brain (`agent.py`) synthesizes a structured response with an LLM.
4. Optional MCP tool server (`mcp_server.py`) exposes reusable tools.

## Demo Inputs To Use

1. Pricing inquiry:
`Hi, I run a coaching business. I need an AI chatbot for my website. What is your pricing?`

2. Escalation case:
`I paid yesterday but my account is still not activated. This is very frustrating.`

3. Integration inquiry:
`Can this integrate with WhatsApp and my website?`

## Interview Talking Points

- Why structured JSON matters for CRM/helpdesk automation.
- Why escalation rules are required for risky customer scenarios.
- How this can evolve from keyword RAG to vector search in production.
