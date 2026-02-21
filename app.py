import streamlit as st
import hashlib
import json
import os
from datetime import datetime

# ── Page config (MUST be first) ───────────────────────────────────────────────
st.set_page_config(
    page_title="TechNova AI Nexus",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Try OpenAI import ─────────────────────────────────────────────────────────
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# ── User DB (JSON file) ───────────────────────────────────────────────────────
DB_FILE = "technova_users.json"

def load_users():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_users(users):
    with open(DB_FILE, "w") as f:
        json.dump(users, f, indent=2)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username, password):
    if not username or not password:
        return False, "Please fill in all fields."
    if not __import__("re").match(r'^[a-zA-Z0-9_]{3,20}$', username):
        return False, "Username: 3-20 chars, letters/numbers/underscore only."
    if len(password) < 6:
        return False, "Password must be at least 6 characters."
    users = load_users()
    if username.lower() in users:
        return False, "Username already taken."
    users[username.lower()] = {
        "username": username,
        "displayName": username,
        "passwordHash": hash_password(password),
        "createdAt": datetime.now().isoformat()
    }
    save_users(users)
    return True, "Account created successfully!"

def verify_user(username, password):
    users = load_users()
    user = users.get(username.lower())
    if not user:
        return False, "Invalid username or password.", {}
    if user["passwordHash"] != hash_password(password):
        return False, "Invalid username or password.", {}
    return True, "Login successful!", user

# ── OpenAI chat ───────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are TECHNOVA AI NEXUS — an elite, unified AI assistant. You auto-detect what the user needs and respond with rich formatting.

Capabilities:
- Deep reasoning, logic, multi-step problem solving
- Code generation, debugging, refactoring (all languages)  
- Data analysis, statistics, spreadsheet formulas
- Writing: essays, emails, blogs, creative fiction, scripts
- Translation across 20+ languages with style control
- Research synthesis, fact analysis, comparative studies
- System design, architecture, technical documentation
- Strategic planning, worldbuilding, brand strategy
- Learning & tutoring at any level
- Productivity frameworks, goal decomposition

Response style:
- Use rich markdown: headers, bullet lists, numbered lists, code blocks with language tags, bold text, tables
- For code always use triple-backtick fenced blocks with language identifier
- Be direct, confident, technically precise
- Proactively suggest follow-ups
- Adapt tone to match user (technical, casual, formal, creative)

You are TECHNOVA AI NEXUS. Deliver excellence."""

def get_ai_response(messages, api_key):
    if not OPENAI_AVAILABLE:
        return "❌ OpenAI package not installed. Run: `pip install openai`"
    try:
        client = OpenAI(api_key=api_key)
        api_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + messages
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=api_messages,
            max_tokens=2000,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ API Error: {str(e)}"

# ── Session state init ────────────────────────────────────────────────────────
for key, default in [
    ("authenticated", False),
    ("user_info", {}),
    ("api_key", ""),
    ("messages", []),
    ("page", "login"),
    ("api_key_entered", False),
]:
    if key not in st.session_state:
        st.session_state[key] = default

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700;900&family=IBM+Plex+Mono:wght@300;400;500;600&display=swap');

/* ── Root & Background ── */
.stApp {
    background: linear-gradient(135deg, #000d14 0%, #001a24 40%, #000d14 100%) !important;
    font-family: 'IBM Plex Mono', monospace !important;
}

/* Animated hex grid overlay */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient(rgba(0,245,212,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,245,212,0.03) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none;
    z-index: 0;
}

/* Glow orbs */
.stApp::after {
    content: '';
    position: fixed;
    top: 20%;
    left: 10%;
    width: 500px;
    height: 500px;
    background: radial-gradient(circle, rgba(0,245,212,0.05) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
    animation: drift 8s ease-in-out infinite alternate;
}

@keyframes drift {
    0% { transform: translate(0, 0); }
    100% { transform: translate(60px, 40px); }
}

@keyframes pulse-glow {
    0%, 100% { opacity: 0.4; }
    50% { opacity: 1; box-shadow: 0 0 12px rgba(0,245,212,0.6); }
}

@keyframes slideIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

/* ── Hide Streamlit defaults ── */
#MainMenu, footer, header { visibility: hidden !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
section[data-testid="stSidebar"] { display: none !important; }

/* ── All text ── */
.stMarkdown, .stText, p, div, span, label {
    font-family: 'IBM Plex Mono', monospace !important;
    color: #c8f7f0 !important;
}

/* ── Inputs ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: rgba(0,245,212,0.04) !important;
    border: 1px solid rgba(0,245,212,0.2) !important;
    border-radius: 8px !important;
    color: #c8f7f0 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 13px !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: rgba(0,245,212,0.5) !important;
    box-shadow: 0 0 0 2px rgba(0,245,212,0.08) !important;
}
.stTextInput > div > div > input::placeholder,
.stTextArea > div > div > textarea::placeholder {
    color: rgba(200,247,240,0.25) !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, rgba(0,245,212,0.12), rgba(6,182,212,0.08)) !important;
    border: 1px solid rgba(0,245,212,0.3) !important;
    border-radius: 8px !important;
    color: #00f5d4 !important;
    font-family: 'Orbitron', monospace !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    letter-spacing: 0.15em !important;
    transition: all 0.2s !important;
    padding: 10px 20px !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, rgba(0,245,212,0.22), rgba(6,182,212,0.15)) !important;
    border-color: rgba(0,245,212,0.6) !important;
    box-shadow: 0 0 20px rgba(0,245,212,0.15) !important;
    transform: translateY(-1px) !important;
}

/* ── Labels ── */
.stTextInput label, .stTextArea label {
    color: rgba(0,245,212,0.5) !important;
    font-size: 10px !important;
    letter-spacing: 0.2em !important;
    text-transform: uppercase !important;
    font-family: 'Orbitron', monospace !important;
}

/* ── Chat messages ── */
.user-bubble {
    background: rgba(0,245,212,0.07);
    border: 1px solid rgba(0,245,212,0.15);
    border-radius: 12px 12px 2px 12px;
    padding: 14px 18px;
    margin: 8px 0;
    color: #c8f7f0;
    font-size: 13.5px;
    line-height: 1.7;
    white-space: pre-wrap;
    animation: slideIn 0.2s ease;
}

.ai-bubble {
    background: rgba(0,8,12,0.8);
    border: 1px solid rgba(0,245,212,0.08);
    border-radius: 2px 12px 12px 12px;
    padding: 16px 20px;
    margin: 8px 0;
    animation: slideIn 0.25s ease;
}

.msg-label-user {
    font-family: 'Orbitron', monospace;
    font-size: 9px;
    color: rgba(0,245,212,0.3);
    letter-spacing: 0.2em;
    text-align: right;
    margin-bottom: 4px;
}
.msg-label-ai {
    font-family: 'Orbitron', monospace;
    font-size: 9px;
    color: rgba(0,245,212,0.3);
    letter-spacing: 0.2em;
    margin-bottom: 4px;
}

/* ── Auth card ── */
.auth-card {
    background: rgba(0,15,20,0.9);
    border: 1px solid rgba(0,245,212,0.15);
    border-radius: 16px;
    padding: 40px 36px;
    box-shadow: 0 0 60px rgba(0,245,212,0.06), 0 30px 60px rgba(0,0,0,0.5);
    backdrop-filter: blur(20px);
    animation: slideIn 0.4s ease;
}

/* ── Header bar ── */
.header-bar {
    background: rgba(0,10,15,0.95);
    border-bottom: 1px solid rgba(0,245,212,0.08);
    padding: 14px 32px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    backdrop-filter: blur(20px);
    position: sticky;
    top: 0;
    z-index: 100;
}

/* ── Status dot ── */
.status-dot {
    display: inline-block;
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #00f5d4;
    margin-right: 6px;
    animation: pulse-glow 2s ease-in-out infinite;
}

/* ── Capability pills ── */
.cap-pill {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    border: 1px solid rgba(0,245,212,0.1);
    background: rgba(0,245,212,0.04);
    color: rgba(0,245,212,0.45);
    font-size: 10px;
    letter-spacing: 0.08em;
    margin: 3px;
}

/* ── Suggestion chip ── */
.suggestion-chip {
    background: rgba(0,245,212,0.03);
    border: 1px solid rgba(0,245,212,0.1);
    border-radius: 10px;
    padding: 12px 14px;
    cursor: pointer;
    transition: all 0.2s;
    font-size: 12px;
    line-height: 1.5;
    color: rgba(200,247,240,0.6);
    margin-bottom: 8px;
}
.suggestion-chip:hover {
    background: rgba(0,245,212,0.08);
    border-color: rgba(0,245,212,0.3);
}

/* ── Error / success boxes ── */
.error-box {
    background: rgba(239,68,68,0.08);
    border: 1px solid rgba(239,68,68,0.25);
    border-radius: 8px;
    padding: 12px 16px;
    color: #fca5a5 !important;
    font-size: 12px;
    margin: 8px 0;
}
.success-box {
    background: rgba(0,245,212,0.07);
    border: 1px solid rgba(0,245,212,0.25);
    border-radius: 8px;
    padding: 12px 16px;
    color: #00f5d4 !important;
    font-size: 12px;
    margin: 8px 0;
}
.info-box {
    background: rgba(0,245,212,0.05);
    border: 1px solid rgba(0,245,212,0.12);
    border-radius: 8px;
    padding: 12px 16px;
    color: rgba(200,247,240,0.6) !important;
    font-size: 12px;
    margin: 8px 0;
    line-height: 1.6;
}

/* ── Title ── */
.nexus-title {
    font-family: 'Orbitron', monospace;
    font-weight: 900;
    font-size: clamp(28px, 5vw, 52px);
    letter-spacing: 0.06em;
    background: linear-gradient(135deg, #00f5d4 0%, #06b6d4 40%, #00f5d4 80%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1;
    text-align: center;
}

/* ── stMarkdown code blocks ── */
.stMarkdown pre {
    background: rgba(0,0,0,0.5) !important;
    border: 1px solid rgba(0,245,212,0.12) !important;
    border-radius: 8px !important;
    color: #a8f5e8 !important;
}
.stMarkdown code {
    background: rgba(0,245,212,0.1) !important;
    color: #00f5d4 !important;
    border-radius: 3px !important;
}

/* ── Divider ── */
hr {
    border-color: rgba(0,245,212,0.08) !important;
}

/* ── Tabs (if used) ── */
.stTabs [data-baseweb="tab"] {
    font-family: 'Orbitron', monospace !important;
    font-size: 10px !important;
    letter-spacing: 0.15em !important;
    color: rgba(0,245,212,0.4) !important;
}
.stTabs [aria-selected="true"] {
    color: #00f5d4 !important;
}

/* scrollbar */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(0,245,212,0.2); border-radius: 4px; }
</style>
""", unsafe_allow_html=True)


# ── Login Page ────────────────────────────────────────────────────────────────
def login_page():
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("""
        <div style='height:60px'></div>
        <div style='text-align:center; margin-bottom:32px;'>
            <div style='font-size:32px; color:#00f5d4;'>◈</div>
            <div style='font-family:Orbitron,monospace; font-weight:900; font-size:20px; color:#00f5d4; letter-spacing:0.12em; line-height:1.2;'>TECHNOVA</div>
            <div style='font-family:Orbitron,monospace; font-size:10px; color:rgba(0,245,212,0.45); letter-spacing:0.35em; margin-top:4px;'>AI NEXUS</div>
        </div>
        """, unsafe_allow_html=True)

        tab_login, tab_signup = st.tabs(["🔐 LOGIN", "📝 SIGN UP"])

        with tab_login:
            st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
            username = st.text_input("Username", placeholder="your_username", key="login_user")
            password = st.text_input("Password", type="password", placeholder="••••••••", key="login_pass")

            if st.button("ENTER NEXUS →", use_container_width=True, key="login_btn"):
                if not username or not password:
                    st.markdown('<div class="error-box">Please fill in all fields.</div>', unsafe_allow_html=True)
                else:
                    ok, msg, user = verify_user(username, password)
                    if ok:
                        st.session_state.user_info = user
                        st.session_state.page = "apikey"
                        st.rerun()
                    else:
                        st.markdown(f'<div class="error-box">{msg}</div>', unsafe_allow_html=True)

        with tab_signup:
            st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
            new_user = st.text_input("Username", placeholder="choose_username", key="signup_user")
            st.markdown('<div style="font-size:10px; color:rgba(200,247,240,0.25); margin-top:-8px; margin-bottom:8px;">3-20 chars · letters, numbers, underscore</div>', unsafe_allow_html=True)
            new_pass = st.text_input("Password", type="password", placeholder="min. 6 characters", key="signup_pass")
            confirm_pass = st.text_input("Confirm Password", type="password", placeholder="repeat password", key="signup_confirm")

            if st.button("CREATE ACCOUNT →", use_container_width=True, key="signup_btn"):
                if new_pass != confirm_pass:
                    st.markdown('<div class="error-box">Passwords do not match.</div>', unsafe_allow_html=True)
                else:
                    ok, msg = create_user(new_user, new_pass)
                    if ok:
                        st.markdown(f'<div class="success-box">✓ {msg} Please log in.</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="error-box">{msg}</div>', unsafe_allow_html=True)

        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        st.markdown('<div style="text-align:center; font-size:10px; color:rgba(0,245,212,0.15); font-family:Orbitron,monospace; letter-spacing:0.2em;">UNIFIED INTELLIGENCE PLATFORM</div>', unsafe_allow_html=True)


# ── API Key Page ──────────────────────────────────────────────────────────────
def api_key_page():
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("<div style='height:80px'></div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style='text-align:center; margin-bottom:28px;'>
            <div style='font-size:28px; color:#00f5d4;'>◈</div>
            <div style='font-family:Orbitron,monospace; font-weight:900; font-size:16px; color:#00f5d4; letter-spacing:0.12em;'>CONNECT API</div>
            <div style='font-size:10px; color:rgba(0,245,212,0.3); letter-spacing:0.2em; margin-top:6px;'>STEP 2 OF 2</div>
        </div>
        <div class='info-box'>
            Welcome, <strong style='color:#00f5d4;'>{st.session_state.user_info.get("displayName", "")}</strong>.
            Enter your OpenAI API key to power NEXUS.
            Your key is only used for this session and never stored on any server.
        </div>
        """, unsafe_allow_html=True)

        api_key = st.text_input("OpenAI API Key", placeholder="sk-...", type="password", key="api_key_input")
        st.markdown('<div style="font-size:10px; color:rgba(200,247,240,0.2); margin-top:-8px; margin-bottom:12px;">Get yours at platform.openai.com · Uses GPT-4o</div>', unsafe_allow_html=True)

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("CONNECT & LAUNCH →", use_container_width=True, key="connect_btn"):
                if not api_key.strip().startswith("sk-"):
                    st.markdown('<div class="error-box">Please enter a valid OpenAI API key (starts with sk-).</div>', unsafe_allow_html=True)
                else:
                    st.session_state.api_key = api_key.strip()
                    st.session_state.authenticated = True
                    st.session_state.page = "chat"
                    st.rerun()
        with col_b:
            if st.button("← BACK", use_container_width=True, key="back_btn"):
                st.session_state.page = "login"
                st.session_state.user_info = {}
                st.rerun()


# ── Chat App ──────────────────────────────────────────────────────────────────
SUGGESTIONS = [
    ("⚡", "Explain quantum entanglement simply, then like a physicist"),
    ("🐍", "Write a Python async web scraper with rate limiting and retry logic"),
    ("📊", "Analyze this data:\nname,age,score\nAlice,25,88\nBob,30,72\nCarla,22,95"),
    ("✍️", "Write a compelling product launch email for a new AI coding assistant"),
    ("🌍", "Translate 'The future belongs to those who believe' to Japanese, Arabic, French"),
    ("🏗️", "Design a microservices architecture for an e-commerce platform with 1M daily users"),
    ("🎭", "Create a worldbuilding framework for a solarpunk civilization on Mars in 2150"),
    ("📈", "Build a 90-day content strategy for a B2B SaaS startup targeting CTOs"),
]

CAPS = ["Reasoning","Code Gen","Data Analysis","Writing","Translation","Research","System Design","Tutoring","Debugging","Strategy","Worldbuilding","Automation"]

def chat_page():
    display_name = st.session_state.user_info.get("displayName", "User")

    # ── Header ────────────────────────────────────────────────────────────────
    st.markdown(f"""
    <div style='background:rgba(0,10,15,0.95); border-bottom:1px solid rgba(0,245,212,0.08);
                padding:14px 32px; display:flex; align-items:center; justify-content:space-between;
                position:sticky; top:0; z-index:100; backdrop-filter:blur(20px);'>
        <div style='display:flex; align-items:center; gap:14px;'>
            <div style='width:36px; height:36px; border-radius:8px;
                        background:linear-gradient(135deg,rgba(0,245,212,0.15),rgba(6,182,212,0.08));
                        border:1px solid rgba(0,245,212,0.25);
                        display:flex; align-items:center; justify-content:center;
                        font-size:18px; color:#00f5d4;'>◈</div>
            <div>
                <div style='font-family:Orbitron,monospace; font-weight:900; font-size:14px; color:#00f5d4; letter-spacing:0.12em;'>TECHNOVA AI NEXUS</div>
                <div style='font-size:9px; color:rgba(0,245,212,0.3); letter-spacing:0.2em;'>UNIFIED INTELLIGENCE PLATFORM</div>
            </div>
        </div>
        <div style='display:flex; align-items:center; gap:20px;'>
            <div>
                <span class='status-dot'></span>
                <span style='font-size:9px; color:rgba(0,245,212,0.4); letter-spacing:0.15em; font-family:Orbitron,monospace;'>GPT-4o ONLINE</span>
            </div>
            <div style='font-size:11px; color:rgba(0,245,212,0.3); padding-left:16px; border-left:1px solid rgba(0,245,212,0.1);'>{display_name}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Top action buttons ────────────────────────────────────────────────────
    col_space, col_clear, col_logout = st.columns([6, 1, 1])
    with col_clear:
        if st.button("CLEAR", key="clear_chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    with col_logout:
        if st.button("LOGOUT", key="logout_btn", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user_info = {}
            st.session_state.api_key = ""
            st.session_state.messages = []
            st.session_state.page = "login"
            st.rerun()

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    # ── Main content area ─────────────────────────────────────────────────────
    main_col, _ = st.columns([3, 0.05])
    with main_col:

        # Welcome screen
        if not st.session_state.messages:
            st.markdown("""
            <div style='text-align:center; padding:40px 0 24px;'>
                <div style='font-family:Orbitron,monospace; font-weight:900; font-size:clamp(28px,5vw,48px);
                            letter-spacing:0.06em; line-height:1.1;
                            background:linear-gradient(135deg,#00f5d4 0%,#06b6d4 40%,#00f5d4 80%);
                            -webkit-background-clip:text; -webkit-text-fill-color:transparent;'>
                    TECHNOVA<br>AI NEXUS
                </div>
                <div style='margin-top:16px; color:rgba(200,247,240,0.35); font-size:11px;
                            letter-spacing:0.3em; text-transform:uppercase; font-family:Orbitron,monospace;'>
                    Unified · Adaptive · Unlimited
                </div>
                <div style='margin-top:14px; color:rgba(200,247,240,0.4); font-size:13px; line-height:1.7;'>
                    One interface. Every AI capability. Just ask.
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Capability pills
            pills_html = "".join([f'<span class="cap-pill">{c}</span>' for c in CAPS])
            st.markdown(f'<div style="text-align:center; margin-bottom:28px;">{pills_html}</div>', unsafe_allow_html=True)

            # Suggestion chips
            st.markdown('<div style="font-size:9px; color:rgba(0,245,212,0.25); letter-spacing:0.25em; text-align:center; margin-bottom:12px; font-family:Orbitron,monospace;">QUICK START</div>', unsafe_allow_html=True)

            cols = st.columns(2)
            for idx, (icon, text) in enumerate(SUGGESTIONS):
                with cols[idx % 2]:
                    preview = text[:75] + "…" if len(text) > 75 else text
                    if st.button(f"{icon}  {preview}", key=f"sug_{idx}", use_container_width=True):
                        st.session_state.messages.append({"role": "user", "content": text})
                        with st.spinner("◈ Processing…"):
                            reply = get_ai_response(st.session_state.messages, st.session_state.api_key)
                        st.session_state.messages.append({"role": "assistant", "content": reply})
                        st.rerun()

        # Chat messages
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f'<div class="msg-label-user">{display_name.upper()}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="user-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="msg-label-ai">◈ NEXUS</div>', unsafe_allow_html=True)
                with st.container():
                    st.markdown(f'<div class="ai-bubble">', unsafe_allow_html=True)
                    st.markdown(msg["content"])
                    st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<div style='height:120px'></div>", unsafe_allow_html=True)

    # ── Input area (bottom) ───────────────────────────────────────────────────
    st.markdown("""
    <div style='position:fixed; bottom:0; left:0; right:0; z-index:200;
                background:rgba(0,10,15,0.97); border-top:1px solid rgba(0,245,212,0.07);
                backdrop-filter:blur(20px); padding:14px 0 16px;'>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        input_col1, input_col2 = st.columns([5, 1])

        with input_col1:
            user_input = st.text_area(
                "Message",
                placeholder="Ask anything — code, analysis, writing, translation, strategy, research…",
                height=80,
                key="chat_input",
                label_visibility="collapsed"
            )

        with input_col2:
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            send_clicked = st.button("SEND ↑", use_container_width=True, key="send_btn")

        st.markdown('<div style="font-size:9px; color:rgba(0,245,212,0.18); letter-spacing:0.12em; text-align:center; font-family:Orbitron,monospace; margin-top:4px;">TECHNOVA AI NEXUS · GPT-4o · Click SEND or press button</div>', unsafe_allow_html=True)

        if send_clicked and user_input and user_input.strip():
            st.session_state.messages.append({"role": "user", "content": user_input.strip()})
            with st.spinner("◈ NEXUS is thinking…"):
                reply = get_ai_response(st.session_state.messages, st.session_state.api_key)
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.rerun()


# ── Router ────────────────────────────────────────────────────────────────────
def main():
    if not st.session_state.authenticated:
        if st.session_state.page == "apikey" and st.session_state.user_info:
            api_key_page()
        else:
            login_page()
    else:
        chat_page()

if __name__ == "__main__":
    main()
