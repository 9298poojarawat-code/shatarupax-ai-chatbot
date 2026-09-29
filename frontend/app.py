import requests
import streamlit as st

BACKEND_URL = "https://shatarupax-ai-chatbot.onrender.com"
CHAT_ENDPOINT = f"{BACKEND_URL}/chat"
HEALTH_ENDPOINT = f"{BACKEND_URL}/health"

WELCOME_MESSAGE = "Hello! 👋 I'm the ShatarupaX AI Assistant. How can I help you today?"

SUGGESTIONS = [
    "What services does ShatarupaX AI Labs provide?",
    "What is Generative AI?",
    "What is RAG?",
    "How can AI help customer support?",
]

USER_AVATAR = ":material/person:"
BOT_AVATAR = ":material/support_agent:"

st.set_page_config(
    page_title="ShatarupaX AI Assistant",
    page_icon=":material/support_agent:",
    layout="centered",
)

CUSTOM_CSS = """
<style>
#MainMenu, footer {visibility: hidden;}

.hero {
    padding: 1.6rem 1.8rem;
    border-radius: 18px;
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 55%, #db2777 100%);
    color: #ffffff;
    margin-bottom: 1.2rem;
    box-shadow: 0 10px 30px rgba(79, 70, 229, 0.25);
}
.hero h1 {
    margin: 0;
    padding: 0;
    font-size: 2rem;
    color: #ffffff;
}
.hero p {
    margin: 0.4rem 0 0 0;
    font-size: 1rem;
    opacity: 0.92;
    color: #ffffff;
}

[data-testid="stChatMessage"] {
    border-radius: 16px;
    padding: 0.9rem 1rem;
    margin-bottom: 0.6rem;
    background: rgba(124, 58, 237, 0.06);
    border: 1px solid rgba(124, 58, 237, 0.12);
}

[data-testid="stChatMessageAvatarAssistant"] {
    background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
    color: #ffffff !important;
}
[data-testid="stChatMessageAvatarUser"] {
    background: #1e293b !important;
    color: #ffffff !important;
}

div.stButton > button {
    border-radius: 12px;
    border: 1px solid rgba(124, 58, 237, 0.35);
    transition: all 0.15s ease-in-out;
}
div.stButton > button:hover {
    border-color: #7c3aed;
    color: #7c3aed;
    transform: translateY(-1px);
}

.status-online {color: #16a34a; font-weight: 600;}
.status-offline {color: #dc2626; font-weight: 600;}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def backend_online() -> bool:
    try:
        return requests.get(HEALTH_ENDPOINT, timeout=2).status_code == 200
    except requests.exceptions.RequestException:
        return False


def ask_backend(message: str, history: list):
    """Sends the question (with recent history) to the backend. Returns: (reply_text, is_error)"""
    try:
        response = requests.post(
            CHAT_ENDPOINT,
            json={"message": message, "history": history},
            timeout=60,
        )

        if response.status_code == 200:
            return response.json()["response"], False

        if response.status_code == 422:
            return "Your message cannot be empty or too long. Please try again.", True

        detail = response.json().get("detail", "Unknown error")
        return f"Sorry, I couldn't generate a response: {detail}", True

    except requests.exceptions.ConnectionError:
        return (
            "Unable to connect to the server. "
            "Please make sure the backend is running (uvicorn backend.main:app --reload).",
            True,
        )
    except requests.exceptions.Timeout:
        return "The request timed out. Please try again.", True
    except Exception:
        return "Something went wrong. Please try again.", True


def reset_chat():
    st.session_state.chat_history = [
        {"role": "assistant", "content": WELCOME_MESSAGE, "error": False}
    ]
    st.session_state.pending_prompt = None


if "chat_history" not in st.session_state:
    reset_chat()
if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("## ShatarupaX AI Labs")
    st.write(
        "This AI assistant answers your questions about Generative AI, "
        "AI agents, RAG, and customer support."
    )
    st.divider()

    if backend_online():
        st.markdown('<span class="status-online">● Server online</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="status-offline">● Server offline</span>', unsafe_allow_html=True)

    st.divider()
    if st.button("🗑️ Clear Chat", use_container_width=True):
        reset_chat()
        st.rerun()

# ---------- Header ----------
st.markdown(
    """
    <div class="hero">
        <h1>ShatarupaX AI Assistant</h1>
        <p>Your smart guide to AI services, technology, and solutions. Ask me anything.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- Input ----------
prompt = st.chat_input("Type your question here...")
if st.session_state.pending_prompt:
    prompt = st.session_state.pending_prompt
    st.session_state.pending_prompt = None

if prompt is not None:
    prompt = prompt.strip()
    if not prompt:
        prompt = None

# ---------- Chat history ----------
for msg in st.session_state.chat_history:
    avatar = BOT_AVATAR if msg["role"] == "assistant" else USER_AVATAR
    with st.chat_message(msg["role"], avatar=avatar):
        if msg.get("error"):
            st.error(msg["content"])
        else:
            st.markdown(msg["content"])

# ---------- Suggestion buttons (only at the start) ----------
if len(st.session_state.chat_history) == 1 and not prompt:
    st.markdown("**Try asking:**")
    cols = st.columns(2)
    for i, suggestion in enumerate(SUGGESTIONS):
        if cols[i % 2].button(suggestion, key=f"sug_{i}", use_container_width=True):
            st.session_state.pending_prompt = suggestion
            st.rerun()

# ---------- New message ----------
if prompt:
    # Build recent history (skip the welcome message and any error messages)
    history = [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.chat_history[1:]
        if not m.get("error")
    ][-10:]

    st.session_state.chat_history.append(
        {"role": "user", "content": prompt, "error": False}
    )
    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar=BOT_AVATAR):
        with st.spinner("Thinking..."):
            reply, is_error = ask_backend(prompt, history)
        if is_error:
            st.error(reply)
        else:
            st.markdown(reply)

    st.session_state.chat_history.append(
        {"role": "assistant", "content": reply, "error": is_error}
    )