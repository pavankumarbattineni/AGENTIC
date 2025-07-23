import streamlit as st
import asyncio
from dotenv import load_dotenv
from agents import Agent, Runner, handoff, RunContextWrapper

load_dotenv()
# Callback functions
def on_math_handoff(ctx: RunContextWrapper[None]):
    st.toast("Handing off to the math tutor agent")

def on_history_handoff(ctx: RunContextWrapper[None]):
    st.toast("Handing off to the history tutor agent")

# Define specialist agents
math_tutor_agent = Agent(
    name="Math Tutor",
    handoff_description="Specialist agent for math questions",
    instructions="You provide assistance with math queries. Explain your reasoning at each step and include examples.",
    handoffs=[]
)

history_tutor_agent = Agent(
    name="History Tutor",
    handoff_description="Specialist agent for historical questions",
    instructions="You provide assistance with historical queries. Explain important events and context clearly.",
    handoffs=[]
)

# Cross handoffs
math_tutor_agent.handoffs = [handoff(history_tutor_agent, on_handoff=on_history_handoff)]
history_tutor_agent.handoffs = [handoff(math_tutor_agent, on_handoff=on_math_handoff)]

# Triage agent
triage_agent = Agent(
    name="Triage Agent",
    instructions="You determine which agent to use based on the user's homework question. If neither agent is relevant, provide a general response.",
    handoffs=[
        handoff(history_tutor_agent, on_handoff=on_history_handoff),
        handoff(math_tutor_agent, on_handoff=on_math_handoff)
    ]
)

# --- Session State Setup ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "last_agent" not in st.session_state:
    st.session_state.last_agent = triage_agent

# --- Sidebar: New Chat ---
st.sidebar.title("🧠 Multi-Agent Tutor")
if st.sidebar.button("➕ New Chat"):
    st.session_state.chat_history = []
    st.session_state.last_agent = triage_agent
    st.rerun()

# --- Chat UI ---
st.title("🗨️ Chat with Agent PK")

# Display chat history
for msg in st.session_state.chat_history:
    is_user = msg["role"] == "user"
    with st.chat_message("user" if is_user else "assistant", avatar="🧑" if is_user else "🤖"):
        st.markdown(msg["content"])

# Chat input
user_input = st.chat_input("Ask  anything about Mathematics and History...")
if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Run the agent
    result = asyncio.run(Runner.run(st.session_state.last_agent, st.session_state.chat_history))

    agent_reply = result.final_output

    # Save assistant reply and agent state
    st.session_state.chat_history.append({"role": "assistant", "content": agent_reply})
    st.session_state.last_agent = result.last_agent

    # Display reply
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(agent_reply)
