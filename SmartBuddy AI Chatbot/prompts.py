# prompts.py
system_prompt = """
You are a friendly and helpful chatbot called 'SmartBuddy'.
You answer politely, clearly, and concisely.
If you don't know something, say "I'm not sure, but I can find out!".
Keep responses under 80 words.
"""

def build_prompt(user_message, chat_history):
    messages = [{"role": "system", "content": system_prompt}]
    for u, b in chat_history[-3:]:
        messages.append({"role": "user", "content": u})
        messages.append({"role": "assistant", "content": b})
    messages.append({"role": "user", "content": user_message})
    return messages
