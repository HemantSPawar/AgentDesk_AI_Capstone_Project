# Chapter 02 - Project Setup

## What This Chapter Teaches

You complete the full one-time setup for the entire course:
- create and activate virtual environment
- install all dependencies used across chapters 2 to 13
- prepare environment variables safely
- configure real OpenAI model settings for LLM + embeddings RAG
- prepare for real MCP server integration in later chapters
- run first CLI loop to verify setup

## Which Files To Open

- `app.py`
- `agentdesk_ai/agent.py`
- `.env.example`
- `requirements.txt`

## What Command To Run

From inside `chapter_02_project_setup`:

```bash
python -m venv .venv
```

Activate environment:

```bash
# Windows PowerShell
.venv\Scripts\Activate.ps1
# macOS/Linux
source .venv/bin/activate
```

Install dependencies once for full course:

```bash
pip install -r requirements.txt
```

Create environment file:

```bash
# Windows PowerShell
Copy-Item .env.example .env
# macOS/Linux
cp .env.example .env
```

Add your `OPENAI_API_KEY` in `.env`, then run:

```bash
python app.py
```

Recommended `.env` values for this course:

```text
MODEL=gpt-4o-mini
EMBEDDING_MODEL=text-embedding-3-small
USE_MCP=false
```

Notes:
- `MODEL` is used for agent response generation.
- `EMBEDDING_MODEL` is used for semantic RAG retrieval.
- Keep `USE_MCP=false` until the MCP chapters, then switch when instructed.

## What Student Should Observe

- Terminal app starts successfully.
- Message loop accepts user input and returns a placeholder JSON response.
- No setup repetition needed in later chapters.
- Environment is ready for real OpenAI RAG and real MCP workflow in upcoming chapters.

## Common Mistakes

- Running commands outside this chapter folder.
- Skipping virtual environment activation.
- Forgetting to add `OPENAI_API_KEY` for LLM chapters.
- Leaving `EMBEDDING_MODEL` unset when running semantic RAG chapters.

## Connection To Next Chapter

Next chapter upgrades placeholder logic into an agentic loop (intent, decision, response), using this same setup.
