import google.genai as genai
from config import GOOGLE_API_KEY

def get_google_response(prompt):
    if not GOOGLE_API_KEY:
        raise Exception("Missing GOOGLE_API_KEY")

    genai.configure(api_key=GOOGLE_API_KEY)

    model = genai.GenerativeModel("gemini-pro")

    response = model.generate_content(prompt)

    if not response.text:
        raise Exception("Empty response from Google")

    return response.text