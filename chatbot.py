import streamlit as st
from groq import Groq
import json, os, time, uuid

# ================= CONFIG =================
st.set_page_config(page_title="EL LOCO MUÑOZ AI", layout="wide")

BG = "https://i.ibb.co/6cymMzFL/curva-savoia.jpg"
CHAT_FILE = "chat_history.json"

# ================= CSS =================
st.markdown(f"""
<style>
.stApp {{
    background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.95)),
    url("{BG}");
    background-size: cover;
}}

.header {{
    position: fixed;
    top: 0;
    width: 100%;
    height: 70px;
    background: rgba(0,0,0,0.95);
    display: flex;
    align-items: center;
    justify-content: center;
    border-bottom: 2px solid white;
    z-index: 999;
}}

.title {{
    color: white;
    font-weight: 900;
    letter-spacing: 3px;
}}

.subtitle {{
    color: #aaa;
    font-size: 11px;
}}

.stChatMessage {{
    background: rgba(255,255,255,0.05) !important;
    border-radius: 15px !important;
    border: 1px solid rgba(255,255,255,0.1);
}}

[data-testid="stSidebar"] {{
    background: #000;
}}

button {{
    font-weight: 800 !important;
}}
</style>

<div class="header">
    <div style="text-align:center;">
        <div class="title">EL LOCO MUÑOZ AI</div>
        <div class="subtitle">SANGUE BIANCOSCUDATO</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ================= STORAGE =================
def load():
    if os.path.exists(CHAT_FILE):
        with open(CHAT_FILE, "r") as f:
            return json.load(f)
    return []

def save():
    with open(CHAT_FILE, "w") as f:
        json.dump(st.session_state.chats, f)

# ================= SESSION =================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chats" not in st.session_state:
    st.session_state.chats = load()

if "chat_id" not in st.session_state:
    st.session_state.chat_id = None

# ================= API =================
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    client = None

# ================= UTILS =================
def new_chat():
    st.session_state.messages = []
    st.session_state.chat_id = None

def typing(text):
    box = st.empty()
    full = ""
    for w in text.split():
        full += w + " "
        box.markdown(full)
        time.sleep(0.015)

def title_gen(u, a):
    try:
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "titolo corto"},
                {"role": "user", "content": u + a}
            ],
            max_tokens=10
        )
        return res.choices[0].message.content
    except:
        return u[:20]

# ================= COMMANDS =================
def cmd(p):
    p = p.lower()
    if "/storia" in p:
        return "Savoia 1908. Non è calcio. È identità."
    if "/motivami" in p:
        return "Stringi i denti. Sempre."
    if "/insulta" in p:
        return "Muoviti. Qua non si piange."
    return None

# ================= SIDEBAR =================
with st.sidebar:

    st.markdown("## ⚪ CURVA")

    if st.button("NUOVA CHAT"):
        new_chat()
        st.rerun()

    st.markdown("---")

    for c in st.session_state.chats:
        if st.button(c["title"]):
            st.session_state.messages = c["messages"]
            st.session_state.chat_id = c["id"]
            st.rerun()

# ================= CHAT =================
st.markdown("<br><br><br>", unsafe_allow_html=True)

if not client:
    st.error("API KEY mancante")
    st.stop()

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Parla..."):

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()

# ================= RESPONSE =================
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":

    prompt = st.session_state.messages[-1]["content"]

    with st.chat_message("assistant"):

        c = cmd(prompt)

        if c:
            res = c
            typing(res)

        else:
            system = """
            Sei El Loco Muñoz.
            Ultras del Savoia 1908.
            Parli con orgoglio, rabbia controllata, mentalità da curva.
            Frasi brevi, dirette, forti.
            Mai banale.
            """

            try:
                comp = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": system}] + st.session_state.messages
                )
                res = comp.choices[0].message.content
                typing(res)
            except:
                res = "Errore."

        st.session_state.messages.append({"role": "assistant", "content": res})

        # SAVE
        if st.session_state.chat_id is None:
            cid = str(uuid.uuid4())
            title = title_gen(prompt, res)

            st.session_state.chats.insert(0, {
                "id": cid,
                "title": title,
                "messages": list(st.session_state.messages)
            })

            st.session_state.chat_id = cid
        else:
            for c in st.session_state.chats:
                if c["id"] == st.session_state.chat_id:
                    c["messages"] = list(st.session_state.messages)

        save()
        st.rerun()
