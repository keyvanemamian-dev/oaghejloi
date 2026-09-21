import os
import requests
from flask import Flask, request

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set")

BASE_URL = f"https://tapi.bale.ai/bot{BOT_TOKEN}"


@app.route("/")
def home():
    return "Bale bot is running!"


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(silent=True)

    if not data:
        return "OK", 200

    print("NEW UPDATE:")
    print(data)

    message = data.get("message")

    if message:
        user = message.get("from", {})
        chat = message.get("chat", {})

        print("User ID:", user.get("id"))
        print("Chat ID:", chat.get("id"))
        print("Name:", user.get("first_name"))
        print("Username:", user.get("username"))
        print("Text:", message.get("text"))

    return "OK", 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
