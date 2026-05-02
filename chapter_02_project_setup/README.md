# Chapter 02 - Project Setup

## What This Chapter Teaches

You complete the full one-time setup for the entire course:
- install Python on Windows
- create and activate virtual environment
- install all dependencies used across chapters 2 to 13
- prepare environment variables safely
- configure real OpenAI model settings for LLM + embeddings RAG
- prepare for real MCP server integration in later chapters
- run first CLI loop to verify setup

## Which Files To Open

- `app.py`
- `agentdesk_ai/agent.py`
- root `.env.example`
- root `requirements.txt`

## What Command To Run

Recommended one-command Windows setup from the project root:

```bash
.\setup_windows.ps1
```

If PowerShell blocks the script, run:

```bash
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\setup_windows.ps1
```

If Python is installed by the script, close and reopen the terminal, then run `.\setup_windows.ps1` again.

Alternative Python installer method:
- Go to `https://www.python.org/downloads/`
- Download the latest Python installer
- Select `Add Python to PATH`
- Click `Install Now`

Manual setup commands, if you do not use the script:

```bash
winget install --id Python.Python.3.14 -e
```

Close and reopen the terminal, then verify Python:

```bash
python --version
```

Run the project setup commands from the project root, not inside each chapter folder:

```bash
cd "D:\Nexient\Projects\AgentDeskAI\AgentDesk_AI_Capstone_Project"
```

Create one shared virtual environment:

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
python -m pip install --upgrade pip
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
cd chapter_02_project_setup
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
- One `.venv` and one `.env` at the project root are reused by later chapters.
- Environment is ready for real OpenAI RAG and real MCP workflow in upcoming chapters.

## Common Mistakes

- Creating `.venv` separately inside every chapter folder.
- Creating `.env` separately inside every chapter folder.
- Forgetting to reopen terminal after installing Python.
- Forgetting to add Python to PATH when using the installer.
- Skipping virtual environment activation.
- Forgetting to add `OPENAI_API_KEY` for LLM chapters.
- Leaving `EMBEDDING_MODEL` unset when running semantic RAG chapters.

## Connection To Next Chapter

Next chapter upgrades placeholder logic into an agentic loop (intent, decision, response), using this same setup.
