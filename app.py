from flask import Flask, request, jsonify, session
import requests
import json
import os

app = Flask(__name__)
app.secret_key = "your-secret-key"

# 🔑 Your API Key
#OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
REFERER = "https://yourdomain.com"
SITE_NAME = "My Chatbot"

# 🎓 System Prompt
SYSTEM_PROMPT = {
    "role": "system",
    "content": "From now on you are an funny and sarcastic extrovert chatbot. Always be consistent with your sarcasm. Your maximum reply is 50 words"
}

@app.route("/")
def index():
    # 🔄 Clear chat history on every refresh
    session["chat_history"] = [SYSTEM_PROMPT]
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.form.get("user_input")

    if "chat_history" not in session:
        session["chat_history"] = [SYSTEM_PROMPT]

    # Add user message
    session["chat_history"].append({
        "role": "user",
        "content": [{"type": "text", "text": user_input}]
    })

    payload = {
        "model": "google/gemma-3-27b-it:free",
        "messages": session["chat_history"]
    }

    headers = {
        "Authorization": f"Bearer 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",
        "Content-Type": "application/json",
        "HTTP-Referer": REFERER,
        "X-Title": SITE_NAME
    }

    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            data=json.dumps(payload)
        )
        response_data = response.json()
        ai_message = response_data['choices'][0]['message']

        # Add assistant reply
        session["chat_history"].append(ai_message)
        session.modified = True

        return jsonify({"reply": ai_message['content']})
    except Exception as e:
        print("Error:", e)
        return jsonify({"reply": "Sorry, something went wrong!"})

@app.route("/reset", methods=["POST"])
def reset_chat():
    session["chat_history"] = [SYSTEM_PROMPT]
    return jsonify({"message": "Chat history cleared."})

if __name__ == "__main__":
    app.run(debug=True)
