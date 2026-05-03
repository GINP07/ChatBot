import streamlit as st
from groq import Groq
import re
import json
import os
import time
from streamlit_extras.stylable_container import stylable_container

# --- CONFIG ---
st.set_page_config(page_title="EL LOCO MUÑOZ AI", page_icon="⚪", layout="wide")

CHAT_FILE = "chat_history.json"

# --- STORAGE ---
def save_chats():
    with open(CHAT_FILE, "w") as f:
        json.dump(st.session_state.chat_sessions, f)

def load_chats():
    if os.path.exists(CHAT_FILE):
        with open(CHAT_FILE, "r") as f:
            return json.load(f)
    return []

# --- SESSION ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = load_chats()
if "current_title" not in st.session_state:
    st.session_state.current_title = "Nuova chat"
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None

# API
try:
    API_KEY = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=API_KEY)
except:
    client = None

# --- UTILS ---
def reset_chat():
    st.session_state.messages = []
    st.session_state.current_title = "Nuova chat"
    st.session_state.current_chat_id = None

def generate_title(user, assistant):
    if not client:
        return user[:20]
    try:
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Titolo breve max 4 parole"},
                {"role": "user", "content": user + assistant}
            ],
            max_tokens=10
        )
        return res.choices[0].message.content.strip()
    except:
        return user[:20]

def handle_commands(prompt):
    p = prompt.lower()
    if p == "/help":
        return "Comandi: /storia /motivami /insulta"
    if p == "/storia":
        return "Savoia 1908: storia, sangue e appartenenza."
    if p == "/motivami":
        return "Non mollare. Mai."
    if p == "/insulta":
        return "Muoviti. Qui si lotta."
    return None

def type_effect(text):
    placeholder = st.empty()
    full = ""
    for w in text.split():
        full += w + " "
        placeholder.markdown(full)
        time.sleep(0.02)

# --- UI ---
st.markdown("""
<style>
.stApp {background: black;}
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:

    if st.button("NUOVA CHAT"):
        reset_chat()
        st.rerun()

    mode_loco = st.toggle("Modalità Loco 🔥", True)

    st.markdown("---")

    for i, s in enumerate(st.session_state.chat_sessions):
        if st.button(s["title"], key=i):
            st.session_state.messages = s["content"]
            st.session_state.current_chat_id = s["id"]
            st.session_state.current_title = s["title"]
            st.rerun()

# --- CHAT ---
if not client:
    st.error("API KEY mancante")
else:

    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    if prompt := st.chat_input("Scrivi..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.rerun()

    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":

        prompt = st.session_state.messages[-1]["content"]

        with st.chat_message("assistant"):

            cmd = handle_commands(prompt)

            if cmd:
                res = cmd
                type_effect(res)

            else:
                if mode_loco:
                    sys = "Sei El Loco Muñoz, ultras del Savoia. Risposte forti, corte."
                else:
                    sys = "Assistente AI utile."

                try:
                    completion = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "system", "content": sys}] + st.session_state.messages
                    )
                    res = completion.choices[0].message.content
                    type_effect(res)

                except:
                    res = "Errore AI"

            st.session_state.messages.append({"role": "assistant", "content": res})

            # SAVE CHAT
            if st.session_state.current_chat_id is None:
                cid = f"id_{len(st.session_state.chat_sessions)}"
                title = generate_title(prompt, res)

                st.session_state.chat_sessions.insert(0, {
                    "id": cid,
                    "title": title,
                    "content": list(st.session_state.messages)
                })

                st.session_state.current_chat_id = cid
                st.session_state.current_title = title
            else:
                for s in st.session_state.chat_sessions:
                    if s["id"] == st.session_state.current_chat_id:
                        s["content"] = list(st.session_state.messages)

            save_chats()
            st.rerun()
