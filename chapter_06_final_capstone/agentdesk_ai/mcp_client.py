import asyncio
import json
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.streamable_http import streamable_http_client

from agentdesk_ai.config import settings

ROOT_DIR = Path(__file__).resolve().parent.parent


def _extract_text(result) -> str:
    texts = []
    for item in result.content:
        text = getattr(item, "text", None)
        if text:
            texts.append(text)
    return "\n".join(texts) if texts else str(result)


def _extract_json(result) -> dict:
    try:
        return json.loads(_extract_text(result))
    except Exception:
        return {}


async def _call_local_mcp(customer_message: str) -> dict:
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "agentdesk_ai.mcp_server"],
        cwd=str(ROOT_DIR),
    )
    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            tools = await session.list_tools()
            tool_names = [tool.name for tool in tools.tools]
            kb = await session.call_tool("rag_search", {"customer_message": customer_message})
            lead = await session.call_tool("lead_score", {"customer_message": customer_message})
            lead_payload = _extract_json(lead)
            lead_score_value = int(lead_payload.get("lead_score", 1))
            esc = await session.call_tool(
                "escalation_check",
                {"customer_message": customer_message, "lead_score_value": lead_score_value},
            )
            return {
                "knowledge_base": _extract_json(kb),
                "lead_score": _extract_json(lead),
                "escalation": _extract_json(esc),
                "tools_disclosed": tool_names,
                "mode": "real_mcp_stdio",
            }


async def _call_remote_mcp(customer_message: str, remote_url: str) -> dict:
    async with streamable_http_client(remote_url) as (read_stream, write_stream, _):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            tools = await session.list_tools()
            tool_names = {tool.name for tool in tools.tools}
            response = {"mode": "remote_mcp_http", "remote_url": remote_url, "remote_tools": sorted(tool_names)}

            if {"rag_search", "lead_score", "escalation_check"}.issubset(tool_names):
                kb = await session.call_tool("rag_search", {"customer_message": customer_message})
                lead = await session.call_tool("lead_score", {"customer_message": customer_message})
                lead_payload = _extract_json(lead)
                lead_score_value = int(lead_payload.get("lead_score", 1))
                esc = await session.call_tool(
                    "escalation_check",
                    {"customer_message": customer_message, "lead_score_value": lead_score_value},
                )
                response.update(
                    {
                        "knowledge_base": _extract_json(kb),
                        "lead_score": _extract_json(lead),
                        "escalation": _extract_json(esc),
                    }
                )
            else:
                response["note"] = "Remote server does not expose capstone tools; discovery-only mode."
            return response


def call_capstone_tools(customer_message: str, mode: str, remote_url: str | None = None) -> dict:
    if mode == "remote":
        return asyncio.run(_call_remote_mcp(customer_message, remote_url or settings.remote_mcp_url))
    return asyncio.run(_call_local_mcp(customer_message))
