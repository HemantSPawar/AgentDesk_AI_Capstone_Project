import json
import sys
from datetime import datetime
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from agentdesk_ai.agent import run_agent

CASES = [
    "I paid yesterday but my account is still not activated. This is frustrating.",
    "We are evaluating for a 50-person team and need CRM and WhatsApp integration.",
    "Send me your pricing and setup timeline for enterprise rollout.",
]


def main():
    output_dir = Path(__file__).resolve().parent.parent / "outputs"
    output_dir.mkdir(exist_ok=True)
    report_path = output_dir / f"demo_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    report = []
    for message in CASES:
        result, trace = run_agent(message, mode="local")
        report.append(
            {
                "message": message,
                "agent_result": result.model_dump(),
                "trace": trace.model_dump(),
            }
        )

    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print(f"Saved demo report: {report_path}")


if __name__ == "__main__":
    main()
