import streamlit as st
import requests
import re
import os
from dotenv import load_dotenv

load_dotenv()

st.title("Ask Me Anything")

if "messages" not in st.session_state:
    st.session_state.messages = []
  
HF_TOKEN = os.getenv("HF_TOKEN")
API_URL = "https://router.huggingface.co/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
}

def query(messages):
    payload = {
        "messages": messages,
        "model": "HuggingFaceTB/SmolLM3-3B:hf-inference"
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

user_input = st.chat_input("Type your question...")

if user_input:
  st.session_state.messages.append({"role": "user", "content": user_input})
  response = query(st.session_state.messages)
  bot_content = response["choices"][0]["message"]["content"]
  cleaned = re.sub(r"<think>.*?</think>", "", bot_content, flags=re.DOTALL).strip()
  st.session_state.messages.append({"role": "assistant", "content": cleaned})
  st.chat_message("assistant").write(cleaned)
