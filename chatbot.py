import streamlit as st
from groq import Groq
import json, os, time, uuid

# ================= CONFIG (CON LOGO BROWSER) =================
st.set_page_config(
    page_title="EL LOCO MUÑOZ AI", 
    page_icon="https://i.ibb.co/NgwLt8cT/logo-savoia.png", 
    layout="wide"
)

BG = "https://i.ibb.co/6cymMzFL/curva-savoia.jpg"
CHAT_FILE = "chat_history.json"

# ================= CSS PREMIUM =================
st.markdown(f"""
<style>
/* Font e Sfondo */
html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
}}

.stApp {{
    background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.95)), url("{BG}");
    background-size: cover;
    background-attachment: fixed;
}}

/* Padding ricalibrato senza header fisso */
.block-container {{ 
    padding-top: 30px !important; 
    padding-bottom: 150px !important; 
}}

/* Sidebar */
[data-testid="stSidebar"] {{ 
    background: #fdfdfd !important; 
    z-index: 1000000 !important; 
}}

/* TASTO SIDEBAR SEMPRE VISIBILE */
[data-testid="stSidebarCollapseButton"] {{
    background-color: rgba(255,255,255,0.2) !important;
    border-radius: 8px !important;
    color: white !important;
}}

/* MESSAGGI CHAT */
.stChatMessage {{
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 15px !important;
    padding: 15px !important;
    margin-bottom: 10px;
}}
.stChatMessage div, .stChatMessage p, .stChatMessage span {{
    color: #FFFFFF !important;
    font-size: 16px !important;
}}

/* INPUT CHAT */
.stChatInputContainer {{
    background-color: rgba(0,0,0,0.8) !important;
    padding: 20px 40px !important;
}}

.stChatInput textarea {{
    background-color: #FFFFFF !important;
    color: #000000 !important;
    border-radius: 25px !important;
    padding: 15px 25px !important;
}}

/* Home Card & Layout Centrale */
.home-container {{
    display:flex; flex-direction:column; align-items:center;
    justify-content:center; height:70vh; text-align:center;
}}

/* Logo sopra il titolo */
.main-logo {{
    height: 80px;
    margin-bottom: 20px;
    filter: drop-shadow(0px 0px 10px rgba(255,255,255,0.3));
}}

.home-card {{
    width: 420px; height: 230px; border-radius: 20px;
    background-image: url('{BG}'); background-size: cover;
    box-shadow: 0 20px 60px rgba(0,0,0,0.8);
    border: 2px solid rgba(255,255,255,0.1);
    margin-bottom: 30px;
}}

.home-title {{ 
    color: #FFFFFF !important; 
    letter-spacing: 5px; 
    font-weight: 900; 
    font-size: 45px !important;
    text-transform: uppercase;
    margin: 0px !important;
}}

.home-sub {{ 
    color: #FF0000; /* Rosso Savoia */
    font-style: italic; 
    font-weight: 600;
    font-size: 18px;
    letter-spacing: 1px;
}}
</style>
""", unsafe_allow_html=True)

# ================= STORAGE =================
def load_chats():
    if os.path.exists(CHAT_FILE):
        try:
            with open(CHAT_FILE, "r") as f:
                return json.load(f)
        except: return []
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

# ================= API =================
client = None
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ================= UTILS =================
def new_chat():
    st.session_state.messages = []
    st.session_state.chat_id = None

def generate_title(user, bot):
    if not client: return "Nuova Chat"
    try:
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Crea un titolo di MAX 4 parole per questa conversazione. No emoji."},
                {"role": "user", "content": f"U: {user}\nA: {bot}"}
            ],
            max_tokens=10
        )
        return res.choices[0].message.content.strip().replace('"', '')
    except: return "Savoia Chat"

# ================= SIDEBAR =================
with st.sidebar:
    st.image("https://i.ibb.co/Xf5VVr4W/dani-munoz.png", use_container_width=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("NUOVA CHAT", use_container_width=True):
        new_chat()
        st.rerun()

    st.markdown("---")
    st.caption("CRONOLOGIA")

    for i, c in enumerate(st.session_state.chats):
        col1, col2 = st.columns([0.8, 0.2])
        with col1:
            if st.button(c["title"], key=f"chat_{i}", use_container_width=True):
                st.session_state.messages = c["messages"]
                st.session_state.chat_id = c["id"]
                st.rerun()
        with col2:
            with st.popover("", key=f"menu_{i}"):
                new_n = st.text_input("Rinomina", value=c["title"], key=f"ren_input_{i}")
                if st.button("Salva", key=f"save_{i}", use_container_width=True):
                    st.session_state.chats[i]["title"] = new_n
                    save_chats()
                    st.rerun()
                st.markdown("---")
                if st.button("Elimina", key=f"del_{i}", use_container_width=True):
                    st.session_state.chats.pop(i)
                    save_chats()
                    new_chat()
                    st.rerun()

# ================= MAIN AREA =================
if not st.session_state.messages:
    # SPAZIO CENTRALE GRANDE (Invece dell'header)
    st.markdown(f"""
    <div class="home-container">
        <img src="https://i.ibb.co/NgwLt8cT/logo-savoia.png" class="main-logo">
        <h1 class="home-title">EL LOCO MUÑOZ</h1>
        <p class="home-sub">Oltre la categoria, solo per la maglia.</p>
        <div class="home-card"></div>
    </div>
    """, unsafe_allow_html=True)
else:
    # Quando la chat inizia, mostriamo un piccolo logo in alto per coerenza
    st.image("https://i.ibb.co/NgwLt8cT/logo-savoia.png", width=60)
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

# ================= INPUT & RESPONSE =================
if prompt := st.chat_input("Scrivi al Loco..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()

if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    if client:
        with st.chat_message("assistant"):
            sys_msg = "Sei El Loco Muñoz, ultras del Savoia 1908. Sei verace, fiero, parli in modo diretto e passionale della tua squadra e della tua città (Torre Annunziata)."
            try:
                full_msgs = [{"role": "system", "content": sys_msg}] + st.session_state.messages
                comp = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=full_msgs,
                    temperature=0.8
                )
                res = comp.choices[0].message.content
                st.markdown(res)
                st.session_state.messages.append({"role": "assistant", "content": res})

                if st.session_state.chat_id is None:
                    cid = str(uuid.uuid4())
                    title = generate_title(prompt, res)
                    st.session_state.chats.insert(0, {"id": cid, "title": title, "messages": list(st.session_state.messages)})
                    st.session_state.chat_id = cid
                else:
                    for c in st.session_state.chats:
                        if c["id"] == st.session_state.chat_id:
                            c["messages"] = list(st.session_state.messages)
                save_chats()
                st.rerun()
            except Exception as e:
                st.error(f"Errore: {e}")
