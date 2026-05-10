from mcp.server.fastmcp import FastMCP

from agentdesk_ai.tools import decide_escalation, score_lead, search_knowledge_base

mcp = FastMCP("agentdesk-capstone-tools")


@mcp.tool()
def rag_search(customer_message: str):
    """Search company knowledge base with embedding retrieval."""
    return search_knowledge_base(customer_message)


@mcp.tool()
def lead_score(customer_message: str):
    """Score lead quality from 1 to 10."""
    return score_lead(customer_message)


@mcp.tool()
def escalation_check(customer_message: str, lead_score_value: int):
    """Decide if case should be escalated to a human."""
    return decide_escalation(customer_message, lead_score_value)


if __name__ == "__main__":
    mcp.run()

