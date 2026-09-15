import requests
import streamlit as st

BACKEND_URL = "http://localhost:8000"
CHAT_ENDPOINT = f"{BACKEND_URL}/chat"

st.set_page_config(page_title="ShatarupaX AI Assistant", page_icon="🤖")
st.title("🤖 ShatarupaX AI Assistant")
st.caption("Apne sawaal poochiye - services, technology, ya kuch bhi general.")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

with st.sidebar:
    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

for role, text in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(text)

user_input = st.chat_input("Apna sawaal type karein...")

if user_input:
    st.session_state.chat_history.append(("user", user_input))
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Soch raha hoon..."):
            try:
                response = requests.post(
                    CHAT_ENDPOINT,
                    json={"message": user_input},
                    timeout=35
                )

                if response.status_code == 200:
                    reply = response.json()["response"]
                    st.markdown(reply)
                    st.session_state.chat_history.append(("assistant", reply))

                elif response.status_code == 422:
                    st.warning("Sawaal khaali nahi ho sakta. Kuch likhein.")

                else:
                    error_detail = response.json().get("detail", "Unknown error")
                    st.error(f"Sorry, jawab nahi de paaya: {error_detail}")

            except requests.exceptions.ConnectionError:
                st.error(
                    "Backend se connect nahi ho paaya. "
                    "Kya FastAPI server chalu hai? (uvicorn backend.main:app --reload)"
                )

            except requests.exceptions.Timeout:
                st.error("Request timeout ho gaya. Dobara try karein.")

            except Exception:
                st.error("Kuch unexpected galat ho gaya. Please try again.")