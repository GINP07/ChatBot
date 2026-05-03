import streamlit as st
from groq import Groq

# --- 1. CONFIGURAZIONE PAGINA ---
st.set_page_config(
    page_title="EL LOCO MUNOZ AI", 
    page_icon="⚪", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CSS AVANZATO: ANIMAZIONI 3D & GLASSMORPHISM ---
st.markdown("""
    <style>
    /* Sfondo animato sfumato scuro */
    .stApp {
        background: linear-gradient(-45deg, #000000, #1a1a1a, #333333, #0f0f0f);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        color: white;
    }

    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Effetto Vetro per i messaggi della chat */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur(12px) saturate(180%);
        -webkit-backdrop-filter: blur(12px) saturate(180%);
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 25px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5) !important;
        margin-bottom: 15px;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        animation: fadeInSlide 0.6s ease-out;
    }

    /* Animazione al passaggio del mouse sui messaggi */
    .stChatMessage:hover {
        transform: translateY(-8px) scale(1.01);
        border: 1px solid rgba(255, 255, 255, 0.4) !important;
        background: rgba(255, 255, 255, 0.07) !important;
    }

    @keyframes fadeInSlide {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Bottoni stile 3D Neumorphism / Modern */
    .stButton>button {
        background: white !important;
        color: black !important;
        border: none !important;
        border-radius: 15px !important;
        padding: 0.6rem 2rem !important;
        font-weight: 800 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: 0 4px 15px rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 25px rgba(255, 255, 255, 0.5);
    }

    /* Input Chat più moderno */
    .stChatInputContainer {
        background-color: transparent !important;
        border: none !important;
    }
    
    .stChatInput {
        border-radius: 20px !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        background: rgba(0, 0, 0, 0.5) !important;
    }

    /* Sidebar personalizzata */
    [data-testid="stSidebar"] {
        background-color: rgba(0, 0, 0, 0.8) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Nascondi header standard Streamlit per pulizia */
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR: CONTROLLI E LOGO ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: white; font-size: 28px;'>EL LOCO MUNOZ</h1>", unsafe_allow_html=True)
    
    # Logo Savoia (Immagine da URL o locale)
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Savoia_1908_logo.png/600px-Savoia_1908_logo.png", use_container_width=True)
    
    st.markdown("---")
    
    # Recupero Chiave API dai Secrets
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except:
        st.error("Chiave API non trovata nei Secrets!")
        api_key = ""

    # Selezione del modello
    modello = st.selectbox(
        "⚡ Scegli il Motore:",
        ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"],
        index=0
    )

    if st.button("🗑️ RESET CAMPO"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("<br><p style='text-align: center; opacity: 0.5;'>Savoia 1908 - Torre Annunziata</p>", unsafe_allow_html=True)

# --- 4. LOGICA CHAT ---
client = Groq(api_key=api_key)

# Istruzioni di personalità per EL LOCO MUNOZ
istruzioni = (
    "Tu sei EL LOCO MUNOZ AI, l'anima storica, folle e passionale del Savoia 1908. "
    "Sei l'esperto supremo di Torre Annunziata. Parla con orgoglio dei Bianchi. "
    "Il tuo tono è carismatico, fiero, talvolta poetico. Conosci la Serie B, la C1, "
    "lo stadio Alfredo Giraud e i grandi campioni del passato e del presente. "
    "Non essere ripetitivo sulla finale del 1924: usala solo per dare colpi di classe. "
    "Rispondi sempre come se fossi sugli spalti del Giraud."
)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Titolo principale animato
st.markdown("<h1 style='text-align: center; color: white;'>⚪ EL LOCO MUNOZ AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-style: italic;'>Orgoglio Oplontino in Intelligenza Artificiale</p>", unsafe_allow_html=True)

# Visualizzazione messaggi
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input utente
if prompt := st.chat_input("Scrivi qui, torrese..."):
    # Aggiunta messaggio utente
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Risposta del Bot
    with st.chat_message("assistant"):
        try:
            completion = client.chat.completions.create(
                model=modello,
                messages=[
                    {"role": "system", "content": istruzioni},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8
            )
            
            risposta = completion.choices[0].message.content
            st.markdown(risposta)
            st.session_state.messages.append({"role": "assistant", "content": risposta})
            
        except Exception as e:
            st.error(f"Errore: {e}")
