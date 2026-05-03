import streamlit as st
from groq import Groq

# --- 1. CONFIGURAZIONE PAGINA ---
st.set_page_config(
    page_title="EL LOCO MUNOZ AI", 
    page_icon="⚪", 
    layout="wide"
)

# --- CONFIGURAZIONE SFONDO ---
# Incolla qui il link della tua immagine (assicurati che finisca in .jpg, .png o .webp)
URL_SFONDO = "https://images.unsplash.com/photo-1557683316-973673baf926?q=80&w=2029&auto=format&fit=crop" 

# --- 2. CSS AVANZATO (CONTRASTO E LEGGIBILITÀ) ---
st.markdown(f"""
    <style>
    /* Sfondo Immagine con Overlay Scuro */
    .stApp {{
        background-image: url("{URL_SFONDO}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* Filtro scuro per far risaltare il testo */
    .stApp::before {{
        content: "";
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0, 0, 0, 0.7); /* Aumentato a 0.7 per massimo contrasto */
        z-index: -1;
    }}

    /* TESTO BIANCO ASSOLUTO PER TUTTO */
    h1, h2, h3, p, span, li, label, .stMarkdown {{
        color: #FFFFFF !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.8) !important;
    }}

    /* MESSAGGI CHAT: EFFETTO VETRO CHIARO */
    .stChatMessage {{
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 20px !important;
        margin-bottom: 15px;
        padding: 15px !important;
    }}

    /* STILE TESTO NEI MESSAGGI */
    .stChatMessage p {{
        color: #FFFFFF !important;
        font-size: 1.1rem !important;
        line-height: 1.5;
    }}

    /* SIDEBAR: SCURA ED ELEGANTE */
    [data-testid="stSidebar"] {{
        background-color: rgba(10, 10, 10, 0.9) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }}

    /* INPUT CHAT: VISIBILE */
    .stChatInput textarea {{
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 15px !important;
    }}
    
    /* FIX PER ICONE E BOTTONI SIDEBAR */
    .stSelectbox label {{ color: white !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR: LOGO E IMPOSTAZIONI ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; border-bottom: 2px solid white; padding-bottom: 10px;'>EL LOCO MUNOZ</h1>", unsafe_allow_html=True)
    
    # Logo del Savoia
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Savoia_1908_logo.png/600px-Savoia_1908_logo.png", use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Recupero Chiave API
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except:
        st.error("ERRORE: Chiave API mancante nei Secrets!")
        api_key = ""

    modello = st.selectbox("⚡ POTENZA AI:", ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"])
    
    if st.button("🗑️ SVUOTA CAMPO"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown("<p style='text-align: center; opacity: 0.7;'>Torre Annunziata Biancoscudata</p>", unsafe_allow_html=True)

# --- 4. LOGICA DEL CHATBOT ---
client = Groq(api_key=api_key)

istruzioni = (
    "Tu sei EL LOCO MUNOZ AI, l'anima ruggente del Savoia 1908. "
    "Sei l'autorità massima su Torre Annunziata e sulla maglia bianca. "
    "Parla con grinta, amore e competenza. Conosci il Giraud come le tue tasche. "
    "Il tuo obiettivo è difendere e raccontare la storia del Savoia con orgoglio. "
    "Non essere monotematico sulla finale del '24, spazia su tutta la storia centenaria."
)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Header centrale
st.markdown("<h1 style='text-align: center; font-size: 50px;'>⚪ EL LOCO MUNOZ AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 20px;'>L'intelligenza artificiale al servizio dei Bianchi</p>", unsafe_allow_html=True)

# Visualizzazione della conversazione
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input utente
if prompt := st.chat_input("Fammi una domanda sul nostro Savoia..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

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
            st.error(f"Errore tecnico: {e}")
