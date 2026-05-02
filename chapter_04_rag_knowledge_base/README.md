# Chapter 04 - RAG Knowledge Base

## What This Chapter Teaches

How to connect a company knowledge base and return grounded context using simple retrieval.

## Which Files To Open

- `agentdesk_ai/rag.py`
- `agentdesk_ai/tools.py`
- `data/company_knowledge_base.json`
- `app.py`

## What Command To Run

```bash
python app.py
```

## What Student Should Observe

- Replies now reference KB results.
- Retrieval chooses top matching entries by keyword overlap.

## Common Mistakes

- Editing KB JSON into invalid format.
- Confusing keyword RAG with embedding/vector RAG.

## Connection To Next Chapter

Next chapter exposes tools through an MCP server so external agent clients can call them.
