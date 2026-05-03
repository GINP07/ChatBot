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

# --- 3. GESTIONE STATO SESSIONE ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = []
if "current_title" not in st.session_state:
    st.session_state.current_title = "Nuova Conversazione"

# --- 4. CSS CUSTOM: FIX TOTALI ---
st.markdown(f"""
    <style>
    /* Sfondo 4K con overlay dinamico */
    .stApp {{
        background-image: linear-gradient(to bottom, rgba(0,0,0,0.3) 0%, rgba(0,0,0,0.85) 100%), url("{URL_SFONDO}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* BARRA SUPERIORE BIANCA FIXATA */
    .custom-header {{
        position: fixed;
        top: 0; left: 0; width: 100%; height: 70px;
        background-color: #FFFFFF;
        display: flex; align-items: center;
        z-index: 1001;
        box-shadow: 0 4px 12px rgba(0,0,0,0.5);
        padding: 0 30px;
    }}
    .header-left {{
        display: flex; align-items: center; gap: 12px;
        flex: 1;
    }}
    .header-center {{
        flex: 2; text-align: center;
        color: #333333 !important;
        font-weight: 600; font-size: 18px;
        font-family: 'Helvetica Neue', sans-serif;
        font-style: italic;
    }}
    .header-right {{
        flex: 1; display: flex; justify-content: flex-end;
    }}
    .header-bot-name {{
        color: #000000 !important;
        font-weight: 900; font-size: 18px;
        text-transform: uppercase; margin: 0;
    }}

    /* Padding per il contenuto principale */
    .main .block-container {{ padding-top: 100px !important; }}

    /* SIDEBAR: FIX CONTRASTO TESTO */
    [data-testid="stSidebar"] {{
        background-color: #1a1a1a !important;
        border-right: 1px solid #333;
    }}
    [data-testid="stSidebar"] .stMarkdown p, 
    [data-testid="stSidebar"] h3, 
    [data-testid="stSidebar"] span {{
        color: #FFFFFF !important;
    }}
    
    /* Bottoni Cronologia Chat */
    .stButton>button {{
        border-radius: 8px !important;
        background-color: #2d2d2d !important;
        color: #FFFFFF !important;
        border: 1px solid #444 !important;
        text-align: left !important;
        font-size: 14px !important;
        margin-bottom: 5px;
        transition: all 0.2s;
    }}
    .stButton>button:hover {{
        background-color: #404040 !important;
        border-color: #FFFFFF !important;
    }}

    /* MESSAGGI CHAT */
    .stChatMessage {{
        background: rgba(10, 10, 10, 0.92) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 18px !important;
        margin-bottom: 15px;
    }}
    .stChatMessage p {{
        color: #FFFFFF !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.8) !important;
    }}

    /* BARRA DI INPUT: PULITA E CHIARA */
    .stChatInputContainer {{
        padding: 0 12% 25px 12% !important;
        background: transparent !important;
    }}
    .stChatInput textarea {{
        background-color: #FFFFFF !important; /* Bianca pulita */
        color: #000000 !important; /* Scrittura nera */
        border: 1px solid #ddd !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2) !important;
    }}
    </style>

    <div class="custom-header">
        <div class="header-left">
            <img src="{URL_IMMAGINE_PNG}" height="35">
            <span class="header-bot-name">EL LOCO MUNOZ AI</span>
        </div>
        <div class="header-center">
             {st.session_state.current_title}
        </div>
        <div class="header-right">
            <img src="{URL_LOGO_SAVOIA}" height="35">
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 5. LOGICA ARCHIVIAZIONE CHAT ---
def archive_current_chat():
    if st.session_state.messages:
        # Archivia la chat corrente con il suo titolo
        st.session_state.chat_sessions.insert(0, {
            "title": st.session_state.current_title,
            "content": st.session_state.messages
        })
        # Reset sessione attuale
        st.session_state.messages = []
        st.session_state.current_title = "Nuova Conversazione"

# --- 6. SIDEBAR: AZIONI E STORICO ---
with st.sidebar:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    if st.button("➕ NUOVA CHAT", use_container_width=True):
        archive_current_chat()
        st.rerun()
    
    st.markdown("---")
    st.subheader("🕒 Cronologia")
    
    for i, session in enumerate(st.session_state.chat_sessions):
        # Il nome del bottone è il titolo sintetizzato della chat
        if st.button(f"💬 {session['title']}", key=f"session_{i}", use_container_width=True):
            # Salva quella attuale e carica quella selezionata
            archive_current_chat()
            st.session_state.messages = session['content']
            st.session_state.current_title = session['title']
            st.session_state.chat_sessions.pop(i)
            st.rerun()

# --- 7. MOTORE CHAT (GROQ) ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Configura GROQ_API_KEY nei Secrets!")
    st.stop()

# Mostra i messaggi correnti
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Gestione Input e Risposta
if prompt := st.chat_input("Parla con il cuore dei Bianchi..."):
    # Se è il primo messaggio, genera il titolo per l'header e la sidebar
    if not st.session_state.messages:
        title_raw = prompt.strip()[:35]
        st.session_state.current_title = title_raw + ("..." if len(prompt) > 35 else "")
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            instruction = (
                "Sei EL LOCO MUNOZ AI, custode della storia centenaria del Savoia 1908. "
                "Rispondi con l'orgoglio di Torre Annunziata. Sii carismatico, fiero e mai banale."
            )
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": instruction}] + st.session_state.messages,
                temperature=0.8
            )
            response = completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun() # Aggiorna per sincronizzare titolo header
        except Exception as e:
            st.error(f"Errore: {e}")
