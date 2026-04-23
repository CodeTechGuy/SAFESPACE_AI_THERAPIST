
import streamlit as st
import requests

BACKEND_URL = "http://localhost:5729/ask"

st.set_page_config(page_title="AI Mental Health Therapist", layout="wide")
st.title("🧠 SafeSpace – AI Mental Health Therapist")


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


user_input = st.chat_input("What's on your mind today?")
if user_input:
    # Append user message
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    
    # AI Agent exists here
    response = requests.post(BACKEND_URL, json={"message": user_input})

    st.session_state.chat_history.append({"role": "assistant", "content": f'{response.json()["response"]}'})


# Step3: Show response from backend
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
