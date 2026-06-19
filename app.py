from flask import Flask, request, jsonify, render_template
from chatbot_core import get_response, init_memory, increment_conversations, log_exchange, get_stored_name

app = Flask(__name__)

memory = init_memory()


@app.route("/")
def index():
    stored_name = get_stored_name()
    return render_template("index.html", stored_name=stored_name)


@app.route("/chat", methods=["POST"])
def chat():
    body = request.get_json(silent=True)
    if not body or "message" not in body:
        return jsonify({"error": "Missing 'message' in JSON body"}), 400

    user_input = body["message"].strip()
    if not user_input:
        return jsonify({"response": "You didn't say anything!"})

    response = get_response(user_input)
    if response is None:
        response = "Goodbye! Talk to you later."

    increment_conversations()
    log_exchange(user_input, response)

    return jsonify({"response": response})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
