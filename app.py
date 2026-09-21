import os
import requests
from flask import Flask, request

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
OWNER_ID = "2020589750"

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

    if not message:
        return "OK", 200

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

    # پیام‌هایی که خود صاحب ربات می‌فرستد
    if chat_id == int(OWNER_ID):

        if text.startswith("/reply "):
            parts = text.split(" ", 2)

            if len(parts) < 3:
                requests.post(
                    f"{BASE_URL}/sendMessage",
                    json={
                        "chat_id": OWNER_ID,
                        "text": "فرمت درست:\n/reply USER_ID متن پیام"
                    }
                )
                return "OK", 200

            target_id = parts[1]
            reply_text = parts[2]

            response = requests.post(
                f"{BASE_URL}/sendMessage",
                json={
                    "chat_id": target_id,
                    "text": reply_text
                }
            )

            if response.ok:
                result_text = "✅ پیام ارسال شد."
            else:
                result_text = "❌ ارسال پیام ناموفق بود."

            requests.post(
                f"{BASE_URL}/sendMessage",
                json={
                    "chat_id": OWNER_ID,
                    "text": result_text
                }
            )

        return "OK", 200

    # پیام کاربر را برای صاحب ربات بفرست
    sender_info = f"👤 {name}"

    if username:
        sender_info += f" (@{username})"

    msg = (
        f"{sender_info}\n"
        f"🆔 {user_id}\n\n"
        f"💬 {text}"
    )

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
