import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.models.schemas import ChatRequest, ChatResponse
from backend.services.groq_service import get_chat_response, GroqServiceError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("shatarupax-chatbot")

app = FastAPI(title="ShatarupaX AI Chatbot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "ShatarupaX AI Chatbot API is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        reply = get_chat_response(request.message)
        return ChatResponse(response=reply)

    except GroqServiceError as e:
        logger.error(f"Groq service error: {e}")
        raise HTTPException(status_code=502, detail=str(e))

    except Exception:
        logger.exception("Unexpected error in /chat endpoint")
        raise HTTPException(
            status_code=500,
            detail="Sorry, kuch galat ho gaya. Please try again."
        )