import os
import requests
from flask import Flask, request

app = Flask(__name__)

BOT_TOKEN = 1273875466:johT6Q_58Z7Gus9iZw8Vzgd0AdV58JpzHX0
OWNER_ID = 2020589750

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set")

if not OWNER_ID:
    raise RuntimeError("OWNER_ID is not set")

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

        user_id = user.get("id")
        chat_id = chat.get("id")
        name = user.get("first_name", "")
        username = user.get("username", "")
        text = message.get("text", "")

        print("User ID:", user_id)
        print("Chat ID:", chat_id)
        print("Name:", name)
        print("Username:", username)
        print("Text:", text)

        if chat_id != int(OWNER_ID):
            sender_info = f"👤 {name}"

            if username:
                sender_info += f" (@{username})"

            msg = f"{sender_info}\n🆔 {user_id}\n\n💬 {text}"

            requests.post(
                f"{BASE_URL}/sendMessage",
                json={
                    "chat_id": OWNER_ID,
                    "text": msg
                }
            )

    return "OK", 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
