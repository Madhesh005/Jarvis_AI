import os
import streamlit as st
import requests
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("❌ API key not found in .env. Please add GEMINI_API_KEY.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.0-flash")

# Load your personal context from file
try:
    with open("madhesh_profile.md", "r", encoding="utf-8") as file:

        USER_KNOWLEDGE = file.read()
except Exception as e:
    USER_KNOWLEDGE = "Madhesh is a passionate developer."  # fallback
    st.warning(f"Couldn't load profile file: {e}")

# UI setup
st.set_page_config(page_title="Madhesh's AI Assistant", page_icon="👾", layout="centered")

# Sidebar with info
with st.sidebar:
    st.image("https://img.icons8.com/color/96/artificial-intelligence.png", width=60)

    st.markdown("""
    ## 🧠 Jarvis - AI Assistant  
    Personal AI assistant trained to help Madhesh with anything from ideas to coding to life advice!

    ##  About Madhesh

    🔹 *Developer & Creator* of this AI  
    🔹 Passionate about AI, Web Dev, and Hackathons  
    🔹 *Portfolio*:  [@Madhesh](http://madheshworks.netlify.app)

    ---
    ### 💡 Tips:
    - Ask me to write, code, or summarize
    - Explore ideas or debug issues
    - Plan your trip or build your startup

    🛠 “Ask me anything, anytime.”

    """, unsafe_allow_html=True)

st.markdown("""
<h1 style='text-align:center;'>🤖 Jarvis – AI Assistant for Madhesh</h1>
<p style='text-align:center; color:gray;'>Ask about his skills, projects, or career.</p>
""", unsafe_allow_html=True)

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input prompt
prompt = st.chat_input("Ask something about Madhesh...")

if prompt:
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        full_prompt = f"{USER_KNOWLEDGE}\n\nUser: {prompt}\nAssistant:"
        with st.spinner("Thinking... 🤔"):
            response = model.generate_content(full_prompt)
            reply = response.text.strip()
    except Exception as e:
        reply = f"⚠️ Error: {str(e)}"

    st.chat_message("assistant").markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
