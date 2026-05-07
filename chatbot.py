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
/* Sfondo e Font */
.stApp {{
    background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.95)), url("{BG}");
    background-size: cover;
    background-attachment: fixed;
}}

/* HEADER FISSO - Utilizziamo l'id per forzare Streamlit */
#custom-header {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 70px;
    background-color: white !important;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 999999;
    border-bottom: 2px solid #ddd;
}}

#custom-header h1 {{
    color: black !important;
    font-size: 22px !important;
    font-weight: 900;
    letter-spacing: 3px;
    margin: 0;
    padding: 0;
    text-transform: uppercase;
}}

/* Padding per il contenuto principale */
.main .block-container {{
    padding-top: 100px !important;
}}

/* Sidebar - Correzione visibilità */
[data-testid="stSidebar"] {{
    background-color: #fdfdfd !important;
    z-index: 1000000;
}}

/* Pulsante Sidebar - Lo spostiamo leggermente per non sovrapporsi al logo */
[data-testid="stSidebarCollapseButton"] {{
    position: fixed;
    top: 15px;
    left: 15px;
    z-index: 1000001;
    background-color: #eee !important;
    color: black !important;
    border-radius: 5px;
}}

/* Messaggi Chat */
.stChatMessage {{
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 15px !important;
    margin-bottom: 10px;
}}

.stChatMessage p {{
    color: white !important;
}}

/* Input Chat - Padding e Stile */
.stChatInputContainer {{
    padding: 20px !important;
    background-color: transparent !important;
}}

.stChatInput textarea {{
    border-radius: 20px !important;
    padding: 10px 20px !important;
}}

/* Home Card */
.home-container {{
    display:flex; flex-direction:column; align-items:center;
    justify-content:center; height:50vh; text-align:center;
}}
.home-card {{
    width: 350px; height: 180px; border-radius: 20px;
    background-image: url('{BG}'); background-size: cover;
    box-shadow: 0 15px 40px rgba(0,0,0,0.8);
    border: 2px solid rgba(255,255,255,0.2);
}}
</style>

<div id="custom-header">
    <img src="https://i.ibb.co/NgwLt8cT/logo-savoia.png" style="height: 40px; margin-right: 15px;">
    <h1>EL LOCO MUÑOZ AI</h1>
</div>
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
                {"role": "system", "content": "Crea un titolo di MAX 4 parole per questa conversazione analizzando utente e bot. No emoji."},
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
                if st.button("Elimina", key=f"del_{i}", use_container_width=True):
                    st.session_state.chats.pop(i)
                    save_chats()
                    new_chat()
                    st.rerun()

# ================= MAIN AREA =================
if not st.session_state.messages:
    st.markdown(f"""
    <div class="home-container">
        <div class="home-card"></div>
        <h2 style="color:white; margin-top:20px; letter-spacing:2px;">EL LOCO MUÑOZ</h2>
        <p style="color:#ccc; font-style:italic;">Sempre e ovunque, per la maglia.</p>
    </div>
    """, unsafe_allow_html=True)
else:
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

# ================= INPUT & RESPONSE =================
if prompt := st.chat_input("Scrivi al Loco..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    if client:
        # Mostriamo il messaggio dell'utente immediatamente
        st.rerun()

if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    if client:
        with st.chat_message("assistant"):
            sys_msg = "Sei El Loco Muñoz, ultras del Savoia 1908. Orgoglioso, verace e diretto."
            try:
                full_msgs = [{"role": "system", "content": sys_msg}] + st.session_state.messages
                comp = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=full_msgs,
                    temperature=0.7
                )
                res = comp.choices[0].message.content
                st.markdown(res)
                st.session_state.messages.append({"role": "assistant", "content": res})

                # Gestione salvataggio chat
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
