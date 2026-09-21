import os
import requests
from flask import Flask, request

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
OWNER_ID = 2020589750

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set")

BASE_URL = f"https://tapi.bale.ai/bot{BOT_TOKEN}"


def send_message(chat_id, text, reply_to_message_id=None):
    data = {
        "chat_id": chat_id,
        "text": text
    }

    if reply_to_message_id:
        data["reply_to_message_id"] = reply_to_message_id

    return requests.post(
        f"{BASE_URL}/sendMessage",
        json=data
    )


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

    chat = message.get("chat", {})
    user = message.get("from", {})

    chat_id = chat.get("id")
    message_id = message.get("message_id")
    text = message.get("text", "")

    # =========================
    # پیام صاحب ربات
    # =========================

    if chat_id == OWNER_ID:

        # اگر صاحب ربات روی پیام یک کاربر Reply کرده باشد
        reply_to = message.get("reply_to_message")

        if reply_to and text:

            original_text = reply_to.get("text", "")

            # User ID را از متن پیام قبلی پیدا می‌کنیم
            if "🆔 " in original_text:
                try:
                    user_id = original_text.split("🆔 ")[1].split("\n")[0]

                    send_message(
                        user_id,
                        text
                    )

                    print("Reply sent to:", user_id)

                except Exception as e:
                    print("Reply error:", e)

        return "OK", 200


    # =========================
    # پیام کاربر
    # =========================

    user_id = user.get("id")
    name = user.get("first_name", "")
    username = user.get("username", "")

    sender_info = f"👤 {name}"

    if username:
        sender_info += f" (@{username})"

    forwarded_text = (
        f"{sender_info}\n"
        f"🆔 {user_id}\n\n"
        f"💬 {text}"
    )

    send_message(
        OWNER_ID,
        forwarded_text
    )

    return "OK", 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(
        host="0.0.0.0",
        port=port
    )
        host="0.0.0.0",
        port=port
    )
