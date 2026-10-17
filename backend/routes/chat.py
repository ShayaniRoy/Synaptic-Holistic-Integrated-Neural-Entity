import os
import ollama
from dotenv import load_dotenv
from google import genai
from openai import OpenAI

# Load variables from .env
load_dotenv()

# Retrieve keys from environment
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
'''GROK_API_KEY = os.getenv("XAI_API_KEY")'''
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")

def chat_with_google(prompt):
    client = genai.Client(api_key=GOOGLE_API_KEY)
    response = client.models.generate_content(
        model="gemini-3-flash-preview", 
        contents=prompt
    )
    return response.text


def chat_with_ollama(prompt):
    response = ollama.chat(
        model="llama3.2",
        messages=[{'role': 'user', 'content': prompt}]
    )
    return response['message']['content']

def main():
    print("--- Multi-Model Chat (Environment Mode) ---")
    print("Select: [1] Gemini | [2] Ollama")
    choice = input("Choice: ")
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ['exit', 'quit']: break

        try:
            if choice == '1':
                print(f"\nGemini: {chat_with_google(user_input)}")
            elif choice == '2':
                print(f"\nOllama: {chat_with_ollama(user_input)}")
            else:
                print("Selection error.")
                break
        except Exception as e:
            print(f"Connection Error: {e}")

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Critical for browser-to-python communication

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "").lower()

        # Simple logic gate for responses
        if "status" in user_message:
            reply = "Neural Core: Optimal. All nodes are synchronized."
        elif "market" in user_message or "price" in user_message:
            reply = "Market Intel: Bitcoin is currently trading at $77,135."
        elif "weather" in user_message:
            reply = "Atmospheric conditions in Kolkata: 34°C, Partly Sunny."
        else:
            reply = f"Nexus processed: '{user_message}'. No anomalies detected."

        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": f"Internal Core Error: {str(e)}"}), 500

if __name__ == '__main__':
    print("Nexus Bridge active on http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
if __name__ == "__main__":
    main()