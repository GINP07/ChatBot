import streamlit as st
from groq import Groq
import re

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
if "api_key" not in st.session_state:
    try:
        st.session_state.api_key = st.secrets["GROQ_API_KEY"]
    except:
        st.session_state.api_key = None

# --- 4. FUNZIONE SINTESI INTELLIGENTE AI (TITOLI) ---
# Chiama l'AI per generare un titolo sintetico basato sul contesto.
def generate_ai_summary(user_prompt, assistant_response):
    if st.session_state.api_key:
        client_summary = Groq(api_key=st.session_state.api_key)
        
        # Istruzioni per generare un titolo breve e pertinente
        sys_prompt = "Genera un titolo sintetico, massimo 6 parole, che riassuma questa conversazione. Non usare emoji."
        messages = [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": f"Domanda: {user_prompt}\nRisposta: {assistant_response}"}
        ]
        
        try:
            completion = client_summary.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                temperature=0.5, # Temperatura bassa per titoli coerenti
                max_tokens=20 # Risposta breve
            )
            summary = completion.choices[0].message.content.strip()
            # Pulisce eventuali virgolette o punti finali
            return re.sub(r'[".]$', '', summary)
        except Exception as e:
            return f"Chat: {user_prompt[:25]}..." # Fallback se l'API fallisce
    else:
        return "Nuova chat" # Fallback se API key manca

# --- 5. LOGICA SALVATAGGIO IMMEDIATO E NUOVA CHAT ---
# Salva la chat corrente istantaneamente e ne avvia una vuota.
def instant_new_chat():
    if st.session_state.messages:
        # Se non è vuota, salvala con l'ultimo titolo generato
        chat_id = f"chat_{len(st.session_state.chat_sessions)}"
        # Aggiungi in cima alla lista (Recent)
        st.session_state.chat_sessions.insert(0, {
            "id": chat_id,
            "title": st.session_state.current_title,
            "content": list(st.session_state.messages)
        })
    # Reset per nuova chat vuota
    st.session_state.messages = []
    st.session_state.current_title = "Nuova chat"

# --- 6. CSS PERSONALIZZATO (TUTTI I CAMBIAMENTI RICHIESTI) ---
st.markdown(f"""
    <style>
    /* 1. Sfondo generale */
    .stApp {{
        background-image: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url("{URL_SFONDO}");
        background-size: cover;
        background-attachment: fixed;
    }}

    /* 2. Header Fisso e Centrato (El Loco Munoz AI) */
    .header-container {{
        position: fixed;
        top: 0; left: 0; width: 100%; height: 65px;
        background: rgba(255, 255, 255, 0.98);
        display: flex; align-items: center; justify-content: center; /* Centratura totale */
        z-index: 1000;
        border-bottom: 1px solid #ddd;
        padding: 0 40px;
    }}
    /* Burger icon placeholder */
    .header-container .burger-icon {{
        position: absolute; left: 40px; font-size: 24px; color: #000; cursor: pointer;
    }}
    /* Titolo Principale Centrato */
    .header-container .header-center-title {{
        color: #000 !important; font-weight: 800; font-size: 18px; text-transform: uppercase;
        letter-spacing: 1px; margin: 0;
    }}
    /* Sottotitolo (current chat title) */
    .header-container .header-subtitle {{
        color: #555 !important; font-weight: 500; font-style: italic; font-size: 13px; margin: 0 10px 0 0;
    }}
    /* Logo Savoia a destra */
    .header-container .header-right-logo {{
        position: absolute; right: 40px; height: 35px;
        }}

    /* 3. Area Contenuto (Padding Header) */
    .main .block-container {{
        max-width: 800px !important;
        padding-top: 90px !important; /* Margine per non finire sotto l'header */
    }}

    /* 4. Sidebar Grigia (f0f0f0 - non nera) */
    [data-testid="stSidebar"] {{
        background-color: #f0f0f0 !important;
        border-right: 1px solid #ddd;
    }}
    /* Colori testi e icone adattati al grigio */
    [data-testid="stSidebar"] .stMarkdown p, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] span {{
        color: #333 !important;
    }}
    
    /* 5. Pulsante "Nuova chat" stilizzato (Gemini style) */
    .sidebar-btn-new {{
        border: 1px solid #ccc !important;
        background-color: #e8e8e8 !important;
        color: #333 !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
    }}
    .sidebar-btn-new:hover {{
        background-color: #dadada !important;
    }}

    /* 6. Cronologia Chat: No X, Allineamento a Sinistra, Hover */
    .sidebar-history-item {{
        width: 100% !important;
        border: none !important;
        background-color: transparent !important;
        color: #444 !important;
        text-align: left !important;
        padding: 10px 15px !important;
        transition: 0.2s;
        display: block !important;
        border-radius: 8px !important;
    }}
    .sidebar-history-item:hover {{
        background-color: rgba(0,0,0,0.05) !important;
        color: #000 !important;
    }}
    
    /* 7. Menù a comparsa (Gemini style con popover) */
    .stPopover > button {{
        background-color: transparent !important;
        border: none !important;
        color: #888 !important;
        padding: 0 !important;
        margin: 0;
    }}
    
    /* 8. Messaggi Chat (Effetto Nuvola) */
    .stChatMessage {{
        background: rgba(255, 255, 255, 0.08) !important;
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 18px !important;
        margin-bottom: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }}
    .stChatMessage p {{
        color: #FFFFFF !important;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.5);
    }}

    /* 9. Barra Input "Fluttuante" (PULITA - No grigio, solo Pill) */
    [data-testid="stChatInputContainer"] {{
        background-color: transparent !important;
        border: none !important;
        bottom: 30px !important;
    }}
    .stChatInput {{
        max-width: 700px !important;
        margin: 0 auto !important;
    }}
    .stChatInput textarea {{
        background-color: #FFFFFF !important; /* Sfondo bianco standard */
        border-radius: 25px !important; /* Bordi smussati */
        border: 1px solid #ccc !important;
        color: #000 !important;
        padding: 12px 20px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3) !important;
    }}
    </style>

    <div class="header-container">
        <!-- Burger icon placeholder for visual reference, not used for actual toggle -->
        <div class="burger-icon">☰</div>
        <!-- Main title: EL LOCO MUNOZ AI - Centered and permanent -->
        <h1 class="header-center-title">EL LOCO MUÑOZ AI</h1>
        <!-- Current chat dynamic title as subtitle -->
        <span class="header-subtitle">{st.session_state.current_title}</span>
        <!-- Savoia logo to the right -->
        <img src="{URL_LOGO_SAVOIA}" class="header-right-logo">
    </div>
    """, unsafe_allow_html=True)

# --- 7. SIDEBAR ---
with st.sidebar:
    st.markdown("<br><br>", unsafe_allow_html=True)
    # Pulsante Nuova Chat: Salva immediatamente quella attuale se piena
    if st.button("✨ Nuova chat", use_container_width=True, key="new_chat_btn", type="primary"):
        instant_new_chat()
        st.rerun()
    
    st.markdown("---")
    st.caption("RECENTI")
    
    # Lista Cronologia con Menù Gemini Style (Puntini e Popover)
    for i, session in enumerate(st.session_state.chat_sessions):
        # Colonne per allineare il nome a sinistra e i puntini a destra
        col_title, col_menu = st.columns([0.9, 0.1])
        
        with col_title:
            # Nome della chat allineato a sinistra (con hover effect CSS)
            if st.button(session['title'], key=f"load_{i}", use_container_width=True, help="Carica chat"):
                # Se è la chat attuale, non fare nulla
                if st.session_state.messages == session['content']:
                    pass
                else:
                    # Carica la chat selezionata
                    st.session_state.messages = session['content']
                    st.session_state.current_title = session['title']
                    st.rerun()
        
        with col_menu:
            # Tasto "tre puntini" verticale (⋮)
            with st.popover("⋮", key=f"popover_{i}"):
                # Menù a comparsa (stile Gemini) con icone e azioni
                # Condividi (placeholder)
                st.markdown(f'<a href="#" style="text-decoration: none; color: #333; display: block; margin-bottom: 10px;">'
                            f'<span style="font-size: 16px; margin-right: 10px;">🔗</span>Condividi conversazione</a>', unsafe_allow_html=True)
                # Fissa (placeholder)
                st.markdown(f'<a href="#" style="text-decoration: none; color: #333; display: block; margin-bottom: 10px;">'
                            f'<span style="font-size: 16px; margin-right: 10px;">📌</span>Fissa</a>', unsafe_allow_html=True)
                # Rinomina (placeholder)
                st.markdown(f'<a href="#" style="text-decoration: none; color: #333; display: block; margin-bottom: 10px;">'
                            f'<span style="font-size: 16px; margin-right: 10px;">✏️</span>Rinomina</a>', unsafe_allow_html=True)
                
                # Elimina (azione reale con conferma)
                st.markdown(f'<a href="#" style="text-decoration: none; color: #d32f2f; display: block;">'
                            f'<span style="font-size: 16px; margin-right: 10px;">🗑️</span>Elimina</a>', unsafe_allow_html=True)
                # Utilizziamo un button invisibile sovrapposto per catturare il click reale senza ricaricare la pagina
                if st.button(session['title'], key=f"confirm_del_{i}", help="Clicca per confermare eliminazione", use_container_width=True):
                    st.session_state.chat_sessions.pop(i)
                    st.rerun()

# --- 8. TASTO CHIUSURA SIDEBAR (Tre lineette) ---
# Un pulsante fluttuante in alto a sinistra per aprire/chiudere la sidebar.
# L'effetto toggle è gestito nativamente da Streamlit tramite lo stato iniziale.
# Questo pulsante agisce come toggle nativo.
# Per renderlo funzionale come toggle dinamico, ricarichiamo la pagina forzando il cambio stato.
if st.session_state.get('initial_sidebar_state', 'expanded') == 'expanded':
    if st.button("☰", key="sidebar_close_btn", help="Chiudi sidebar"):
        st.session_state.initial_sidebar_state = 'collapsed'
        st.rerun()
else:
    if st.button("☰", key="sidebar_open_btn", help="Apri sidebar"):
        st.session_state.initial_sidebar_state = 'expanded'
        st.rerun()

# --- 9. CORE AI ---
if not st.session_state.api_key:
    st.error("Configura GROQ_API_KEY nei Secrets.")
    st.stop()

client = Groq(api_key=st.session_state.api_key)

# Visualizzazione dei messaggi correnti
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input Utente (PULITO: No grigio, Pill shape)
if prompt := st.chat_input("Chiedi al Loco..."):
    # Aggiungi messaggio utente
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Personalità del bot
            sys_instr = "Sei El loco Muñoz, l'anima ruggente del Savoia 1908. Rispondi con fierezza torrese."
            messages_full = [{"role": "system", "content": sys_instr}] + st.session_state.messages
            
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages_full,
                temperature=0.7
            )
            res = completion.choices[0].message.content
            
            # SINTESI INTELLIGENTE TITOLO (AI): Al primo scambio, genera il titolo AI dinamico
            if len(st.session_state.messages) == 1:
                # Chiama la funzione per generare il titolo tramite AI
                st.session_state.current_title = generate_ai_summary(prompt, res)
            
            st.markdown(res)
            st.session_state.messages.append({"role": "assistant", "content": res})
            st.rerun()
        except Exception as e:
            st.error(f"Errore: {e}")
