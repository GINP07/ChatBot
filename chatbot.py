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
# NUOVO: ID della chat attuale caricata
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None
if "api_key" not in st.session_state:
    try:
        st.session_state.api_key = st.secrets["GROQ_API_KEY"]
    except:
        st.session_state.api_key = None

# ... generate_ai_summary rimarrà invariato ...
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

# NUOVO: Logica reset alla schermata di benvenuto
def reset_to_welcome():
    """Resetta l'interfaccia alla schermata di benvenuto senza salvare."""
    st.session_state.messages = []
    st.session_state.current_title = "Nuova chat"
    st.session_state.current_chat_id = None # Rimuovi ID chat attuale

# --- 4. CSS AGGIORNATO (HEADER CENTRALIZZATO E NASCONDI FRECCIA POPOVER) ---
st.markdown(f"""
    <style>
    /* 1. Sfondo generale */
    .stApp {{
        background-image: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url("{URL_SFONDO}");
        background-size: cover;
        background-attachment: fixed;
    }}

    /* 2. Header Fisso e Centrato (El Loco Munoz AI + Titolo Chat sotto) */
    .header-container {{
        position: fixed;
        top: 0; left: 0; width: 100%; height: 65px;
        background: rgba(255, 255, 255, 0.98);
        display: flex; align-items: center; justify-content: center; /* Centratura totale */
        z-index: 999;
        border-bottom: 1px solid #ddd;
        padding: 0 40px;
    }}
    /* Burger icon placeholder - rimosso CSS specifico Sezione 8 ma mantenuto placeholder HTML */
    .header-container .burger-icon {{
        /* Burger icon placeholder - rimosso CSS specifico */
    }}
    
    /* Logo Savoia a destra con posizionamento assoluto */
    .header-container .header-right-logo {{
        position: absolute; right: 40px; height: 35px;
        }}
    /* Container per Titolo e Sottotitolo centrali */
    .header-container .header-titles-group {{
        display: flex; flex-direction: column; align-items: center;
    }}
    /* Titolo Principale Centrato */
    .header-container .header-titles-group .header-center-title {{
        color: #000 !important; font-weight: 800; font-size: 18px; text-transform: uppercase;
        letter-spacing: 1px; margin: 0;
    }}
    /* Sottotitolo (current chat title) */
    .header-container .header-titles-group .header-subtitle {{
        color: #555 !important; font-weight: 500; font-style: italic; font-size: 13px; margin: 0;
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
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label {{ /* Aggiunto label per Rinomina input */
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
    .sidebar-history-item-container {{
        width: 100%;
        text-align: left;
    }}
    .sidebar-history-item {{
        width: 100% !important;
        border: none !important;
        background-color: transparent !important;
        color: #444 !important;
        text-align: left !important;
        padding: 10px 15px !important;
        font-size: 14px !important;
        transition: 0.2s;
        display: block !important;
        border-radius: 8px !important;
    }}
    .sidebar-history-item:hover {{
        background-color: rgba(0,0,0,0.05) !important;
        color: #000 !important;
    }}
    
    /* 7. Menù a comparsa (Gemini style con popover) */
    [data-testid="stSidebar"] .stPopover > button {{
        background-color: transparent !important;
        border: none !important;
        color: #888 !important;
        padding: 0 !important;
        margin: 0;
    }}
    
    /* NUOVO CSS mirato: Nascondi la freccia nel popover dei tre puntini verticali (⋮) */
    [data-testid="stSidebar"] .stPopover > button div > span:last-child {{
        display: none !important;
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
        <!-- Burger icon placeholder - rimosso in Sezione 8 ma mantenuto placeholder HTML -->
        <div class="burger-icon"></div>
        <!-- Group for centered title and subtitle -->
        <div class="header-titles-group">
            <!-- Main title: EL LOCO MUNOZ AI - Centered and permanent -->
            <h1 class="header-center-title">EL LOCO MUÑOZ AI</h1>
            <!-- Current chat dynamic title as subtitle -->
            <span class="header-subtitle">{st.session_state.current_title}</span>
        </div>
        <!-- Savoia logo to the right -->
        <img src="{URL_LOGO_SAVOIA}" class="header-right-logo">
    </div>
    """, unsafe_allow_html=True)

# ... RIMOSSO: Sezione 8 TASTO CHIUSURA SIDEBAR (Tre lineette) ...

# --- 6. SIDEBAR AGGIORNATA (LOGICA FUNZIONI CHAT) ---
with st.sidebar:
    st.markdown("<br><br>", unsafe_allow_html=True)
    # Pulsante Nuova Chat: Ora resetta l'interfaccia senza salvare
    if st.button("✨ Nuova chat", use_container_width=True, key="new_chat_btn", type="primary"):
        reset_to_welcome()
        st.rerun()
    
    st.markdown("---")
    st.caption("RECENTI")
    
    # Lista Cronologia con Menù Gemini Style (Puntini e Popover funzionanti, no freccia)
    for i, session in enumerate(st.session_state.chat_sessions):
        # Colonne per allineare il nome a sinistra e i puntini a destra
        col_title, col_menu = st.columns([0.9, 0.1])
        
        with col_title:
            # Nome della chat allineato a sinistra (con hover effect CSS)
            st.markdown(f'<div class="sidebar-history-item-container">', unsafe_allow_html=True)
            if st.button(session['title'], key=f"load_{i}", use_container_width=True, help="Carica chat", type="secondary"):
                # Se è la chat attuale, non fare nulla (ottimizzazione)
                if st.session_state.current_chat_id != session.get('id'):
                    # Carica la chat selezionata
                    st.session_state.messages = session['content']
                    st.session_state.current_title = session['title']
                    st.session_state.current_chat_id = session.get('id') # Imposta ID attuale
                    st.rerun()
            st.markdown(f'</div>', unsafe_allow_html=True)
        
        with col_menu:
            # Tasto "tre puntini" verticale (⋮) con CSS per nascondere la freccia giù
            # use_container_width=False per il popover stesso
            with st.popover("⋮", key=f"popover_{i}", use_container_width=False):
                # Menù a comparsa (stile Gemini) con pulsanti funzionanti
                
                st.markdown("**Gestisci chat**")
                
                # 1. Fissa conversazione (placeholder per ora)
                if st.button("📌 Fissa", key=f"fissa_{i}", use_container_width=True):
                    st.toast("Funzione 'Fissa' non ancora implementata.")
                    # st.rerun()
                
                # 2. Rinomina (mostra input e salva)
                with st.container():
                    st.markdown("**Rinomina**")
                    col_input, col_save = st.columns([0.7, 0.3])
                    with col_input:
                        new_title = st.text_input("Nuovo titolo", value=session['title'], key=f"rinomina_in_{i}", label_visibility="collapsed")
                    with col_save:
                        if st.button("💾", key=f"salva_{i}", help="Salva nuovo titolo", type="primary"):
                            if new_title and new_title != session['title']:
                                # Semplice rinomina manuale
                                final_title = new_title 
                                st.session_state.chat_sessions[i]['title'] = final_title
                                
                                # Se stiamo rinominando la chat attuale, aggiorna anche l'header subtitle
                                if st.session_state.current_chat_id == session.get('id'):
                                    st.session_state.current_title = final_title
                                    
                                st.rerun() # Chiude popover e aggiorna sidebar

                # 3. Condividi (placeholder per ora)
                if st.button("🔗 Condividi", key=f"condividi_{i}", use_container_width=True):
                    st.toast("Funzione 'Condividi' non ancora implementata.")
                    # st.rerun()

                # 4. Elimina conversazione (conferma)
                with st.expander("🗑️ Elimina conversazione"):
                    st.warning("Sei sicuro? Questa azione non è reversibile.")
                    if st.button("Conferma eliminazione", key=f"confirm_del_{i}", type="primary", use_container_width=True):
                        st.session_state.chat_sessions.pop(i)
                        # Se stiamo eliminando la chat attuale, resetta l'interfaccia
                        if st.session_state.get('current_chat_id') == session.get('id'):
                            reset_to_welcome()
                        st.rerun()

# ... CORE AI AGGIORNATO (LOGICA CREAZIONE CHAT DOPO PRIMO SCAMBIO COMPLETO) ...
if not st.session_state.api_key:
    st.error("Configura GROQ_API_KEY nei Secrets.")
    st.stop()

client = Groq(api_key=st.session_state.api_key)

# Visualizzazione dei messaggi correnti
# NUOVO: Aggiungi un contenitore principale per l'area chat per gestire lo scroll se necessario
chat_container = st.container()

with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Input Utente (PULITO: No grigio, Pill shape)
if prompt := st.chat_input("Chiedi al Loco..."):
    # Aggiungi messaggio utente
    st.session_state.messages.append({"role": "user", "content": prompt})
    with chat_container:
        with st.chat_message("user"):
            st.markdown(prompt)

    with chat_container:
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
                
                st.markdown(res)
                st.session_state.messages.append({"role": "assistant", "content": res})
                
                # AGGIORNATO: Al primo scambio completo (utente e assistente), genera titolo AI e SALVA
                if len(st.session_state.messages) == 2:
                    # Chiama la funzione per generare il titolo tramite AI
                    st.session_state.current_title = generate_ai_summary(prompt, res)
                    
                    # Salva questa NUOVA chat
                    chat_id = f"chat_{len(st.session_state.chat_sessions)}"
                    st.session_state.current_chat_id = chat_id # Imposta ID attuale
                    st.session_state.chat_sessions.insert(0, {
                        "id": chat_id,
                        "title": st.session_state.current_title,
                        "content": list(st.session_state.messages)
                    })
                
                st.rerun() # Forza aggiornamento per vedere i messaggi e il titolo header
            except Exception as e:
                st.error(f"Errore: {e}")
