import streamlit as st
from groq import Groq

# --- 1. CONFIGURAZIONE PAGINA E STILE ---
st.set_page_config(page_title="Savoia & Napoli AI", page_icon="⚽", layout="wide")

# CSS personalizzato per un tocco azzurro e bordi arrotondati
st.markdown("""
    <style>
    .stChatMessage { border-radius: 15px; border: 1px solid #71b7e6; margin-bottom: 10px; }
    .stChatInput { border-top: 2px solid #71b7e6; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SIDEBAR (BARRA LATERALE) ---
with st.sidebar:
    st.title("⚙️ Impostazioni")
    st.info("Configura il tuo esperto di calcio campano.")
    
    # Inserisci qui la tua chiave GSK per non doverla digitare ogni volta
    api_key = st.secrets["GROQ_API_KEY"]
    
    # Selezione del modello (Llama 3.3 è il top attuale)
    modello_scelto = st.selectbox(
        "Cervello del bot:",
        ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"],
        index=0
    )
    
    # Bottone per resettare la conversazione
    if st.button("🗑️ Svuota Chat"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.write("🏟️ **Savoia 1908**: Vice-campione d'Italia 1924")
    st.write("💙 **SSC Napoli**: La storia continua")

# --- 3. LOGICA DEL CHATBOT ---
# Inizializziamo il client Groq
client = Groq(api_key=api_key)

# Definizione del carattere del bot
istruzioni = (
    "Sei un esperto appassionato della SSC Napoli e del Savoia 1908. "
    "Rispondi in modo colto, fiero e coinvolgente. Usa un tono caloroso e campano. "
    "Se ti chiedono del Savoia, esalta la finale del 1924 contro il Genoa."
)

# Inizializzazione della cronologia
if "messages" not in st.session_state:
    st.session_state.messages = []

# Layout principale: Titolo
st.title("⚽ Esperto Napoli & Savoia AI")
st.caption("Passione azzurra e biancoscudata con la velocità di Groq.")

# Mostra i messaggi a video
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Gestione dell'input utente
if prompt := st.chat_input("Chiedimi della finale del 1924 o del Napoli..."):
    # Aggiungi messaggio utente alla memoria
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generazione risposta dell'assistente
    with st.chat_message("assistant"):
        try:
            # Chiamata API a Groq
            completion = client.chat.completions.create(
                model=modello_scelto,
                messages=[
                    {"role": "system", "content": istruzioni},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            
            risposta = completion.choices[0].message.content
            st.markdown(risposta)
            
            # Salva la risposta nella memoria
            st.session_state.messages.append({"role": "assistant", "content": risposta})
            
        except Exception as e:
            st.error(f"Errore tecnico: {e}")
            st.info("Assicurati che la chiave API sia corretta e che il modello sia disponibile.")