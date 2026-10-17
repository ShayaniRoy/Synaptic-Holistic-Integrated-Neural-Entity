import requests
from config import OLLAMA_BASE_URL

def get_ollama_response(prompt):
    url = f"{OLLAMA_BASE_URL}/api/generate"

    data = {
        "model": "llama3.2",
        "prompt": prompt,
        "stream": False
    }

    res = requests.post(url, json=data, timeout=15)

    if res.status_code != 200:
        raise Exception("Ollama not responding")

    result = res.json()

    return result.get("response", "")