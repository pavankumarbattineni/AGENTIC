import streamlit as st
import asyncio
import uuid
from coordinator import ResearchCoordinator
from streamlit.runtime.scriptrunner import add_script_run_ctx
import threading
from streamlit.components.v1 import html

st.set_page_config(page_title="Deep Research", layout="wide")
st.markdown("""
    <style>
    .user-msg {
        background-color: #005eff;
        color: white;
        padding: 0.75rem 1rem;
        border-radius: 1rem;
        margin: 0.5rem 0;
        max-width: 80%;
        float: right;
        clear: both;
    }
    .ai-msg {
        background-color: #f1f1f1;
        color: black;
        padding: 0.75rem 1rem;
        border-radius: 1rem;
        margin: 0.5rem 0;
        max-width: 80%;
        float: left;
        clear: both;
    }
    </style>
""", unsafe_allow_html=True)

st.title(" Deep Research")

# --- Session State Setup ---
if "chat_id" not in st.session_state:
    st.session_state.chat_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []
if "running" not in st.session_state:
    st.session_state.running = False

# --- Sidebar: New Chat ---
with st.sidebar:
    st.header("🧠 Research Sessions")
    if st.button("➕ New Chat"):
        st.session_state.chat_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.experimental_rerun()

# --- Chat Display Area ---
chat_container = st.container()
with chat_container:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"<div class='user-msg'>{msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='ai-msg'>{msg['content']}</div>", unsafe_allow_html=True)

# --- Chat Input ---
user_input = st.chat_input("Ask your research question here...")

# --- Async Task Execution Helper ---
def run_async_task(coro):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    add_script_run_ctx(threading.current_thread())
    return loop.run_until_complete(coro)

# --- On Submit ---
if user_input and not st.session_state.running:
    st.session_state.running = True
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.spinner("Researching with agents..."):
        try:
            coordinator = ResearchCoordinator(user_input)
            report_md = run_async_task(coordinator.research())
            st.session_state.messages.append({"role": "ai", "content": report_md})
        except Exception as e:
            st.error(f"Error: {str(e)}")
    st.session_state.running = False
    st.rerun()