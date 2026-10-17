from flask import Flask, request, jsonify
import base64
import os

app = Flask(__name__)

# Folder to save captured frames if you want to inspect them
UPLOAD_FOLDER = 'space_logs'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def save_debug_image(b64_string, prefix):
    """Helper to save incoming Base64 frames as JPG files"""
    if not b64_string:
        return None
    try:
        # Remove header (data:image/jpeg;base64,)
        header, encoded = b64_string.split(",", 1)
        data = base64.b64decode(encoded)
        filename = f"{prefix}_capture.jpg"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        with open(filepath, "wb") as f:
            f.write(data)
        return filepath
    except Exception as e:
        print(f"Error decoding image: {e}")
        return None

@app.route('/chat.py', methods=['POST'])
def handle_chat():
    data = request.json
    
    user_message = data.get('message', '')
    bio_frame = data.get('biometrics') # Base64 string
    env_frame = data.get('environment') # Base64 string
    emotion = data.get('emotion_tag', '[ UNKNOWN ]')

    # 1. Process images (Optional: Save them to disk to see if it's working)
    bio_path = save_debug_image(bio_frame, "bio")
    env_path = save_debug_image(env_frame, "env")

    print(f"--- Incoming Transmission ---")
    print(f"User: {user_message}")
    print(f"Detected Emotion: {emotion}")
    if bio_path: print(f"Biometrics saved to: {bio_path}")
    if env_path: print(f"Environment saved to: {env_path}")
    print(f"-----------------------------")

    # 2. Logic for AI Response
    # Here you would typically call an LLM (OpenAI, Gemini, etc.)
    # For now, let's create a cosmos-themed response based on the emotion
    
    if "HAPPY" in emotion:
        reply = f"Your neural rhythm is vibrant. The stars reflect your light. You said: '{user_message}'"
    elif "FOCUSED" in emotion:
        reply = f"Logic gates stable. I am processing your inquiry with maximum precision: '{user_message}'"
    else:
        reply = f"Signal received across the void. Analyzing your request... '{user_message}'"

    return jsonify({
        "status": "success",
        "reply": reply,
        "received_emotion": emotion
    })

if __name__ == '__main__':
    # Run on port 5000
    app.run(debug=True, port=5000)