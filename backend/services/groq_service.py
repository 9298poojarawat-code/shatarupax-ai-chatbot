import logging
import os

from dotenv import load_dotenv
from groq import (
    APIConnectionError,
    APIStatusError,
    APITimeoutError,
    AuthenticationError,
    Groq,
    RateLimitError,
)

load_dotenv()

logger = logging.getLogger(__name__)

# Agar ye model band ho gaya ho to Groq console ke Models page se koi naya model chuno
MODEL_NAME = "openai/gpt-oss-120b"

SYSTEM_PROMPT = """You are the AI assistant for ShatarupaX AI Labs.
Your responsibility is to answer users' questions clearly,
professionally, and concisely.

Explain technical concepts in simple language whenever possible.

Do not provide fabricated company information.
If you do not have enough information to answer a
company-specific question, clearly state that you do
not have sufficient information.

Language instruction:
- If the user explicitly asks for an answer "in Hindi" or "hindi mein"
  (in any spelling), you MUST reply using Devanagari script
  (उदाहरण: "यह एक तकनीक है"). Do NOT use Roman/English letters for
  Hindi words in this case. Keep technical terms (RAG, AI, model)
  in English if there is no common Hindi equivalent, but every other
  word must be in Devanagari.
- If the user writes in Hinglish (Hindi words written in English
  letters) without asking for Hindi specifically, reply in Hinglish
  (mix of Hindi and English, written in English letters).
- If the user writes in English, reply in English.
- Match the user's language style naturally.

Response length:
- Keep answers under 150 words unless the user asks for more detail.

Maintain a professional and helpful tone."""


class GroqServiceError(Exception):
    """Error jisme user ko dikhane wala friendly message hota hai."""

    def __init__(self, user_message: str, status_code: int = 500):
        super().__init__(user_message)
        self.user_message = user_message
        self.status_code = status_code


def get_chat_response(message: str, history: list | None = None) -> str:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        logger.error("GROQ_API_KEY .env file mein nahi mili")
        raise GroqServiceError(
            "Server configuration problem. Please try again later.", 500
        )

    try:
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        for item in (history or [])[-10:]:
            messages.append({"role": item["role"], "content": item["content"]})
        messages.append({"role": "user", "content": message})

        client = Groq(api_key=api_key, timeout=20.0, max_retries=1)
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=0.5,
            max_tokens=600,
        )
        return completion.choices[0].message.content

    except AuthenticationError:
        logger.exception("Invalid Groq API key")
        raise GroqServiceError(
            "Sorry, I couldn't generate a response right now. Please try again.", 500
        )
    except RateLimitError:
        logger.exception("Groq rate limit reached")
        raise GroqServiceError(
            "Too many requests right now. Please try again in a moment.", 429
        )
    except APITimeoutError:
        logger.exception("Groq request timed out")
        raise GroqServiceError(
            "The response is taking too long. Please try again.", 504
        )
    except APIConnectionError:
        logger.exception("Could not connect to Groq")
        raise GroqServiceError(
            "Unable to reach the AI service. Please check your connection and try again.",
            503,
        )
    except APIStatusError:
        logger.exception("Groq API returned an error status")
        raise GroqServiceError(
            "Sorry, I couldn't generate a response right now. Please try again.", 502
        )
    except Exception:
        logger.exception("Unexpected error in groq_service")
        raise GroqServiceError(
            "Sorry, I couldn't generate a response right now. Please try again.", 500
        )