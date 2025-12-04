# chatbox.py
import requests
import pandas as pd
from datetime import datetime
from prompts import build_prompt
from dotenv import load_dotenv
import os

# -----------------------------
# 🔧 Setup
# -----------------------------
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise ValueError("❌ No OpenRouter API key found in .env")

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# -----------------------------
# 🗂 Log Conversations
# -----------------------------
def log_conversation(user_msg, bot_reply):
    log = pd.DataFrame([{
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user_message": user_msg,
        "bot_reply": bot_reply
    }])
    log.to_csv("conversation_log.csv", mode='a', index=False, header=False)

# -----------------------------
# 💬 Chat Function
# -----------------------------
def chat():
    chat_history = []
    print("🤖 SmartBuddy: Hi! I'm your chatbot. Type 'exit' to end.\n")

    while True:
        user_msg = input("You: ")
        if user_msg.lower() in ["exit", "quit"]:
            print("🤖 SmartBuddy: Goodbye! 👋")
            break

        messages = build_prompt(user_msg, chat_history)

        try:
            response = requests.post(
                OPENROUTER_URL,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "HTTP-Referer": "http://localhost",
                    "X-Title": "SmartBuddy Chatbot"
                },
                json={
                    "model": "mistralai/mistral-7b-instruct:free",  # ✅ free model
                    "messages": messages,
                    "temperature": 0.7,
                    "max_tokens": 100
                }
            )
            data = response.json()

            if "choices" in data:
                bot_reply = data["choices"][0]["message"]["content"].strip()
            else:
                bot_reply = f"[Error: {data}]"
        except Exception as e:
            bot_reply = f"[Error: {e}]"

        print("🤖 SmartBuddy:", bot_reply, "\n")
        chat_history.append((user_msg, bot_reply))
        log_conversation(user_msg, bot_reply)

# -----------------------------
# 🚀 Run
# -----------------------------
if __name__ == "__main__":
    chat()
