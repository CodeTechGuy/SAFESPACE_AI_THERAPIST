import streamlit as st
import requests
import time

st.set_page_config(page_title="SafeSpace AI", layout="centered")


st.markdown("""
<style>
.user-msg {
    background-color: #2563eb;
    color: white;
    padding: 12px;
    border-radius: 12px;
    margin: 8px 0;
    text-align: right;
}

.bot-msg {
    background-color: #1e293b;
    color: white;
    padding: 12px;
    border-radius: 12px;
    margin: 8px 0;
    text-align: left;
}
</style>
""", unsafe_allow_html=True)


if "messages" not in st.session_state:
    st.session_state.messages = []


st.markdown("<h2 style='text-align:center;'>  SafeSpace AI</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:gray;'>I'm here to listen.</p>", unsafe_allow_html=True)


if len(st.session_state.messages) == 0:
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Hi, I’m here with you. How are you feeling today?"
    })


for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='user-msg'>{msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-msg'>{msg['content']}</div>", unsafe_allow_html=True)


user_input = st.chat_input("Type your message...")

if user_input:
    
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    
    with st.spinner("Listening..."):
        time.sleep(1.2)

        try:
            response = requests.post(
                "http://localhost:5729/ask",
                json={"message": user_input}
            ).json()

            bot_reply = response.get("response", "I'm here with you.")
        except:
            bot_reply = "⚠️ I'm having trouble responding right now."

    # Save bot reply
    st.session_state.messages.append({
        "role": "assistant",
        "content": bot_reply
    })

    st.rerun()
