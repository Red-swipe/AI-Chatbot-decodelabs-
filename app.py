from flask import Flask, request, jsonify, render_template, Response
from chatbot_core import get_response, init_memory, increment_conversations, log_exchange, get_stored_name
import uuid
import json
import os
import re
from datetime import datetime
from typing import Any

app = Flask(__name__)

CONVERSATIONS_DIR = "conversations"
os.makedirs(CONVERSATIONS_DIR, exist_ok=True)


def load_conversation(conv_id: str) -> Any:
    path = os.path.join(CONVERSATIONS_DIR, f"{conv_id}.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def save_conversation(data: Any) -> None:
    path = os.path.join(CONVERSATIONS_DIR, f"{data['id']}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def list_conversations() -> list[dict[str, Any]]:
    convs: list[dict[str, Any]] = []
    if not os.path.exists(CONVERSATIONS_DIR):
        return convs
    for fname in os.listdir(CONVERSATIONS_DIR):
        if not fname.endswith(".json"):
            continue
        conv_id = fname[:-5]
        data = load_conversation(conv_id)
        if data:
            msgs = data.get("messages", [])
            convs.append({
                "id": conv_id,
                "title": data.get("title", "Untitled"),
                "message_count": len(msgs),
                "updated_at": msgs[-1]["timestamp"] if msgs else ""
            })
    convs.sort(key=lambda c: c["updated_at"], reverse=True)
    return convs

memory = init_memory()


def _is_safe_origin(req: request) -> bool:
    origin = req.headers.get("Origin") or req.headers.get("Referer")
    if not origin:
        return True
    allowed = req.host_url.rstrip("/")
    return origin.startswith(allowed)


@app.route("/")
def index() -> str:
    stored_name = get_stored_name()
    return render_template("index.html", stored_name=stored_name)


@app.route("/chat", methods=["POST"])
def chat() -> tuple[Response, int] | Response:
    if not _is_safe_origin(request):
        return jsonify({"error": "Forbidden"}), 403
    body = request.get_json(silent=True)
    if not body or "message" not in body:
        return jsonify({"error": "Missing 'message' in JSON body"}), 400

    user_input = body["message"].strip()
    if not user_input:
        return jsonify({"response": "You didn't say anything!"})

    conversation_id = body.get("conversation_id")

    conversation = None
    if conversation_id:
        conversation = load_conversation(conversation_id)

    if not conversation:
        conversation = {"id": str(uuid.uuid4()), "title": "", "messages": []}

    response = get_response(user_input)
    if response is None:
        response = "Goodbye! Talk to you later."

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conversation["messages"].append({
        "role": "user", "text": user_input, "timestamp": timestamp
    })
    conversation["messages"].append({
        "role": "bot", "text": response, "timestamp": timestamp
    })

    if not conversation["title"]:
        conversation["title"] = user_input[:40].rstrip()

    increment_conversations()
    log_exchange(user_input, response)
    save_conversation(conversation)

    return jsonify({"response": response, "conversation_id": conversation["id"]})


@app.route("/conversations", methods=["GET"])
def conversations_list() -> Response:
    return jsonify(list_conversations())


@app.route("/conversations/new", methods=["POST"])
def conversations_new() -> tuple[Response, int] | Response:
    if not _is_safe_origin(request):
        return jsonify({"error": "Forbidden"}), 403
    conv = {"id": str(uuid.uuid4()), "title": "New conversation", "messages": []}
    save_conversation(conv)
    return jsonify({"id": conv["id"]})


_SAFE_ID_RE = re.compile(r"^[a-zA-Z0-9_-]+$")

def _validate_conv_id(conv_id: str) -> tuple[Response, int] | None:
    if not _SAFE_ID_RE.match(conv_id):
        return jsonify({"error": "Invalid conversation ID"}), 400
    return None


@app.route("/conversations/<conv_id>", methods=["GET"])
def conversations_get(conv_id: str) -> tuple[Response, int] | Response:
    err = _validate_conv_id(conv_id)
    if err:
        return err
    data = load_conversation(conv_id)
    if data is None:
        return jsonify({"error": "Conversation not found"}), 404
    return jsonify(data)


@app.route("/conversations/<conv_id>", methods=["DELETE"])
def conversations_delete(conv_id: str) -> tuple[Response, int] | Response:
    if not _is_safe_origin(request):
        return jsonify({"error": "Forbidden"}), 403
    err = _validate_conv_id(conv_id)
    if err:
        return err
    path = os.path.join(CONVERSATIONS_DIR, f"{conv_id}.json")
    if os.path.exists(path):
        os.remove(path)
        return jsonify({"status": "deleted"})
    return jsonify({"error": "Conversation not found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
