# AgentDesk AI Course Project Guide

This repository is now organized as a progressive, chapter-by-chapter capstone build.

## How To Use This Course Project

1. Start at `chapter_01_intro`.
2. Complete one-time setup from the project root during `chapter_02_project_setup`.
3. Complete each chapter in order.
4. Run chapter demos from inside that chapter folder after activating the root `.venv`.
5. Do not skip forward until the current chapter behavior is clear.
6. Use `chapter_13_final_capstone` as the production-ready reference build.

## Chapter Map

1. `chapter_01_intro`: Capstone scope and learning outcome.
2. `chapter_02_project_setup`: Environment setup and first runnable CLI loop.
3. `chapter_03_agentic_ai_foundations`: Intent -> decision -> response pattern.
4. `chapter_04_rag_knowledge_base`: Add OpenAI embeddings-based semantic RAG.
5. `chapter_05_mcp_tool_server`: Expose real MCP tools for OpenAI-compatible orchestration.
6. `chapter_06_agent_brain`: Add LLM-based response synthesis.
7. `chapter_07_end_to_end_workflow`: Complete working flow with RAG + scoring + escalation.
8. `chapter_08_guardrails_escalation`: Strengthen escalation and safety behavior.
9. `chapter_09_lead_followup`: Add lead follow-up plan generation.
10. `chapter_10_testing_demos`: Add repeatable testing and demo scripts.
11. `chapter_11_product_ready_polish`: Add schema validation and safer runtime behavior.
12. `chapter_12_portfolio_packaging`: Add packaging docs and presentation assets.
13. `chapter_13_final_capstone`: Final complete capstone implementation.

## Shared Conventions

- Never commit real secrets.
- Use `.env.example` only.
- Complete setup one time from the project root during `chapter_02_project_setup`.
- After chapter 2, do not repeat environment setup in each chapter.
- Use one root `.venv` and one root `.env` for the whole course.
- Recommended Windows setup script:

```bash
.\setup_windows.ps1
```

- One-time dependency install command:

```bash
pip install -r requirements.txt
```

- Run each chapter from inside that chapter's directory.

## Suggested Student Flow

1. Read chapter README.
2. Open only the files listed in the README.
3. Run the command shown.
4. Compare behavior with expected observations.
5. Continue to next chapter.
