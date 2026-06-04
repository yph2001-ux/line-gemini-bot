import os
import requests
from flask import Flask, request, abort
import google.generativeai as genai

app = Flask(__name__)

# 從環境變數讀取金鑰
LINE_TOKEN = os.environ.get("LINE_TOKEN")
LINE_SECRET = os.environ.get("LINE_SECRET")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# 設定 Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

def reply_to_line(reply_token, text):
    """回覆訊息給 LINE 使用者"""
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
        # 只處理文字訊息
        if event.get("type") == "message" and event["message"].get("type") == "text":
            user_message = event["message"]["text"]
            reply_token = event["replyToken"]
            
            try:
                # 呼叫 Gemini 產生回覆
                response = model.generate_content(user_message)
                reply_text = response.text
            except Exception as e:
                reply_text = "抱歉，我現在無法回應，請稍後再試。"
            
            reply_to_line(reply_token, reply_text)
    
    return "OK", 200

@app.route("/", methods=["GET"])
def index():
    return "YP的AI助理正在運行中！", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
