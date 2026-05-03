import streamlit as st
from groq import Groq

# --- 1. CONFIGURAZIONE PAGINA ---
st.set_page_config(
    page_title="EL LOCO MUNOZ AI", 
    page_icon="⚪", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. RISORSE ---
URL_SFONDO = "https://i.ibb.co/6cymMzFL/curva-savoia.jpg" 
URL_LOGO_SAVOIA = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Savoia_1908_logo.png/600px-Savoia_1908_logo.png"
URL_IMMAGINE_PNG = "https://cdn-icons-png.flaticon.com/512/1141/1141771.png" 

# --- 3. CSS AVANZATO (FIX CONTRASTO E BARRA PICCOLA) ---
st.markdown(f"""
    <style>
    /* Sfondo 4K High-Res */
    .stApp {{
        background-image: linear-gradient(to bottom, rgba(0,0,0,0.4) 0%, rgba(0,0,0,0.8) 100%), url("{URL_SFONDO}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* Barra Bianca Superiore (Testo Nero Leggibile) */
    .custom-header {{
        position: fixed;
        top: 0; left: 0; width: 100%; height: 70px;
        background-color: #FFFFFF;
        display: flex; align-items: center; justify-content: center;
        z-index: 1000;
        box-shadow: 0 2px 10px rgba(0,0,0,0.5);
    }}
    .header-title {{
        color: #000000 !important;
        font-weight: 800; font-size: 22px; margin: 0;
        text-transform: uppercase; letter-spacing: 1px;
    }}

    /* Padding Chat */
    .main .block-container {{ padding-top: 90px !important; }}

    /* Messaggi Chat: contrasto migliorato */
    .stChatMessage {{
        background: rgba(0, 0, 0, 0.85) !important; /* Molto scuro per far risaltare il bianco */
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 15px !important;
    }}
    .stChatMessage p, .stChatMessage span {{
        color: #FFFFFF !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,1) !important;
    }}

    /* Barra di input (PIÙ PICCOLA) */
    .stChatInputContainer {{
        padding: 10px 10% !important;
        background: transparent !important;
    }}
    .stChatInput textarea {{
        height: 45px !important;
        background: rgba(255,255,255,0.1) !important;
        color: white !important;
        border-radius: 10px !important;
    }}

    /* Sidebar Dark */
    [data-testid="stSidebar"] {{
        background-color: #0e1117 !important;
    }}
    [data-testid="stSidebar"] * {{
        color: white !important;
    }}
    </style>

    <div class="custom-header">
        <div class="header-content" style="display: flex; align-items: center; gap: 15px;">
            <img src="{URL_IMMAGINE_PNG}" height="40">
            <h1 class="header-title">EL LOCO MUNOZ AI</h1>
            <img src="{URL_LOGO_SAVOIA}" height="40">
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 4. LOGICA CRONOLOGIA CON TITOLI INTELLIGENTI ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [] # Lista di dizionari: {"title": str, "msgs": list}

def save_current_chat():
    if st.session_state.messages:
        # Prendi i primi 30 caratteri del primo messaggio come titolo provvisorio
        first_msg = st.session_state.messages[0]["content"]
        title = (first_msg[:30] + '...') if len(first_msg) > 30 else first_msg
        st.session_state.chat_history.append({"title": title, "msgs": st.session_state.messages})
        st.session_state.messages = []

# --- 5. SIDEBAR ---
with st.sidebar:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    if st.button("➕ Nuova Chat", use_container_width=True):
        save_current_chat()
        st.rerun()
    
    st.markdown("### 🕒 Cronologia")
    for i, chat in enumerate(reversed(st.session_state.chat_history)):
        if st.button(f"💬 {chat['title']}", key=f"hist_{i}", use_container_width=True):
            # Scambia la chat attuale con quella selezionata
            current_tmp = st.session_state.messages
            st.session_state.messages = chat['msgs']
            # Rimuovi questa chat dalla cronologia perché ora è attiva
            st.session_state.chat_history.pop(len(st.session_state.chat_history) - 1 - i)
            st.rerun()

# --- 6. CORE CHAT ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Chiave API mancante!")
    st.stop()

# Visualizza messaggi
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input
if prompt := st.chat_input("Chiedi al Loco..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Personalità
            system_p = "Sei EL LOCO MUNOZ AI, anima del Savoia 1908. Parla con fierezza torrese."
            
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": system_p}] + st.session_state.messages,
                temperature=0.7
            )
            
            # Se è il primo messaggio, potremmo chiedere all'AI un titolo (opzionale)
            # Per ora usiamo il contenuto del messaggio utente come titolo nella sidebar
            
            risposta = completion.choices[0].message.content
            st.markdown(risposta)
            st.session_state.messages.append({"role": "assistant", "content": risposta})
        except Exception as e:
            st.error(f"Errore: {e}")
