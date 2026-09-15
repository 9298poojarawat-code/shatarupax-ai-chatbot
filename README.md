# ShatarupaX AI Assistant

Ek AI-powered customer support chatbot jo Groq API, FastAPI, aur Streamlit
use karke bana hai.

## Architecture

User → Streamlit (frontend) → FastAPI (backend) → Groq API → LLM

Streamlit kabhi bhi Groq ko directly call nahi karta - har request
FastAPI backend se hokar jaati hai.

## Technology Stack

- **Language:** Python
- **Backend:** FastAPI
- **Frontend:** Streamlit
- **LLM Provider:** Groq API
- **Validation:** Pydantic
- **HTTP:** requests
- **Env variables:** python-dotenv
- **Server:** Uvicorn

## Project Structure

## Installation

1. Virtual environment banayein:

2. Dependencies install karein:

3. `.env` file banayein (root folder mein) aur apni Groq API key daalein:
   (`.env.example` file dekh sakte hain reference ke liye)

## How to Run

**Step 1 — Backend chalayein** (project root folder se, ek terminal mein):
Backend yahan chalega: http://localhost:8000
API docs yahan dekh sakte hain: http://localhost:8000/docs

**Step 2 — Frontend chalayein** (doosre terminal mein):
Browser mein automatically khul jayega: http://localhost:8501

Dono terminal ek saath chalu rehne chahiye - backend pehle start karein,
fir frontend.

## API Endpoints

| Method | Endpoint  | Description                    |
|--------|-----------|---------------------------------|
| GET    | `/`       | Backend running hai ya nahi     |
| GET    | `/health` | Health check                    |
| POST   | `/chat`   | Message bhejo, response paao    |

### Example `/chat` request:
```json
{ "message": "What is Generative AI?" }
```

### Example `/chat` response:
```json
{ "response": "Generative AI is..." }
```

## Example Questions

- What services does ShatarupaX AI Labs provide?
- What is Generative AI?
- What is RAG?
- generative ai kya hota hai (Hindi/Hinglish support bhi hai)

## Known Limitations

- Company-specific documents se answer nahi de sakta (RAG future mein add hoga)
- Chat history sirf browser session tak rehti hai, restart hone par gayab ho jaati hai
- Koi authentication/login system nahi hai

## Future Improvements

- Company documents ke liye RAG add karna
- Database mein chat history save karna
- User authentication
- Cloud par deploy karna
