
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
import os
import time  # ⏱️ Import time module

app = Flask(__name__)
CORS(app, origins=["https://your-frontend-site.netlify.app"])  # Replace with your real frontend domain

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
