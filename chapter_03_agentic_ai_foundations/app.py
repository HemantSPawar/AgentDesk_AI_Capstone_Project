from agentdesk_ai.agent import build_agent_response


def main():
    print("AgentDesk AI - Chapter 03 Agentic Foundations")
    print("Type a customer message. Type 'exit' to stop.\n")

    while True:
        message = input("Customer message: ").strip()
        if message.lower() in ["exit", "quit"]:
            break
        print(build_agent_response(message))
        print("-" * 80)


if __name__ == "__main__":
    main()
