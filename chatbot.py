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

# --- 3. GESTIONE STATO ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = []
if "current_title" not in st.session_state:
    st.session_state.current_title = "Nuova chat"

# --- 4. CSS PROFESSIONALE ---
st.markdown(f"""
    <style>
    /* Sfondo Generale */
    .stApp {{
        background-image: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url("{URL_SFONDO}");
        background-size: cover;
        background-attachment: fixed;
    }}

    /* HEADER FIX: Spostato e calibrato per la Sidebar */
    .header-container {{
        position: fixed;
        top: 0; 
        left: 0;
        width: 100%;
        height: 65px;
        background: rgba(255, 255, 255, 0.98);
        display: flex; 
        align-items: center; 
        justify-content: space-between;
        padding: 0 40px 0 320px; /* Spazio per non finire sotto la sidebar */
        z-index: 999;
        border-bottom: 1px solid #ddd;
    }}
    .header-left {{ color: #000 !important; font-weight: 800; font-size: 18px; text-transform: uppercase; }}
    .header-center {{ color: #555 !important; font-weight: 500; font-style: italic; font-size: 14px; text-align: center; }}

    /* SIDEBAR DARK & CLEAN */
    [data-testid="stSidebar"] {{
        background-color: #111 !important;
        border-right: 1px solid #333;
    }}
    [data-testid="stSidebar"] * {{ color: #eee !important; }}
    
    /* Bottoni Cronologia: Allineati a sinistra, senza icone, hover effect */
    .stButton>button {{
        background-color: transparent !important;
        color: #bbb !important;
        border: none !important;
        text-align: left !important;
        width: 100% !important;
        padding: 8px 15px !important;
        font-size: 14px !important;
        transition: 0.2s;
        display: block !important;
    }}
    .stButton>button:hover {{
        background-color: rgba(255,255,255,0.1) !important;
        color: #fff !important;
        border-radius: 5px !important;
    }}

    /* AREA MESSAGGI: EFFETTO NUVOLA */
    .main .block-container {{
        max-width: 800px !important;
        padding-top: 90px !important;
    }}
    .stChatMessage {{
        background: rgba(255, 255, 255, 0.08) !important;
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 18px !important;
        margin-bottom: 12px;
    }}
    .stChatMessage p {{
        color: #FFFFFF !important;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.5);
    }}

    /* BARRA DI INPUT: FLOATING (NO STRISCIA BIANCA) */
    .stChatInputContainer {{
        background-color: transparent !important;
        border: none !important;
        padding-bottom: 40px !important;
    }}
    .stChatInput {{
        max-width: 700px !important;
        margin: 0 auto !important;
        background-color: transparent !important;
    }}
    .stChatInput textarea {{
        background-color: #FFFFFF !important;
        border-radius: 25px !important;
        border: 1px solid #ccc !important;
        color: #000 !important;
        padding: 12px 20px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3) !important;
    }}
    </style>

    <div class="header-container">
        <div class="header-left">EL LOCO MUÑOZ AI</div>
        <div class="header-center">{st.session_state.current_title}</div>
        <div class="header-right"><img src="{URL_LOGO_SAVOIA}" height="35"></div>
    </div>
    """, unsafe_allow_html=True)

# --- 5. LOGICA AI PER SINTESI TITOLO ---
def generate_summary(prompt, response):
    # Crea un titolo breve combinando domanda e risposta
    summary = f"{prompt[:15]}.. / {response[:20]}.."
    return summary.replace("\n", " ").strip()

def reset_chat_and_archive():
    if st.session_state.messages:
        # Recupera l'ultimo messaggio AI per la sintesi
        last_ai = next((m["content"] for m in reversed(st.session_state.messages) if m["role"] == "assistant"), "Chat")
        first_user = next((m["content"] for m in st.session_state.messages if m["role"] == "user"), "Domanda")
        
        smart_title = generate_summary(first_user, last_ai)
        st.session_state.chat_sessions.insert(0, {
            "title": smart_title,
            "content": list(st.session_state.messages)
        })
    st.session_state.messages = []
    st.session_state.current_title = "Nuova chat"

# --- 6. SIDEBAR ---
with st.sidebar:
    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("➕ Nuova chat", use_container_width=True):
        reset_chat_and_archive()
        st.rerun()
    
    st.markdown("---")
    st.caption("RECENTI")
    
    # Lista Cronologia con tasto Elimina individuale
    for i, session in enumerate(st.session_state.chat_sessions):
        col1, col2 = st.columns([0.85, 0.15])
        with col1:
            if st.button(session['title'], key=f"load_{i}"):
                st.session_state.messages = session['content']
                st.session_state.current_title = session['title']
                st.rerun()
        with col2:
            if st.button("✕", key=f"del_{i}", help="Elimina questa chat"):
                st.session_state.chat_sessions.pop(i)
                st.rerun()

# --- 7. CORE AI ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Configura GROQ_API_KEY nei Secrets.")
    st.stop()

# Visualizzazione messaggi
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input Utente
if prompt := st.chat_input("Chiedi al Loco..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            instruction = "Sei El loco Muñoz, l'anima ruggente del Savoia 1908. Rispondi con fierezza torrese e competenza."
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": instruction}] + st.session_state.messages,
                temperature=0.7
            )
            res = completion.choices[0].message.content
            
            # Al primo scambio, genera il titolo dinamico centrato nell'header
            if len(st.session_state.messages) == 1:
                st.session_state.current_title = generate_summary(prompt, res)
            
            st.markdown(res)
            st.session_state.messages.append({"role": "assistant", "content": res})
            st.rerun()
        except Exception as e:
            st.error(f"Errore: {e}")
