import re
import random
import datetime


class Chatbot:
    def __init__(self, name="DecodeBot"):
        self.name = name
        self.context = {}

    def greet(self):
        hour = datetime.datetime.now().hour
        period = "morning" if hour < 12 else "afternoon" if hour < 18 else "evening"
        greetings = [
            f"Good {period}! I'm {self.name}, your AI assistant.",
            f"Hey there! {self.name} at your service. Good {period}!",
            f"Hi! Welcome. I'm {self.name}. How can I help you this {period}?",
        ]
        return random.choice(greetings)

    def respond(self, user_input):
        text = user_input.strip().lower()

        if not text:
            return "Say something — I'm all ears!"

        if text in ("quit", "exit", "bye", "goodbye"):
            return random.choice([
                "Goodbye! Come back anytime.",
                "See you later!",
                "Bye! It was nice talking to you.",
            ])

        if text in ("help", "?"):
            return ("I can: chat with you, tell the time, answer basic questions, "
                    "or just keep you company. Try asking about the weather, "
                    "telling me a joke, or just say hi!")

        patterns = self._get_patterns()
        for pattern, responses in patterns:
            match = re.search(pattern, text)
            if match:
                response = random.choice(responses)
                if "{name}" in response:
                    response = response.replace("{name}", self.name)
                return self._handle_context(response, match)

        return random.choice([
            f"Hmm, I'm not sure how to answer that. Try asking differently!",
            f"Interesting! Tell me more about '{user_input.strip()}'.",
            f"I don't have a great response for that yet. What else is on your mind?",
            f"Can you rephrase that? I'm still learning!",
        ])

    def _get_patterns(self):
        return [
            (r"hi|hello|hey|howdy|sup|greetings", [
                "Hello there! How are you today?",
                "Hi! What's up?",
                "Hey! Great to see you.",
            ]),
            (r"how are you|how('s| is) it going|what('s| is) up|how do you do", [
                "I'm doing great, thanks for asking!",
                "All systems operational! How about you?",
                "Doing well! Ready to chat.",
            ]),
            (r"your name|who are you|what are you", [
                "I'm {name}, your friendly AI chatbot built with Python!",
                "They call me {name}. I'm a rule-based chatbot — no neural nets, just good old logic!",
            ]),
            (r"(time|clock|what.*time)", [
                f"The current time is {datetime.datetime.now():%I:%M %p}.",
                f"It's {datetime.datetime.now():%I:%M %p} right now!",
            ]),
            (r"(date|day|today)", [
                f"Today is {datetime.datetime.now():%A, %B %d, %Y}.",
                f"It's {datetime.datetime.now():%A, %B %d, %Y}.",
            ]),
            (r"joke|funny|laugh|humor", [
                "Why do programmers prefer dark mode? Because light attracts bugs!",
                "What do you call a AI that sings? A-tune-ated!",
                "Why was the Python interpreter so good at relationships? It didn't have any 'null' expectations!",
                "I'm reading a book on anti-gravity. It's impossible to put down!",
            ]),
            (r"weather", [
                "I can't check live weather data, but I hope it's sunny where you are!",
                "No weather API here — but I'd recommend looking out the window!",
            ]),
            (r"thank|thanks|thx", [
                "You're welcome!",
                "Happy to help!",
                "Anytime!",
            ]),
            (r"good|great|awesome|nice|amazing|fantastic", [
                "Glad to hear it!",
                "That's wonderful!",
                "Awesome! Keep that positivity going!",
            ]),
            (r"sad|bad|terrible|awful|rough|tough", [
                "Sorry to hear that. Want to talk about it?",
                "That sounds tough. I'm here to listen.",
                "Hang in there! Things will get better.",
            ]),
            (r"python|programming|code", [
                "Python is a fantastic language! Simple yet powerful.",
                "I was built with Python — it's great for AI projects like this!",
            ]),
            (r"what can you do|capabilities|features", [
                "I can hold a conversation, tell jokes, share the time/date, "
                "and respond to basic questions. All with zero external dependencies!",
            ]),
        ]

    def _handle_context(self, response, match):
        return response

    def chat_loop(self):
        print(f"\n{'='*50}")
        print(f"  {self.name} — Basic AI Chatbot")
        print(f"{'='*50}")
        print(f"\n  {self.greet()}")
        print(f"  (type 'quit' to exit, 'help' for commands)\n")

        while True:
            try:
                user_input = input("  You: ")
                response = self.respond(user_input)
                print(f"  {self.name}: {response}")

                if user_input.strip().lower() in ("quit", "exit", "bye", "goodbye"):
                    break
            except (EOFError, KeyboardInterrupt):
                print(f"\n  {self.name}: Goodbye!")
                break


if __name__ == "__main__":
    bot = Chatbot()
    bot.chat_loop()
