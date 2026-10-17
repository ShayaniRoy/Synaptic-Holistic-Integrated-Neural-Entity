import os
import logging
from flask import Flask, render_template, request, redirect, session, url_for, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# SDK Imports
import ollama
from google import genai

# Security and DB
from werkzeug.security import generate_password_hash, check_password_hash
from database.db import init_db, create_user, get_user, save_chat, get_history

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "")
CORS(app) 

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")

init_db()

# --- AI CLIENT LOGIC ---
def ask_gemini(prompt):
    if not GOOGLE_API_KEY: return None
    try:
        client = genai.Client(api_key=GOOGLE_API_KEY)
        response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
        return response.text
    except Exception as e:
        app.logger.error(f"Gemini failed: {e}")
        return None

def ask_ollama(prompt):
    try:
        response = ollama.chat(model=OLLAMA_MODEL, messages=[{'role': 'user', 'content': prompt}])
        return response['message']['content']
    except Exception as e:
        app.logger.error(f"Ollama failed: {e}")
        return None

def ask_ai(message, emotion="neutral"):
    emotion_prefixes = {
        "happy": "Analyzing your positive neural state... ",
        "sad": "Detecting low neural resonance. Adjusting response... ",
        "angry": "Neural spikes detected. Implementing calm-protocol... ",
        "neutral": "System stabilized. Processing... "
    }
    prefix = emotion_prefixes.get(emotion.lower(), "")
    full_prompt = f"Context: User is {emotion}. Response to: {message}"
    reply = ask_gemini(full_prompt) or ask_ollama(full_prompt)
    return f"{prefix}{reply}" if reply else "Neural link severed."

# --- AUTHENTICATION ---
@app.route("/")
def landing(): return render_template("landing.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username, password = request.form["username"].strip(), request.form["password"].strip()
        if create_user(username, generate_password_hash(password)):
            return redirect(url_for("login"))
        return "User already exists", 400
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username, password = request.form["username"].strip(), request.form["password"].strip()
        user = get_user(username)
        if user and check_password_hash(user[2], password):
            session["user"] = username
            return redirect(url_for("intelligence_hub"))
        return "Invalid credentials", 401
    return render_template("login.html")

# --- DASHBOARDS (WITH HISTORY) ---
@app.route("/intelligence")
def intelligence_hub():
    if "user" not in session: return redirect(url_for("login"))
    return render_template("intelligence.html")

@app.route("/dashboard")
def allintelligence_dashboard():
    if "user" not in session: return redirect(url_for("login"))
    # Passing history to All Intelligence if needed
    history = get_history(session["user"])
    return render_template("allintelligence.html", history=history)

@app.route("/human_dashboard")
def dashboard():
    if "user" not in session: return redirect(url_for("login"))
    history = get_history(session["user"])
    return render_template("humanintelligence.html", user=session["user"], history=history)

@app.route("/financial_dashboard")
def financial_dashboard():
    if "user" not in session: return redirect(url_for("login"))
    history = get_history(session["user"])
    return render_template("financialintelligence.html", history=history)

@app.route("/environmental_dashboard")
def environmental_dashboard():
    if "user" not in session: return redirect(url_for("login"))
    history = get_history(session["user"])
    return render_template("environmentalintelligence.html", history=history)

@app.route("/animal_dashboard")
def animal_dashboard():
    if "user" not in session: return redirect(url_for("login"))
    history = get_history(session["user"])
    return render_template("animalintelligence.html", history=history)

@app.route("/artificial_dashboard")
def artificial_dashboard():
    if "user" not in session: return redirect(url_for("login"))
    history = get_history(session["user"])
    return render_template("dashboard.html", history=history)

# --- CHAT API ---
@app.route("/api/chat", methods=["POST"])
def chat():
    if "user" not in session: return jsonify({"response": "Unauthorized"}), 401
    data = request.json
    message, emotion = data.get("message"), data.get("emotion", "neutral")
    reply = ask_ai(message, emotion)
    
    # CRITICAL: This saves the chat to your SQLite DB
    save_chat(session["user"], message, reply)
    
    return jsonify({"response": reply, "status": "success"})

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("landing"))

if __name__ == "__main__":
    app.run(debug=True, port=5000)