import os
import re
import logging
import ollama
from flask import Flask, render_template, request, redirect, session, url_for, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from google import genai
from groq import Groq  # New Import
from werkzeug.security import generate_password_hash, check_password_hash

# Security and DB
from database.db import init_db, create_user, get_user, save_chat, get_history

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
CORS(app) 

# --- 2026 MODEL HIERARCHY CONFIG ---
# Added Groq as Tier 0 (Cloud Fast)




MODEL_GROQ1 = os.getenv("GROQ_MODEL", "meta-llama/llama-4-scout-17b-16e-instruct") 
MODEL_GROQ2 = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
MODEL_GROQ3 = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
MODEL_GROQ4 = os.getenv("GROQ_MODEL", "whisper-large-v3")
MODEL_GROQ5 = os.getenv("GROQ_MODEL", "whisper-large-v3-turbo")


MODEL_PRIMARY = os.getenv("OLLAMA_MODEL","gemma4:e4b")            # Tier 1: Fast Expert
MODEL_LOGIC = os.getenv("OLLAMA_MODEL", "llama3.2")              # Tier 2: Deep Reasoning
MODEL_REFLEX = os.getenv("OLLAMA_MODEL","deepseek-r1")           # Tier 3: Instant Reflex
MODEL_SPEED = os.getenv("OLLAMA_MODEL", "deepseek-r1:1.5b")      # Tier 4: Generalist

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

init_db()

# --- AI CORE LOGIC ---

def clean_reasoning(text):
    """Removes <think> tags from DeepSeek R1 to clean output for UI."""
    if not text: return ""
    return re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL).strip()

def ask_ai(message, emotion="neutral"):
    """
    Refactored Orchestrator: Groq Primary -> Gemma 4 -> Multi-tier fallback.
    """
    emotion_prefixes = {
        "happy": "Analyzing your positive neural state... ",
        "sad": "Detecting low neural resonance... ",
        "angry": "Neural spikes detected. Implementing calm-protocol... ",
        "neutral": "System stabilized. Processing... "
    }
    prefix = emotion_prefixes.get(emotion.lower(), "")
    full_prompt = f"Context: User is {emotion}. Response to: {message}"

    # --- ATTEMPT 0: GROQ (Tier 0 - Ultra Fast Cloud) ---
    if GROQ_API_KEY:
        try:
            client = Groq(api_key=GROQ_API_KEY)
            completion = client.chat.completions.create(
                model=MODEL_GROQ1,
                messages=[{"role": "user", "content": full_prompt}],
                temperature=0.5,
                max_tokens=2048
            )
            reply = completion.choices[0].message.content
            if reply: return f"{prefix}{reply}"
        except Exception as e:
            app.logger.warning(f"Groq failed: {e}. Falling back to Ollama...")

    if GROQ_API_KEY:
        try:
            client = Groq(api_key=GROQ_API_KEY)
            completion = client.chat.completions.create(
                model=MODEL_GROQ2,
                messages=[{"role": "user", "content": full_prompt}],
                temperature=0.5,
                max_tokens=2048
            )
            reply = completion.choices[0].message.content
            if reply: return f"{prefix}{reply}"
        except Exception as e:
            app.logger.warning(f"Groq failed: {e}. Falling back to Ollama...")

    if GROQ_API_KEY:
        try:
            client = Groq(api_key=GROQ_API_KEY)
            completion = client.chat.completions.create(
                model=MODEL_GROQ3,
                messages=[{"role": "user", "content": full_prompt}],
                temperature=0.5,
                max_tokens=2048
            )
            reply = completion.choices[0].message.content
            if reply: return f"{prefix}{reply}"
        except Exception as e:
            app.logger.warning(f"Groq failed: {e}. Falling back to Ollama...")

    if GROQ_API_KEY:
        try:
            client = Groq(api_key=GROQ_API_KEY)
            completion = client.chat.completions.create(
                model=MODEL_GROQ4,
                messages=[{"role": "user", "content": full_prompt}],
                temperature=0.5,
                max_tokens=2048
            )
            reply = completion.choices[0].message.content
            if reply: return f"{prefix}{reply}"
        except Exception as e:
            app.logger.warning(f"Groq failed: {e}. Falling back to Ollama...")

    if GROQ_API_KEY:
        try:
            client = Groq(api_key=GROQ_API_KEY)
            completion = client.chat.completions.create(
                model=MODEL_GROQ5,
                messages=[{"role": "user", "content": full_prompt}],
                temperature=0.5,
                max_tokens=2048
            )
            reply = completion.choices[0].message.content
            if reply: return f"{prefix}{reply}"
        except Exception as e:
            app.logger.warning(f"Groq failed: {e}. Falling back to Ollama...")


    # Global options for Local Ollama Speed
    fast_options = {
        "num_predict": 2048,
        "num_ctx": 4096,
        "temperature": 0.4,
        "num_thread": 8,
        "top_p": 0.9
    }

    # --- ATTEMPT 1: GEMMA 4 E4B (Primary Local Expert) ---
    try:
        response = ollama.chat(
            model=MODEL_PRIMARY, 
            messages=[{'role': 'user', 'content': full_prompt}],
            options=fast_options
        )
        reply = response['message']['content']
        if reply: return f"{prefix}{reply}"
    except Exception as e:
        app.logger.warning(f"Gemma 4 failed: {e}. Switching to Logic Core...")

    # --- ATTEMPT 2: DEEPSEEK R1 FULL (Deep Reasoning) ---
    try:
        response = ollama.chat(
            model=MODEL_LOGIC, 
            messages=[{'role': 'user', 'content': full_prompt}],
            options={"num_predict": 2048, "num_ctx": 8192}
        )
        reply = clean_reasoning(response['message']['content'])
        if reply: return f"{prefix}{reply}"
    except Exception:
        pass

    # --- ATTEMPT 3: DEEPSEEK R1 1.5B (Speed Reflex) ---
    try:
        response = ollama.chat(
            model=MODEL_REFLEX, 
            messages=[{'role': 'user', 'content': full_prompt}],
            options={"num_predict": 1024}
        )
        reply = clean_reasoning(response['message']['content'])
        if reply: return f"{prefix}{reply}"
    except Exception:
        pass

    # --- ATTEMPT 4: LLAMA 3.2 (Generalist) ---
    try:
        response = ollama.chat(model=MODEL_SPEED, messages=[{'role': 'user', 'content': full_prompt}])
        if response['message']['content']: return f"{prefix}{response['message']['content']}"
    except Exception:
        pass

    # --- ATTEMPT 5: GEMINI CLOUD FALLBACK ---
    if GOOGLE_API_KEY:
        try:
            client = genai.Client(api_key=GOOGLE_API_KEY)
            res = client.models.generate_content(model="gemini-2.0-flash", contents=full_prompt)
            return f"{prefix}{res.text}"
        except Exception:
            pass

    return "Neural link severed. Systems offline."

# --- AUTHENTICATION ROUTES ---
@app.route("/")
def main_portal(): 
    return redirect(url_for("mainpg"))

@app.route("/landing")
def landing(): 
    return render_template("landing.html")

@app.route("/mainpg")
def mainpg():
    return render_template("mainpg.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        u, p = request.form["username"].strip(), request.form["password"].strip()
        if create_user(u, generate_password_hash(p)):
            return redirect(url_for("login"))
        return "User already exists", 400
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u, p = request.form["username"].strip(), request.form["password"].strip()
        user = get_user(u)
        if user and check_password_hash(user[2], p):
            session["user"] = u
            return redirect(url_for("intelligence_hub"))
        return "Invalid credentials", 401
    return render_template("login.html")

# --- DASHBOARD ROUTES ---

@app.route("/intelligence")
def intelligence_hub():
    if "user" not in session: return redirect(url_for("login"))
    return render_template("intelligence.html")

@app.route("/dashboard")
def allintelligence_dashboard():
    if "user" not in session: return redirect(url_for("login"))
    return render_template("allintelligence.html", history=get_history(session["user"]))

@app.route("/human_dashboard")
def human_dashboard():
    if "user" not in session: return redirect(url_for("login"))
    return render_template("humanintelligence.html", user=session["user"], history=get_history(session["user"]))

@app.route("/financial_dashboard")
def financial_dashboard():
    if "user" not in session: return redirect(url_for("login"))
    return render_template("financialintelligence.html", history=get_history(session["user"]))

@app.route("/environmental_dashboard")
def environmental_dashboard():
    if "user" not in session: return redirect(url_for("login"))
    return render_template("environmentalintelligence.html", history=get_history(session["user"]))

@app.route("/animal_dashboard")
def animal_dashboard():
    if "user" not in session: return redirect(url_for("login"))
    return render_template("animalintelligence.html", history=get_history(session["user"]))

@app.route("/artificial_dashboard")
def artificial_dashboard():
    if "user" not in session: return redirect(url_for("login"))
    return render_template("dashboard.html", history=get_history(session["user"]))

@app.route("/medical_dashboard")
def medical_dashboard():
    if "user" not in session: return redirect(url_for("login"))
    return render_template("medichalintelligence.html", history=get_history(session["user"]))

@app.route("/gamming_dashboard")
def gamming_dashboard():
    if "user" not in session: return redirect(url_for("login"))
    return render_template("gammingintelligence.html", history=get_history(session["user"]))

@app.route("/musical_dashboard")
def musical_dashboard():
    if "user" not in session: return redirect(url_for("login"))
    return render_template("musicalintelligence.html", history=get_history(session["user"]))

@app.route("/map_dashboard")
def map_dashboard():
    if "user" not in session: return redirect(url_for("login"))
    return render_template("map.html", history=get_history(session["user"]))

@app.route("/movemap_dashboard")
def movemap_dashboard():
    if "user" not in session: return redirect(url_for("login"))
    return render_template("movemap.html", history=get_history(session["user"]))


# --- CHAT API ---

@app.route("/api/chat", methods=["POST"])
def chat():
    if "user" not in session: return jsonify({"response": "Unauthorized"}), 401
    data = request.json
    msg, emtn = data.get("message"), data.get("emotion", "neutral")
    
    reply = ask_ai(msg, emtn)
    save_chat(session["user"], msg, reply)
    
    return jsonify({"response": reply, "status": "success"})

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("landing"))

if __name__ == "__main__":
    app.run(debug=True, threaded=True, port=5000)
