
import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage
import time

st.set_page_config(page_title="LangGraph Chatbot", page_icon="🤖", layout="centered")

st.markdown("""
<style>
body {
    background-color: #0d1117;
    color: white;
}

.chat-container {
    max-width: 800px;
    margin: auto;
    padding: 1rem;
}

.chat-header {
    text-align: center;
    font-size: 28px;
    font-weight: bold;
    padding: 1rem;
    border-radius: 14px;
    background: linear-gradient(to right, #4e54c8, #8f94fb);
    color: white;
    margin-bottom: 30px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
}

.chat-message {
    padding: 14px 18px;
    border-radius: 18px;
    margin-bottom: 18px;
    max-width: 75%;
    font-size: 16px;
    line-height: 1.4;
    position: relative;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.25);
}

.user-msg {
    background: #cbc0bd;
    margin-left: auto;
    color: #001e00;
    border-bottom-right-radius: 4px;
}

.user-msg::after {
    content: "";
    position: absolute;
    right: -10px;
    top: 15px;
    border-width: 10px 0 10px 10px;
    border-style: solid;
    border-color: transparent transparent transparent #cda0bd;
}

.assistant-msg {
    background: #ffffff;
    margin-right: auto;
    color: #0b0f19;
    border-bottom-left-radius: 4px;
}

.assistant-msg::after {
    content: "";
    position: absolute;
    left: -10px;
    top: 15px;
    border-width: 10px 10px 10px 0;
    border-style: solid;
    border-color: transparent #ffffff transparent transparent;
}

.stChatInput input {
    background-color: #21262d !important;
    color: white !important;
    border-radius: 16px;
    padding: 12px !important;
    border: none;
    font-size: 16px;
    outline: none;
}

.stChatInput input:focus {
    border: 1px solid #8f94fb !important;
}

.stChatInput button {
    border: none !important;
    background: transparent !important;
}

.loading {
    color: #8f94fb;
    font-size: 16px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

CONFIG = {'configurable': {'thread_id': 'thread-1'}}

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

# Chat container
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
st.markdown('<div class="chat-header">💬 LangGraph Chatbot</div>', unsafe_allow_html=True)

# Display messages
for msg in st.session_state['message_history']:
    role = msg['role']
    content = msg['content']

    bubble_class = 'user-msg' if role == 'user' else 'assistant-msg'
    st.markdown(f'<div class="chat-message {bubble_class}">{content}</div>', unsafe_allow_html=True)

# Chat input
user_input = st.chat_input("Type your message...")

if user_input:
    # Add and show user message
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    st.markdown(f'<div class="chat-message user-msg">{user_input}</div>', unsafe_allow_html=True)

    # Show loading message
    loading_message = st.empty()
    loading_message.markdown('<div class="loading">AI is generating a response...</div>', unsafe_allow_html=True)

    # Call LangGraph bot
    response = chatbot.invoke({'messages': [HumanMessage(content=user_input)]}, config=CONFIG)
    bot_reply = response['messages'][-1].content

    # Clear loading message
    loading_message.empty()

    # Add and show assistant message
    st.session_state['message_history'].append({'role': 'assistant', 'content': bot_reply})
    st.markdown(f'<div class="chat-message assistant-msg">{bot_reply}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  
