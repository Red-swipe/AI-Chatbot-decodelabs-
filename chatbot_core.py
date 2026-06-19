import string
import os
import re
import operator
from datetime import datetime

MEMORY_FILE = "memory.txt"
LOG_FILE = "conversation_log.txt"

NAME_PATTERNS = ["my name is", "call me", "you can call me"]

MOTIVATIONAL_QUOTES = [
    "You've got this! Every expert was once a beginner. Keep pushing forward!",
    "Believe in yourself. You are capable of amazing things!",
    "The only way to do great work is to love what you do. Keep going!",
    "Success is not final, failure is not fatal — it's the courage to continue that counts.",
    "Your limitation is only your imagination. Dream big!",
    "Don't watch the clock; do what it does. Keep going.",
]

FUN_FACTS = [
    "Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still edible!",
    "Octopuses have three hearts, and two of them stop beating when they swim.",
    "A day on Venus is longer than a year on Venus.",
    "Bananas are berries, but strawberries are not.",
    "The Eiffel Tower can be 15 cm taller during the summer due to thermal expansion.",
    "There are more trees on Earth than stars in the Milky Way — roughly 3 trillion of them!",
    "Cleopatra lived closer in time to the Moon landing than to the building of the Great Pyramid.",
]

_quote_index = 0
_fact_index = 0


def normalize(text):
    text = text.lower().strip()
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text.strip()


def tokenize(text):
    return normalize(text).split()


INTENTS = {
    "greeting": {
        "keywords": [
            "hi", "hello", "hey", "heyy", "hii", "yo", "hey there",
            "good morning", "good evening", "good afternoon",
            "whats up", "sup", "wassup", "whassup", "howdy",
        ],
        "response": "Hey there! How can I help you today?",
    },
    "farewell": {
        "keywords": [
            "bye", "goodbye", "see you", "see ya", "see you later",
            "take care", "catch you later", "later", "peace out",
            "adios", "got to go", "gotta go", "talk to you later",
        ],
        "response": "Goodbye! Talk to you later.",
    },
    "how_are_you": {
        "keywords": [
            "how are you", "how are you doing", "how do you do",
            "how is it going", "how it going", "you okay",
            "are you okay", "how are things", "you doing okay",
            "how you doing", "whats up with you",
        ],
        "response": "I'm functioning optimally! Thanks for asking.",
    },
    "thanks": {
        "keywords": [
            "thank you", "thanks", "thank you so much", "thanks a lot",
            "thank you very much", "much appreciated", "thanks a bunch",
            "im grateful", "thx", "ty", "appreciate it", "thankyou",
        ],
        "response": "You're very welcome!",
    },
    "bot_identity": {
        "keywords": [
            "what is your name", "who are you", "what are you",
            "who made you", "who created you", "who built you",
            "tell me about yourself", "what do you do",
            "what can you do", "your name",
        ],
        "response": "I'm AXIOM — a rule-based chatbot built for Decode Labs.",
    },
    "motivation": {
        "keywords": [
            "motivate me", "inspire me", "i need motivation",
            "give me motivation", "encourage me", "motivational quote",
            "cheer me up", "make me feel better", "im feeling down",
            "give me a quote", "quote of the day",
        ],
    },
    "weather_chat": {
        "keywords": [
            "what is the weather", "how is the weather", "weather today",
            "weather forecast", "is it raining", "is it sunny",
            "whats the temperature", "weather outside",
            "how is it outside", "whats it like outside",
        ],
        "response": "I can't check weather data yet, but I hope it's sunny where you are!",
    },
    "time": {
        "keywords": [
            "what time is it", "tell me the time", "current time",
            "do you know the time", "whats the time",
        ],
    },
    "date": {
        "keywords": [
            "what is the date", "whats the date", "what day is it",
            "todays date", "current date", "what day is today",
        ],
    },
    "help": {
        "keywords": [
            "help", "what can i do", "what do you know",
            "commands", "show commands", "what are your features",
            "how do you work", "tell me what you can do",
        ],
        "response": "You can ask me about the time, get motivated, say hello, or just chat. Try it out!",
    },
    "help_about": {
        "keywords": [
            "tell me about axiom", "what is axiom", "what are you made of",
            "how were you built", "what technology do you use",
            "what stack", "explain yourself",
        ],
        "response": "AXIOM is a rule-based chatbot built entirely in Python. It uses intent-matching with keyword tokens to understand what you're saying. No AI, no APIs — just clean logic!",
    },
    "who_am_i": {
        "keywords": [
            "who am i", "what is my name", "whats my name",
            "do you know my name", "do you remember me",
            "who do you think i am",
        ],
    },
    "fun_fact": {
        "keywords": [
            "tell me a fun fact", "fun fact", "interesting fact",
            "give me a fact", "did you know", "i want a fact",
            "random fact", "tell me something interesting",
        ],
    },
}

FALLBACK = "I don't understand that yet. Try asking me something else."


def match_intent(tokens):
    best_intent = None
    best_keyword_len = 0

    for name, config in INTENTS.items():
        keywords = config.get("keywords", [])
        for keyword in keywords:
            keyword_tokens = tokenize(keyword)
            if all(kt in tokens for kt in keyword_tokens):
                if len(keyword_tokens) > best_keyword_len:
                    best_keyword_len = len(keyword_tokens)
                    best_intent = name

    return best_intent


def extract_name(text):
    text_lower = text.lower().strip()
    for pattern in NAME_PATTERNS:
        if pattern in text_lower:
            parts = text_lower.split(pattern, 1)
            if len(parts) > 1:
                raw_name = parts[1].strip().strip(string.punctuation)
                name_tokens = raw_name.split()
                if name_tokens:
                    return name_tokens[0]
    return None


_OP_MAP = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
    "//": operator.floordiv,
    "%": operator.mod,
}


def detect_arithmetic(text):
    patterns = [
        rf"(\d+(?:\.\d+)?)\s*({''.join(re.escape(op) for op in _OP_MAP)})\s*(\d+(?:\.\d+)?)",
        rf"what\s+is\s+(\d+(?:\.\d+)?)\s*({''.join(re.escape(op) for op in _OP_MAP)})\s*(\d+(?:\.\d+)?)",
        rf"calculate\s+(\d+(?:\.\d+)?)\s*({''.join(re.escape(op) for op in _OP_MAP)})\s*(\d+(?:\.\d+)?)",
        rf"what's\s+(\d+(?:\.\d+)?)\s*({''.join(re.escape(op) for op in _OP_MAP)})\s*(\d+(?:\.\d+)?)",
        rf"what\s+is\s+(\d+(?:\.\d+)?)\s+(plus|minus|times|divided\s+by)\s+(\d+(?:\.\d+)?)",
        rf"(\d+(?:\.\d+)?)\s+(plus|minus|times|divided\s+by)\s+(\d+(?:\.\d+)?)",
    ]
    _WORD_OPS = {
        "plus": "+",
        "minus": "-",
        "times": "*",
        "divided by": "/",
    }

    text_lower = text.lower().strip().lstrip("?")
    for pat in patterns:
        m = re.search(pat, text_lower)
        if not m:
            continue
        a = m.group(1)
        op = m.group(2)
        b = m.group(3)

        if op in _WORD_OPS:
            op = _WORD_OPS[op]

        if op not in _OP_MAP:
            continue

        try:
            a_f = float(a)
            b_f = float(b)
        except ValueError:
            continue

        if op == "/" and b_f == 0:
            return "Division by zero? That's a mathematical sin!"

        result = _OP_MAP[op](a_f, b_f)

        if result == int(result):
            result = int(result)

        return f"{a} {op} {b} = {result}"

    return None


def get_response(user_input):
    clean = normalize(user_input)

    if clean in ("exit", "quit"):
        return None

    tokens = tokenize(clean)

    name = extract_name(user_input)
    if name:
        save_name(name)
        return f"Nice to meet you, {name.capitalize()}! I've noted that."

    intent = match_intent(tokens)

    if intent == "who_am_i":
        data = init_memory()
        stored = data.get("name")
        if stored:
            return f"You're {stored.capitalize()}! I remember."
        return "I don't know your name yet. Tell me with 'my name is ...'"

    if intent == "time":
        now = datetime.now()
        return f"The current time is {now.strftime('%I:%M %p').lstrip('0')}."
    elif intent == "date":
        now = datetime.now()
        return f"Today is {now.strftime('%A, %B %d, %Y')}."
    elif intent == "motivation":
        global _quote_index
        quote = MOTIVATIONAL_QUOTES[_quote_index % len(MOTIVATIONAL_QUOTES)]
        _quote_index += 1
        return quote
    elif intent == "fun_fact":
        global _fact_index
        fact = FUN_FACTS[_fact_index % len(FUN_FACTS)]
        _fact_index += 1
        return fact
    elif intent:
        return INTENTS[intent]["response"]

    arith = detect_arithmetic(user_input)
    if arith:
        return arith

    return FALLBACK


def init_memory():
    data = {"name": None, "conversations": 0}
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if ":" in line:
                    key, _, value = line.partition(":")
                    key = key.strip()
                    value = value.strip()
                    if key == "name":
                        data["name"] = value if value else None
                    elif key == "conversations":
                        data["conversations"] = int(value) if value.isdigit() else 0
    return data


def save_memory(data):
    with open(MEMORY_FILE, "w") as f:
        f.write(f"name:{data.get('name', '') or ''}\n")
        f.write(f"conversations:{data.get('conversations', 0)}\n")


def save_name(name):
    data = init_memory()
    data["name"] = name.strip().lower()
    save_memory(data)


def increment_conversations():
    data = init_memory()
    data["conversations"] = data.get("conversations", 0) + 1
    save_memory(data)
    return data["conversations"]


def get_stored_name():
    data = init_memory()
    return data.get("name")


def log_exchange(user_input, response):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] User: {user_input}\n")
        f.write(f"[{timestamp}] AXIOM: {response}\n")
