from flask import Flask, request, jsonify, session
import requests as external_requests
import os

app = Flask(__name__)
app.secret_key = "your-secret-key"

# Get OpenRouter API Key from env
#OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
SITE_URL = "https://yourfrontend.com"
SITE_NAME = "Brandice AI"
MODEL = "google/gemma-3-27b-it:free"

# System prompt (you can change this from backend)
SYSTEM_PROMPT = {
    "role": "system",
    "content": "You are Brandice AI, a helpful and witty assistant."
}

'''
@app.route("/")
def index():
    session["chat_history"] = [SYSTEM_PROMPT]  # Clear history on refresh
    return render_template("index.html")
'''

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message")

    if "chat_history" not in session:
        session["chat_history"] = [SYSTEM_PROMPT]

    # Append user's message
    session["chat_history"].append({"role": "user", "content": user_message})

    # Call OpenRouter API
    try:
        response = external_requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer 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",
                "Content-Type": "application/json",
                "HTTP-Referer": SITE_URL,
                "X-Title": SITE_NAME,
            },
            json={
                "model": MODEL,
                "messages": session["chat_history"]
            }
        )

        result = response.json()
        reply = result["choices"][0]["message"]["content"]

        # Save bot reply in session
        session["chat_history"].append({"role": "assistant", "content": reply})

        return jsonify({"reply": reply})

    except Exception as e:
        print("Error:", e)
        return jsonify({"reply": "Oops! Something went wrong. Please try again."}), 500


if __name__ == "__main__":
    app.run(debug=True)
