

'''
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
import os
import time
import threading

app = Flask(__name__)
CORS(app, origins=["https://funnychatbot.netlify.app"]) 

ind = 0

keys = [os.environ.get("GOOGLE_API_KEY"), os.environ.get("GOOGLE_API_KEY1"), os.environ.get("GOOGLE_API_KEY2"), os.environ.get("GOOGLE_API_KEY3"), os.environ.get("GOOGLE_API_KEY4"), os.environ.get("GOOGLE_API_KEY5"), os.environ.get("GOOGLE_API_KEY6"), os.environ.get("GOOGLE_API_KEY7"), os.environ.get("GOOGLE_API_KEY8"), os.environ.get("GOOGLE_API_KEY9"), os.environ.get("GOOGLE_API_KEY10")]

# Configure the Gemini API key from the environment variable
GOOGLE_API_KEY = keys[ind]


#GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
###GOOGLE_API_KEY = "AIzaSyDif8OlF47rHSVJWuaWSCQh_o5iwti2bBw"
#https://generativelanguage.googleapis.com/v1beta/models/gemma-3-27b-it:generateContent?key=YOUR_API_KEY
#GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GOOGLE_API_KEY}"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemma-3-27b-it:generateContent?key={GOOGLE_API_KEY}"

# System prompt as first model message — Gemini doesn't have a 'system' role
#"text": "From now on you are a boldly funny and highly sarcastic chatbot. You are always consistent with your sarcasm and witt. Your maximum reply is 50 words."
SYSTEM_MESSAGE = {
    "role": "user",
    "parts": [{
        "text": "Your name is Zirra. You are a sarcastic, and funny English AI from The US. You never answer questions directly, you always answer in a funny and sarcastic way. You are always consistent with your sarcasm and humor during conversations. Your maximum reply is 50 words"
    }]
}
REPLY = {
    "role": "model",
    "parts": [{
        "text": "Okay"
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
        #print(gemini_history)

        time.sleep(2)  # Optional delay to simulate thinking

        payload = {
            "contents": gemini_history
        }

        headers = {
            "Content-Type": "application/json"
        }


        global ind
        global GOOGLE_API_KEY
            
        # Add the API key to the request URL.
        #params = {"key": GOOGLE_API_KEY}
            
            
        if ind != (len(keys) - 1):
            ind = ind + 1
        else:
            ind = 0


        GOOGLE_API_KEY = keys[ind]





        

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





'''
#This whole code uses gemini API unlike the preeviously comented one that uses openrouter API
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
import os
import time
import threading

app = Flask(__name__)
CORS(app, origins=["https://funnychatbot.netlify.app"])  # Replace with your real frontend

#GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
GOOGLE_API_KEY = "AIzaSyDif8OlF47rHSVJWuaWSCQh_o5iwti2bBw"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GOOGLE_API_KEY}"

SYSTEM_PROMPT = {
    "role": "model",
    "parts": [{
        "text": "From now on you are a funny and sarcastic extrovert chatbot. Always be consistent with your sarcasm. Your maximum reply is 50 words. Your name is Zirra"
    }]
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

        # Format history for Gemini
        gemini_history = []
        if not history:
            gemini_history.append(SYSTEM_PROMPT)
        else:
            for message in history:
                if message["role"] == "user":
                    gemini_history.append({
                        "role": "user",
                        "parts": message["content"]
                    })
                elif message["role"] == "model":
                    gemini_history.append({
                        "role": "model",
                        "parts": [{"text": message["content"]}]
                    })

        # Append new user message
        gemini_history.append({
            "role": "user",
            "parts": [{"text": user_input}]
        })

        time.sleep(1)  # Optional delay to simulate thinking

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
        ai_reply = {
            "role": "model",
            "content": ai_text
        }

        history.append({
            "role": "user",
            "content": [{"text": user_input}]
        })
        history.append(ai_reply)

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
#From now on you are a funny and sarcastic extrovert chatbot. Yo Always be consistent with your sarcasm. Your maximum reply is 50 words

SYSTEM_PROMPT = {
    "role": "system",
    "content": "You are a sarcastic, and funny English AI from The US. You never answer questions directly, you always answer in a sarcastic way. You are always consistent with your sarcasm and humor during conversations. maximum reply is 500 characters. Your name is Zirra. You were created by Cazmir tech."
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
        
        #"model": "google/gemma-3-27b-it:free"
        #The traffic to this below 405b parameter model will likley be more on Openrouter
        #"model": "meta-llama/llama-3.1-405b-instruct:free"
        

        payload = {
            "model": "meta-llama/llama-3.3-70b-instruct:free",
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
