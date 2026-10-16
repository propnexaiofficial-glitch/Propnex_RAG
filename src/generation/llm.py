import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
_client = None


def generate(prompt: str) -> str:
    global _client
    if _client is None:
        _client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    resp = _client.models.generate_content(
        model=os.getenv("GEMINI_MODEL"),
        contents=prompt,
    )
    return resp.text