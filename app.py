import os
import requests
from flask import Flask, request
from groq import Groq

app = Flask(__name__)

LINE_TOKEN = os.environ.get("LINE_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

def reply_to_line(reply_token, text):
    headers = {
        "Authorization": f"Bearer {LINE_TOKEN}",
        "Content-Type": "application/json"
    }
    body = {
        "replyToken": reply_token,
        "messages": [{"type": "text", "text": text}]
    }
    requests.post("https://api.line.me/v2/bot/message/reply", headers=headers, json=body)

@app.route("/webhook", methods=["POST"])
def webhook():
    body = request.get_json()
    for event in body.get("events", []):
        if event.get("type") == "message" and event["message"].get("type") == "text":
            user_message = event["message"]["text"]
            reply_token = event["replyToken"]
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": user_message}]
                )
                reply_text = response.choices[0].message.content
            except Exception as e:
                reply_text = f"錯誤：{str(e)}"
            reply_to_line(reply_token, reply_text)
    return "OK", 200

@app.route("/", methods=["GET"])
def index():
    return "YP的AI助理正在運行中！", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
