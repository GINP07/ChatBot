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
    background: linear-gradient(rgba(0,0,0,0.75), rgba(0,0,0,0.9)),
    url("{BG}");
    background-size: cover;
}}

.block-container {{
    padding-top: 90px;
}}

/* HEADER */
.header {{
    position: fixed;
    top: 0;
    width: 100%;
    height: 70px;
    background: rgba(0,0,0,0.9);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 999;
}}
.header h1 {{
    color: white;
    margin: 0;
    font-size: 20px;
    letter-spacing: 2px;
}}

/* SIDEBAR */
[data-testid="stSidebar"] {{
    background: #e6e6e6;
}}
[data-testid="stSidebar"] button {{
    background: transparent !important;
    color: #000 !important;
    border: none !important;
    text-align: left !important;
}}
[data-testid="stSidebar"] button:hover {{
    background: #d0d0d0 !important;
}}

/* CHAT */
.stChatMessage {{
    background: rgba(255,255,255,0.05) !important;
    border-radius: 12px !important;
}}

/* INPUT */
.stChatInput {{
    max-width: 600px;
    margin: auto;
}}
.stChatInput input {{
    border-radius: 20px !important;
}}
</style>

<div class="header">
    <h1>EL LOCO MUÑOZ AI</h1>
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
client = None
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    pass

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

def generate_title(user, bot):
    try:
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Crea un titolo breve (max 5 parole) basato su domanda e risposta."},
                {"role": "user", "content": f"{user} {bot}"}
            ],
            max_tokens=15
        )
        return res.choices[0].message.content.strip()
    except:
        return "Conversazione"

# ================= SIDEBAR =================
with st.sidebar:

    if st.button("Nuova chat"):
        new_chat()
        st.rerun()

    st.markdown("---")

    for i, c in enumerate(st.session_state.chats):

        col1, col2 = st.columns([0.85, 0.15])

        with col1:
            if st.button(c["title"], key=f"chat_{i}"):
                st.session_state.messages = c["messages"]
                st.session_state.chat_id = c["id"]
                st.rerun()

        with col2:
            with st.popover("⋮", key=f"menu_{i}"):

                if st.button("Rinomina", key=f"ren_{i}"):
                    new = st.text_input("Nuovo nome", value=c["title"], key=f"in_{i}")
                    if new:
                        st.session_state.chats[i]["title"] = new
                        save()
                        st.rerun()

                if st.button("Elimina", key=f"del_{i}"):
                    st.session_state.chats.pop(i)
                    new_chat()
                    save()
                    st.rerun()

# ================= CHAT =================
if not client:
    st.error("API KEY mancante")
    st.stop()

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Chiedi al Loco"):

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()

# ================= RESPONSE =================
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":

    prompt = st.session_state.messages[-1]["content"]

    with st.chat_message("assistant"):

        system = """
        Sei El Loco Muñoz, ultras del Savoia.
        Parli con orgoglio, diretto, forte, mai banale.
        """

        try:
            comp = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": system}] + st.session_state.messages
            )
            res = comp.choices[0].message.content
            typing(res)
        except:
            res = "Errore AI"

        st.session_state.messages.append({"role": "assistant", "content": res})

        # CREATE CHAT SOLO DOPO RISPOSTA
        if st.session_state.chat_id is None:
            cid = str(uuid.uuid4())
            title = generate_title(prompt, res)

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
