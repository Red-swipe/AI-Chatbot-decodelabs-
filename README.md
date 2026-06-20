# AXIOM — Rule-Based AI Chatbot

A deterministic, dictionary-driven chatbot with a Flask web UI and CLI interface — built for the DecodeLabs AI Internship (Project 1).

---

## Project Overview

This is **Project 1** of the **DecodeLabs AI Internship Track**, designed to introduce the fundamentals of rule-based deterministic logic before progressing to probabilistic and ML-based approaches.

The bot — named **AXIOM** — uses a predefined knowledge base of intent-response pairs to simulate conversation. Every user input is sanitized, matched against a hash-map dictionary, and answered with a fixed response. No external libraries (beyond Flask), no neural networks — just pure Python control flow and data structures.

This project establishes the foundation: understanding how input processing, deterministic lookups, and structured code design work in an AI pipeline.

---

## Core Architecture

```
┌─────────────────────────────────────────────────────┐
│                    User                              │
│  (Browser ──► HTTP)      (Terminal ──► CLI)         │
└──────────┬──────────────────────────┬────────────────┘
           │                          │
           ▼                          ▼
     ┌──────────┐             ┌──────────────┐
     │  app.py  │             │   cli.py     │
     │  (Flask) │             │ (input loop) │
     └────┬─────┘             └──────┬───────┘
          │                          │
          └──────────┬───────────────┘
                     ▼
           ┌──────────────────┐
           │  chatbot_core.py │
           │  -get_response() │
           │  -match_intent() │
           │  -save_memory()  │
           │  -log_exchange() │
           │  -arithmetic     │
           └──────────────────┘
```

### Three layers

| Layer | File | Role |
|---|---|---|
| **Web UI** | `app.py` | Flask server — serves `index.html`, handles REST API (`POST /chat`, `GET /chat/conversations`, etc.), manages per-conversation JSON storage, validates origins for CSRF protection |
| **CLI** | `cli.py` | Terminal input loop — banner, stdin → response → stdout |
| **Core engine** | `chatbot_core.py` | Intent matching (dictionary-based), input sanitization, arithmetic detection (via `operator` module), memory persistence (`memory.txt`), conversation logging with rotation |

### Dictionary over if-elif

| Approach | Time Complexity | Why It Matters |
|---|---|---|
| Dictionary (hash map) | **O(1)** — constant time | Scales effortlessly — adding 1 or 1000 intents has no lookup penalty |
| if-elif chain | **O(n)** — linear time | Every new intent slows down every previous check |

### Sanitization

Every raw input is converted to lowercase and stripped of surrounding whitespace before the lookup. Non-ASCII punctuation is normalized to ensure Unicode text does not break matching.

---

## Features

### Web UI (Flask)
- **Sidebar conversation list** — create, switch between, and delete conversations
- **Real-time chat** — send messages and receive responses via `POST /chat`
- **User settings panel** — configure bot name, user name, theme (light/dark), and response style
- **Persistent memory** — name, preferences, and conversation history survive server restarts
- **Cross-session identity** — AXIOM remembers who you are across conversations
- **CSRF protection** — `Origin`/`Referer` header validation on state-changing routes

### CLI
- **Continuous input loop** — runs until `exit` or `quit`
- **Input sanitization** — `.lower().strip()` applied to every user message
- **30+ intent dictionary** — greetings, farewell, identity, capabilities, status, time, motivation, gratitude, creator, weather, jokes, fun facts, and more
- **Fallback response** — unrecognized inputs receive a polite default message
- **Styled startup banner** — AXIOM branding, version, and instructions printed at launch

### Core Engine
- **Arithmetic intent detection** — evaluates simple math expressions (+, -, *, /, //, **) via the `operator` module — no `eval()` used
- **Multi-conversation support** — individual JSON files per conversation ID
- **Motivational quotes** — random rotation of 10+ quotes
- **Fun facts** — random fact generation
- **Memory file locking** — `threading.Lock` prevents race conditions on `memory.txt`
- **Log rotation** — auto-truncates `conversation_log.txt` to last 1000 lines

---

## How to Run

### Web UI (Flask)

```bash
pip install -r requirements.txt
python app.py
```

Open `http://localhost:5000` in your browser.

### CLI

```bash
python cli.py
```

No additional setup required for CLI mode.

---

## File Structure

```
decode-labs-ai-p1/
├── app.py               Flask web server — routes, sessions, serving index.html
├── chatbot_core.py      Core engine — intent matching, memory, logging, arithmetic
├── cli.py               Terminal input loop with banner
├── requirements.txt     flask>=3.0
├── templates/
│   └── index.html       Chat UI — sidebar, chat area, settings panel, theme toggle
├── conversations/       Per-conversation JSON files (created at runtime)
├── memory.txt           Persistent user memory (created at runtime)
├── conversation_log.txt Activity log (created at runtime)
├── BUGS.md              Bug audit and resolution tracking
├── README.md            This file — project documentation
└── .gitignore           Git ignore rules
```

---

## Technologies Used

- **Python 3** — Core language
- **Flask 3.x** — Web framework for the chat UI
- **Standard Library only** — no third-party ML/AI packages, no external APIs

---

## Internship

| | |
|---|---|
| **Organization** | DecodeLabs |
| **Track** | AI Internship |
| **Project** | 1 of N — Rule-Based AI Chatbot |
| **Batch** | 2026 |
| **Bot Name** | AXIOM v3.0 |
