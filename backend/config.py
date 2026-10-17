import os
from dotenv import load_dotenv

load_dotenv()

GROK_API_KEY = os.getenv("XAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")