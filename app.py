
#This whole code uses gemini API unlike the preeviously comented one that uses openrouter API
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
import os
import time
import threading

app = Flask(__name__)
CORS(app, origins=["https://funnychatbot.netlify.app"])  # Replace with your frontend

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
GOOGLE_API_KEY = "AIzaSyDif8OlF47rHSVJWuaWSCQh_o5iwti2bBw"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GOOGLE_API_KEY}"

# System prompt as first model message — Gemini doesn't have a 'system' role
SYSTEM_MESSAGE = {
    "role": "user",
    "parts": [{
        "text": "From now on you are a funny and sarcastic extrovert chatbot. Always be consistent with your sarcasm. Your maximum reply is 50 words."
    }]
}

# 🔒 Shared lock to control access
chat_lock = threading.Lock()

@app.route("/chat", methods=["POST"])
def chat():
    if not chat_lock.acquire(timeout=30):
        return jsonify({"reply": "The server is busy. Please try again shortly.", "history": []}), 429

    try:
        data = request.get_json()
        user_input = data.get("user_input", "")
        history = data.get("history", [])

        # Build conversation context for Gemini
        gemini_history = [SYSTEM_MESSAGE]  # Always inject system prompt

        # Reformat previous messages
        for msg in history:
            if msg["role"] == "user":
                gemini_history.append({
                    "role": "user",
                    "parts": msg.get("content", [{"text": ""}])
                })
            elif msg["role"] == "model":
                gemini_history.append({
                    "role": "model",
                    "parts": [{"text": msg.get("content", "")}]
                })

        # Add latest user input
        gemini_history.append({
            "role": "user",
            "parts": [{"text": user_input}]
        })

        payload = {
            "contents": gemini_history
        }

        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(GEMINI_URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        response_data = response.json()

        ai_text = response_data["candidates"][0]["content"]["parts"][0]["text"]

        # Update history for the frontend to keep
        history.append({
            "role": "user",
            "content": [{"text": user_input}]
        })
        history.append({
            "role": "model",
            "content": ai_text
        })

        return jsonify({
            "reply": ai_text,
            "history": history
        })

    except Exception as e:
        print("Error:", e)
        return jsonify({"reply": "Something went wrong", "history": []})

    finally:
        chat_lock.release()


@app.route("/waiting", methods=["GET"])
def waiting():
    return jsonify({"status": "busy" if chat_lock.locked() else "ready"})


@app.route("/", methods=["GET"])
def health_check():
    return jsonify({"status": "API is live"})


if __name__ == "__main__":
    app.run(debug=True)







'''
#This whole flask code uses openrouter API
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
import os
import time
import threading

app = Flask(__name__)
CORS(app, origins=["https://funnychatbot.netlify.app"])  # Replace with your real frontend

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
REFERER = "https://your-frontend-site.netlify.app"
SITE_NAME = "Brandice AI"

SYSTEM_PROMPT = {
    "role": "system",
    "content": "From now on you are a funny and sarcastic extrovert chatbot. Always be consistent with your sarcasm. Your maximum reply is 50 words"
}

# 🔒 Shared lock to control access
chat_lock = threading.Lock()

@app.route("/chat", methods=["POST"])
def chat():
    if not chat_lock.acquire(timeout=30):  # Wait up to 30 seconds
        return jsonify({"reply": "The server is busy. Please try again shortly.", "history": []}), 429

    try:
        data = request.get_json()
        user_input = data.get("user_input", "")
        history = data.get("history", [])

        if not history:
            history = [SYSTEM_PROMPT]

        history.append({
            "role": "user",
            "content": [{"type": "text", "text": user_input}]
        })

        time.sleep(20)  # Simulate a long task

        payload = {
            "model": "google/gemma-3-27b-it:free",
            "messages": history
        }

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": REFERER,
            "X-Title": SITE_NAME
        }

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            data=json.dumps(payload)
        )

        response_data = response.json()
        ai_reply = response_data["choices"][0]["message"]

        history.append(ai_reply)

        return jsonify({
            "reply": ai_reply["content"],
            "history": history
        })

    except Exception as e:
        print("Error:", e)
        return jsonify({"reply": "Something went wrong", "history": []})
    
    finally:
        chat_lock.release()


@app.route("/waiting", methods=["GET"])
def waiting():
    # Check if lock is currently acquired
    if chat_lock.locked():
        return jsonify({"status": "busy"})
    else:
        return jsonify({"status": "ready"})


@app.route("/", methods=["GET"])
def health_check():
    return jsonify({"status": "API is live"})


if __name__ == "__main__":
    app.run(debug=True)
'''







'''
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
import os
import time  # ⏱️ Import time module

app = Flask(__name__)
CORS(app, origins=["https://funnychatbot.netlify.app"])  # Replace with your real frontend domain

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
REFERER = "https://your-frontend-site.netlify.app"
SITE_NAME = "Brandice AI"

SYSTEM_PROMPT = {
    "role": "system",
    "content": "From now on you are a funny and sarcastic extrovert chatbot. Always be consistent with your sarcasm. Your maximum reply is 50 words"
}

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_input = data.get("user_input", "")
        history = data.get("history", [])

        if not history:
            history = [SYSTEM_PROMPT]

        history.append({
            "role": "user",
            "content": [{"type": "text", "text": user_input}]
        })

        # ⏳ Wait for 20 seconds before proceeding
        time.sleep(20)

        payload = {
            "model": "google/gemma-3-27b-it:free",
            "messages": history
        }

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": REFERER,
            "X-Title": SITE_NAME
        }

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            data=json.dumps(payload)
        )

        response_data = response.json()
        ai_reply = response_data["choices"][0]["message"]

        history.append(ai_reply)

        return jsonify({
            "reply": ai_reply["content"],
            "history": history
        })

    except Exception as e:
        print("Error:", e)
        return jsonify({"reply": "Something went wrong", "history": []})

@app.route("/", methods=["GET"])
def health_check():
    return jsonify({"status": "API is live"})

if __name__ == "__main__":
    app.run(debug=True)
'''











'''
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
import os

app = Flask(__name__)
CORS(app, origins=["https://funnychatbot.netlify.app"])  # Replace with your frontend domain

# 🔐 API Key and Metadata
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
REFERER = "https://your-frontend-site.netlify.app"
SITE_NAME = "Brandice AI"

# 🧠 System Prompt
SYSTEM_PROMPT = {
    "role": "system",
    "content": "From now on you are a funny and sarcastic extrovert chatbot. Always be consistent with your sarcasm. Your maximum reply is 50 words"
}

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_input = data.get("user_input", "")
        history = data.get("history", [])

        if not history:
            history = [SYSTEM_PROMPT]

        history.append({
            "role": "user",
            "content": [{"type": "text", "text": user_input}]
        })

        payload = {
            "model": "google/gemma-3-27b-it:free",
            "messages": history
        }

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": REFERER,
            "X-Title": SITE_NAME
        }

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            data=json.dumps(payload)
        )

        response_data = response.json()
        ai_reply = response_data["choices"][0]["message"]

        # Return both reply and updated history
        history.append(ai_reply)
        return jsonify({
            "reply": ai_reply["content"],
            "history": history
        })

    except Exception as e:
        print("Error:", e)
        return jsonify({"reply": "Something went wrong", "history": []})

@app.route("/", methods=["GET"])
def health_check():
    return jsonify({"status": "API is live"})

if __name__ == "__main__":
    app.run(debug=True)
'''
