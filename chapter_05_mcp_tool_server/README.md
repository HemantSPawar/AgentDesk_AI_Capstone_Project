# Chapter 05 - MCP Tool Server

## What This Chapter Teaches

How to expose business tools using an MCP server abstraction.

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
- Clear MCP tool definitions that wrap local Python logic.

## Common Mistakes

- Forgetting to install `mcp` dependency.
- Renaming tool functions and breaking script calls.

## Connection To Next Chapter

Next chapter introduces the LLM "brain" that uses tool context to generate polished replies.
