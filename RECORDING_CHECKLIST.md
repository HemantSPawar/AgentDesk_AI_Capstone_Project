# Recording Checklist (Instructor)

Use this checklist while recording each chapter lesson.

## Global Recording Rules

- Show chapter folder path before coding.
- Keep terminal focused on current chapter folder.
- Use `.env.example`, never a real `.env` with live keys.
- Do complete setup only once in chapter 2; do not repeat setup in later chapters.
- Hide private files, OneDrive folders, browser tabs, and unrelated project directories.
- Do not show hidden system files.

## Chapter-by-Chapter Run List

1. `chapter_01_intro`
- Show: `README.md`
- Run: no command
- Expect: clear course goal and roadmap
- Do not show: unrelated project files

2. `chapter_02_project_setup`
- Show: `README.md`, `app.py`
- Run: `python -m venv .venv`, activate env, `pip install -r requirements.txt`, create `.env`, then `python app.py`
- Expect: setup complete message loop
- Do not show: any real API keys

3. `chapter_03_agentic_ai_foundations`
- Show: `agentdesk_ai/agent.py`, `agentdesk_ai/tools.py`
- Run: `python app.py`
- Expect: structured JSON from deterministic logic
- Do not show: future chapter files

4. `chapter_04_rag_knowledge_base`
- Show: `agentdesk_ai/rag.py`, `data/company_knowledge_base.json`
- Run: `python app.py`
- Expect: KB-grounded reply behavior
- Do not show: MCP server yet

5. `chapter_05_mcp_tool_server`
- Show: `agentdesk_ai/mcp_server.py`, `scripts/test_mcp_tools.py`
- Run: `python scripts/test_mcp_tools.py`
- Expect: tool outputs for RAG/lead/escalation
- Do not show: final production polish files

6. `chapter_06_agent_brain`
- Show: `agentdesk_ai/agent.py`, `.env.example`
- Run: `python app.py`
- Expect: LLM-generated structured response
- Do not show: real `.env`

7. `chapter_07_end_to_end_workflow`
- Show: `agentdesk_ai/agent.py`, `agentdesk_ai/tools.py`
- Run: `python app.py`
- Expect: end-to-end orchestrated output
- Do not show: hidden files

8. `chapter_08_guardrails_escalation`
- Show: `agentdesk_ai/tools.py`, `agentdesk_ai/agent.py`
- Run: `python app.py`
- Expect: stronger escalation behavior on risky messages
- Do not show: unrelated datasets

9. `chapter_09_lead_followup`
- Show: `agentdesk_ai/tools.py`, `agentdesk_ai/agent.py`
- Run: `python app.py`
- Expect: lead follow-up plan in output
- Do not show: private notes

10. `chapter_10_testing_demos`
- Show: `scripts/test_mcp_tools.py`, `scripts/run_demo_cases.py`
- Run: `python scripts/run_demo_cases.py`
- Expect: repeatable demo outputs
- Do not show: local machine secrets or tokens

11. `chapter_11_product_ready_polish`
- Show: `agentdesk_ai/schema.py`, `agentdesk_ai/agent.py`
- Run: `python app.py`
- Expect: validated, stable JSON response format
- Do not show: stack traces with sensitive paths

12. `chapter_12_portfolio_packaging`
- Show: `README.md`, `PORTFOLIO_NOTES.md`
- Run: `python app.py`
- Expect: polished project narrative + working demo
- Do not show: draft-only or personal files

13. `chapter_13_final_capstone`
- Show: full final flow
- Run: `python app.py`
- Expect: complete capstone behavior
- Do not show: real secrets, hidden files, unrelated folders
