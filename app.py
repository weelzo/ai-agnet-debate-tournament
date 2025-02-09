import streamlit as st
import requests
from debate_visualizer import visualize_debate

st.set_page_config(layout="wide")

st.title("🤖 AI Agent Debate Tournament")

topic = st.text_input("Enter a debate topic:", "Should AI replace human judges?")

def get_message_style(role):
    if role == "Proponent":
        return "info"
    elif role == "Opponent":
        return "warning"
    elif role == "Moderator":
        return "success"
    elif role == "Judge":
        return "error"
    else:
        return "info"

def get_role_emoji(role):
    if role == "Topic":
        return "🎤"
    elif role == "Proponent":
        return "🟢"
    elif role == "Opponent":
        return "🔴"
    elif role == "Moderator":
        return "⚖️"
    elif role == "Judge":
        return "👨‍⚖️"
    else:
        return ""

if st.button("Start Debate"):
    with st.spinner("Debate in progress..."):
        response = requests.get(f"http://127.0.0.1:8000/debate?topic={topic}")
        debate_results = response.json()

        # Create two columns
        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader("💬 Debate Conversation")
            
            # Display each round of the debate
            current_round = -1
            for message in debate_results["rounds"]:
                if message["round"] != current_round:
                    current_round = message["round"]
                    if current_round > 0:
                        st.write(f"\n### Round {current_round}")
                
                message_style = get_message_style(message["role"])
                emoji = get_role_emoji(message["role"])
                
                if message["type"] == "topic":
                    st.write(f"### {emoji} Topic: {message['text']}")
                else:
                    st.write(f"{emoji} **{message['role']}**")
                    getattr(st, message_style)(message["text"])

        with col2:
            st.subheader("🖼️ Debate Visualization")
            # Generate visualization
            visualize_debate(debate_results)
            st.image("debate_graph.png", use_container_width=True)