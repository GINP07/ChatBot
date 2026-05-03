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
    if st.session_state.api_key:
        client_summary = Groq(api_key=st.session_state.api_key)
        sys_prompt = "Genera un titolo sintetico, massimo 5 parole. No emoji."
        messages = [{"role": "system", "content": sys_prompt}, {"role": "user", "content": f"D: {user_prompt}"}]
        try:
            completion = client_summary.chat.completions.create(model="llama-3.3-70b-versatile", messages=messages, temperature=0.5, max_tokens=15)
            return re.sub(r'[".]$', '', completion.choices[0].message.content.strip())
        except: return f"{user_prompt[:20]}..."
    return "Nuova chat"

def reset_to_welcome():
    st.session_state.messages = []
    st.session_state.current_title = "Nuova chat"
    st.session_state.current_chat_id = None

# --- 4. CSS CUSTOM (NERO/BIANCO E PULIZIA) ---
st.markdown(f"""
    <style>
    /* Sfondo generale */
    .stApp {{
        background-image: linear-gradient(rgba(0,0,0,0.75), rgba(0,0,0,0.75)), url("{URL_SFONDO}");
        background-size: cover;
        background-attachment: fixed;
    }}

    /* Header superiore */
    .header-container {{
        position: fixed; top: 0; left: 0; width: 100%; height: 70px;
        background: rgba(255, 255, 255, 0.98);
        display: flex; align-items: center; justify-content: center;
        z-index: 999; border-bottom: 2px solid #000;
    }}
    .header-center-title {{ color: #000 !important; font-weight: 900; font-size: 22px; text-transform: uppercase; margin: 0; letter-spacing: 1px; }}

    /* Sidebar */
    [data-testid="stSidebar"] {{ background-color: #ffffff !important; border-right: 1px solid #ddd; }}
    
    /* Popover (Freccetta) - Pulizia Totale */
    [data-testid="stSidebar"] .stPopover > button {{
        border: none !important;
        background: transparent !important;
        color: #999 !important;
        padding: 0 !important;
        font-size: 14px !important;
    }}
    [data-testid="stSidebar"] .stPopover > button div > span:last-child {{ display: none !important; }}

    /* 3D Card Benvenuto */
    .welcome-container {{ display: flex; flex-direction: column; align-items: center; justify-content: center; height: 60vh; text-align: center; }}
    .image-3d-card {{
        width: 380px; height: 210px; border-radius: 12px;
        background-image: url('{URL_IMMAGINE_BENVENUTO}');
        background-size: cover; box-shadow: 0 25px 50px rgba(0,0,0,0.6);
        transition: transform 0.6s cubic-bezier(0.2, 0.8, 0.2, 1);
        transform-style: preserve-3d; border: 1px solid rgba(255,255,255,0.1);
    }}
    .image-3d-card:hover {{ transform: perspective(1000px) rotateX(5deg) rotateY(-5deg) scale(1.02); }}

    /* Chat Bubbles */
    .stChatMessage {{ background: rgba(255,255,255,0.05) !important; border-radius: 15px !important; margin-bottom: 10px; border: 1px solid rgba(255,255,255,0.1) !important; }}
    .stChatMessage p {{ color: #eee !important; font-size: 16px; }}
    </style>

    <div class="header-container">
        <div style="text-align:center;">
            <h1 class="header-center-title">EL LOCO MUÑOZ AI</h1>
            <div style="font-size:11px; color:#777; text-transform: uppercase; font-weight: bold;">{st.session_state.current_title}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 5. SIDEBAR: GESTIONE MODERNA ---
with st.sidebar:
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Pulsante Nuova Chat (Nero/Bianco con stylable container)
    with stylable_container(
        key="black_button",
        css_styles="""
            button {
                background-color: #000000 !important;
                color: #ffffff !important;
                border-radius: 5px !important;
                font-weight: bold !important;
                text-transform: uppercase !important;
                border: none !important;
                height: 45px !important;
            }
        """,
    ):
        if st.button("Nuova chat", use_container_width=True):
            reset_to_welcome()
            st.rerun()
    
    st.markdown("---")
    st.caption("STORICO CONVERSAZIONI")
    
    # Lista Chat
    for i, session in enumerate(st.session_state.chat_sessions):
        col_chat, col_opt = st.columns([0.85, 0.15])
        
        with col_chat:
            if st.button(session['title'], key=f"session_{i}", use_container_width=True):
                st.session_state.messages = session['content']
                st.session_state.current_title = session['title']
                st.session_state.current_chat_id = session.get('id')
                st.rerun()
        
        with col_opt:
            with st.popover("▼", key=f"pop_{i}"):
                # Opzioni senza emoji
                st.markdown("**Opzioni chat**")
                new_title = st.text_input("Rinomina", value=session['title'], key=f"rename_{i}")
                if st.button("Conferma nome", key=f"sv_{i}", use_container_width=True):
                    st.session_state.chat_sessions[i]['title'] = new_title
                    st.rerun() # Il rerun chiude il menu automaticamente
                
                st.markdown("---")
                
                if st.button("Elimina", key=f"del_{i}", use_container_width=True):
                    tid = session.get('id')
                    st.session_state.chat_sessions.pop(i)
                    if st.session_state.current_chat_id == tid:
                        reset_to_welcome()
                    st.rerun() # Il rerun chiude il menu automaticamente e torna alla home

# --- 6. AREA CHAT PRINCIPALE ---
if st.session_state.api_key:
    client = Groq(api_key=st.session_state.api_key)

    if not st.session_state.messages:
        # Schermata Iniziale
        st.markdown(f"""
            <div class="welcome-container">
                <div class="image-3d-card"></div>
                <div style="margin-top:40px; color:#fff;">
                    <h2 style="letter-spacing:4px; font-weight:300;">ONORA LA MAGLIA</h2>
                    <p style="opacity:0.5; font-style: italic;">Parla con la leggenda del Savoia 1908.</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        # Render messaggi
        for m in st.session_state.messages:
            with st.chat_message(m["role"]):
                st.markdown(m["content"])

    # Input Chat
    if prompt := st.chat_input("Invia un messaggio..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.rerun()

    # Risposta AI
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        with st.chat_message("assistant"):
            sys_instr = "Sei El loco Muñoz. Rispondi con la foga e l'orgoglio di un guerriero del Savoia."
            msgs = [{"role": "system", "content": sys_instr}] + st.session_state.messages
            
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=msgs,
                temperature=0.7
            )
            res = completion.choices[0].message.content
            st.markdown(res)
            st.session_state.messages.append({"role": "assistant", "content": res})
            
            # Salvataggio sessione
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
