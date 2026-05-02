# Chapter 06 - Agent Brain

## What This Chapter Teaches

How to use an LLM to convert internal context into a business-ready structured JSON response.

Prerequisite: complete one-time setup in `chapter_02_project_setup`.

## Which Files To Open

- `agentdesk_ai/agent.py`
- `agentdesk_ai/tools.py`
- `.env.example`

## What Command To Run

```bash
python app.py
```

## What Student Should Observe

- LLM-generated `customer_reply`.
- Structured output with intent, score, escalation, and next action.

## Common Mistakes

- Missing `OPENAI_API_KEY`.
- Expecting RAG context in this chapter (added in chapter 7 workflow integration).

## Connection To Next Chapter

Next chapter combines brain + RAG + business tools into full end-to-end orchestration.
