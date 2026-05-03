import streamlit as st
from groq import Groq

# --- 1. CONFIGURAZIONE PAGINA ---
st.set_page_config(
    page_title="EL LOCO MUNOZ AI", 
    page_icon="⚪", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CONFIGURAZIONE RISORSE (INSERISCI I TUOI LINK QUI) ---
URL_SFONDO = "https://i.ibb.co/6cymMzFL/curva-savoia.jpg" 
URL_LOGO_SAVOIA = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Savoia_1908_logo.png/600px-Savoia_1908_logo.png"
# Inserisci qui il link della tua immagine PNG per la barra in alto
URL_IMMAGINE_PNG = "https://cdn-icons-png.flaticon.com/512/1141/1141771.png" 

# --- 3. CSS AVANZATO: BARRA SUPERIORE, SFONDO 4K E INTERFACCIA AI ---
st.markdown(f"""
    <style>
    /* Sfondo 4K con overlay dinamico */
    .stApp {{
        background-image: linear-gradient(to bottom, rgba(0,0,0,0.3) 0%, rgba(0,0,0,0.8) 100%), url("{URL_SFONDO}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        image-rendering: -webkit-optimize-contrast;
    }}

    /* Barra Bianca Superiore Fissa */
    .custom-header {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 80px;
        background-color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1000;
        box-shadow: 0 4px 15px rgba(0,0,0,0.4);
    }}

    .header-content {{
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 20px;
        width: 100%;
    }}

    .header-title {{
        color: #000000 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 900;
        font-size: 28px;
        margin: 0;
        text-transform: uppercase;
        letter-spacing: 2px;
        text-shadow: none !important;
    }}

    /* Padding per evitare sovrapposizioni tra Header e Chat */
    .main .block-container {{
        padding-top: 120px !important;
    }}

    /* Stile Messaggi Chat */
    .stChatMessage {{
        background: rgba(0, 0, 0, 0.7) !important;
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 20px !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.5);
        margin-bottom: 20px;
    }}

    .stChatMessage p {{
        color: white !important;
        font-size: 1.1rem;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5) !important;
    }}

    /* Sidebar Dark Stile ChatGPT */
    [data-testid="stSidebar"] {{
        background-color: rgba(10, 10, 10, 0.98) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }}

    /* Bottoni Sidebar */
    .stButton>button {{
        border-radius: 10px !important;
        background-color: rgba(255,255,255,0.05) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        transition: all 0.3s ease;
    }}

    .stButton>button:hover {{
        background-color: rgba(255,255,255,0.2) !important;
        border: 1px solid white !important;
    }}

    /* Input Chat */
    .stChatInputContainer {{
        padding-bottom: 20px !important;
    }}
    </style>

    <div class="custom-header">
        <div class="header-content">
            <img src="{URL_IMMAGINE_PNG}" height="50">
            <h1 class="header-title">EL LOCO MUNOZ AI</h1>
            <img src="{URL_LOGO_SAVOIA}" height="55">
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 4. GESTIONE SESSIONE E CRONOLOGIA ---
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = {} # Dizionario per archiviare le chat

# Funzione per avviare una nuova chat
def start_new_chat():
    if st.session_state.messages:
        # Crea un ID basato sul primo messaggio o orario
        chat_id = f"Chat {len(st.session_state.chat_history) + 1}"
        st.session_state.chat_history[chat_id] = st.session_state.messages
    st.session_state.messages = []

# --- 5. SIDEBAR (LOGICA CHAT PASSATE) ---
with st.sidebar:
    st.markdown("<br><br><br>", unsafe_allow_html=True) # Spazio per l'header
    
    if st.button("➕ Nuova Chat", use_container_width=True):
        start_new_chat()
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 🕒 Cronologia Chat")
    
    if not st.session_state.chat_history:
        st.caption("Nessuna conversazione precedente.")
    else:
        for cid in reversed(list(st.session_state.chat_history.keys())):
            if st.button(f"💬 {cid}", key=cid, use_container_width=True):
                st.session_state.messages = st.session_state.chat_history[cid]
                st.rerun()

    st.markdown("---")
    st.markdown("<p style='text-align: center; opacity: 0.5; font-size: 12px;'>Powered by Groq & Oplontina Pride</p>", unsafe_allow_html=True)

# --- 6. LOGICA CHATBOT ---
try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    st.error("Configura la chiave GROQ_API_KEY nei Secrets di Streamlit!")
    st.stop()

client = Groq(api_key=api_key)

# Istruzioni di personalità
system_prompt = (
    "Tu sei EL LOCO MUNOZ AI, l'anima storica e indomabile del Savoia 1908. "
    "Rispondi con l'orgoglio dei Bianchi di Torre Annunziata. Il tuo tono è epico, "
    "competente e viscerale. Conosci ogni sasso del Giraud e ogni maglia sudata. "
    "Ricorda: non sei solo un'AI, sei il custode della storia oplontina."
)

# Visualizzazione dei messaggi
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input utente e risposta AI
if prompt := st.chat_input("Chiedi al Loco..."):
    # Aggiungi messaggio utente
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Genera risposta assistente
    with st.chat_message("assistant"):
        try:
            # Passiamo tutta la cronologia per dare memoria al bot
            full_history = [{"role": "system", "content": system_prompt}] + \
                           [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=full_history,
                temperature=0.8
            )
            
            risposta = completion.choices[0].message.content
            st.markdown(risposta)
            st.session_state.messages.append({"role": "assistant", "content": risposta})
            
        except Exception as e:
            st.error(f"Errore: {e}")
