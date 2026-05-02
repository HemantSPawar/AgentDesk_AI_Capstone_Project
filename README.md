# AgentDesk AI - Business Agent Capstone

A practical AI Business Agent for customer support and lead follow-up.

## What this capstone demonstrates

- Agentic AI loop: understand, decide, use tools, respond
- OpenAI embeddings-based RAG over a company knowledge base
- Real MCP tool server for reusable tools
- Lead scoring and follow-up drafting
- Human escalation and guardrails
- Structured JSON output for business workflows

## Setup

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
```

Add your API key in `.env`.

## Run without MCP first

```bash
python app.py
```

## Test MCP tools

```bash
python scripts/test_mcp_tools.py
```

## Run with MCP

In `.env`, set:

```text
USE_MCP=true
```

Then run:

```bash
python app.py
```

## Demo messages

```text
Hi, I run a coaching business. I need an AI chatbot for my website. What is your pricing?
```

```text
I paid yesterday but my account is still not activated. This is very frustrating.
```

```text
Can this integrate with WhatsApp and my website?
```
