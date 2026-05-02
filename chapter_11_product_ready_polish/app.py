from agentdesk_ai.agent import build_agent_response


def main():
    print("AgentDesk AI - Business Agent")
    print("Type a customer message. Type 'exit' to stop.\n")

    while True:
        message = input("Customer message: ")
        if message.lower().strip() in ["exit", "quit"]:
            break
        result = build_agent_response(message)
        print("\nAgent Output:\n")
        print(result)
        print("\n" + "-" * 80 + "\n")


if __name__ == "__main__":
    main()
