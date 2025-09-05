import streamlit as st
from groq import Groq

st.set_page_config(page_title="SmartStudy AI", page_icon="📘")
st.title("📘 SmartStudy AI (Groq-powered Chatbot)")

# 🔑 API Key input (on the main page, not sidebar)
api_key = st.text_input("Enter your Groq API Key", type="password")

# Stop app until key is provided
if not api_key:
    st.warning("Please enter your API key above to continue.")
    st.stop()

# Create Groq client
client = Groq(api_key=api_key)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful AI tutor for NCERT and State board syllabus."}
    ]

# Show chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.markdown(msg["content"])
    elif msg["role"] == "assistant":
        with st.chat_message("assistant"):
            st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Ask me anything from NCERT or State syllabus..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=st.session_state.messages
            )
            reply = response.choices[0].message.content
            st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
