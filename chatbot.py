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

# --- 3. GESTIONE STATO ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = []
if "current_title" not in st.session_state:
    st.session_state.current_title = "Nuova Conversazione"

# --- 4. CSS PROFESSIONALE (STILE GEMINI/CHATGPT) ---
st.markdown(f"""
    <style>
    /* Sfondo Generale */
    .stApp {{
        background-image: linear-gradient(to bottom, rgba(0,0,0,0.5) 0%, rgba(0,0,0,0.9) 100%), url("{URL_SFONDO}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* HEADER FISSO BIANCO */
    .custom-header {{
        position: fixed;
        top: 0; left: 0; width: 100%; height: 60px;
        background-color: #FFFFFF;
        display: flex; align-items: center; justify-content: space-between;
        z-index: 1000;
        box-shadow: 0 2px 10px rgba(0,0,0,0.3);
        padding: 0 20px;
    }}
    .header-left {{ display: flex; align-items: center; gap: 10px; color: #000; font-weight: 800; font-size: 16px; }}
    .header-center {{ color: #444 !important; font-size: 14px; font-weight: 500; text-align: center; font-style: italic; }}
    .header-right {{ display: flex; align-items: center; }}

    /* CONTENITORE CHAT */
    .main .block-container {{
        padding-top: 80px !important;
        max-width: 800px !important; /* Centra la chat come nei siti famosi */
    }}

    /* MESSAGGI CHAT (VETRO SCURO) */
    .stChatMessage {{
        background: rgba(20, 20, 20, 0.8) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 15px !important;
        color: #ececf1 !important;
        margin-bottom: 10px;
    }}
    .stChatMessage p {{ color: #ececf1 !important; }}

    /* SIDEBAR (SCURA E PULITA) */
    [data-testid="stSidebar"] {{
        background-color: #111111 !important;
        border-right: 1px solid #333;
    }}
    [data-testid="stSidebar"] * {{ color: #d1d1d1 !important; }}
    
    /* Bottoni Sidebar */
    .stButton>button {{
        background-color: transparent !important;
        border: 1px solid #444 !important;
        color: #fff !important;
        border-radius: 10px !important;
        text-align: left !important;
        padding: 10px !important;
        font-size: 14px !important;
        width: 100% !important;
    }}
    .stButton>button:hover {{
        background-color: #2a2a2a !important;
        border-color: #666 !important;
    }}

    /* BARRA DI INPUT (STILE FLOATING) */
    .stChatInputContainer {{
        background: transparent !important;
        padding-bottom: 30px !important;
    }}
    .stChatInput textarea {{
        background-color: #ffffff !important;
        color: #000000 !important;
        border-radius: 20px !important;
        border: 1px solid #ccc !important;
        box-shadow: 0 0 15px rgba(0,0,0,0.2) !important;
    }}
    </style>

    <div class="custom-header">
        <div class="header-left">
            <img src="{URL_IMMAGINE_PNG}" height="30">
            <span>EL LOCO MUNOZ AI</span>
        </div>
        <div class="header-center">
            {st.session_state.current_title}
        </div>
        <div class="header-right">
            <img src="{URL_LOGO_SAVOIA}" height="35">
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 5. LOGICA CHAT ---
def archive_and_reset():
    if st.session_state.messages:
        st.session_state.chat_sessions.insert(0, {
            "title": st.session_state.current_title,
            "content": list(st.session_state.messages)
        })
    st.session_state.messages = []
    st.session_state.current_title = "Nuova Conversazione"

# --- 6. SIDEBAR ---
with st.sidebar:
    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("➕ Nuova Chat"):
        archive_and_reset()
        st.rerun()
    
    st.markdown("---")
    st.markdown("### Cronologia")
    for i, session in enumerate(st.session_state.chat_sessions):
        if st.button(f"💬 {session['title']}", key=f"s_{i}"):
            # Salva la chat corrente prima di caricare la vecchia
            temp_msgs = list(st.session_state.messages)
            temp_title = st.session_state.current_title
            
            st.session_state.messages = session['content']
            st.session_state.current_title = session['title']
            
            st.session_state.chat_sessions.pop(i)
            if temp_msgs:
                st.session_state.chat_sessions.insert(0, {"title": temp_title, "content": temp_msgs})
            st.rerun()

# --- 7. CORE AI ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Inserisci la chiave API nei Secrets!")
    st.stop()

# Mostra messaggi
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input utente
if prompt := st.chat_input("Chiedi al Loco..."):
    # Crea titolo se è il primo messaggio
    if not st.session_state.messages:
        st.session_state.current_title = (prompt[:30] + '...') if len(prompt) > 30 else prompt
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            instruction = "Sei EL LOCO MUNOZ AI, custode della storia del Savoia 1908. Rispondi con orgoglio e competenza."
            response_stream = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": instruction}] + st.session_state.messages,
                temperature=0.7
            )
            full_response = response_stream.choices[0].message.content
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            st.rerun()
        except Exception as e:
            st.error(f"Errore: {e}")
