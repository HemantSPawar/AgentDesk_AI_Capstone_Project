from mcp.server.fastmcp import FastMCP
from agentdesk_ai.tools import search_knowledge_base, score_lead, decide_escalation

mcp = FastMCP("agentdesk-tools")


@mcp.tool()
def rag_search(customer_message: str):
    """Search AgentDesk company knowledge base."""
    return search_knowledge_base(customer_message)


@mcp.tool()
def lead_score(customer_message: str):
    """Score a customer lead from 1 to 10."""
    return score_lead(customer_message)


@mcp.tool()
def escalation_check(customer_message: str, lead_score_value: int):
    """Decide whether the customer case needs human escalation."""
    return decide_escalation(customer_message, lead_score_value)


if __name__ == "__main__":
    mcp.run()
