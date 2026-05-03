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

# --- 4. CSS (NERO/BIANCO E PULIZIA) ---
st.markdown(f"""
    <style>
    .stApp {{
        background-image: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url("{URL_SFONDO}");
        background-size: cover;
        background-attachment: fixed;
    }}

    .header-container {{
        position: fixed; top: 0; left: 0; width: 100%; height: 70px;
        background: rgba(255, 255, 255, 0.95);
        display: flex; align-items: center; justify-content: center;
        z-index: 999; border-bottom: 1px solid #ddd;
    }}
    .header-right-logo {{ position: absolute; right: 40px; height: 40px; }}
    .header-titles-group {{ display: flex; flex-direction: column; align-items: center; }}
    .header-center-title {{ color: #000 !important; font-weight: 800; font-size: 19px; text-transform: uppercase; margin: 0; }}
    .header-subtitle {{ color: #666 !important; font-weight: 500; font-style: italic; font-size: 13px; margin: 0; }}

    .main .block-container {{ max-width: 850px !important; padding-top: 100px !important; }}

    /* 3D CARD */
    .welcome-container {{ display: flex; flex-direction: column; align-items: center; justify-content: center; height: 50vh; }}
    .image-3d-card {{
        width: 320px; height: 180px; border-radius: 20px;
        background-image: url('{URL_IMMAGINE_BENVENUTO}');
        background-size: cover; box-shadow: 0 20px 40px rgba(0,0,0,0.4);
        transition: transform 0.4s ease; transform-style: preserve-3d;
        border: 2px solid rgba(255,255,255,0.15); margin-bottom: 25px;
    }}
    .image-3d-card:hover {{ transform: perspective(1000px) rotateX(8deg) rotateY(-8deg) scale(1.05); }}

    /* SIDEBAR */
    [data-testid="stSidebar"] {{ background-color: #f4f4f4 !important; }}
    
    /* PULSANTE NUOVA CHAT NERO */
    div[data-testid="stSidebar"] .stButton > button {{
        background-color: #000000 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: bold !important;
    }}

    /* ICONA FRECCETTA MENU */
    [data-testid="stSidebar"] .stPopover > button {{
        background-color: transparent !important;
        border: none !important;
        color: #000 !important;
        padding: 0px !important;
        font-size: 12px !important;
    }}
    /* Nascondi freccia extra di streamlit */
    [data-testid="stSidebar"] .stPopover > button div > span:last-child {{ display: none !important; }}

    /* CHAT BUBBLES */
    .stChatMessage {{
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(15px); border-radius: 20px !important;
        padding: 15px 20px !important; margin-bottom: 15px;
    }}
    .stChatMessage p {{ color: #fff !important; }}

    /* INPUT */
    [data-testid="stChatInputContainer"] {{ background-color: transparent !important; border: none !important; }}
    .stChatInput textarea {{ border-radius: 30px !important; box-shadow: 0 5px 20px rgba(0,0,0,0.3) !important; }}
    </style>

    <div class="header-container">
        <div class="header-titles-group">
            <h1 class="header-center-title">EL LOCO MUÑOZ AI</h1>
            <span class="header-subtitle">{st.session_state.current_title}</span>
        </div>
        <img src="{URL_LOGO_SAVOIA}" class="header-right-logo">
    </div>
    """, unsafe_allow_html=True)

# --- 5. SIDEBAR: MENU PULITO ---
with st.sidebar:
    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("Nuova chat", use_container_width=True):
        reset_to_welcome()
        st.rerun()
    
    st.markdown("---")
    st.caption("STORICO")
    
    for i, session in enumerate(st.session_state.chat_sessions):
        col_t, col_m = st.columns([0.85, 0.15])
        
        with col_t:
            if st.button(session['title'], key=f"load_{i}", use_container_width=True):
                st.session_state.messages = session['content']
                st.session_state.current_title = session['title']
                st.session_state.current_chat_id = session.get('id')
                st.rerun()
        
        with col_m:
            # Solo freccetta
            with st.popover("▼", key=f"pop_{i}"):
                st.write("Opzioni")
                new_title = st.text_input("Rinomina", value=session['title'], key=f"edit_{i}")
                
                if st.button("Salva", key=f"save_{i}", use_container_width=True):
                    st.session_state.chat_sessions[i]['title'] = new_title
                    if st.session_state.current_chat_id == session.get('id'):
                        st.session_state.current_title = new_title
                    st.rerun()

                if st.button("Elimina", key=f"del_{i}", use_container_width=True):
                    target_id = session.get('id')
                    st.session_state.chat_sessions.pop(i)
                    if st.session_state.current_chat_id == target_id:
                        reset_to_welcome()
                    st.rerun()

# --- 6. CORE AI ---
if st.session_state.api_key:
    client = Groq(api_key=st.session_state.api_key)

    if not st.session_state.messages:
        st.markdown(f"""
            <div class="welcome-container">
                <div class="image-3d-card"></div>
                <div class="welcome-text" style="text-align:center;">
                    <h1 style="color:white;">Pronto per la battaglia?</h1>
                    <p style="color:#ccc;">Chiedi al Loco qualsiasi cosa sul Savoia 1908.</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("Scrivi al Loco..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.rerun()

    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        with st.chat_message("assistant"):
            sys_instr = "Sei El loco Muñoz. Rispondi con fierezza."
            msgs = [{"role": "system", "content": sys_instr}] + st.session_state.messages
            completion = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=msgs, temperature=0.7)
            res = completion.choices[0].message.content
            st.markdown(res)
            st.session_state.messages.append({"role": "assistant", "content": res})
            
            if len(st.session_state.messages) == 2:
                st.session_state.current_title = generate_ai_summary(prompt, res)
                new_id = f"chat_{len(st.session_state.chat_sessions)}"
                st.session_state.current_chat_id = new_id
                st.session_state.chat_sessions.insert(0, {"id": new_id, "title": st.session_state.current_title, "content": list(st.session_state.messages)})
            else:
                for s in st.session_state.chat_sessions:
                    if s["id"] == st.session_state.current_chat_id:
                        s["content"] = list(st.session_state.messages)
            st.rerun()
