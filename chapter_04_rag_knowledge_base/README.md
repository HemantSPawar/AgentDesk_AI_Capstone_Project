# Chapter 04 - RAG Knowledge Base

## What This Chapter Teaches

How to connect a company knowledge base and return grounded context using OpenAI embeddings-based semantic retrieval.

Prerequisite: complete one-time setup in `chapter_02_project_setup`.

## Which Files To Open

- `agentdesk_ai/rag.py`
- `agentdesk_ai/tools.py`
- `data/company_knowledge_base.json`
- `app.py`

## What Command To Run

```bash
python app.py
```

## Reliability Note (Training Mode)

- If embedding calls fail, or `OPENAI_API_KEY` is missing, the code enters fallback mode.
- Fallback uses `_keyword_fallback`, which counts query-word overlap with each document and returns top results deterministically.
- This means students can still run the chapter offline (or without a key) and observe retrieval behavior.
- If you want to run actual embeddings:
  1. Go to your OpenAI developer account.
  2. Create an API key.
  3. Add it to your `.env` file as `OPENAI_API_KEY`.
  4. Run this chapter again.
- For `OPENAI_API_KEY` setup details, refer to this Chapter 4 `README.md`.
- For now, we are not entering any key and will depend on fallback for training purposes. It still returns RAG-like behavior so you can observe the result.

## What Student Should Observe

- Replies now reference KB results.
- Retrieval chooses top matching entries by semantic similarity.

## Common Mistakes

- Editing KB JSON into invalid format.
- Forgetting `OPENAI_API_KEY`, causing fallback retrieval behavior.

## Connection To Next Chapter

Next chapter exposes tools through an MCP server so external agent clients can call them.
