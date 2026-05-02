# Chapter 07 - End-to-End Workflow

## What This Chapter Teaches

How to orchestrate complete customer message handling:
- RAG lookup
- lead scoring
- escalation decision
- LLM reply generation

## Which Files To Open

- `app.py`
- `agentdesk_ai/agent.py`
- `agentdesk_ai/tools.py`
- `agentdesk_ai/rag.py`

## What Command To Run

```bash
python app.py
```

## What Student Should Observe

- Full JSON workflow output from one customer input.
- Behavior feels closer to a business-ready assistant.

## Common Mistakes

- Running without `.env` configured from `.env.example`.
- Misreading internal summary as customer-facing text.

## Connection To Next Chapter

Next chapter hardens the flow with stricter guardrails and escalation logic.
