import streamlit as st
from groq import Groq
import re

# --- 1. CONFIGURAZIONE PAGINA ---
st.set_page_config(
    page_title="EL LOCO MUNOZ AI", 
    page_icon="⚽", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. RISORSE ---
URL_SFONDO = "https://i.ibb.co/6cymMzFL/curva-savoia.jpg" 
URL_LOGO_SAVOIA = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Savoia_1908_logo.png/600px-Savoia_1908_logo.png"
URL_IMMAGINE_BENVENUTO = "https://i.ibb.co/6cymMzFL/curva-savoia.jpg" # Immagine per la card 3D

# --- 3. GESTIONE STATO ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = []
if "current_title" not in st.session_state:
    st.session_state.current_title = "Nuova chat"
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None
if "api_key" not in st.session_state:
    try:
        st.session_state.api_key = st.secrets["GROQ_API_KEY"]
    except:
        st.session_state.api_key = None

def generate_ai_summary(user_prompt, assistant_response):
    if st.session_state.api_key:
        client_summary = Groq(api_key=st.session_state.api_key)
        sys_prompt = "Genera un titolo sintetico, massimo 5 parole, che riassuma questa conversazione. Non usare emoji o punteggiatura finale."
        messages = [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": f"Domanda: {user_prompt}\nRisposta: {assistant_response}"}
        ]
        try:
            completion = client_summary.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                temperature=0.5,
                max_tokens=15
            )
            summary = completion.choices[0].message.content.strip()
            return re.sub(r'[".]$', '', summary)
        except:
            return f"{user_prompt[:20]}..."
    return "Nuova chat"

def reset_to_welcome():
    """Resetta l'interfaccia alla schermata di benvenuto 3D."""
    st.session_state.messages = []
    st.session_state.current_title = "Nuova chat"
    st.session_state.current_chat_id = None

# --- 4. CSS: DESIGN MODERNO E 3D ---
st.markdown(f"""
    <style>
    /* Sfondo generale */
    .stApp {{
        background-image: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url("{URL_SFONDO}");
        background-size: cover;
        background-attachment: fixed;
    }}

    /* Header Fisso e Centrato */
    .header-container {{
        position: fixed; top: 0; left: 0; width: 100%; height: 70px;
        background: rgba(255, 255, 255, 0.95);
        display: flex; align-items: center; justify-content: center;
        z-index: 999; border-bottom: 1px solid #ddd; padding: 0 40px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }}
    .header-right-logo {{ position: absolute; right: 40px; height: 40px; }}
    .header-titles-group {{ display: flex; flex-direction: column; align-items: center; }}
    .header-center-title {{ color: #000 !important; font-weight: 800; font-size: 19px; text-transform: uppercase; letter-spacing: 1px; margin: 0; }}
    .header-subtitle {{ color: #666 !important; font-weight: 500; font-style: italic; font-size: 13px; margin: 0; }}

    /* Layout Principale */
    .main .block-container {{
        max-width: 850px !important;
        padding-top: 100px !important;
        padding-bottom: 120px !important;
    }}

    /* EFFETTO 3D CARD BENVENUTO */
    .welcome-container {{
        display: flex; flex-direction: column; align-items: center;
        justify-content: center; height: 50vh; text-align: center;
        animation: fadeIn 0.8s ease-out;
    }}
    .image-3d-card {{
        width: 320px; height: 180px;
        border-radius: 20px;
        background-image: url('{URL_IMMAGINE_BENVENUTO}');
        background-size: cover; background-position: center;
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
        transition: transform 0.4s ease, box-shadow 0.4s ease;
        transform-style: preserve-3d;
        border: 2px solid rgba(255,255,255,0.15);
        margin-bottom: 25px;
    }}
    .image-3d-card:hover {{
        transform: perspective(1000px) rotateX(8deg) rotateY(-8deg) scale(1.05);
        box-shadow: -15px 25px 45px rgba(0,0,0,0.6);
        border: 2px solid rgba(255,255,255,0.4);
    }}
    .welcome-text h1 {{ color: #fff; font-weight: 800; font-size: 2.5rem; margin-bottom: 5px; text-shadow: 2px 2px 5px rgba(0,0,0,0.5); }}
    .welcome-text p {{ color: #ddd; font-size: 1.1rem; font-weight: 400; }}
    @keyframes fadeIn {{ from {{opacity: 0; transform: translateY(20px);}} to {{opacity: 1; transform: translateY(0);}} }}

    /* Sidebar Grigia */
    [data-testid="stSidebar"] {{
        background-color: #f4f4f4 !important;
        border-right: 1px solid #e0e0e0;
    }}
    [data-testid="stSidebar"] * {{ color: #222 !important; }}
    
    /* Cronologia e Allineamento Bottone Menu */
    .stSidebar .stButton>button {{ border-radius: 10px !important; }}
    
    /* Tasto Ingranaggio (Menu Popover) */
    [data-testid="stSidebar"] .stPopover > button {{
        background-color: transparent !important;
        border: none !important;
        color: #666 !important;
        padding: 5px !important;
        height: 100% !important; /* Allinea l'altezza */
        display: flex; align-items: center; justify-content: center;
        transition: 0.2s;
    }}
    [data-testid="stSidebar"] .stPopover > button:hover {{ background-color: #ddd !important; border-radius: 8px !important; color: #000 !important; }}
    /* Nascondi la freccettina di default del popover */
    [data-testid="stSidebar"] .stPopover > button div > span:last-child {{ display: none !important; }}

    /* Messaggi Chat (Nuvola) */
    .stChatMessage {{
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 20px !important;
        margin-bottom: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.15);
        padding: 15px 20px !important;
    }}
    .stChatMessage p {{ color: #fff !important; text-shadow: 1px 1px 2px rgba(0,0,0,0.4); font-size: 16px; }}

    /* Barra Input Fluttuante e Smussata */
    [data-testid="stChatInputContainer"] {{
        background-color: transparent !important;
        border: none !important;
        bottom: 30px !important;
    }}
    .stChatInput textarea {{
        background-color: #fff !important;
        border-radius: 30px !important;
        border: 1px solid #bbb !important;
        color: #000 !important;
        padding: 14px 22px !important;
        box-shadow: 0 5px 20px rgba(0,0,0,0.3) !important;
        font-size: 16px !important;
    }}
    </style>

    <div class="header-container">
        <div class="header-titles-group">
            <h1 class="header-center-title">EL LOCO MUÑOZ AI</h1>
            <span class="header-subtitle">{st.session_state.current_title}</span>
        </div>
        <img src="{URL_LOGO_SAVOIA}" class="header-right-logo">
    </div>
    """, unsafe_allow_html=True)


# --- 5. SIDEBAR: CRONOLOGIA E MENU MODERNO ---
with st.sidebar:
    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("✨ Nuova chat", use_container_width=True, type="primary"):
        reset_to_welcome()
        st.rerun()
    
    st.markdown("---")
    st.caption("STORICO CONVERSAZIONI")
    
    for i, session in enumerate(st.session_state.chat_sessions):
        # Colonne per allineare perfettamente il nome chat e l'icona
        col_title, col_menu = st.columns([0.85, 0.15])
        
        with col_title:
            if st.button(session['title'], key=f"load_{i}", use_container_width=True):
                if st.session_state.current_chat_id != session.get('id'):
                    st.session_state.messages = session['content']
                    st.session_state.current_title = session['title']
                    st.session_state.current_chat_id = session.get('id')
                    st.rerun()
        
        with col_menu:
            # Menu Popover moderno (Ingranaggio invece dei tre puntini)
            with st.popover("⚙️", key=f"popover_{i}"):
                st.markdown("**Opzioni Chat**")
                
                # RINOMINA
                new_title = st.text_input("Rinomina:", value=session['title'], key=f"rinomina_{i}")
                if st.button("💾 Salva nome", key=f"salva_{i}", use_container_width=True):
                    if new_title and new_title != session['title']:
                        st.session_state.chat_sessions[i]['title'] = new_title
                        if st.session_state.current_chat_id == session.get('id'):
                            st.session_state.current_title = new_title
                    st.rerun() # Forza il ricaricamento chiudendo il popover

                st.markdown("---")
                
                # ELIMINA
                if st.button("🗑️ Elimina Chat", key=f"elimina_{i}", type="primary", use_container_width=True):
                    st.session_state.chat_sessions.pop(i)
                    if st.session_state.get('current_chat_id') == session.get('id'):
                        reset_to_welcome()
                    st.rerun() # Elimina e chiude istantaneamente il popover


# --- 6. CORE AI E SCHERMATA BENVENUTO ---
if not st.session_state.api_key:
    st.error("⚠️ Configura GROQ_API_KEY nei Secrets di Streamlit.")
    st.stop()

client = Groq(api_key=st.session_state.api_key)

# Mostra il 3D SOLO se non ci sono messaggi
if not st.session_state.messages:
    st.markdown(f"""
        <div class="welcome-container">
            <div class="image-3d-card"></div>
            <div class="welcome-text">
                <h1>Pronto per la battaglia?</h1>
                <p>Chiedi al Loco qualsiasi cosa sulla storia e la passione del Savoia 1908.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
else:
    # Mostra la chat se ci sono messaggi
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# --- 7. INPUT UTENTE E RISPOSTA AI ---
if prompt := st.chat_input("Scrivi un messaggio al Loco..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            sys_instr = "Sei El loco Muñoz, l'anima ruggente e passionale del Savoia 1908. Rispondi con fierezza."
            messages_full = [{"role": "system", "content": sys_instr}] + st.session_state.messages
            
            with st.spinner("Il Loco sta scrivendo..."):
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=messages_full,
                    temperature=0.75
                )
                res = completion.choices[0].message.content
            
            st.markdown(res)
            st.session_state.messages.append({"role": "assistant", "content": res})
            
            # Se è il primo scambio della nuova chat, genera il titolo e salvala nella sidebar
            if len(st.session_state.messages) == 2:
                st.session_state.current_title = generate_ai_summary(prompt, res)
                chat_id = f"chat_{len(st.session_state.chat_sessions)}"
                st.session_state.current_chat_id = chat_id
                
                st.session_state.chat_sessions.insert(0, {
                    "id": chat_id,
                    "title": st.session_state.current_title,
                    "content": list(st.session_state.messages)
                })
            else:
                # Se la chat esiste già, aggiorna il suo contenuto nella cronologia
                for session in st.session_state.chat_sessions:
                    if session.get("id") == st.session_state.current_chat_id:
                        session["content"] = list(st.session_state.messages)
                        break
            
            st.rerun() # Aggiorna la vista (compreso il titolo in alto)
        except Exception as e:
            st.error(f"Errore di connessione: {e}")
