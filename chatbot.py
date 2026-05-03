import streamlit as st
from groq import Groq
import json, os, time, uuid

# ================= CONFIG =================
st.set_page_config(page_title="EL LOCO MUÑOZ AI", layout="wide")

CHAT_FILE = "chat_history.json"

# ================= STORAGE =================
def load_chats():
    if os.path.exists(CHAT_FILE):
        with open(CHAT_FILE, "r") as f:
            return json.load(f)
    return []

def save_chats():
    with open(CHAT_FILE, "w") as f:
        json.dump(st.session_state.chats, f)

# ================= SESSION =================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chats" not in st.session_state:
    st.session_state.chats = load_chats()

if "chat_id" not in st.session_state:
    st.session_state.chat_id = None

if "title" not in st.session_state:
    st.session_state.title = "Nuova chat"

# ================= API =================
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    client = None

# ================= UTILS =================
def new_chat():
    st.session_state.messages = []
    st.session_state.chat_id = None
    st.session_state.title = "Nuova chat"

def typing(text):
    box = st.empty()
    full = ""
    for w in text.split():
        full += w + " "
        box.markdown(full)
        time.sleep(0.02)

def generate_title(user, bot):
    if not client:
        return user[:20]
    try:
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Crea titolo max 4 parole"},
                {"role": "user", "content": user + bot}
            ],
            max_tokens=10
        )
        return res.choices[0].message.content.strip()
    except:
        return user[:20]

# ================= COMMANDS =================
def commands(p):
    p = p.lower()
    if p == "/help":
        return "Comandi: /storia /motivami /insulta"
    if p == "/storia":
        return "Savoia 1908. Identità. Orgoglio. Battaglia."
    if p == "/motivami":
        return "Non mollare mai. Testa alta."
    if p == "/insulta":
        return "Qua si combatte. Non fare il morto."
    return None

# ================= SIDEBAR =================
with st.sidebar:
    st.title("⚪ LOCO AI")

    if st.button("➕ Nuova Chat"):
        new_chat()
        st.rerun()

    mode = st.toggle("Modalità Loco 🔥", True)

    st.markdown("---")

    for chat in st.session_state.chats:
        if st.button(chat["title"]):
            st.session_state.messages = chat["messages"]
            st.session_state.chat_id = chat["id"]
            st.session_state.title = chat["title"]
            st.rerun()

# ================= CHAT UI =================
st.title("EL LOCO MUÑOZ AI")
st.caption(st.session_state.title)

if not client:
    st.error("Inserisci API KEY nei secrets")
    st.stop()

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Scrivi..."):

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()

# ================= RESPONSE =================
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":

    prompt = st.session_state.messages[-1]["content"]

    with st.chat_message("assistant"):

        cmd = commands(prompt)

        if cmd:
            response = cmd
            typing(response)

        else:
            system = (
                "Sei El Loco Muñoz, ultras del Savoia. Diretto, potente, carismatico."
                if mode else
                "Assistente AI utile e preciso."
            )

            try:
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": system}] + st.session_state.messages
                )
                response = completion.choices[0].message.content
                typing(response)

            except:
                response = "Errore AI"

        st.session_state.messages.append({"role": "assistant", "content": response})

        # SAVE CHAT
        if st.session_state.chat_id is None:
            cid = str(uuid.uuid4())
            title = generate_title(prompt, response)

            st.session_state.chats.insert(0, {
                "id": cid,
                "title": title,
                "messages": list(st.session_state.messages)
            })

            st.session_state.chat_id = cid
            st.session_state.title = title

        else:
            for c in st.session_state.chats:
                if c["id"] == st.session_state.chat_id:
                    c["messages"] = list(st.session_state.messages)

        save_chats()
        st.rerun()
