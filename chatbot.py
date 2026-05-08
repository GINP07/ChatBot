import streamlit as st
from groq import Groq
import google.generativeai as genai 
import json, os, time, uuid
import docx 

# ================= CONFIG =================
st.set_page_config(
    page_title="EL LOCO MUÑOZ AI", 
    page_icon="https://i.ibb.co/NgwLt8cT/logo-savoia.png", 
    layout="wide"
)

BG_GENERALE = "https://i.ibb.co/6cymMzFL/curva-savoia.jpg"
IMMAGINE_HOME_CENTRALE = "https://i.ibb.co/6cymMzFL/curva-savoia.jpg" 
LOGO_PICCOLO = "https://i.ibb.co/NgwLt8cT/logo-savoia.png"
CHAT_FILE = "chat_history.json"
DATABASE_FILE = "Database_Savoia.docx"

# ================= FUNZIONI =================
def load_savoia_database(file_path):
    if os.path.exists(file_path):
        try:
            doc = docx.Document(file_path)
            return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
        except: return "Errore lettura docx."
    return "Database non trovato."

KNOWLEDGE_BASE = load_savoia_database(DATABASE_FILE)

# ================= CSS =================
st.markdown(f"""
<style>
    .stApp {{ background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.95)), url("{BG_GENERALE}"); background-size: cover; background-attachment: fixed; }}
    .stChatMessage {{ background: rgba(255,255,255,0.08) !important; border-radius: 15px !important; color: white !important; }}
    .home-container {{ display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 60vh; text-align: center; }}
    .home-card {{ width: 300px; height: 180px; border-radius: 20px; background-image: url('{IMMAGINE_HOME_CENTRALE}'); background-size: cover; border: 2px solid white; }}
    .home-title {{ color: white; font-weight: 800; font-size: 2.5rem; }}
</style>
""", unsafe_allow_html=True)

# ================= SESSION =================
if "messages" not in st.session_state: st.session_state.messages = []
if "chats" not in st.session_state: st.session_state.chats = []
if "chat_id" not in st.session_state: st.session_state.chat_id = None

# ================= API CONFIG (VERSIONE 2026) =================
if "GEMINI_API_KEY" in st.secrets:
    # Usiamo la configurazione suggerita per evitare il 404
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    
    # Se gemini-3-flash-preview non va, il sistema userà gemini-1.5-flash come fallback
    MODEL_NAME = 'gemini-1.5-flash' 
    model_gemini = genai.GenerativeModel(MODEL_NAME)
else:
    st.error("Manca GEMINI_API_KEY nei Secrets!")

# ================= SIDEBAR =================
with st.sidebar:
    st.image("https://i.ibb.co/Xf5VVr4W/dani-munoz.png")
    if st.button("NUOVA CHAT"):
        st.session_state.messages = []
        st.session_state.chat_id = None
        st.rerun()

# ================= MAIN AREA =================
if not st.session_state.messages:
    st.markdown(f'<div class="home-container"><div class="home-card"></div><h1 class="home-title">EL LOCO MUÑOZ</h1></div>', unsafe_allow_html=True)
else:
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.markdown(m["content"])

# ================= CHAT LOGIC =================
if prompt := st.chat_input("Scrivi al Loco..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()

if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant"):
        try:
            # Costruiamo il contesto Ultras
            full_context = f"Sei El Loco Muñoz, ultras del Savoia 1908. Conoscenza: {KNOWLEDGE_BASE}\n\n"
            for m in st.session_state.messages:
                full_context += f"{m['role']}: {m['content']}\n"
            
            # Chiamata al modello
            response = model_gemini.generate_content(
                full_context,
                safety_settings=[
                    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
                ]
            )
            
            res_text = response.text
            st.markdown(res_text)
            st.session_state.messages.append({"role": "assistant", "content": res_text})
            st.rerun()
            
        except Exception as e:
            st.error(f"Errore: {e}")
            if "404" in str(e):
                st.info("Consiglio: Cambia il nome del modello in 'gemini-pro' nel codice se l'errore persiste.")
