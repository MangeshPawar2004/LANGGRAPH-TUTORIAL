import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage

CONFIG = {'configurable': {'thread_id': 'thread-1'}}
st.set_page_config(page_title="LangGraph Chatbot", page_icon="💬", layout="centered")

# -------------------- CUSTOM CSS --------------------
st.markdown("""
<style>
.chat-wrapper {
    max-width: 600px;
    margin: auto;
}

.stApp {
    background-color: #476a6f; /* Magnolia */
    font-family: 'Segoe UI', sans-serif;
}

/* Header */
.chat-header {
    text-align: center;
    font-size: 24px;
    font-weight: bold;
    padding: 12px;
    background: linear-gradient(90deg, #012622, #59114D); /* Dark green → Palatinate */
    border-radius: 12px;
    color: white;
    margin-bottom: 20px;
}

/* Chat bubbles */
.user-message, .assistant-message {
    padding: 10px 14px;
    border-radius: 16px;
    margin: 6px 0;
    display: inline-block;
    max-width: 80%;
    word-wrap: break-word;
    animation: fadeIn 0.3s ease-in-out;
}

/* User bubble */
.user-message {
    background-color: #140f2d; /* Dark green */
    color: white;
    align-self: flex-end;
}

/* Assistant bubble */
.assistant-message {
    background-color: #E98A15; /* Fulvous */
    color: black;
    align-self: flex-start;
}

/* Animation */
@keyframes fadeIn {
    from {opacity: 0; transform: translateY(5px);}
    to {opacity: 1; transform: translateY(0);}
}
</style>
""", unsafe_allow_html=True)

# -------------------- HEADER --------------------
st.markdown('<div class="chat-header">💬 LangGraph AI Assistant</div>', unsafe_allow_html=True)

# -------------------- SESSION STATE --------------------
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

# -------------------- CHAT DISPLAY --------------------
st.markdown('<div class="chat-wrapper">', unsafe_allow_html=True)
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        div_class = "user-message" if message['role'] == 'user' else "assistant-message"
        st.markdown(f'<div class="{div_class}">{message["content"]}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# -------------------- USER INPUT --------------------
user_input = st.chat_input("Type your message here...")

if user_input:
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.markdown(f'<div class="user-message">{user_input}</div>', unsafe_allow_html=True)

    ai_response = ""
    for message_chunk, metadata in chatbot.stream(
        {'messages': [HumanMessage(content=user_input)]},
        config=CONFIG,
        stream_mode='messages'
    ):
        ai_response += "".join(message_chunk.content) if hasattr(message_chunk.content, "__iter__") else str(message_chunk.content)

    with st.chat_message('assistant'):
        st.markdown(f'<div class="assistant-message">{ai_response}</div>', unsafe_allow_html=True)

    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_response})
