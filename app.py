import streamlit as st
from groq import Groq

st.set_page_config(page_title="SmartStudy AI", page_icon="📘")
st.title("📘 SmartStudy AI (Groq-powered Chatbot)")

# 1) Try to load key from secrets.toml
api_key = None
try:
    api_key = st.secrets.get("GROQ_API_KEY", None)
except Exception:
    api_key = None

# 2) If not found, ask in sidebar
with st.sidebar:
    st.header("Settings")
    if not api_key:
        api_key = st.text_input("Enter your Groq API Key", type="password")
    st.caption("You can store it in .streamlit/secrets.toml as GROQ_API_KEY.")

# Stop if no key
if not api_key:
    st.error("❌ Please provide a Groq API Key (in secrets or sidebar).")
    st.stop()

# Create Groq client
client = Groq(api_key=api_key)

# Session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system",
         "content": (
             "You are SmartStudy AI, a friendly tutor for Grade 9 students. "
             "Focus on NCERT and Indian State Board syllabi. Explain simply, with steps and examples."
         )}
    ]

# Tools: Clear chat
col1, col2 = st.columns(2)
with col1:
    if st.button("🧹 Clear chat"):
        st.session_state.messages = st.session_state.messages[:1]
        st.experimental_rerun()
with col2:
    st.caption("Model: Groq Mixtral-8x7b-32768")

# Show history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.markdown(msg["content"])
    elif msg["role"] == "assistant":
        with st.chat_message("assistant"):
            st.markdown(msg["content"])

# Chat input
prompt = st.chat_input("Ask from NCERT/State syllabus…")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate reply
    with st.chat_message("assistant"):
        with st.spinner("Thinking…"):
            resp = client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=st.session_state.messages,
                temperature=0.3,
                max_tokens=800
            )
            reply = resp.choices[0].message.content
            st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
