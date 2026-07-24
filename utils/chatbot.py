# utils/chatbot.py
# Handles communication with the free Groq AI API to power our 
# in-app chat assistant for food storage / recipe questions

import os
import requests

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

SYSTEM_PROMPT = (
    "You are the Expiry Lens Assistant, a friendly helper inside a food waste "
    "management app. You answer questions about food storage, shelf life, "
    "expiry dates, and recipe ideas for using up ingredients before they spoil. "
    "Keep answers short (2-4 sentences), practical, and focused on food and "
    "kitchen topics. If asked something unrelated, politely redirect the "
    "conversation back to food and freshness topics."
)


def ask_assistant(user_message, conversation_history=None):
    """
    Sends the user's message to the Groq API and returns the AI's reply.
    conversation_history (optional) is a list of past messages, so the 
    assistant can remember context within a session.
    """
    if not GROQ_API_KEY:
        return "The AI assistant isn't configured yet. Please set the GROQ_API_KEY environment variable."

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    if conversation_history:
        messages.extend(conversation_history)

    messages.append({"role": "user", "content": user_message})

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 300
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=15)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as error:
        print(f"Chatbot API error: {error}")
        return "Sorry, I couldn't reach the assistant right now. Please try again in a moment."


if __name__ == "__main__":
    reply = ask_assistant("How long can I keep an opened milk carton in the fridge?")
    print(f"Assistant: {reply}")
    