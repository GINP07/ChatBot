import streamlit as st
from groq import Groq
import json, os, time, uuid

# ================= CONFIG =================
st.set_page_config(page_title="EL LOCO MUÑOZ AI", layout="wide")

BG = "https://i.ibb.co/6cymMzFL/curva-savoia.jpg"
CHAT_FILE = "chat_history.json"

# ================= CSS PREMIUM =================
st.markdown(f"""
<style>

/* GLOBAL */
html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
}}

/* BACKGROUND */
.stApp {{
    background:
    linear-gradient(rgba(0,0,0,0.82), rgba(0,0,0,0.92)),
    url("{BG}");
    background-size: cover;
    background-attachment: fixed;
}}

/* HEADER */
.header {{
    position: fixed;
    top: 0;
    width: 100%;
    height: 70px;
    background: rgba(0,0,0,0.95);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 999;
    border-bottom: 1px solid rgba(255,255,255,0.1);
}}

.header h1 {{
    color: white;
    font-size: 20px;
    letter-spacing: 2px;
    margin: 0;
}}

.block-container {{
    padding-top: 100px;
}}

/* SIDEBAR */
[data-testid="stSidebar"] {{
    background: #f2f2f2;
}}

[data-testid="stSidebar"] * {{
    color: #000 !important;
}}

[data-testid="stSidebar"] button {{
    background: transparent !important;
    border: none !important;
    text-align: left !important;
}}

[data-testid="stSidebar"] button:hover {{
    background: #e0e0e0 !important;
}}

/* CHAT */
.stChatMessage {{
    background: rgba(0,0,0,0.6) !important;
    border-radius: 14px !important;
    padding: 12px !important;
}}

/* INPUT */
.stChatInput {{
    max-width: 600px;
    margin: auto;
}}

.stChatInput input {{
    border-radius: 25px !important;
    padding: 12px !important;
    background: #fff !important;
    color: #000 !important;
}}

/* HOME CARD */
.home-card {{
    width: 420px;
    height: 240px;
    border-radius: 18px;
    background-image: url('{BG}');
    background-size: cover;
    box-shadow: 0 30px 80px rgba(0,0,0,0.8);
    border: 1px solid rgba(255,255,255,0.1);
    transition: all 0.4s ease;
}}

.home-card:hover {{
    transform: scale(1.03);
    box-shadow: 0 40px 100px rgba(0,0,0,0.9);
}}

.home-container {{
    display:flex;
    flex-direction:column;
    align-items:center;
    justify-content:center;
    height:60vh;
    text-align:center;
}}

.home-title {{
    margin-top:30px;
    color:white;
    letter-spacing:3px;
}}

.home-sub {{
    color:#aaa;
}}

</style>

<div class="header">
    <h1>EL LOCO MUÑOZ AI</h1>
</div>
""", unsafe_allow_html=True)

# ================= STORAGE =================
def load_chats():
    try:
        if os.path.exists(CHAT_FILE):
            with open(CHAT_FILE, "r") as f:
                return json.load(f)
    except:
        return []
    return []

def save_chats():
    try:
        with open(CHAT_FILE, "w") as f:
            json.dump(st.session_state.chats, f)
    except:
        pass

# ================= SESSION =================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chats" not in st.session_state:
    st.session_state.chats = load_chats()

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
                {"role": "system", "content": "Crea titolo breve (max 5 parole) basato su domanda e risposta."},
                {"role": "user", "content": f"{user} {bot}"}
            ],
            max_tokens=15
        )
        return res.choices[0].message.content.strip()
    except:
        return "Chat"

# ================= SIDEBAR =================
with st.sidebar:

    if st.button("Nuova chat"):
        new_chat()
        st.rerun()

    st.markdown("---")

    for i, c in enumerate(st.session_state.chats):
        col1, col2 = st.columns([0.8, 0.2])

        with col1:
            if st.button(c["title"], key=f"chat_{i}"):
                st.session_state.messages = c["messages"]
                st.session_state.chat_id = c["id"]
                st.rerun()

        with col2:
            if st.button("✕", key=f"del_{i}"):
                st.session_state.chats.pop(i)
                new_chat()
                save_chats()
                st.rerun()

# ================= HOME / CHAT =================
if not st.session_state.messages:

    st.markdown(f"""
    <div class="home-container">

        <div class="home-card"></div>

        <h2 class="home-title">CHIEDI AL LOCO...</h2>
        <p class="home-sub">Orgoglio. Identità. Savoia.</p>

    </div>
    """, unsafe_allow_html=True)

else:
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

# ================= INPUT =================
if prompt := st.chat_input("Chiedi al Loco"):

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()

# ================= RESPONSE =================
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":

    prompt = st.session_state.messages[-1]["content"]

    with st.chat_message("assistant"):

        system = """
        Sei El Loco Muñoz, ultras del Savoia.
        Diretto, carismatico, mai banale.
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

        save_chats()
        st.rerun()
