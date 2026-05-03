import streamlit as st
from groq import Groq

# --- 1. CONFIGURAZIONE PAGINA ---
st.set_page_config(
    page_title="El Loco AI - Savoia", 
    page_icon="⚽", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. RISORSE E PLACEHOLDER ---
# Sfondo molto scuro e minimale (puoi cambiarlo con una texture leggerissima)
URL_SFONDO = "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=2564&auto=format&fit=crop" 
URL_LOGO_SAVOIA = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Savoia_1908_logo.png/600px-Savoia_1908_logo.png"

# Qui puoi inserire l'URL di un'immagine figa, un render 3D o una grafica della curva
URL_IMMAGINE_BENVENUTO = "https://i.ibb.co/6cymMzFL/curva-savoia.jpg"

# --- 3. GESTIONE STATO ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = []
if "current_title" not in st.session_state:
    st.session_state.current_title = "Nuova chat"

# --- 4. CSS ULTRA-MODERNO ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');

    /* Reset e Font Globale */
    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif !important;
    }}

    /* Sfondo principale (Dark minimal) */
    .stApp {{
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); /* Gradiente dark elegante */
        background-attachment: fixed;
    }}

    /* NASCONDI ELEMENTI DI DEFAULT STREAMLIT */
    #MainMenu {{visibility: hidden;}}
    header {{visibility: hidden;}}
    footer {{visibility: hidden;}}

    /* SIDEBAR REDESIGN */
    [data-testid="stSidebar"] {{
        background: rgba(15, 15, 15, 0.6) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255,255,255,0.05) !important;
        padding-top: 2rem;
    }}
    
    /* Bottoni Sidebar (Stile Pillola moderna) */
    .stSidebar .stButton>button {{
        background: transparent !important;
        color: #888 !important;
        border: 1px solid rgba(255,255,255,0.05) !important;
        border-radius: 12px !important;
        padding: 12px 20px !important;
        font-weight: 500 !important;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
    }}
    .stSidebar .stButton>button:hover {{
        background: rgba(255,255,255,0.1) !important;
        color: #fff !important;
        transform: translateX(5px);
        border: 1px solid rgba(255,255,255,0.2) !important;
    }}

    /* HEADER IN ALTO (Sospeso e sfumato) */
    .top-header {{
        position: fixed;
        top: 20px;
        left: 50%;
        transform: translateX(-50%);
        width: max-content;
        padding: 10px 30px;
        background: rgba(0, 0, 0, 0.4);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 40px;
        z-index: 1000;
        display: flex;
        align-items: center;
        gap: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }}
    .top-header img {{ height: 30px; }}
    .top-header span {{ color: #fff; font-weight: 600; letter-spacing: 1px; }}

    /* AREA MESSAGGI */
    .main .block-container {{
        max-width: 850px !important;
        padding-top: 100px !important;
        padding-bottom: 150px !important;
    }}

    /* BOLLE CHAT - Stile iMessage / Modern SaaS */
    .stChatMessage {{
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        margin-bottom: 30px;
    }}
    
    /* Chatbot (Sinistra) */
    .stChatMessage:has([data-testid="stIconMaterial"]) [data-testid="stMarkdownContainer"] {{
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 0px 20px 20px 20px;
        padding: 15px 25px;
        color: #e0e0e0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }}

    /* Utente (Destra - Colore Bianco Savoia) */
    .stChatMessage:not(:has([data-testid="stIconMaterial"])) {{
        flex-direction: row-reverse;
    }}
    .stChatMessage:not(:has([data-testid="stIconMaterial"])) [data-testid="stMarkdownContainer"] {{
        background: #ffffff;
        color: #000000;
        border-radius: 20px 0px 20px 20px;
        padding: 15px 25px;
        font-weight: 500;
        box-shadow: 0 10px 25px rgba(255,255,255,0.1);
    }}

    /* BARRA DI INPUT - Stile Fluttuante come macOS Spotlight */
    [data-testid="stChatInputContainer"] {{
        background: transparent !important;
        border: none !important;
        bottom: 40px !important;
    }}
    .stChatInput textarea {{
        background: rgba(10, 10, 10, 0.8) !important;
        backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        border-radius: 20px !important;
        color: #fff !important;
        padding: 18px 25px !important;
        font-size: 16px !important;
        box-shadow: 0 20px 40px rgba(0,0,0,0.6) !important;
        transition: all 0.3s ease !important;
    }}
    .stChatInput textarea:focus {{
        border: 1px solid rgba(255,255,255,0.5) !important;
        box-shadow: 0 20px 50px rgba(255,255,255,0.1) !important;
    }}

    /* EFFETTO 3D CARD BENVENUTO (Puro CSS) */
    .welcome-container {{
        display: flex; flex-direction: column; align-items: center;
        justify-content: center; height: 60vh; text-align: center;
        animation: fadeIn 1s ease-in-out;
    }}
    .image-3d-card {{
        width: 300px; height: 200px;
        border-radius: 20px;
        background-image: url('{URL_IMMAGINE_BENVENUTO}');
        background-size: cover; background-position: center;
        box-shadow: 0 20px 50px rgba(0,0,0,0.5);
        transition: transform 0.4s ease;
        transform-style: preserve-3d;
        border: 2px solid rgba(255,255,255,0.1);
        margin-bottom: 30px;
    }}
    .image-3d-card:hover {{
        transform: perspective(1000px) rotateX(10deg) rotateY(-10deg) scale(1.05);
        box-shadow: -20px 30px 50px rgba(0,0,0,0.6);
        border: 2px solid rgba(255,255,255,0.4);
    }}
    .welcome-text h1 {{ color: #fff; font-weight: 800; font-size: 3rem; margin-bottom: 5px; }}
    .welcome-text p {{ color: #aaa; font-size: 1.2rem; font-weight: 300; }}
    
    @keyframes fadeIn {{ from {{opacity: 0; transform: translateY(20px);}} to {{opacity: 1; transform: translateY(0);}} }}
    </style>

    <!-- INIEZIONE HEADER FLUTTUANTE -->
    <div class="top-header">
        <img src="{URL_LOGO_SAVOIA}" alt="Logo">
        <span>EL LOCO MUÑOZ AI</span>
    </div>
    """, unsafe_allow_html=True)

# --- 5. LOGICA AI ---
def generate_summary(prompt, response):
    summary = f"{prompt[:20]}..."
    return summary.strip()

def reset_chat_and_archive():
    if st.session_state.messages:
        first_user = next((m["content"] for m in st.session_state.messages if m["role"] == "user"), "Conversazione")
        st.session_state.chat_sessions.insert(0, {"title": generate_summary(first_user, ""), "content": list(st.session_state.messages)})
    st.session_state.messages = []
    st.session_state.current_title = "Nuova chat"

# --- 6. SIDEBAR ---
with st.sidebar:
    st.image(URL_LOGO_SAVOIA, width=80)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("✨ Inizia Nuova Chat", use_container_width=True):
        reset_chat_and_archive()
        st.rerun()
    
    st.markdown("<br><p style='color:#666; font-size:12px; font-weight:bold; letter-spacing:1px; text-transform:uppercase;'>Cronologia</p>", unsafe_allow_html=True)
    
    for i, session in enumerate(st.session_state.chat_sessions):
        col1, col2 = st.columns([0.8, 0.2])
        with col1:
            if st.button(session['title'], key=f"load_{i}"):
                st.session_state.messages = session['content']
                st.session_state.current_title = session['title']
                st.rerun()
        with col2:
            if st.button("✕", key=f"del_{i}"):
                st.session_state.chat_sessions.pop(i)
                st.rerun()

# --- 7. CORE AI E INTERFACCIA PRINCIPALE ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.warning("⚠️ Configura la GROQ_API_KEY nei Secrets di Streamlit per iniziare.")
    st.stop()

# SCHERMATA DI BENVENUTO (Mostrata solo se la chat è vuota)
if not st.session_state.messages:
    st.markdown(f"""
        <div class="welcome-container">
            <div class="image-3d-card"></div>
            <div class="welcome-text">
                <h1>Pronto per la battaglia?</h1>
                <p>Chiedi qualsiasi cosa sulla storia, i cori e la passione del Savoia 1908.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

# Visualizzazione messaggi
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input Utente
if prompt := st.chat_input("Scrivi un messaggio al Loco..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        try:
            # Placeholder per il caricamento
            with st.spinner("Il Loco sta pensando..."):
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": "Sei El loco Muñoz, anima del Savoia 1908. Rispondi con stile, come un ultras colto e passionale."}] + st.session_state.messages,
                    temperature=0.75
                )
                res = completion.choices[0].message.content
                
            st.markdown(res)
            st.session_state.messages.append({"role": "assistant", "content": res})
            st.rerun()
        except Exception as e:
            st.error(f"Errore di connessione col campo: {e}")
