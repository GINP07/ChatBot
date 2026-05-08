import streamlit as st
from groq import Groq
import json, os, time, uuid
import docx  # Libreria per leggere il database

# ================= CONFIG (CON LOGO BROWSER) =================
st.set_page_config(
    page_title="EL LOCO MUÑOZ AI", 
    page_icon="https://i.ibb.co/NgwLt8cT/logo-savoia.png", 
    layout="wide"
)

# --- LINK E FILE ---
BG_GENERALE = "https://i.ibb.co/6cymMzFL/curva-savoia.jpg"
IMMAGINE_HOME_CENTRALE = "https://i.ibb.co/6cymMzFL/curva-savoia.jpg" 
LOGO_PICCOLO = "https://i.ibb.co/NgwLt8cT/logo-savoia.png"
CHAT_FILE = "chat_history.json"
DATABASE_FILE = "Database_Savoia.docx" # Assicurati che il file sia nella stessa cartella dello script

# ================= FUNZIONE CARICAMENTO DATI =================
def load_savoia_database(file_path):
    if os.path.exists(file_path):
        try:
            doc = docx.Document(file_path)
            full_text = []
            for para in doc.paragraphs:
                if para.text.strip():
                    full_text.append(para.text)
            return "\n".join(full_text)
        except Exception as e:
            return f"Errore caricamento database: {e}"
    return "Database non trovato."

# Carichiamo tutto il database all'avvio
KNOWLEDGE_BASE = load_savoia_database(DATABASE_FILE)

# ================= CSS PREMIUM (RESPONSIVE) =================
st.markdown(f"""
<style>
html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; }}
.stApp {{
    background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.95)), url("{BG_GENERALE}");
    background-size: cover;
    background-attachment: fixed;
}}
.block-container {{ padding-top: 50px !important; padding-bottom: 150px !important; }}
[data-testid="stSidebar"] {{ background: #fdfdfd !important; z-index: 1000 !important; }}
[data-testid="stSidebar"] * {{ color: #000000 !important; }}
.stChatMessage {{
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 15px !important;
    padding: 15px !important;
    margin-bottom: 10px;
}}
.stChatMessage div, .stChatMessage p, .stChatMessage span {{ color: #FFFFFF !important; font-size: 16px !important; }}
.stChatInputContainer {{ background-color: rgba(0,0,0,0.8) !important; padding: 20px 40px !important; }}

/* Home Card & Centratura */
.home-container {{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 65vh;
    text-align: center;
    width: 100%;
}}
.home-card {{
    width: 90%;
    max-width: 420px;
    height: 240px; 
    border-radius: 20px;
    background-image: url('{IMMAGINE_HOME_CENTRALE}'); 
    background-size: cover;
    background-position: center;
    box-shadow: 0 20px 60px rgba(0,0,0,0.8);
    border: 2px solid rgba(255,255,255,0.2);
    margin: 15px auto;
}}
.home-title {{ 
    margin-top: 25px; 
    color: #FFFFFF !important; 
    letter-spacing: 4px; 
    font-weight: 800; 
    text-transform: uppercase;
    font-size: 2.8rem;
}}
.home-sub {{ 
    color: #A52A2A !important; 
    font-style: italic; 
    font-weight: 800;
    font-size: 1.25rem;
    margin-top: 10px;
}}

@media (max-width: 768px) {{
    .home-title {{ font-size: 1.8rem !important; }}
    .home-sub {{ font-size: 1rem !important; }}
    .home-card {{ height: 180px; }}
}}
</style>
""", unsafe_allow_html=True)

# ================= STORAGE & SESSION =================
def load_chats():
    if os.path.exists(CHAT_FILE):
        try:
            with open(CHAT_FILE, "r") as f: return json.load(f)
        except: return []
    return []

def save_chats():
    with open(CHAT_FILE, "w") as f: json.dump(st.session_state.chats, f)

if "messages" not in st.session_state: st.session_state.messages = []
if "chats" not in st.session_state: st.session_state.chats = load_chats()
if "chat_id" not in st.session_state: st.session_state.chat_id = None

client = None
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ================= SIDEBAR =================
with st.sidebar:
    st.image("https://i.ibb.co/Xf5VVr4W/dani-munoz.png", use_container_width=True)
    if st.button("NUOVA CHAT", use_container_width=True):
        st.session_state.messages = []
        st.session_state.chat_id = None
        st.rerun()
    st.markdown("---")
    st.caption("CRONOLOGIA")
    for i, c in enumerate(st.session_state.chats):
        if st.button(c["title"], key=f"chat_{i}", use_container_width=True):
            st.session_state.messages = c["messages"]
            st.session_state.chat_id = c["id"]
            st.rerun()

# ================= MAIN AREA =================
if not st.session_state.messages:
    st.markdown(f"""
    <div class="home-container">
        <img src="{LOGO_PICCOLO}" style="width:70px; margin-bottom:20px;">
        <div class="home-card"></div>
        <h1 class="home-title">EL LOCO MUÑOZ</h1>
        <p class="home-sub">Sempre e ovunque, per la maglia.</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.image(LOGO_PICCOLO, width=50)
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.markdown(m["content"])

# ================= INPUT & RESPONSE =================
if prompt := st.chat_input("Scrivi al Loco..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()

if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    if client:
        with st.chat_message("assistant"):
            # INIETTIAMO IL DATABASE NEL SYSTEM MESSAGE
            sys_msg = f"""Sei El Loco Muñoz, ultras del Savoia 1908. Orgoglioso, diretto e passionale.
            Usa questo database ufficiale per rispondere a ogni domanda sulla storia, i giocatori e le stagioni del Savoia:
            
            {KNOWLEDGE_BASE}
            
            Se qualcuno ti chiede della stagione 2024/25 o 2025/26, sai che siamo tornati in Serie C! 
            Rispondi sempre con lo spirito della Curva Sud."""
            
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

                # Salvataggio chat
                if st.session_state.chat_id is None:
                    cid = str(uuid.uuid4())
                    st.session_state.chats.insert(0, {"id": cid, "title": "Conversazione Savoia", "messages": list(st.session_state.messages)})
                    st.session_state.chat_id = cid
                else:
                    for c in st.session_state.chats:
                        if c["id"] == st.session_state.chat_id: c["messages"] = list(st.session_state.messages)
                save_chats()
                st.rerun()
            except Exception as e:
                st.error(f"Errore: {e}")
