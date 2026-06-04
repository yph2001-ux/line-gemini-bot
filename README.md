# YP的AI助理 - LINE + Gemini 聊天機器人

## 部署步驟

### 1. 上傳到 GitHub
把這個資料夾的所有檔案上傳到 GitHub repository

### 2. 在 Render 設定環境變數
- LINE_TOKEN = 你的 Channel access token
- LINE_SECRET = 你的 Channel secret  
- GEMINI_API_KEY = 你的 Gemini API Key

### 3. 設定 Webhook URL
在 LINE Developers Console 的 Messaging API 頁籤填入：
https://你的render網址.onrender.com/webhook
