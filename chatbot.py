import streamlit as st
from groq import Groq

# --- 1. CONFIGURAZIONE PAGINA E STILE ---
st.set_page_config(page_title="EL LOCO MUNOZ AI", page_icon="⚪", layout="wide")

# CSS personalizzato: Tema Bianco, Nero e Grigio per il Savoia
st.markdown("""
    <style>
    .stChatMessage { border-radius: 15px; border: 1px solid #333333; margin-bottom: 10px; }
    .stChatInput { border-top: 2px solid #333333; }
    /* Cambia il colore del bottone sidebar */
    .stButton>button { background-color: #333333; color: white; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SIDEBAR (BARRA LATERALE) ---
with st.sidebar:
    st.title("⚽ EL LOCO MUNOZ AI")
    st.info("L'anima biancoscudata di Torre Annunziata.")
    
    api_key = st.secrets["GROQ_API_KEY"]
    
    modello_scelto = st.selectbox(
        "Cervello del bot:",
        ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"],
        index=0
    )
    
    if st.button("🗑️ Reset Conversazione"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.write("🏟️ **Savoia 1908**")
    st.write("⚪ **Colori**: Bianco Reale")
    st.write("⚓ **Città**: Torre Annunziata")

# --- 3. LOGICA DEL CHATBOT ---
client = Groq(api_key=api_key)

# Istruzioni calibrate: Esperto del Savoia, grintoso ma non ripetitivo
istruzioni = (
    "Tu sei EL LOCO MUNOZ AI, l'anima storica e passionale del Savoia 1908. "
    "Il tuo tono è fiero, esperto e profondamente legato a Torre Annunziata. "
    "Conosci ogni dettaglio della storia dei Bianchi: dai pionieri del calcio oplontino "
    "fino ai giorni nostri, passando per il Giraud, i campionati di Serie B e la C1. "
    "Non limitarti a citare sempre la finale del 1924; parlane solo se è pertinente "
    "alla domanda o se vuoi sottolineare la grandezza storica del club. "
    "Usa un linguaggio che mostri appartenenza (es. 'Noi Bianchi', 'La nostra maglia')."
)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Layout principale
st.title("⚪ EL LOCO MUNOZ AI")
st.caption("Risponde l'orgoglio di Torre Annunziata.")

# Mostra messaggi
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Gestione input
if prompt := st.chat_input("Chiedimi dei Bianchi, del Giraud o dei grandi bomber del Savoia..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            completion = client.chat.completions.create(
                model=modello_scelto,
                messages=[
                    {"role": "system", "content": istruzioni},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8 # Un po' più di 'follia' e carisma nel parlare
            )
            
            risposta = completion.choices[0].message.content
            st.markdown(risposta)
            st.session_state.messages.append({"role": "assistant", "content": risposta})
            
        except Exception as e:
            st.error(f"Errore tecnico: {e}")
