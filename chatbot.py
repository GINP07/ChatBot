import streamlit as st
from groq import Groq

# --- 1. CONFIGURAZIONE PAGINA ---
st.set_page_config(
    page_title="Gemini - El Loco Munoz", 
    page_icon="https://www.gstatic.com/lamda/images/favicon_v1_150160d133481239.png", # Icona Gemini
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CONFIGURAZIONE RISORSE ---
URL_SFONDO = "https://i.ibb.co/6cymMzFL/curva-savoia.jpg" 
URL_LOGO_SAVOIA = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Savoia_1908_logo.png/600px-Savoia_1908_logo.png"

# --- 3. GESTIONE STATO ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = []
if "current_title" not in st.session_state:
    st.session_state.current_title = "Nuova chat"

# --- 4. CSS PER REPLICARE L'INTERFACCIA GEMINI ---
st.markdown(f"""
    <style>
    /* Sfondo generale con immagine curva Savoia */
    .stApp {{
        background-image: linear-gradient(rgba(255,255,255,0.9), rgba(255,255,255,0.9)), url("{URL_SFONDO}");
        background-size: cover;
        background-attachment: fixed;
    }}

    /* SIDEBAR (GRIGIO GEMINI) */
    [data-testid="stSidebar"] {{
        background-color: #f0f4f9 !important;
        border-right: none !important;
        padding-top: 20px;
    }}
    
    /* Bottoni Sidebar (Titoli chat) */
    .stButton>button {{
        background-color: transparent !important;
        border: none !important;
        color: #1f1f1f !important;
        text-align: left !important;
        padding: 10px 15px !important;
        width: 100% !important;
        border-radius: 20px !important;
        font-size: 14px !important;
        font-weight: 500 !important;
    }}
    .stButton>button:hover {{
        background-color: #e1e5ea !important;
    }}
    
    /* Titolo Chat Attiva nella Sidebar */
    .active-chat {{
        background-color: #d3e3fd !important; /* Blu chiaro selezione Gemini */
    }}

    /* HEADER SUPERIORE */
    .header-container {{
        position: fixed;
        top: 0; left: 0; width: 100%; height: 60px;
        background: rgba(255,255,255,0.8);
        backdrop-filter: blur(10px);
        display: flex; align-items: center; justify-content: space-between;
        padding: 0 20px; z-index: 1000;
    }}
    .header-text {{
        color: #444746; font-size: 18px; font-weight: 400;
    }}

    /* AREA CHAT */
    .main .block-container {{
        max-width: 850px !important;
        padding-top: 80px !important;
    }}

    /* MESSAGGI */
    .stChatMessage {{
        background-color: transparent !important;
        border: none !important;
    }}
    .stChatMessage [data-testid="stMarkdownContainer"] p {{
        color: #1f1f1f !important;
        font-size: 16px !important;
        line-height: 1.6 !important;
    }}

    /* BARRA INPUT (ARROTONDATA GEMINI) */
    .stChatInputContainer {{
        background-color: transparent !important;
        padding-bottom: 40px !important;
    }}
    .stChatInput textarea {{
        background-color: #f0f4f9 !important;
        border-radius: 28px !important;
        border: none !important;
        padding: 15px 25px !important;
        color: #1f1f1f !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
    }}
    </style>

    <div class="header-container">
        <div style="display:flex; align-items:center; gap:10px;">
            <span style="font-size:20px; font-weight:500; color:#1f1f1f;">Gemini</span>
        </div>
        <div class="header-text">{st.session_state.current_title}</div>
        <div>
            <img src="{URL_LOGO_SAVOIA}" height="35">
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 5. LOGICA CHAT ---
def new_chat():
    if st.session_state.messages:
        st.session_state.chat_sessions.insert(0, {
            "title": st.session_state.current_title,
            "content": list(st.session_state.messages)
        })
    st.session_state.messages = []
    st.session_state.current_title = "Nuova chat"

# --- 6. SIDEBAR ---
with st.sidebar:
    if st.button("➕ Nuova chat", use_container_width=True):
        new_chat()
        st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<p style='color:#444746; font-size:12px; font-weight:500; padding-left:15px;'>Recenti</p>", unsafe_allow_html=True)
    
    for i, session in enumerate(st.session_state.chat_sessions):
        if st.button(f" {session['title']}", key=f"s_{i}"):
            # Salva corrente e carica vecchia
            temp_m = list(st.session_state.messages)
            temp_t = st.session_state.current_title
            
            st.session_state.messages = session['content']
            st.session_state.current_title = session['title']
            
            st.session_state.chat_sessions.pop(i)
            if temp_m:
                st.session_state.chat_sessions.insert(0, {"title": temp_t, "content": temp_m})
            st.rerun()

# --- 7. CORE AI (GROQ) ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Inserisci GROQ_API_KEY nei Secrets.")
    st.stop()

# Visualizzazione messaggi
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input
if prompt := st.chat_input("Chiedi a Gemini..."):
    if not st.session_state.messages:
        st.session_state.current_title = (prompt[:35] + '...') if len(prompt) > 35 else prompt
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            instruction = "Sei EL LOCO MUNOZ AI, custode della storia del Savoia 1908. Rispondi con lo stile di Gemini, professionale ma appassionato."
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": instruction}] + st.session_state.messages,
                temperature=0.7
            )
            full_res = response.choices[0].message.content
            st.markdown(full_res)
            st.session_state.messages.append({"role": "assistant", "content": full_res})
            st.rerun()
        except Exception as e:
            st.error(f"Errore: {e}")
