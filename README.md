# AXIOM — Rule-Based AI Chatbot

A deterministic, dictionary-driven chatbot built for the DecodeLabs AI Internship (Project 1).

---

## 🌿 Branches

This repo has **three branches**, each building on the last:

| Branch | Description |
|---|---|
| [`main`](https://github.com/Red-swipe/decodelabs-p1-AI_Chatbot/tree/main) | Baseline — single-file CLI chatbot with dictionary-based intent matching |
| [`branch-2`](https://github.com/Red-swipe/decodelabs-p1-AI_Chatbot/tree/branch-2) | Normalized token matching, response variety, name memory — more natural dialogue |
| [`branch-3`](https://github.com/Red-swipe/decodelabs-p1-AI_Chatbot/tree/branch-3) | **Most advanced** — modular refactor (`chatbot_core.py` + `cli.py` + `app.py`), persistent multi-conversation JSON storage, Flask web UI with sidebar/theme switching, arithmetic via `operator` module (`eval()` banned), and all security/stability fixes |

👉 **See [`branch-3`](https://github.com/Red-swipe/decodelabs-p1-AI_Chatbot/tree/branch-3) for the latest work.**

---

## Project Overview

This is **Project 1** of the **DecodeLabs AI Internship Track**, designed to introduce the fundamentals of rule-based deterministic logic before progressing to probabilistic and ML-based approaches.

The bot — named **AXIOM** — uses a predefined knowledge base of intent-response pairs to simulate conversation. Every user input is sanitized, matched against a hash-map dictionary, and answered with a fixed response. No external libraries, no neural networks — just pure Python control flow and data structures.

This project establishes the foundation: understanding how input processing, deterministic lookups, and structured code design work in an AI pipeline.

---

## Core Architecture

The bot follows the classic **IPO (Input → Process → Output)** model:

```
User Input  ──►  Sanitize (.lower().strip())  ──►  Dictionary Lookup  ──►  Bot Response
```

### Dictionary over if-elif

| Approach | Time Complexity | Why It Matters |
|---|---|---|
| Dictionary (hash map) | **O(1)** — constant time | Scales effortlessly — adding 1 or 1000 intents has no lookup penalty |
| if-elif chain | **O(n)** — linear time | Every new intent slows down every previous check |

A dictionary was chosen because:
- Lookups are instantaneous regardless of the number of intents
- The code remains clean, maintainable, and data-driven
- Adding new responses is a single line in a data structure — no control flow changes

### Sanitization

Every raw input is converted to lowercase and stripped of surrounding whitespace before the lookup. This ensures partial or accidental casing, spacing, and newlines do not break matching.

---

## Features

- **Continuous input loop** — the bot runs indefinitely until explicitly killed
- **Input sanitization** — `.lower().strip()` applied to every user message
- **10+ intent dictionary** — covers greetings, farewell, identity, capabilities, status, time, motivation, gratitude, creator, and weather intents
- **Fallback response** — unrecognized inputs receive a polite default message
- **Clean exit command** — type `exit` or `quit` to break the loop gracefully
- **Styled startup banner** — AXIOM branding, version, and instructions printed at launch
- **Modular code design** — separate `get_response()` and `main()` functions with the standard `if __name__ == "__main__"` guard

---

## How to Run

```bash
python chatbot.py
```

No additional setup, virtual environment, or package installation required.

---

## File Structure

```
decode-labs-ai-p1/
├── chatbot.py          Main program — input loop, knowledge base, and response logic
├── requirements.txt    Empty — no external dependencies needed
├── README.md           This file — project documentation
└── .gitignore          Git ignore rules
```

---

## Technologies Used

- **Python 3** — Core language
- **Standard Library only** — no third-party packages, no external APIs, no machine learning frameworks

---

## Internship

| | |
|---|---|
| **Organization** | DecodeLabs |
| **Track** | AI Internship |
| **Project** | 1 of N — Rule-Based AI Chatbot |
| **Batch** | 2026 |
| **Bot Name** | AXIOM v1.0 |
