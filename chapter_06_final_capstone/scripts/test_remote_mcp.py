import json
import os
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from agentdesk_ai.agent import run_agent

MESSAGE = "Can I get enterprise pricing and CRM integration details?"


def main():
    remote_url = sys.argv[1] if len(sys.argv) > 1 else os.getenv("REMOTE_MCP_URL", "http://127.0.0.1:3010/mcp")
    result, trace = run_agent(MESSAGE, mode="remote", remote_url=remote_url)
    print("Final Agent Output:")
    print(json.dumps(result.model_dump(), indent=2))
    print("\nTrace:")
    print(json.dumps(trace.model_dump(), indent=2))


if __name__ == "__main__":
    main()
