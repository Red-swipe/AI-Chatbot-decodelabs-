from chatbot_core import (
    get_response, init_memory, increment_conversations, log_exchange,
)


def main():
    memory = init_memory()
    name = memory.get("name")
    conv_count = memory.get("conversations", 0)

    print("=" * 40)
    print("           AXIOM — v2.0")
    print("   Your rule-based AI conversation bot")
    print("  Type 'exit' or 'quit' to stop the bot")
    print("=" * 40)
    print()

    if name:
        print(f"AXIOM: Welcome back, {name.capitalize()}! Great to see you again.")
    else:
        print("AXIOM: Welcome to AXIOM! What's your name?")

    while True:
        raw = input("You: ")

        response = get_response(raw)
        if response is None:
            print("AXIOM: Goodbye! Have a great day.")
            break

        log_exchange(raw, response)
        increment_conversations()
        print(f"AXIOM: {response}")


if __name__ == "__main__":
    main()
