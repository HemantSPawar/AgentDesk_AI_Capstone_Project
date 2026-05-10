import asyncio
import os
import sys

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

DEFAULT_REMOTE_MCP_URL = "http://127.0.0.1:3005/mcp"


def _extract_text(result):
    texts = []
    for item in result.content:
        text = getattr(item, "text", None)
        if text:
            texts.append(text)
    return "\n".join(texts) if texts else str(result)


async def main():
    remote_mcp_url = sys.argv[1] if len(sys.argv) > 1 else os.getenv("REMOTE_MCP_URL", DEFAULT_REMOTE_MCP_URL)
    print(f"Connecting to remote MCP URL: {remote_mcp_url}")

    async with streamable_http_client(remote_mcp_url) as (read_stream, write_stream, _):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            tools = await session.list_tools()
            tool_names = [tool.name for tool in tools.tools]
            print("Remote MCP Tools (first 10):")
            print(tool_names[:10])

            if "echo" in tool_names:
                result = await session.call_tool("echo", {"message": "hello from AgentDesk chapter 5"})
                print("\nEcho Tool Result:")
                print(_extract_text(result))
            else:
                print("\nNo `echo` tool found on remote server. Listing only.")


if __name__ == "__main__":
    asyncio.run(main())
