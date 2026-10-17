import time

from grok_service import get_grok_response
from google_service import get_google_response
from ollama_service import get_ollama_response


def generate_response(prompt):
    """
    Main AI router:
    Priority → Grok → Google → Ollama
    """

    providers = [
        ("Grok", get_grok_response),
        ("Google", get_google_response),
        ("Ollama", get_ollama_response)
    ]

    for name, func in providers:
        try:
            start = time.time()

            response = func(prompt)

            end = time.time()

            print(f"[INFO] {name} used | Time: {round(end - start, 2)}s")

            if response and len(response.strip()) > 0:
                return response

        except Exception as e:
            print(f"[ERROR] {name} failed: {e}")
            continue

    return "⚠️ All AI services are currently unavailable. Try again later."