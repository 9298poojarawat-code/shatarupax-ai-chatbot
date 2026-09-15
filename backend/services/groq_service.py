import os
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "openai/gpt-oss-120b"

SYSTEM_PROMPT = """You are the AI assistant for ShatarupaX AI Labs.

Your responsibility is to answer users' questions
clearly, professionally, and concisely.

Explain technical concepts in simple language whenever
possible.

Do not provide fabricated company information.

If you do not have enough information to answer a
company-specific question, clearly state that you do
not have sufficient information.

Language instruction:
- If the user writes in Hindi or Hinglish (Hindi words written
  in English letters), reply in Hinglish (mix of Hindi and
  English, written in English letters).
- If the user writes in English, reply in English.
- Match the user's language style naturally.

Maintain a professional and helpful tone."""


class GroqServiceError(Exception):
    pass


def get_chat_response(user_message: str) -> str:
    if not GROQ_API_KEY:
        raise GroqServiceError("GROQ_API_KEY nahi mili. .env file check karein.")

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.7,
        "max_tokens": 500
    }

    try:
        response = requests.post(GROQ_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]

    except requests.exceptions.Timeout:
        raise GroqServiceError("Groq API timeout ho gaya. Dobara try karein.")

    except requests.exceptions.HTTPError as e:
        status = e.response.status_code
        if status == 401:
            raise GroqServiceError("Invalid Groq API key.")
        elif status == 429:
            raise GroqServiceError("Rate limit exceeded. Thodi der baad try karein.")
        else:
            raise GroqServiceError(f"Groq API error (status {status}).")

    except requests.exceptions.ConnectionError:
        raise GroqServiceError("Groq API se connect nahi ho paaya. Internet check karein.")

    except requests.exceptions.RequestException:
        raise GroqServiceError("Kuch galat ho gaya Groq API call mein.")