import streamlit as st
from groq import Groq
import google.generativeai as genai
import json, os, time, uuid
import docx

# ================= CONFIG (CON LOGO BROWSER) =================
st.set_page_config(
    page_title="EL LOCO MUÑOZ AI", 
    page_icon="https://i.ibb.co/NgwLt8cT/logo-savoia.png", 
    layout="wide"
)

# --- LINK IMMAGINI ---
BG_GENERALE = "https://i.ibb.co/6cymMzFL/curva-savoia.jpg"
IMMAGINE_HOME_CENTRALE = "https://i.ibb.co/6cymMzFL/curva-savoia.jpg" 
LOGO_PICCOLO = "https://i.ibb.co/NgwLt8cT/logo-savoia.png"
CHAT_FILE = "chat_history.json"
DATABASE_FILE = "Database_Savoia.docx"

# ================= FUNZIONE CARICAMENTO DATABASE =================
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

KNOWLEDGE_BASE = load_savoia_database(DATABASE_FILE)

# ================= CSS PREMIUM =================
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
[data-testid="stSidebar"] [data-testid="stImage"] img {{ pointer-events: none !important; user-select: none !important; cursor: default !important; }}
[data-testid="stSidebar"] * {{ color: #000000 !important; }}
[data-testid="stSidebar"] button {{ background: transparent !important; border: 1px solid #eee !important; text-align: left !important; margin-bottom: 5px; }}
[data-testid="stSidebar"] button:hover {{ background: #f0f0f0 !important; }}
.stChatMessage {{ background: rgba(255,255,255,0.08) !important; border: 1px solid rgba(255,255,255,0.15) !important; border-radius: 15px !important; padding: 15px !important; margin-bottom: 10px; }}
.stChatMessage div, .stChatMessage p, .stChatMessage span {{ color: #FFFFFF !important; font-size: 16px !important; }}
.stChatInputContainer {{ background-color: rgba(0,0,0,0.8) !important; padding: 20px 40px !important; border-top: 1px solid rgba(255,255,255,0.1); }}
.stChatInput textarea {{ background-color: #FFFFFF !important; color: #000000 !important; border-radius: 25px !important; padding: 15px 25px !important; line-height: 1.5 !important; }}
.home-container {{ display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 65vh; text-align: center; width: 100%; padding: 0 10px; }}
.logo-home-mini {{ width: 70px; margin-bottom: 20px; filter: drop-shadow(0 2px 5px rgba(0,0,0,0.5)); }}
.home-card {{ width: 90%; max-width: 420px; height: 240px; border-radius: 20px; background-image: url('{IMMAGINE_HOME_CENTRALE}'); background-size: cover; background-position: center; box-shadow: 0 20px 60px rgba(0,0,0,0.8); border: 2px solid rgba(255,255,255,0.2); margin: 15px auto; }}
.home-title {{ margin-top: 25px; color: #FFFFFF !important; letter-spacing: 4px; font-weight: 800; text-transform: uppercase; font-size: 2.8rem; width: 100%; }}
.home-sub {{ color: #A52A2A !important; font-style: italic; font-weight: 800; font-size: 1.25rem; margin-top: 10px; width: 100%; text-shadow: 1px 1px 2px rgba(0,0,0,0.5); }}
@media (max-width: 768px) {{
    .home-title {{ font-size: 1.8rem !important; letter-spacing: 2px; }}
    .home-sub {{ font-size: 1rem !important; }}
    .home-card {{ height: 180px; }}
}}
</style>
""", unsafe_allow_html=True)

# ================= STORAGE =================
def load_chats():
    if os.path.exists(CHAT_FILE):
        try:
            with open(CHAT_FILE, "r") as f: return json.load(f)
        except: return []
    return []

def save_chats():
    with open(CHAT_FILE, "w") as f: json.dump(st.session_state.chats, f)

# ================= SESSION =================
if "messages" not in st.session_state: st.session_state.messages = []
if "chats" not in st.session_state: st.session_state.chats = load_chats()
if "chat_id" not in st.session_state: st.session_state.chat_id = None

# ================= API CONFIG =================
client_groq = None
if "GROQ_API_KEY" in st.secrets:
    client_groq = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model_gemini = genai.GenerativeModel(model_name="gemini-1.5-flash")
else:
    st.error("Manca GEMINI_API_KEY nei Secrets!")

# ================= UTILS =================
def new_chat():
    st.session_state.messages = []
    st.session_state.chat_id = None

def generate_title(user, bot):
    try:
        prompt_title = f"Crea un titolo di MAX 4 parole per questa conversazione. No emoji.\nU: {user}\nA: {bot}"
        if "GEMINI_API_KEY" in st.secrets:
            res = model_gemini.generate_content(prompt_title, safety_settings=[{"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"}])
            return res.text.strip().replace('"', '')
    except: pass
    return "Savoia Chat"

# ================= SIDEBAR =================
with st.sidebar:
    st.image("https://i.ibb.co/Xf5VVr4W/dani-munoz.png", use_container_width=True)
    if st.button("NUOVA CHAT", use_container_width=True):
        new_chat()
        st.rerun()
    st.markdown("---")
    for i, c in enumerate(st.session_state.chats):
        if st.button(c["title"], key=f"chat_{i}", use_container_width=True):
            st.session_state.messages = c["messages"]
            st.session_state.chat_id = c["id"]
            st.rerun()

# ================= MAIN AREA =================
if not st.session_state.messages:
    st.markdown(f'<div class="home-container"><img src="{LOGO_PICCOLO}" class="logo-home-mini"><div class="home-card"></div><h1 class="home-title">EL LOCO MUÑOZ</h1><p class="home-sub">Sempre e ovunque, per la maglia.</p></div>', unsafe_allow_html=True)
else:
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.markdown(m["content"])

# ================= INPUT & RESPONSE =================
if prompt := st.chat_input("Scrivi al Loco..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()

if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant"):
        sys_msg = f"Sei El Loco Muñoz, ultras del Savoia. Usa: {KNOWLEDGE_BASE}"
        try:
            history_text = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
            full_prompt = f"{sys_msg}\n\n{history_text}\n\nassistant:"
            
            response = model_gemini.generate_content(
                full_prompt,
                safety_settings=[
                    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
                ]
            )
            res = response.text
            st.markdown(res)
            st.session_state.messages.append({"role": "assistant", "content": res})

            if st.session_state.chat_id is None:
                st.session_state.chat_id = str(uuid.uuid4())
                title = generate_title(prompt, res)
                st.session_state.chats.insert(0, {"id": st.session_state.chat_id, "title": title, "messages": list(st.session_state.messages)})
            else:
                for c in st.session_state.chats:
                    if c["id"] == st.session_state.chat_id: c["messages"] = list(st.session_state.messages)
            save_chats()
            st.rerun()
        except Exception as e:
            st.error(f"Errore: {e}")
