import json
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from agentdesk_ai.agent import run_agent

MESSAGE = "I paid yesterday but my account is still not activated. This is frustrating."


def main():
    result, trace = run_agent(MESSAGE, mode="local")
    print("Final Agent Output:")
    print(json.dumps(result.model_dump(), indent=2))
    print("\nTrace:")
    print(json.dumps(trace.model_dump(), indent=2))


if __name__ == "__main__":
    main()
