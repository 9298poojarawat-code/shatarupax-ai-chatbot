import logging

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.models.schemas import ChatRequest, ChatResponse
from backend.services.groq_service import GroqServiceError, get_chat_response

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(title="ShatarupaX AI Chatbot API", version="0.1.0")

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
        answer = get_chat_response(
            request.message, [m.model_dump() for m in request.history]
        )
        return ChatResponse(response=answer)
    except GroqServiceError as e:
        raise HTTPException(status_code=e.status_code, detail=e.user_message)
    except Exception:
        logger.exception("Unexpected error in /chat")
        raise HTTPException(
            status_code=500,
            detail="Sorry, I couldn't generate a response right now. Please try again.",
        )