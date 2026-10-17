import requests
from config import GROK_API_KEY

def get_grok_response(prompt):
    if not GROK_API_KEY:
        raise Exception("Missing GROK_API_KEY")

    url = ""

    headers = {
        "Authorization": f"Bearer {GROK_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "grok-1",
        "messages": [{"role": "user", "content": prompt}]
    }

    res = requests.post(url, json=data, headers=headers, timeout=10)

    if res.status_code != 200:
        raise Exception(f"Grok API Error: {res.text}")

    return res.json()["choices"][0]["message"]["content"]