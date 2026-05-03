import streamlit as st
from groq import Groq

# --- 1. CONFIGURAZIONE PAGINA ---
st.set_page_config(
    page_title="EL LOCO MUNOZ AI", 
    page_icon="⚪", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. RISORSE ESTETICHE ---
URL_SFONDO = "https://i.ibb.co/6cymMzFL/curva-savoia.jpg" 
URL_LOGO_SAVOIA = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Savoia_1908_logo.png/600px-Savoia_1908_logo.png"
URL_IMMAGINE_PNG = "https://cdn-icons-png.flaticon.com/512/1141/1141771.png" 

# --- 3. CSS CUSTOM: CONTRASTO, HEADER FISSO E INPUT COMPATTO ---
st.markdown(f"""
    <style>
    /* Sfondo 4K con oscuramento calibrato per la profondità */
    .stApp {{
        background-image: linear-gradient(to bottom, rgba(0,0,0,0.3) 0%, rgba(0,0,0,0.85) 100%), url("{URL_SFONDO}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* Barra Superiore Bianca (Testo Nero Leggibile) */
    .custom-header {{
        position: fixed;
        top: 0; left: 0; width: 100%; height: 70px;
        background-color: #FFFFFF;
        display: flex; align-items: center; justify-content: center;
        z-index: 1001;
        box-shadow: 0 4px 12px rgba(0,0,0,0.5);
    }}
    .header-title {{
        color: #000000 !important;
        font-weight: 900; font-size: 24px; margin: 0;
        text-transform: uppercase; letter-spacing: 2px;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }}

    /* Spazio per non coprire la chat */
    .main .block-container {{ padding-top: 100px !important; }}

    /* Messaggi Chat: Sfondo scuro opaco per leggere bene il bianco */
    .stChatMessage {{
        background: rgba(10, 10, 10, 0.9) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 18px !important;
        margin-bottom: 15px;
    }}
    .stChatMessage p {{
        color: #FFFFFF !important;
        font-size: 1.05rem !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.8) !important;
    }}

    /* Barra di input PICCOLA e centrata */
    .stChatInputContainer {{
        padding: 0 15% 20px 15% !important;
        background: transparent !important;
    }}
    .stChatInput textarea {{
        background-color: rgba(30, 30, 30, 0.9) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        height: 42px !important;
    }}

    /* Sidebar Dark Mode */
    [data-testid="stSidebar"] {{
        background-color: #080808 !important;
        border-right: 1px solid #222;
    }}
    .stButton>button {{
        border-radius: 8px !important;
        background-color: #1a1a1a !important;
        color: white !important;
        border: 1px solid #333 !important;
    }}
    </style>

    <div class="custom-header">
        <div style="display: flex; align-items: center; gap: 20px;">
            <img src="{URL_IMMAGINE_PNG}" height="45">
            <h1 class="header-title">EL LOCO MUNOZ AI</h1>
            <img src="{URL_LOGO_SAVOIA}" height="45">
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 4. GESTIONE STATO E CRONOLOGIA ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = [] # Lista di {"title": str, "content": list}

# Funzione per salvare la chat con un titolo intelligente
def archive_chat():
    if st.session_state.messages:
        # Crea titolo: usa il primo messaggio utente (max 25 car.)
        user_msgs = [m["content"] for m in st.session_state.messages if m["role"] == "user"]
        raw_title = user_msgs[0] if user_msgs else "Conversazione Vuota"
        smart_title = (raw_title[:25] + '...') if len(raw_title) > 25 else raw_title
        
        st.session_state.chat_sessions.insert(0, {"title": smart_title, "content": st.session_state.messages})
        st.session_state.messages = []

# --- 5. SIDEBAR: NUOVA CHAT E STORICO ---
with st.sidebar:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    if st.button("➕ NUOVA CHAT", use_container_width=True):
        archive_chat()
        st.rerun()
    
    st.markdown("---")
    st.subheader("🕒 Chat Precedenti")
    
    for i, session in enumerate(st.session_state.chat_sessions):
        if st.button(f"💬 {session['title']}", key=f"session_{i}", use_container_width=True):
            # Recupera la sessione e scambiala con quella attuale
            temp_content = st.session_state.messages
            st.session_state.messages = session['content']
            st.session_state.chat_sessions.pop(i)
            if temp_content:
                # Ri-archivia la vecchia se non era vuota
                raw_t = temp_content[0]["content"] if temp_content else "Chat"
                st.session_state.chat_sessions.insert(0, {"title": raw_t[:25], "content": temp_content})
            st.rerun()

# --- 6. MOTORE CHAT ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Errore: Chiave API Groq non configurata correttamente.")
    st.stop()

# Visualizzazione messaggi
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Prompt Utente
if prompt := st.chat_input("Scrivi qui, cuore biancoscudato..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Personalità del bot
            instruction = (
                "Sei EL LOCO MUNOZ AI. Parla come un ultra-esperto del Savoia 1908. "
                "Usa un tono fiero, torrese, mai banale. Non scrivere testi troppo lunghi se non richiesto."
            )
            
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": instruction}] + st.session_state.messages,
                temperature=0.8
            )
            
            response = completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Errore tecnico: {e}")
