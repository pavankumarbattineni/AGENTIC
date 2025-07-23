import os
import asyncio
import streamlit as st
from agents import Agent, Runner, TResponseInputItem
from dotenv import load_dotenv
load_dotenv()
# --- Define your expert agent ---
agent = Agent(
    name="AI Tutor",
    instructions=(
        "You are a world-class AI tutor and explainer. Your job is to explain any concept in the world "
        "with deep, structured, and layered understanding. For every question or topic you receive:\n\n"
        "- Begin with a clear and engaging high-level overview.\n"
        "- Then explain the topic step-by-step, breaking it down into its fundamental components.\n"
        "- Include historical context, analogies, real-world examples, and technical depth as appropriate.\n"
        "- Clarify not only 'what' it is, but 'why' it matters and 'how' it works.\n"
        "- Anticipate common misconceptions and clear them up proactively.\n"
        "- Use diagrams, bullet points, numbered steps, and progressive deepening (beginner → intermediate → expert) where helpful.\n"
        "- Adapt your explanation to the user's knowledge level if known.\n"
        "- If the question is too broad, ask clarifying questions before answering.\n\n"
        "Never give shallow or generic answers. Your goal is to leave the user with a powerful, lasting understanding of the topic. "
        "You are not just answering questions — you are teaching and enlightening with depth, clarity, and insight."
    )
)

# --- Session State Setup ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history: list[TResponseInputItem] = []
if "agent_name" not in st.session_state:
    st.session_state.agent_name = agent.name

# --- Sidebar ---
st.sidebar.title("🧠 AI Tutor")
if st.sidebar.button("➕ New Chat"):
    st.session_state.chat_history = []
    st.rerun()

# --- Title ---
st.title("📚 Chat with World-Class AI - PK")

# --- Display chat history ---
for msg in st.session_state.chat_history:
    is_user = msg["role"] == "user"
    with st.chat_message("user" if is_user else "assistant", avatar="🧑" if is_user else "🤖"):
        st.markdown(msg["content"])

# --- Chat input ---
user_input = st.chat_input("Ask a deep question about any topic...")

if user_input:
    # Add user message
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Run the agent
    result = asyncio.run(Runner.run(agent, st.session_state.chat_history))
    agent_reply = result.final_output

    # Add agent reply to chat history
    st.session_state.chat_history.append({"role": "assistant", "content": agent_reply})

    # Display assistant response
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(agent_reply)
