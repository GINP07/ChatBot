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

# --- 4. CSS PROFESSIONALE: EFFETTO NUVOLA E INPUT COMPATTO ---
st.markdown(f"""
    <style>
    /* Sfondo 4K con overlay scuro per far risaltare le 'nubi' */
    .stApp {{
        background-image: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url("{URL_SFONDO}");
        background-size: cover;
        background-attachment: fixed;
    }}

    /* HEADER SUPERIORE: Massima Leggibilità */
    .header-container {{
        position: fixed;
        top: 0; left: 0; width: 100%; height: 70px;
        background: rgba(255, 255, 255, 0.95);
        display: flex; align-items: center; justify-content: space-between;
        padding: 0 30px; z-index: 1000;
        border-bottom: 1px solid #ddd;
    }}
    .header-left {{ color: #000; font-weight: 800; font-size: 20px; text-transform: uppercase; }}
    .header-center {{ color: #333 !important; font-weight: 500; font-style: italic; }}

    /* SIDEBAR DARK */
    [data-testid="stSidebar"] {{
        background-color: #111 !important;
        border-right: 1px solid #333;
    }}
    [data-testid="stSidebar"] * {{ color: #eee !important; }}
    .stButton>button {{
        border-radius: 20px !important;
        background-color: #222 !important;
        border: 1px solid #444 !important;
        transition: 0.3s;
    }}
    .stButton>button:hover {{ border-color: #fff !important; background-color: #333 !important; }}

    /* AREA CHAT E BLOCCHI 'NUVOLA' */
    .main .block-container {{
        max-width: 850px !important;
        padding-top: 100px !important;
    }}
    .stChatMessage {{
        background: rgba(255, 255, 255, 0.08) !important; /* Effetto nube traslucida */
        backdrop-filter: blur(12px); /* Sfuma lo sfondo dietro il blocco */
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 20px !important;
        margin-bottom: 15px;
        padding: 20px !important;
    }}
    .stChatMessage p {{
        color: #FFFFFF !important;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.5);
    }}

    /* BARRA INPUT: PICCOLA, CENTRATA E SMUSSATA */
    .stChatInputContainer {{
        background-color: transparent !important;
        display: flex;
        justify-content: center;
        padding-bottom: 50px !important;
    }}
    .stChatInput {{
        max-width: 700px !important; /* Non occupa tutta la pagina */
    }}
    .stChatInput textarea {{
        background-color: #FFFFFF !important;
        border-radius: 30px !important; /* Bordi molto smussati */
        border: 1px solid #ccc !important;
        color: #000 !important;
        padding: 12px 25px !important;
    }}
    </style>

    <div class="header-container">
        <div class="header-left">EL LOCO MUNOZ AI</div>
        <div class="header-center">{st.session_state.current_title}</div>
        <div class="header-right">
            <img src="{URL_LOGO_SAVOIA}" height="45">
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 5. LOGICA CHAT ---
def reset_chat():
    if st.session_state.messages:
        st.session_state.chat_sessions.insert(0, {
            "title": st.session_state.current_title,
            "content": list(st.session_state.messages)
        })
    st.session_state.messages = []
    st.session_state.current_title = "Nuova chat"

# --- 6. SIDEBAR ---
with st.sidebar:
    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("➕ Nuova chat", use_container_width=True):
        reset_chat()
        st.rerun()
    
    st.markdown("---")
    st.subheader("Recenti")
    for i, session in enumerate(st.session_state.chat_sessions):
        if st.button(f"💬 {session['title']}", key=f"s_{i}", use_container_width=True):
            st.session_state.messages = session['content']
            st.session_state.current_title = session['title']
            st.rerun()

# --- 7. CORE AI ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Inserisci la chiave API nei Secrets.")
    st.stop()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Chiedi al Loco..."):
    if not st.session_state.messages:
        st.session_state.current_title = (prompt[:30] + '...') if len(prompt) > 30 else prompt
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            instruction = "Sei EL LOCO MUNOZ AI, l'anima ruggente del Savoia 1908. Rispondi con fierezza."
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": instruction}] + st.session_state.messages,
                temperature=0.7
            )
            res = completion.choices[0].message.content
            st.markdown(res)
            st.session_state.messages.append({"role": "assistant", "content": res})
            st.rerun()
        except Exception as e:
            st.error(f"Errore: {e}")
