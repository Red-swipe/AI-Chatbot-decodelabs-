### AI chatbot, decode labs internship 

def get_response(user_input, knowledge_base, fallback):
    """Look up the cleaned input in the knowledge base dictionary."""
    return knowledge_base.get(user_input, fallback)


def main():
    #knowledgebase 
    knowledge_base = {
        "hello": "Hey there! How can I help you today?",
        "hi": "Hi! What's on your mind?",
        "hey": "Hey! Good to see you.",
        "good morning": "Good morning! Hope you have a great day ahead!",
        "good evening": "Good evening! How was your day?",
        "bye": "Goodbye! Talk to you later.",
        "goodbye": "See you soon! Take care.",
        "see you": "Catch you later!",
        "take care": "You too! Stay safe.",
        "what is your name": "I'm AXIOM, your AI assistant.",
        "who are you": "I'm AXIOM — a rule-based chatbot built for Decode Labs.",
        "what are you": "I'm AXIOM, a Python chatbot that runs on pattern matching.",
        "what can you do": "I can chat with you, answer questions, give you motivation, tell you the time, and more!",
        "help": "You can ask me about the time, get motivated, say hello, or just chat. Try it out!",
        "what do you know": "I know greetings, time, motivation, and basic conversation. Type 'help' to see what I can do.",
        "how are you": "I'm functioning optimally! Thanks for asking.",
        "are you okay": "All systems green. I'm doing great!",
        "how is it going": "Going well! Ready to assist you.",
        "what time is it": "I don't have access to live time, but you can check your system clock!",
        "what day is it": "I can't fetch the current date, but your device will know!",
        "motivate me": "You've got this! Every expert was once a beginner. Keep pushing forward!",
        "inspire me": "Believe in yourself. You are capable of amazing things!",
        "i need motivation": "The only way to do great work is to love what you do. Keep going!",
        "thank you": "You're very welcome!",
        "thanks": "Anytime! Happy to help.",
        "thank you so much": "My pleasure! I'm here whenever you need me.",
        "who made you": "I was built by a Decode Labs intern as part of the AI chatbot project.",
        "who created you": "My creator is an aspiring AI engineer at Decode Labs!",
        "who built you": "I was built from scratch in Python by a Decode Labs intern.",
        "what is the weather": "I can't check weather data yet, but I hope it's sunny where you are!",
        "how is the weather": "No weather API here — look out the window for the most accurate forecast!",
    }
    fallback = "I don't understand that yet. Try asking me something else."

    #startup output 
    print("========================================")
    print("           AXIOM — v1.0")
    print("   Your rule-based AI conversation bot")
    print("  Type 'exit' or 'quit' to stop the bot")
    print("========================================")
    print()

    # loop for input 
    while True:
        raw_input = input("You: ")

        
        clean_input = raw_input.lower().strip()

       
        if clean_input in ("exit", "quit"):
            print("AXIOM: Goodbye! Have a great day.")
            break

        
        response = get_response(clean_input, knowledge_base, fallback)

        #output 
        print(f"AXIOM: {response}")


if __name__ == "__main__":
    main()
