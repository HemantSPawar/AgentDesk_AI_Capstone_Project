import asyncio
import json
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

ROOT_DIR = Path(__file__).resolve().parent.parent


def _extract_text(result):
    texts = []
    for item in result.content:
        text = getattr(item, "text", None)
        if text:
            texts.append(text)
    return "\n".join(texts) if texts else str(result)


def _extract_json(result):
    text = _extract_text(result)
    try:
        return json.loads(text)
    except Exception:
        return {}


async def main():
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "agentdesk_ai.mcp_server"],
        cwd=str(ROOT_DIR),
    )

    message = "I paid yesterday but my account is still not activated. This is frustrating."

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            tools = await session.list_tools()
            tool_names = [tool.name for tool in tools.tools]
            print("MCP Tools Exposed by Server:")
            print(tool_names)

            kb = await session.call_tool("rag_search", {"customer_message": message})
            lead = await session.call_tool("lead_score", {"customer_message": message})
            lead_payload = _extract_json(lead)
            lead_score_value = int(lead_payload.get("lead_score", 0))
            escalation = await session.call_tool(
                "escalation_check",
                {
                    "customer_message": message,
                    "lead_score_value": lead_score_value,
                },
            )

            print("\nKnowledge Base Result:")
            print(_extract_text(kb))
            print("\nLead Score Result:")
            print(_extract_text(lead))
            print("\nEscalation Result:")
            print(_extract_text(escalation))


if __name__ == "__main__":
    asyncio.run(main())
