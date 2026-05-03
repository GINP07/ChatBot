import streamlit as st
from groq import Groq
import re
import streamlit_antd_components as sac
from streamlit_extras.stylable_container import stylable_container

# --- 1. CONFIGURAZIONE PAGINA ---
st.set_page_config(
    page_title="EL LOCO MUÑOZ AI", 
    page_icon="⚪", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. RISORSE ---
URL_SFONDO = "https://i.ibb.co/6cymMzFL/curva-savoia.jpg" 
URL_LOGO_SAVOIA = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Savoia_1908_logo.png/600px-Savoia_1908_logo.png"
URL_IMMAGINE_BENVENUTO = "https://i.ibb.co/6cymMzFL/curva-savoia.jpg" 

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
    """Sintesi intelligente del titolo basata su bot e utente"""
    if st.session_state.api_key:
        client_summary = Groq(api_key=st.session_state.api_key)
        sys_prompt = (
            "Sei un assistente che riassume conversazioni. "
            "Leggi la domanda dell'utente e la risposta dell'assistente e crea un titolo brevissimo (max 4-5 parole) "
            "che identifichi l'argomento. Non usare emoji, non usare virgolette, sii diretto."
        )
        user_content = f"UTENTE: {user_prompt}\nASSISTENTE: {assistant_response}"
        messages = [{"role": "system", "content": sys_prompt}, {"role": "user", "content": user_content}]
        try:
            completion = client_summary.chat.completions.create(model="llama-3.3-70b-versatile", messages=messages, temperature=0.3, max_tokens=20)
            return re.sub(r'[".]$', '', completion.choices[0].message.content.strip())
        except: return f"{user_prompt[:20]}..."
    return "Nuova chat"

def reset_to_welcome():
    st.session_state.messages = []
    st.session_state.current_title = "Nuova chat"
    st.session_state.current_chat_id = None

# --- 4. CSS CUSTOM (STILE NERO/BIANCO RIGOROSO) ---
st.markdown(f"""
    <style>
    .stApp {{
        background-image: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), url("{URL_SFONDO}");
        background-size: cover;
        background-attachment: fixed;
    }}

    /* Header */
    .header-container {{
        position: fixed; top: 0; left: 0; width: 100%; height: 70px;
        background: rgba(255, 255, 255, 0.98);
        display: flex; align-items: center; justify-content: center;
        z-index: 999; border-bottom: 2px solid #000;
    }}
    .header-center-title {{ color: #000 !important; font-weight: 900; font-size: 22px; text-transform: uppercase; margin: 0; }}

    /* Sidebar - Rimozione freccetta default bottoni cronologia */
    [data-testid="stSidebar"] {{ background-color: #ffffff !important; }}
    
    /* Forza stile bottoni cronologia: niente freccette, solo testo */
    [data-testid="stSidebar"] .stButton > button {{
        border: none !important;
        background-color: transparent !important;
        color: #333 !important;
        text-align: left !important;
        padding-left: 5px !important;
        font-weight: 500 !important;
    }}
    [data-testid="stSidebar"] .stButton > button:hover {{
        color: #000 !important;
        background-color: #f0f0f0 !important;
    }}

    /* Popover (Freccetta Opzioni) */
    [data-testid="stSidebar"] .stPopover > button {{
        border: none !important;
        background: transparent !important;
        color: #bbb !important;
    }}
    [data-testid="stSidebar"] .stPopover > button div > span:last-child {{ display: none !important; }}

    /* Welcome Card */
    .welcome-container {{ display: flex; flex-direction: column; align-items: center; justify-content: center; height: 60vh; }}
    .image-3d-card {{
        width: 350px; height: 200px; border-radius: 10px;
        background-image: url('{URL_IMMAGINE_BENVENUTO}');
        background-size: cover; box-shadow: 0 20px 40px rgba(0,0,0,0.6);
        border: 1px solid rgba(255,255,255,0.1);
    }}

    /* Chat Bubbles */
    .stChatMessage {{ background: rgba(255,255,255,0.05) !important; border-radius: 15px !important; border: 1px solid rgba(255,255,255,0.1) !important; }}
    </style>

    <div class="header-container">
        <div style="text-align:center;">
            <h1 class="header-center-title">EL LOCO MUÑOZ AI</h1>
            <div style="font-size:11px; color:#666; font-weight: bold; text-transform: uppercase;">{st.session_state.current_title}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 5. SIDEBAR ---
with st.sidebar:
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # PULSANTE NERO - NUOVA CHAT
    with stylable_container(
        key="new_chat_btn",
        css_styles="""
            button {
                background-color: #000 !important;
                color: #fff !important;
                border-radius: 4px !important;
                height: 45px !important;
                font-weight: 800 !important;
                border: none !important;
                width: 100% !important;
            }
        """,
    ):
        if st.button("NUOVA CHAT"):
            reset_to_welcome()
            st.rerun()
    
    st.markdown("---")
    
    for i, session in enumerate(st.session_state.chat_sessions):
        col_txt, col_opt = st.columns([0.85, 0.15])
        
        with col_txt:
            # Bottone pulito senza freccia
            if st.button(session['title'], key=f"s_{i}", use_container_width=True):
                st.session_state.messages = session['content']
                st.session_state.current_title = session['title']
                st.session_state.current_chat_id = session.get('id')
                st.rerun()
        
        with col_opt:
            with st.popover("▼", key=f"p_{i}"):
                new_n = st.text_input("Modifica titolo", value=session['title'], key=f"re_{i}")
                if st.button("Salva", key=f"sv_{i}", use_container_width=True):
                    st.session_state.chat_sessions[i]['title'] = new_n
                    st.rerun()
                if st.button("Elimina", key=f"dl_{i}", use_container_width=True):
                    tid = session.get('id')
                    st.session_state.chat_sessions.pop(i)
                    if st.session_state.current_chat_id == tid: reset_to_welcome()
                    st.rerun()

# --- 6. CHAT AREA ---
if st.session_state.api_key:
    client = Groq(api_key=st.session_state.api_key)

    if not st.session_state.messages:
        st.markdown(f"""
            <div class="welcome-container">
                <div class="image-3d-card"></div>
                <div style="margin-top:30px; text-align:center; color:#fff;">
                    <h2 style="letter-spacing:3px;">SANGUE BIANCOSCUDATO</h2>
                    <p style="opacity:0.6;">Chiedi e ti sarà risposto, con onore.</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        for m in st.session_state.messages:
            with st.chat_message(m["role"]):
                st.markdown(m["content"])

    if prompt := st.chat_input("Scrivi al Loco..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.rerun()

    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        with st.chat_message("assistant"):
            sys_instr = "Sei El loco Muñoz. Rispondi con la foga e l'orgoglio del Savoia 1908."
            msgs = [{"role": "system", "content": sys_instr}] + st.session_state.messages
            
            completion = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=msgs, temperature=0.7)
            res = completion.choices[0].message.content
            st.markdown(res)
            st.session_state.messages.append({"role": "assistant", "content": res})
            
            # Sintesi Intelligente (Prima e Seconda parte)
            if len(st.session_state.messages) == 2:
                st.session_state.current_title = generate_ai_summary(prompt, res)
                cid = f"id_{len(st.session_state.chat_sessions)}"
                st.session_state.current_chat_id = cid
                st.session_state.chat_sessions.insert(0, {
                    "id": cid, 
                    "title": st.session_state.current_title, 
                    "content": list(st.session_state.messages)
                })
            else:
                for s in st.session_state.chat_sessions:
                    if s["id"] == st.session_state.current_chat_id:
                        s["content"] = list(st.session_state.messages)
            st.rerun()
