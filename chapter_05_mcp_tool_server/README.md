# Chapter 05 - MCP Tool Server

## What This Chapter Teaches

How to expose business tools using a real MCP server that can be integrated into OpenAI-driven agent workflows.

Prerequisite: complete one-time setup in `chapter_02_project_setup`.

## Which Files To Open

- `agentdesk_ai/mcp_server.py`
- `agentdesk_ai/tools.py`
- `scripts/test_mcp_tools.py`

## What Command To Run

```bash
python scripts/test_mcp_tools.py
```

## What Student Should Observe

- Tool outputs for RAG search, lead scoring, and escalation checks.
- Clear MCP tool definitions ready for real model orchestration.

## Common Mistakes

- Skipping chapter 2 setup and missing dependencies in the environment.
- Renaming tool functions and breaking script calls.

## Connection To Next Chapter

Next chapter introduces the LLM "brain" that uses tool context to generate polished replies.
