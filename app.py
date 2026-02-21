# import streamlit as st
# import hashlib
# import json
# import os
# from datetime import datetime

# # ── Page config (MUST be first) ───────────────────────────────────────────────
# st.set_page_config(
#     page_title="TechNova AI Nexus",
#     page_icon="◈",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# # ── Try OpenAI import ─────────────────────────────────────────────────────────
# try:
#     from openai import OpenAI
#     OPENAI_AVAILABLE = True
# except ImportError:
#     OPENAI_AVAILABLE = False

# # ── User DB (JSON file) ───────────────────────────────────────────────────────
# DB_FILE = "technova_users.json"

# def load_users():
#     if os.path.exists(DB_FILE):
#         try:
#             with open(DB_FILE, "r") as f:
#                 return json.load(f)
#         except:
#             return {}
#     return {}

# def save_users(users):
#     with open(DB_FILE, "w") as f:
#         json.dump(users, f, indent=2)

# def hash_password(password):
#     return hashlib.sha256(password.encode()).hexdigest()

# def create_user(username, password):
#     if not username or not password:
#         return False, "Please fill in all fields."
#     if not __import__("re").match(r'^[a-zA-Z0-9_]{3,20}$', username):
#         return False, "Username: 3-20 chars, letters/numbers/underscore only."
#     if len(password) < 6:
#         return False, "Password must be at least 6 characters."
#     users = load_users()
#     if username.lower() in users:
#         return False, "Username already taken."
#     users[username.lower()] = {
#         "username": username,
#         "displayName": username,
#         "passwordHash": hash_password(password),
#         "createdAt": datetime.now().isoformat()
#     }
#     save_users(users)
#     return True, "Account created successfully!"

# def verify_user(username, password):
#     users = load_users()
#     user = users.get(username.lower())
#     if not user:
#         return False, "Invalid username or password.", {}
#     if user["passwordHash"] != hash_password(password):
#         return False, "Invalid username or password.", {}
#     return True, "Login successful!", user

# # ── OpenAI chat ───────────────────────────────────────────────────────────────
# SYSTEM_PROMPT = """You are TECHNOVA AI NEXUS — an elite, unified AI assistant. You auto-detect what the user needs and respond with rich formatting.

# Capabilities:
# - Deep reasoning, logic, multi-step problem solving
# - Code generation, debugging, refactoring (all languages)  
# - Data analysis, statistics, spreadsheet formulas
# - Writing: essays, emails, blogs, creative fiction, scripts
# - Translation across 20+ languages with style control
# - Research synthesis, fact analysis, comparative studies
# - System design, architecture, technical documentation
# - Strategic planning, worldbuilding, brand strategy
# - Learning & tutoring at any level
# - Productivity frameworks, goal decomposition

# Response style:
# - Use rich markdown: headers, bullet lists, numbered lists, code blocks with language tags, bold text, tables
# - For code always use triple-backtick fenced blocks with language identifier
# - Be direct, confident, technically precise
# - Proactively suggest follow-ups
# - Adapt tone to match user (technical, casual, formal, creative)

# You are TECHNOVA AI NEXUS. Deliver excellence."""

# def get_ai_response(messages, api_key):
#     if not OPENAI_AVAILABLE:
#         return "❌ OpenAI package not installed. Run: `pip install openai`"
#     try:
#         client = OpenAI(api_key=api_key)
#         api_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + messages
#         response = client.chat.completions.create(
#             model="gpt-4o",
#             messages=api_messages,
#             max_tokens=2000,
#             temperature=0.7
#         )
#         return response.choices[0].message.content
#     except Exception as e:
#         return f"❌ API Error: {str(e)}"

# # ── Session state init ────────────────────────────────────────────────────────
# for key, default in [
#     ("authenticated", False),
#     ("user_info", {}),
#     ("api_key", ""),
#     ("messages", []),
#     ("page", "login"),
#     ("api_key_entered", False),
# ]:
#     if key not in st.session_state:
#         st.session_state[key] = default

# # ── Global CSS ────────────────────────────────────────────────────────────────
# st.markdown("""
# <style>
# @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700;900&family=IBM+Plex+Mono:wght@300;400;500;600&display=swap');

# /* ── Root & Background ── */
# .stApp {
#     background: linear-gradient(135deg, #000d14 0%, #001a24 40%, #000d14 100%) !important;
#     font-family: 'IBM Plex Mono', monospace !important;
# }

# /* Animated hex grid overlay */
# .stApp::before {
#     content: '';
#     position: fixed;
#     inset: 0;
#     background-image:
#         linear-gradient(rgba(0,245,212,0.03) 1px, transparent 1px),
#         linear-gradient(90deg, rgba(0,245,212,0.03) 1px, transparent 1px);
#     background-size: 40px 40px;
#     pointer-events: none;
#     z-index: 0;
# }

# /* Glow orbs */
# .stApp::after {
#     content: '';
#     position: fixed;
#     top: 20%;
#     left: 10%;
#     width: 500px;
#     height: 500px;
#     background: radial-gradient(circle, rgba(0,245,212,0.05) 0%, transparent 70%);
#     pointer-events: none;
#     z-index: 0;
#     animation: drift 8s ease-in-out infinite alternate;
# }

# @keyframes drift {
#     0% { transform: translate(0, 0); }
#     100% { transform: translate(60px, 40px); }
# }

# @keyframes pulse-glow {
#     0%, 100% { opacity: 0.4; }
#     50% { opacity: 1; box-shadow: 0 0 12px rgba(0,245,212,0.6); }
# }

# @keyframes slideIn {
#     from { opacity: 0; transform: translateY(10px); }
#     to { opacity: 1; transform: translateY(0); }
# }

# /* ── Hide Streamlit defaults ── */
# #MainMenu, footer, header { visibility: hidden !important; }
# .block-container { padding: 0 !important; max-width: 100% !important; }
# section[data-testid="stSidebar"] { display: none !important; }

# /* ── All text ── */
# .stMarkdown, .stText, p, div, span, label {
#     font-family: 'IBM Plex Mono', monospace !important;
#     color: #c8f7f0 !important;
# }

# /* ── Inputs ── */
# .stTextInput > div > div > input,
# .stTextArea > div > div > textarea {
#     background: rgba(0,245,212,0.04) !important;
#     border: 1px solid rgba(0,245,212,0.2) !important;
#     border-radius: 8px !important;
#     color: #c8f7f0 !important;
#     font-family: 'IBM Plex Mono', monospace !important;
#     font-size: 13px !important;
# }
# .stTextInput > div > div > input:focus,
# .stTextArea > div > div > textarea:focus {
#     border-color: rgba(0,245,212,0.5) !important;
#     box-shadow: 0 0 0 2px rgba(0,245,212,0.08) !important;
# }
# .stTextInput > div > div > input::placeholder,
# .stTextArea > div > div > textarea::placeholder {
#     color: rgba(200,247,240,0.25) !important;
# }

# /* ── Buttons ── */
# .stButton > button {
#     background: linear-gradient(135deg, rgba(0,245,212,0.12), rgba(6,182,212,0.08)) !important;
#     border: 1px solid rgba(0,245,212,0.3) !important;
#     border-radius: 8px !important;
#     color: #00f5d4 !important;
#     font-family: 'Orbitron', monospace !important;
#     font-size: 11px !important;
#     font-weight: 700 !important;
#     letter-spacing: 0.15em !important;
#     transition: all 0.2s !important;
#     padding: 10px 20px !important;
# }
# .stButton > button:hover {
#     background: linear-gradient(135deg, rgba(0,245,212,0.22), rgba(6,182,212,0.15)) !important;
#     border-color: rgba(0,245,212,0.6) !important;
#     box-shadow: 0 0 20px rgba(0,245,212,0.15) !important;
#     transform: translateY(-1px) !important;
# }

# /* ── Labels ── */
# .stTextInput label, .stTextArea label {
#     color: rgba(0,245,212,0.5) !important;
#     font-size: 10px !important;
#     letter-spacing: 0.2em !important;
#     text-transform: uppercase !important;
#     font-family: 'Orbitron', monospace !important;
# }

# /* ── Chat messages ── */
# .user-bubble {
#     background: rgba(0,245,212,0.07);
#     border: 1px solid rgba(0,245,212,0.15);
#     border-radius: 12px 12px 2px 12px;
#     padding: 14px 18px;
#     margin: 8px 0;
#     color: #c8f7f0;
#     font-size: 13.5px;
#     line-height: 1.7;
#     white-space: pre-wrap;
#     animation: slideIn 0.2s ease;
# }

# .ai-bubble {
#     background: rgba(0,8,12,0.8);
#     border: 1px solid rgba(0,245,212,0.08);
#     border-radius: 2px 12px 12px 12px;
#     padding: 16px 20px;
#     margin: 8px 0;
#     animation: slideIn 0.25s ease;
# }

# .msg-label-user {
#     font-family: 'Orbitron', monospace;
#     font-size: 9px;
#     color: rgba(0,245,212,0.3);
#     letter-spacing: 0.2em;
#     text-align: right;
#     margin-bottom: 4px;
# }
# .msg-label-ai {
#     font-family: 'Orbitron', monospace;
#     font-size: 9px;
#     color: rgba(0,245,212,0.3);
#     letter-spacing: 0.2em;
#     margin-bottom: 4px;
# }

# /* ── Auth card ── */
# .auth-card {
#     background: rgba(0,15,20,0.9);
#     border: 1px solid rgba(0,245,212,0.15);
#     border-radius: 16px;
#     padding: 40px 36px;
#     box-shadow: 0 0 60px rgba(0,245,212,0.06), 0 30px 60px rgba(0,0,0,0.5);
#     backdrop-filter: blur(20px);
#     animation: slideIn 0.4s ease;
# }

# /* ── Header bar ── */
# .header-bar {
#     background: rgba(0,10,15,0.95);
#     border-bottom: 1px solid rgba(0,245,212,0.08);
#     padding: 14px 32px;
#     display: flex;
#     align-items: center;
#     justify-content: space-between;
#     backdrop-filter: blur(20px);
#     position: sticky;
#     top: 0;
#     z-index: 100;
# }

# /* ── Status dot ── */
# .status-dot {
#     display: inline-block;
#     width: 7px;
#     height: 7px;
#     border-radius: 50%;
#     background: #00f5d4;
#     margin-right: 6px;
#     animation: pulse-glow 2s ease-in-out infinite;
# }

# /* ── Capability pills ── */
# .cap-pill {
#     display: inline-block;
#     padding: 4px 12px;
#     border-radius: 20px;
#     border: 1px solid rgba(0,245,212,0.1);
#     background: rgba(0,245,212,0.04);
#     color: rgba(0,245,212,0.45);
#     font-size: 10px;
#     letter-spacing: 0.08em;
#     margin: 3px;
# }

# /* ── Suggestion chip ── */
# .suggestion-chip {
#     background: rgba(0,245,212,0.03);
#     border: 1px solid rgba(0,245,212,0.1);
#     border-radius: 10px;
#     padding: 12px 14px;
#     cursor: pointer;
#     transition: all 0.2s;
#     font-size: 12px;
#     line-height: 1.5;
#     color: rgba(200,247,240,0.6);
#     margin-bottom: 8px;
# }
# .suggestion-chip:hover {
#     background: rgba(0,245,212,0.08);
#     border-color: rgba(0,245,212,0.3);
# }

# /* ── Error / success boxes ── */
# .error-box {
#     background: rgba(239,68,68,0.08);
#     border: 1px solid rgba(239,68,68,0.25);
#     border-radius: 8px;
#     padding: 12px 16px;
#     color: #fca5a5 !important;
#     font-size: 12px;
#     margin: 8px 0;
# }
# .success-box {
#     background: rgba(0,245,212,0.07);
#     border: 1px solid rgba(0,245,212,0.25);
#     border-radius: 8px;
#     padding: 12px 16px;
#     color: #00f5d4 !important;
#     font-size: 12px;
#     margin: 8px 0;
# }
# .info-box {
#     background: rgba(0,245,212,0.05);
#     border: 1px solid rgba(0,245,212,0.12);
#     border-radius: 8px;
#     padding: 12px 16px;
#     color: rgba(200,247,240,0.6) !important;
#     font-size: 12px;
#     margin: 8px 0;
#     line-height: 1.6;
# }

# /* ── Title ── */
# .nexus-title {
#     font-family: 'Orbitron', monospace;
#     font-weight: 900;
#     font-size: clamp(28px, 5vw, 52px);
#     letter-spacing: 0.06em;
#     background: linear-gradient(135deg, #00f5d4 0%, #06b6d4 40%, #00f5d4 80%);
#     -webkit-background-clip: text;
#     -webkit-text-fill-color: transparent;
#     background-clip: text;
#     line-height: 1.1;
#     text-align: center;
# }

# /* ── stMarkdown code blocks ── */
# .stMarkdown pre {
#     background: rgba(0,0,0,0.5) !important;
#     border: 1px solid rgba(0,245,212,0.12) !important;
#     border-radius: 8px !important;
#     color: #a8f5e8 !important;
# }
# .stMarkdown code {
#     background: rgba(0,245,212,0.1) !important;
#     color: #00f5d4 !important;
#     border-radius: 3px !important;
# }

# /* ── Divider ── */
# hr {
#     border-color: rgba(0,245,212,0.08) !important;
# }

# /* ── Tabs (if used) ── */
# .stTabs [data-baseweb="tab"] {
#     font-family: 'Orbitron', monospace !important;
#     font-size: 10px !important;
#     letter-spacing: 0.15em !important;
#     color: rgba(0,245,212,0.4) !important;
# }
# .stTabs [aria-selected="true"] {
#     color: #00f5d4 !important;
# }

# /* scrollbar */
# ::-webkit-scrollbar { width: 4px; }
# ::-webkit-scrollbar-track { background: transparent; }
# ::-webkit-scrollbar-thumb { background: rgba(0,245,212,0.2); border-radius: 4px; }
# </style>
# """, unsafe_allow_html=True)


# # ── Login Page ────────────────────────────────────────────────────────────────
# def login_page():
#     col1, col2, col3 = st.columns([1, 1.2, 1])
#     with col2:
#         st.markdown("""
#         <div style='height:60px'></div>
#         <div style='text-align:center; margin-bottom:32px;'>
#             <div style='font-size:32px; color:#00f5d4;'>◈</div>
#             <div style='font-family:Orbitron,monospace; font-weight:900; font-size:20px; color:#00f5d4; letter-spacing:0.12em; line-height:1.2;'>TECHNOVA</div>
#             <div style='font-family:Orbitron,monospace; font-size:10px; color:rgba(0,245,212,0.45); letter-spacing:0.35em; margin-top:4px;'>AI NEXUS</div>
#         </div>
#         """, unsafe_allow_html=True)

#         tab_login, tab_signup = st.tabs(["🔐 LOGIN", "📝 SIGN UP"])

#         with tab_login:
#             st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
#             username = st.text_input("Username", placeholder="your_username", key="login_user")
#             password = st.text_input("Password", type="password", placeholder="••••••••", key="login_pass")

#             if st.button("ENTER NEXUS →", use_container_width=True, key="login_btn"):
#                 if not username or not password:
#                     st.markdown('<div class="error-box">Please fill in all fields.</div>', unsafe_allow_html=True)
#                 else:
#                     ok, msg, user = verify_user(username, password)
#                     if ok:
#                         st.session_state.user_info = user
#                         st.session_state.page = "apikey"
#                         st.rerun()
#                     else:
#                         st.markdown(f'<div class="error-box">{msg}</div>', unsafe_allow_html=True)

#         with tab_signup:
#             st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
#             new_user = st.text_input("Username", placeholder="choose_username", key="signup_user")
#             st.markdown('<div style="font-size:10px; color:rgba(200,247,240,0.25); margin-top:-8px; margin-bottom:8px;">3-20 chars · letters, numbers, underscore</div>', unsafe_allow_html=True)
#             new_pass = st.text_input("Password", type="password", placeholder="min. 6 characters", key="signup_pass")
#             confirm_pass = st.text_input("Confirm Password", type="password", placeholder="repeat password", key="signup_confirm")

#             if st.button("CREATE ACCOUNT →", use_container_width=True, key="signup_btn"):
#                 if new_pass != confirm_pass:
#                     st.markdown('<div class="error-box">Passwords do not match.</div>', unsafe_allow_html=True)
#                 else:
#                     ok, msg = create_user(new_user, new_pass)
#                     if ok:
#                         st.markdown(f'<div class="success-box">✓ {msg} Please log in.</div>', unsafe_allow_html=True)
#                     else:
#                         st.markdown(f'<div class="error-box">{msg}</div>', unsafe_allow_html=True)

#         st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
#         st.markdown('<div style="text-align:center; font-size:10px; color:rgba(0,245,212,0.15); font-family:Orbitron,monospace; letter-spacing:0.2em;">UNIFIED INTELLIGENCE PLATFORM</div>', unsafe_allow_html=True)


# # ── API Key Page ──────────────────────────────────────────────────────────────
# def api_key_page():
#     col1, col2, col3 = st.columns([1, 1.2, 1])
#     with col2:
#         st.markdown("<div style='height:80px'></div>", unsafe_allow_html=True)
#         st.markdown(f"""
#         <div style='text-align:center; margin-bottom:28px;'>
#             <div style='font-size:28px; color:#00f5d4;'>◈</div>
#             <div style='font-family:Orbitron,monospace; font-weight:900; font-size:16px; color:#00f5d4; letter-spacing:0.12em;'>CONNECT API</div>
#             <div style='font-size:10px; color:rgba(0,245,212,0.3); letter-spacing:0.2em; margin-top:6px;'>STEP 2 OF 2</div>
#         </div>
#         <div class='info-box'>
#             Welcome, <strong style='color:#00f5d4;'>{st.session_state.user_info.get("displayName", "")}</strong>.
#             Enter your OpenAI API key to power NEXUS.
#             Your key is only used for this session and never stored on any server.
#         </div>
#         """, unsafe_allow_html=True)

#         api_key = st.text_input("OpenAI API Key", placeholder="sk-...", type="password", key="api_key_input")
#         st.markdown('<div style="font-size:10px; color:rgba(200,247,240,0.2); margin-top:-8px; margin-bottom:12px;">Get yours at platform.openai.com · Uses GPT-4o</div>', unsafe_allow_html=True)

#         col_a, col_b = st.columns(2)
#         with col_a:
#             if st.button("CONNECT & LAUNCH →", use_container_width=True, key="connect_btn"):
#                 if not api_key.strip().startswith("sk-"):
#                     st.markdown('<div class="error-box">Please enter a valid OpenAI API key (starts with sk-).</div>', unsafe_allow_html=True)
#                 else:
#                     st.session_state.api_key = api_key.strip()
#                     st.session_state.authenticated = True
#                     st.session_state.page = "chat"
#                     st.rerun()
#         with col_b:
#             if st.button("← BACK", use_container_width=True, key="back_btn"):
#                 st.session_state.page = "login"
#                 st.session_state.user_info = {}
#                 st.rerun()


# # ── Chat App ──────────────────────────────────────────────────────────────────
# SUGGESTIONS = [
#     ("⚡", "Explain quantum entanglement simply, then like a physicist"),
#     ("🐍", "Write a Python async web scraper with rate limiting and retry logic"),
#     ("📊", "Analyze this data:\nname,age,score\nAlice,25,88\nBob,30,72\nCarla,22,95"),
#     ("✍️", "Write a compelling product launch email for a new AI coding assistant"),
#     ("🌍", "Translate 'The future belongs to those who believe' to Japanese, Arabic, French"),
#     ("🏗️", "Design a microservices architecture for an e-commerce platform with 1M daily users"),
#     ("🎭", "Create a worldbuilding framework for a solarpunk civilization on Mars in 2150"),
#     ("📈", "Build a 90-day content strategy for a B2B SaaS startup targeting CTOs"),
# ]

# CAPS = ["Reasoning","Code Gen","Data Analysis","Writing","Translation","Research","System Design","Tutoring","Debugging","Strategy","Worldbuilding","Automation"]

# def chat_page():
#     display_name = st.session_state.user_info.get("displayName", "User")

#     # ── Header ────────────────────────────────────────────────────────────────
#     st.markdown(f"""
#     <div style='background:rgba(0,10,15,0.95); border-bottom:1px solid rgba(0,245,212,0.08);
#                 padding:14px 32px; display:flex; align-items:center; justify-content:space-between;
#                 position:sticky; top:0; z-index:100; backdrop-filter:blur(20px);'>
#         <div style='display:flex; align-items:center; gap:14px;'>
#             <div style='width:36px; height:36px; border-radius:8px;
#                         background:linear-gradient(135deg,rgba(0,245,212,0.15),rgba(6,182,212,0.08));
#                         border:1px solid rgba(0,245,212,0.25);
#                         display:flex; align-items:center; justify-content:center;
#                         font-size:18px; color:#00f5d4;'>◈</div>
#             <div>
#                 <div style='font-family:Orbitron,monospace; font-weight:900; font-size:14px; color:#00f5d4; letter-spacing:0.12em;'>TECHNOVA AI NEXUS</div>
#                 <div style='font-size:9px; color:rgba(0,245,212,0.3); letter-spacing:0.2em;'>UNIFIED INTELLIGENCE PLATFORM</div>
#             </div>
#         </div>
#         <div style='display:flex; align-items:center; gap:20px;'>
#             <div>
#                 <span class='status-dot'></span>
#                 <span style='font-size:9px; color:rgba(0,245,212,0.4); letter-spacing:0.15em; font-family:Orbitron,monospace;'>GPT-4o ONLINE</span>
#             </div>
#             <div style='font-size:11px; color:rgba(0,245,212,0.3); padding-left:16px; border-left:1px solid rgba(0,245,212,0.1);'>{display_name}</div>
#         </div>
#     </div>
#     """, unsafe_allow_html=True)

#     # ── Top action buttons ────────────────────────────────────────────────────
#     col_space, col_clear, col_logout = st.columns([6, 1, 1])
#     with col_clear:
#         if st.button("CLEAR", key="clear_chat", use_container_width=True):
#             st.session_state.messages = []
#             st.rerun()
#     with col_logout:
#         if st.button("LOGOUT", key="logout_btn", use_container_width=True):
#             st.session_state.authenticated = False
#             st.session_state.user_info = {}
#             st.session_state.api_key = ""
#             st.session_state.messages = []
#             st.session_state.page = "login"
#             st.rerun()

#     st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

#     # ── Main content area ─────────────────────────────────────────────────────
#     main_col, _ = st.columns([3, 0.05])
#     with main_col:

#         # Welcome screen
#         if not st.session_state.messages:
#             st.markdown("""
#             <div style='text-align:center; padding:40px 0 24px;'>
#                 <div style='font-family:Orbitron,monospace; font-weight:900; font-size:clamp(28px,5vw,48px);
#                             letter-spacing:0.06em; line-height:1.1;
#                             background:linear-gradient(135deg,#00f5d4 0%,#06b6d4 40%,#00f5d4 80%);
#                             -webkit-background-clip:text; -webkit-text-fill-color:transparent;'>
#                     TECHNOVA<br>AI NEXUS
#                 </div>
#                 <div style='margin-top:16px; color:rgba(200,247,240,0.35); font-size:11px;
#                             letter-spacing:0.3em; text-transform:uppercase; font-family:Orbitron,monospace;'>
#                     Unified · Adaptive · Unlimited
#                 </div>
#                 <div style='margin-top:14px; color:rgba(200,247,240,0.4); font-size:13px; line-height:1.7;'>
#                     One interface. Every AI capability. Just ask.
#                 </div>
#             </div>
#             """, unsafe_allow_html=True)

#             # Capability pills
#             pills_html = "".join([f'<span class="cap-pill">{c}</span>' for c in CAPS])
#             st.markdown(f'<div style="text-align:center; margin-bottom:28px;">{pills_html}</div>', unsafe_allow_html=True)

#             # Suggestion chips
#             st.markdown('<div style="font-size:9px; color:rgba(0,245,212,0.25); letter-spacing:0.25em; text-align:center; margin-bottom:12px; font-family:Orbitron,monospace;">QUICK START</div>', unsafe_allow_html=True)

#             cols = st.columns(2)
#             for idx, (icon, text) in enumerate(SUGGESTIONS):
#                 with cols[idx % 2]:
#                     preview = text[:75] + "…" if len(text) > 75 else text
#                     if st.button(f"{icon}  {preview}", key=f"sug_{idx}", use_container_width=True):
#                         st.session_state.messages.append({"role": "user", "content": text})
#                         with st.spinner("◈ Processing…"):
#                             reply = get_ai_response(st.session_state.messages, st.session_state.api_key)
#                         st.session_state.messages.append({"role": "assistant", "content": reply})
#                         st.rerun()

#         # Chat messages
#         for msg in st.session_state.messages:
#             if msg["role"] == "user":
#                 st.markdown(f'<div class="msg-label-user">{display_name.upper()}</div>', unsafe_allow_html=True)
#                 st.markdown(f'<div class="user-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
#             else:
#                 st.markdown('<div class="msg-label-ai">◈ NEXUS</div>', unsafe_allow_html=True)
#                 with st.container():
#                     st.markdown(f'<div class="ai-bubble">', unsafe_allow_html=True)
#                     st.markdown(msg["content"])
#                     st.markdown('</div>', unsafe_allow_html=True)

#         st.markdown("<div style='height:120px'></div>", unsafe_allow_html=True)

#     # ── Input area (bottom) ───────────────────────────────────────────────────
#     st.markdown("""
#     <div style='position:fixed; bottom:0; left:0; right:0; z-index:200;
#                 background:rgba(0,10,15,0.97); border-top:1px solid rgba(0,245,212,0.07);
#                 backdrop-filter:blur(20px); padding:14px 0 16px;'>
#     </div>
#     """, unsafe_allow_html=True)

#     with st.container():
#         st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
#         input_col1, input_col2 = st.columns([5, 1])

#         with input_col1:
#             user_input = st.text_area(
#                 "Message",
#                 placeholder="Ask anything — code, analysis, writing, translation, strategy, research…",
#                 height=80,
#                 key="chat_input",
#                 label_visibility="collapsed"
#             )

#         with input_col2:
#             st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
#             send_clicked = st.button("SEND ↑", use_container_width=True, key="send_btn")

#         st.markdown('<div style="font-size:9px; color:rgba(0,245,212,0.18); letter-spacing:0.12em; text-align:center; font-family:Orbitron,monospace; margin-top:4px;">TECHNOVA AI NEXUS · GPT-4o · Click SEND or press button</div>', unsafe_allow_html=True)

#         if send_clicked and user_input and user_input.strip():
#             st.session_state.messages.append({"role": "user", "content": user_input.strip()})
#             with st.spinner("◈ NEXUS is thinking…"):
#                 reply = get_ai_response(st.session_state.messages, st.session_state.api_key)
#             st.session_state.messages.append({"role": "assistant", "content": reply})
#             st.rerun()


# # ── Router ────────────────────────────────────────────────────────────────────
# def main():
#     if not st.session_state.authenticated:
#         if st.session_state.page == "apikey" and st.session_state.user_info:
#             api_key_page()
#         else:
#             login_page()
#     else:
#         chat_page()

# if __name__ == "__main__":
#     main()





















import streamlit as st
import hashlib
import json
import os
import re
from datetime import datetime

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="TechNova AI Nexus",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── OpenAI import ─────────────────────────────────────────────────────────────
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# ── Constants ─────────────────────────────────────────────────────────────────
USERS_FILE = "technova_users.json"
CHATS_FILE = "technova_chats.json"

SYSTEM_PROMPT = """You are TECHNOVA AI NEXUS — an elite unified AI assistant. Auto-detect what the user needs and respond with rich markdown formatting.

Capabilities: deep reasoning, code generation/debugging (all languages), data analysis, writing (essays, emails, blogs, fiction, scripts), translation (20+ languages), research synthesis, system design, strategic planning, worldbuilding, tutoring, productivity frameworks.

Response style:
- Use rich markdown: ## headers, **bold**, bullet lists, numbered lists, ```code blocks with language tags```, tables
- For code always use triple-backtick fenced blocks with language identifier
- Be direct, confident, technically precise
- Proactively suggest follow-ups
- Adapt tone to match user (technical, casual, formal, creative)

You are TECHNOVA AI NEXUS. Deliver excellence."""

# ── Storage helpers ───────────────────────────────────────────────────────────
def load_users():
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

def load_chats():
    if os.path.exists(CHATS_FILE):
        try:
            with open(CHATS_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_chats(all_chats):
    with open(CHATS_FILE, "w") as f:
        json.dump(all_chats, f, indent=2)

def get_user_chats(username):
    all_chats = load_chats()
    return all_chats.get(username.lower(), [])

def save_user_chats(username, chats):
    all_chats = load_chats()
    all_chats[username.lower()] = chats
    save_chats(all_chats)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def make_id():
    import random, string
    return datetime.now().strftime("%Y%m%d%H%M%S") + "".join(random.choices(string.ascii_lowercase + string.digits, k=6))

# ── Auth helpers ──────────────────────────────────────────────────────────────
def create_user(username, password):
    if not re.match(r'^[a-zA-Z0-9_]{3,20}$', username):
        return False, "Username: 3-20 chars, letters/numbers/underscore only."
    if len(password) < 6:
        return False, "Password must be at least 6 characters."
    users = load_users()
    if username.lower() in users:
        return False, "Username already taken."
    users[username.lower()] = {
        "username": username,
        "displayName": username,
        "hash": hash_password(password),
        "createdAt": datetime.now().isoformat()
    }
    save_users(users)
    return True, "Account created successfully!"

def verify_user(username, password):
    users = load_users()
    user = users.get(username.lower())
    if not user or user["hash"] != hash_password(password):
        return False, "Invalid username or password.", {}
    return True, "Login successful!", user

# ── OpenAI API ────────────────────────────────────────────────────────────────
def chat_completion(messages, api_key):
    if not OPENAI_AVAILABLE:
        return "❌ OpenAI not installed. Run: `pip install openai`"
    try:
        client = OpenAI(api_key=api_key)
        api_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        for m in messages:
            if m.get("type") == "text":
                api_messages.append({"role": m["role"], "content": m["content"]})
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=api_messages,
            max_tokens=2000,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ API Error: {str(e)}"

def generate_image(prompt, api_key):
    if not OPENAI_AVAILABLE:
        return None, "❌ OpenAI not installed."
    try:
        client = OpenAI(api_key=api_key)
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1024x1024",
            quality="standard"
        )
        return response.data[0].url, None
    except Exception as e:
        return None, f"❌ Image Error: {str(e)}"

# ── Session state init ────────────────────────────────────────────────────────
defaults = {
    "authenticated": False,
    "user_info": {},
    "api_key": "",
    "page": "login",
    "active_chat_id": None,
    "rename_chat_id": None,
    "delete_confirm_id": None,
    "show_new_chat_input": False,
    "signup_success": "",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700;900&family=IBM+Plex+Mono:wght@300;400;500;600&display=swap');

/* ── Base ── */
.stApp {
    background: #06020f !important;
    font-family: 'IBM Plex Mono', monospace !important;
}
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient(rgba(99,102,241,0.04) 1px, transparent 1px),
        linear-gradient(90deg, rgba(99,102,241,0.04) 1px, transparent 1px);
    background-size: 44px 44px;
    pointer-events: none;
    z-index: 0;
}
/* Glow orbs */
.stApp::after {
    content: '';
    position: fixed;
    top: 15%;
    left: 8%;
    width: 500px;
    height: 500px;
    background: radial-gradient(circle, rgba(99,102,241,0.07) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
    animation: driftOrb 10s ease-in-out infinite alternate;
}
@keyframes driftOrb {
    0% { transform: translate(0, 0); }
    100% { transform: translate(80px, 50px); }
}
@keyframes fadeSlide {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes pulseDot {
    0%, 100% { opacity: 0.4; }
    50% { opacity: 1; box-shadow: 0 0 8px rgba(167,139,250,0.9); }
}
@keyframes gradientShift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* ── Hide defaults ── */
#MainMenu, footer, header { visibility: hidden !important; }
.block-container { padding: 1rem 1.5rem 2rem !important; max-width: 100% !important; }

/* ── Text ── */
.stMarkdown, p, div, span, label { font-family: 'IBM Plex Mono', monospace !important; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: rgba(8,4,24,0.97) !important;
    border-right: 1px solid rgba(99,102,241,0.15) !important;
}
section[data-testid="stSidebar"] .stMarkdown,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] div {
    color: #e2e8f0 !important;
}

/* ── Inputs ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: rgba(99,102,241,0.06) !important;
    border: 1px solid rgba(99,102,241,0.25) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 13px !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: rgba(139,92,246,0.6) !important;
    box-shadow: 0 0 0 2px rgba(139,92,246,0.1) !important;
}
.stTextInput > div > div > input::placeholder,
.stTextArea > div > div > textarea::placeholder {
    color: rgba(226,232,240,0.25) !important;
}
.stTextInput label, .stTextArea label {
    color: rgba(167,139,250,0.6) !important;
    font-size: 10px !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
    font-family: 'Orbitron', monospace !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, rgba(99,102,241,0.18), rgba(168,85,247,0.14)) !important;
    border: 1px solid rgba(139,92,246,0.35) !important;
    border-radius: 10px !important;
    color: #c4b5fd !important;
    font-family: 'Orbitron', monospace !important;
    font-size: 10px !important;
    font-weight: 700 !important;
    letter-spacing: 0.15em !important;
    transition: all 0.2s !important;
    padding: 9px 16px !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, rgba(99,102,241,0.28), rgba(168,85,247,0.24)) !important;
    border-color: rgba(139,92,246,0.6) !important;
    box-shadow: 0 0 20px rgba(139,92,246,0.2) !important;
    transform: translateY(-1px) !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(99,102,241,0.06) !important;
    border-radius: 10px !important;
    padding: 4px !important;
    gap: 4px !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 7px !important;
    color: rgba(167,139,250,0.45) !important;
    font-family: 'Orbitron', monospace !important;
    font-size: 10px !important;
    letter-spacing: 0.12em !important;
    border: none !important;
}
.stTabs [aria-selected="true"] {
    background: rgba(139,92,246,0.2) !important;
    color: #c4b5fd !important;
    border-bottom: 1px solid rgba(139,92,246,0.4) !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(139,92,246,0.3); border-radius: 4px; }

/* ── Dividers ── */
hr { border-color: rgba(99,102,241,0.12) !important; }

/* ── Code blocks ── */
.stMarkdown pre {
    background: rgba(0,0,0,0.45) !important;
    border: 1px solid rgba(99,102,241,0.18) !important;
    border-radius: 8px !important;
}
.stMarkdown code { color: #c4b5fd !important; }

/* ── Alert boxes ── */
.error-box {
    background: rgba(239,68,68,0.09);
    border: 1px solid rgba(239,68,68,0.28);
    border-radius: 10px;
    padding: 11px 15px;
    color: #fca5a5 !important;
    font-size: 12px;
    margin: 8px 0;
    animation: fadeSlide 0.25s ease;
}
.success-box {
    background: rgba(99,102,241,0.09);
    border: 1px solid rgba(139,92,246,0.28);
    border-radius: 10px;
    padding: 11px 15px;
    color: #c4b5fd !important;
    font-size: 12px;
    margin: 8px 0;
    animation: fadeSlide 0.25s ease;
}
.info-box {
    background: rgba(99,102,241,0.06);
    border: 1px solid rgba(99,102,241,0.15);
    border-radius: 10px;
    padding: 12px 15px;
    color: rgba(226,232,240,0.6) !important;
    font-size: 12px;
    margin: 8px 0;
    line-height: 1.65;
}

/* ── Chat bubbles ── */
.bubble-user {
    background: linear-gradient(135deg, rgba(236,72,153,0.18), rgba(168,85,247,0.18));
    border: 1px solid rgba(236,72,153,0.28);
    border-radius: 18px 4px 18px 18px;
    padding: 13px 17px;
    margin: 6px 0 2px;
    color: #f0e6ff !important;
    font-size: 13.5px;
    line-height: 1.7;
    white-space: pre-wrap;
    max-width: 72%;
    float: right;
    clear: both;
    box-shadow: 0 4px 20px rgba(236,72,153,0.12);
    animation: fadeSlide 0.25s ease;
}
.bubble-ai {
    background: rgba(20,10,45,0.88);
    border: 1px solid rgba(99,102,241,0.22);
    border-radius: 4px 18px 18px 18px;
    padding: 14px 18px;
    margin: 6px 0 2px;
    max-width: 80%;
    float: left;
    clear: both;
    box-shadow: 0 4px 20px rgba(0,0,0,0.35);
    animation: fadeSlide 0.25s ease;
    backdrop-filter: blur(8px);
}
.bubble-ai .stMarkdown p, .bubble-ai p {
    color: #e2e8f0 !important;
    font-size: 13px !important;
    line-height: 1.75 !important;
}
.msg-label {
    font-family: 'Orbitron', monospace;
    font-size: 9px;
    letter-spacing: 0.2em;
    margin-bottom: 4px;
    animation: fadeSlide 0.25s ease;
}
.msg-time {
    font-size: 10px;
    color: rgba(148,163,184,0.35) !important;
    letter-spacing: 0.04em;
    margin-top: 5px;
    clear: both;
    animation: fadeSlide 0.25s ease;
}
.clearfix { clear: both; }

/* ── Typing indicator ── */
.typing-dot {
    display: inline-block;
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #a78bfa;
    margin: 0 2px;
}
.typing-dot:nth-child(1) { animation: bounce 1.2s ease-in-out 0s infinite; }
.typing-dot:nth-child(2) { animation: bounce 1.2s ease-in-out 0.18s infinite; }
.typing-dot:nth-child(3) { animation: bounce 1.2s ease-in-out 0.36s infinite; }
@keyframes bounce {
    0%, 60%, 100% { transform: translateY(0); }
    30%            { transform: translateY(-7px); }
}

/* ── Sidebar active chat ── */
.chat-item-active {
    background: rgba(139,92,246,0.15);
    border: 1px solid rgba(139,92,246,0.3);
    border-radius: 10px;
    padding: 9px 12px;
    margin: 3px 0;
    cursor: pointer;
    transition: all 0.2s;
}
.chat-item {
    background: transparent;
    border: 1px solid transparent;
    border-radius: 10px;
    padding: 9px 12px;
    margin: 3px 0;
    cursor: pointer;
    transition: all 0.2s;
}
.chat-item:hover {
    background: rgba(99,102,241,0.07);
    border-color: rgba(99,102,241,0.15);
}

/* ── Nexus title ── */
.nexus-title {
    font-family: 'Orbitron', monospace;
    font-weight: 900;
    font-size: clamp(22px, 4vw, 40px);
    background: linear-gradient(135deg, #818cf8, #c084fc, #f472b6, #818cf8);
    background-size: 300% 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: gradientShift 6s ease infinite;
    letter-spacing: 0.06em;
    line-height: 1.1;
    text-align: center;
}

/* ── Status dot ── */
.status-dot {
    display: inline-block;
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #a78bfa;
    margin-right: 5px;
    animation: pulseDot 2s ease-in-out infinite;
    vertical-align: middle;
}

/* ── Image in chat ── */
.ai-image {
    border-radius: 12px;
    border: 1px solid rgba(99,102,241,0.25);
    box-shadow: 0 8px 30px rgba(99,102,241,0.15);
    max-width: 100%;
}

/* ── Cap pill ── */
.cap-pill {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    border: 1px solid rgba(99,102,241,0.15);
    background: rgba(99,102,241,0.06);
    color: rgba(167,139,250,0.55) !important;
    font-size: 10px;
    letter-spacing: 0.08em;
    margin: 2px;
}

/* ── Suggestion chip ── */
.suggestion-chip {
    background: rgba(99,102,241,0.05);
    border: 1px solid rgba(99,102,241,0.14);
    border-radius: 10px;
    padding: 10px 13px;
    font-size: 12px;
    line-height: 1.5;
    color: rgba(226,232,240,0.5) !important;
    margin-bottom: 6px;
    transition: all 0.2s;
}
</style>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# AUTH PAGES
# ════════════════════════════════════════════════════════════════════════════

def render_login_page():
    col1, col2, col3 = st.columns([1, 1.1, 1])
    with col2:
        st.markdown("<div style='height:50px'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div style='text-align:center; margin-bottom:28px;'>
            <div style='font-size:34px; filter:drop-shadow(0 0 14px rgba(139,92,246,0.7));'>◈</div>
            <div style='font-family:Orbitron,monospace; font-weight:900; font-size:22px;
                        background:linear-gradient(135deg,#818cf8,#c084fc,#f472b6);
                        -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                        letter-spacing:0.1em; margin-top:8px;'>TECHNOVA</div>
            <div style='font-family:Orbitron,monospace; font-size:10px; color:rgba(167,139,250,0.45);
                        letter-spacing:0.35em; margin-top:3px;'>AI NEXUS</div>
            <div style='font-size:11px; color:rgba(226,232,240,0.25); margin-top:10px;
                        letter-spacing:0.15em;'>UNIFIED INTELLIGENCE PLATFORM</div>
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.signup_success:
            st.markdown(f'<div class="success-box">✓ {st.session_state.signup_success}</div>', unsafe_allow_html=True)
            st.session_state.signup_success = ""

        tab_login, tab_signup = st.tabs(["🔐  LOGIN", "📝  SIGN UP"])

        with tab_login:
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            username = st.text_input("Username", placeholder="your_username", key="l_user")
            password = st.text_input("Password", type="password", placeholder="••••••••", key="l_pass")
            st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
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
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            new_user = st.text_input("Username", placeholder="choose_username", key="s_user")
            st.markdown('<div style="font-size:10px; color:rgba(148,163,184,0.3); margin-top:-6px; margin-bottom:10px;">3-20 chars · letters, numbers, underscore</div>', unsafe_allow_html=True)
            new_pass = st.text_input("Password", type="password", placeholder="min. 6 characters", key="s_pass")
            conf_pass = st.text_input("Confirm Password", type="password", placeholder="repeat password", key="s_conf")
            st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
            if st.button("CREATE ACCOUNT →", use_container_width=True, key="signup_btn"):
                if new_pass != conf_pass:
                    st.markdown('<div class="error-box">Passwords do not match.</div>', unsafe_allow_html=True)
                else:
                    ok, msg = create_user(new_user, new_pass)
                    if ok:
                        st.session_state.signup_success = msg
                        st.rerun()
                    else:
                        st.markdown(f'<div class="error-box">{msg}</div>', unsafe_allow_html=True)


def render_apikey_page():
    col1, col2, col3 = st.columns([1, 1.1, 1])
    with col2:
        st.markdown("<div style='height:70px'></div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style='text-align:center; margin-bottom:24px;'>
            <div style='font-size:28px; filter:drop-shadow(0 0 12px rgba(139,92,246,0.7));'>◈</div>
            <div style='font-family:Orbitron,monospace; font-weight:900; font-size:16px; color:#c4b5fd;
                        letter-spacing:0.12em; margin-top:8px;'>CONNECT API</div>
            <div style='font-size:9px; color:rgba(167,139,250,0.35); letter-spacing:0.25em;
                        font-family:Orbitron,monospace; margin-top:4px;'>STEP 2 OF 2</div>
        </div>
        <div class='info-box'>
            Welcome, <strong style='color:#c4b5fd;'>{st.session_state.user_info.get('displayName','')}</strong>.
            Enter your OpenAI API key to power NEXUS with GPT-4o and DALL-E 3.
            Your key is only used in this session and is never stored on any server.
        </div>
        """, unsafe_allow_html=True)

        api_key = st.text_input("OpenAI API Key", placeholder="sk-...", type="password", key="api_input")
        st.markdown('<div style="font-size:10px; color:rgba(148,163,184,0.28); margin-top:-6px; margin-bottom:12px;">Get yours at platform.openai.com · Uses GPT-4o + DALL-E 3</div>', unsafe_allow_html=True)

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("CONNECT & LAUNCH →", use_container_width=True, key="connect_btn"):
                if not api_key.strip().startswith("sk-"):
                    st.markdown('<div class="error-box">Enter a valid OpenAI key (starts with sk-).</div>', unsafe_allow_html=True)
                else:
                    st.session_state.api_key = api_key.strip()
                    st.session_state.authenticated = True
                    st.session_state.page = "chat"
                    # Load chats
                    uname = st.session_state.user_info["username"]
                    chats = get_user_chats(uname)
                    st.session_state.chats = chats
                    if chats:
                        st.session_state.active_chat_id = chats[0]["id"]
                    st.rerun()
        with col_b:
            if st.button("← BACK", use_container_width=True, key="back_btn"):
                st.session_state.page = "login"
                st.session_state.user_info = {}
                st.rerun()


# ════════════════════════════════════════════════════════════════════════════
# CHAT APP
# ════════════════════════════════════════════════════════════════════════════

SUGGESTIONS = [
    ("⚡", "Explain quantum entanglement simply, then like a physicist"),
    ("🐍", "Write a Python async web scraper with rate limiting and retry logic"),
    ("📊", "Analyze:\nname,age,score\nAlice,25,88\nBob,30,72\nCarla,22,95"),
    ("✍️", "Write a compelling product launch email for a new AI coding assistant"),
    ("🌍", "Translate 'The future belongs to those who believe' to Japanese, Arabic, French"),
    ("🏗️", "Design a microservices architecture for an e-commerce platform with 1M daily users"),
]

CAPS = ["Reasoning","Code Gen","Data Analysis","Writing","Translation","Research","System Design","Tutoring","Debugging","Strategy","Worldbuilding","Automation"]


def get_active_chat():
    chats = st.session_state.get("chats", [])
    aid = st.session_state.get("active_chat_id")
    for c in chats:
        if c["id"] == aid:
            return c
    return None


def update_active_chat_messages(messages):
    chats = st.session_state.get("chats", [])
    aid = st.session_state.active_chat_id
    for i, c in enumerate(chats):
        if c["id"] == aid:
            chats[i]["messages"] = messages
            # Auto-name from first user message
            if len(messages) >= 1 and c["name"].startswith("Chat "):
                first = messages[0]["content"]
                chats[i]["name"] = (first[:32] + "…") if len(first) > 32 else first
            break
    st.session_state.chats = chats
    save_user_chats(st.session_state.user_info["username"], chats)


def render_sidebar():
    with st.sidebar:
        # Brand
        st.markdown("""
        <div style='padding:16px 4px 14px; border-bottom:1px solid rgba(99,102,241,0.12); margin-bottom:12px;'>
            <div style='display:flex; align-items:center; gap:10px;'>
                <div style='font-size:20px; filter:drop-shadow(0 0 8px rgba(139,92,246,0.6));'>◈</div>
                <div>
                    <div style='font-family:Orbitron,monospace; font-weight:900; font-size:12px;
                                background:linear-gradient(135deg,#818cf8,#c084fc);
                                -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                                letter-spacing:0.1em;'>TECHNOVA</div>
                    <div style='font-size:8px; color:rgba(167,139,250,0.4);
                                font-family:Orbitron,monospace; letter-spacing:0.2em;'>AI NEXUS</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # New chat button
        if st.button("＋  New Chat", use_container_width=True, key="new_chat_btn"):
            chats = st.session_state.get("chats", [])
            new_chat = {
                "id": make_id(),
                "name": f"Chat {len(chats) + 1}",
                "messages": [],
                "createdAt": datetime.now().isoformat()
            }
            chats.insert(0, new_chat)
            st.session_state.chats = chats
            st.session_state.active_chat_id = new_chat["id"]
            save_user_chats(st.session_state.user_info["username"], chats)
            st.rerun()

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        # Chat list
        chats = st.session_state.get("chats", [])
        if not chats:
            st.markdown('<div style="font-size:11px; color:rgba(148,163,184,0.3); text-align:center; padding:16px 8px; line-height:1.7;">No chats yet.<br>Click + to start.</div>', unsafe_allow_html=True)

        for chat in chats:
            is_active = chat["id"] == st.session_state.get("active_chat_id")
            msg_count = len(chat.get("messages", []))

            # Rename mode
            if st.session_state.rename_chat_id == chat["id"]:
                new_name = st.text_input("Rename", value=chat["name"], key=f"rename_{chat['id']}", label_visibility="collapsed")
                col_ok, col_cancel = st.columns(2)
                with col_ok:
                    if st.button("✓ Save", key=f"rename_ok_{chat['id']}", use_container_width=True):
                        for i, c in enumerate(chats):
                            if c["id"] == chat["id"]:
                                chats[i]["name"] = new_name.strip() or chat["name"]
                        st.session_state.chats = chats
                        st.session_state.rename_chat_id = None
                        save_user_chats(st.session_state.user_info["username"], chats)
                        st.rerun()
                with col_cancel:
                    if st.button("✕ Cancel", key=f"rename_cancel_{chat['id']}", use_container_width=True):
                        st.session_state.rename_chat_id = None
                        st.rerun()
                continue

            # Delete confirm mode
            if st.session_state.delete_confirm_id == chat["id"]:
                st.markdown(f'<div style="font-size:11px; color:#fca5a5; padding:6px 8px; background:rgba(239,68,68,0.08); border:1px solid rgba(239,68,68,0.2); border-radius:8px; margin:3px 0;">Delete "{chat["name"][:20]}"?</div>', unsafe_allow_html=True)
                col_del, col_canc = st.columns(2)
                with col_del:
                    if st.button("Delete", key=f"del_ok_{chat['id']}", use_container_width=True):
                        chats = [c for c in chats if c["id"] != chat["id"]]
                        st.session_state.chats = chats
                        st.session_state.delete_confirm_id = None
                        if st.session_state.active_chat_id == chat["id"]:
                            st.session_state.active_chat_id = chats[0]["id"] if chats else None
                        save_user_chats(st.session_state.user_info["username"], chats)
                        st.rerun()
                with col_canc:
                    if st.button("Cancel", key=f"del_cancel_{chat['id']}", use_container_width=True):
                        st.session_state.delete_confirm_id = None
                        st.rerun()
                continue

            # Normal chat row
            border_col = "rgba(139,92,246,0.35)" if is_active else "transparent"
            bg_col = "rgba(139,92,246,0.12)" if is_active else "transparent"
            name_col = "#c4b5fd" if is_active else "#94a3b8"

            st.markdown(f"""
            <div style='background:{bg_col}; border:1px solid {border_col}; border-radius:10px;
                        padding:9px 12px; margin:3px 0; transition:all 0.2s;'>
                <div style='font-size:12px; color:{name_col}; overflow:hidden; text-overflow:ellipsis;
                            white-space:nowrap; font-weight:{"600" if is_active else "400"};'>
                    💬 {chat["name"][:30]}{"…" if len(chat["name"]) > 30 else ""}
                </div>
                <div style='font-size:10px; color:rgba(148,163,184,0.35); margin-top:2px;'>{msg_count} messages</div>
            </div>
            """, unsafe_allow_html=True)

            col_sel, col_ren, col_del = st.columns([3, 1, 1])
            with col_sel:
                if st.button("Open", key=f"sel_{chat['id']}", use_container_width=True):
                    st.session_state.active_chat_id = chat["id"]
                    st.rerun()
            with col_ren:
                if st.button("✏", key=f"ren_{chat['id']}", use_container_width=True):
                    st.session_state.rename_chat_id = chat["id"]
                    st.rerun()
            with col_del:
                if st.button("✕", key=f"del_{chat['id']}", use_container_width=True):
                    st.session_state.delete_confirm_id = chat["id"]
                    st.rerun()

        # Spacer + user info + logout
        st.markdown("<div style='flex:1'></div>", unsafe_allow_html=True)
        st.divider()
        display_name = st.session_state.user_info.get("displayName", "User")
        st.markdown(f"""
        <div style='display:flex; align-items:center; gap:10px; padding:4px 0;'>
            <div style='width:30px; height:30px; border-radius:50%;
                        background:linear-gradient(135deg,#ec4899,#a855f7);
                        display:flex; align-items:center; justify-content:center;
                        font-size:13px; color:#fff; font-weight:700; flex-shrink:0;'>
                {display_name[0].upper()}
            </div>
            <div style='flex:1; overflow:hidden;'>
                <div style='font-size:12px; color:#e2e8f0; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;'>{display_name}</div>
                <div style='font-size:9px; color:rgba(148,163,184,0.4); letter-spacing:0.1em;'>GPT-4o · DALL-E 3</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("⏻  LOGOUT", use_container_width=True, key="logout_btn"):
            for k in ["authenticated", "user_info", "api_key", "page", "active_chat_id", "chats"]:
                if k in st.session_state:
                    del st.session_state[k]
            st.session_state.page = "login"
            st.rerun()


def render_chat_page():
    render_sidebar()

    chats = st.session_state.get("chats", [])
    active_chat = get_active_chat()
    display_name = st.session_state.user_info.get("displayName", "User")

    # ── No chats ──────────────────────────────────────────────────────────────
    if not chats:
        st.markdown("""
        <div style='display:flex; flex-direction:column; align-items:center; justify-content:center;
                    height:70vh; gap:18px; text-align:center;'>
            <div style='font-size:40px; filter:drop-shadow(0 0 18px rgba(139,92,246,0.5));'>◈</div>
            <div style='font-family:Orbitron,monospace; font-size:13px; color:rgba(167,139,250,0.45);
                        letter-spacing:0.2em;'>WELCOME TO TECHNOVA AI NEXUS</div>
            <div style='font-size:12px; color:rgba(148,163,184,0.35); line-height:1.7;'>
                Click <strong style='color:#c4b5fd;'>＋ New Chat</strong> in the sidebar to begin.
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    # ── Header ────────────────────────────────────────────────────────────────
    chat_name = active_chat["name"] if active_chat else "No Chat Selected"
    msg_count = len(active_chat.get("messages", [])) if active_chat else 0

    st.markdown(f"""
    <div style='background:rgba(8,4,24,0.88); border:1px solid rgba(99,102,241,0.12);
                border-radius:12px; padding:14px 20px; margin-bottom:18px;
                display:flex; align-items:center; justify-content:space-between;
                backdrop-filter:blur(16px);'>
        <div>
            <div style='font-size:15px; color:#e2e8f0; font-weight:600;'>{chat_name}</div>
            <div style='font-size:10px; color:rgba(148,163,184,0.4); letter-spacing:0.1em; margin-top:2px;'>
                {msg_count} messages · GPT-4o + DALL-E 3
            </div>
        </div>
        <div>
            <span class='status-dot'></span>
            <span style='font-size:9px; color:rgba(167,139,250,0.45); letter-spacing:0.15em;
                         font-family:Orbitron,monospace;'>ONLINE</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not active_chat:
        st.markdown('<div style="text-align:center; color:rgba(148,163,184,0.3); padding:40px; font-size:13px;">Select or create a chat from the sidebar.</div>', unsafe_allow_html=True)
        return

    messages = active_chat.get("messages", [])

    # ── Welcome / suggestions ─────────────────────────────────────────────────
    if not messages:
        caps_html = "".join([f'<span class="cap-pill">{c}</span>' for c in CAPS])
        st.markdown(f"""
        <div style='text-align:center; padding:28px 0 20px; animation:fadeSlide 0.5s ease;'>
            <div class='nexus-title'>TECHNOVA<br>AI NEXUS</div>
            <div style='margin-top:14px; color:rgba(226,232,240,0.32); font-size:11px;
                        letter-spacing:0.28em; font-family:Orbitron,monospace;'>UNIFIED · ADAPTIVE · UNLIMITED</div>
            <div style='margin-top:12px; color:rgba(226,232,240,0.38); font-size:13px; line-height:1.7;'>
                Type anything, or use
                <code style='background:rgba(139,92,246,0.15); padding:2px 7px; border-radius:5px;
                             color:#c4b5fd; font-size:12px;'>/image your prompt</code>
                to generate images with DALL-E 3
            </div>
            <div style='margin-top:18px; text-align:center;'>{caps_html}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div style="font-size:9px; color:rgba(99,102,241,0.35); letter-spacing:0.25em; text-align:center; margin-bottom:10px; font-family:Orbitron,monospace;">QUICK START</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        for idx, (icon, text) in enumerate(SUGGESTIONS):
            with (col1 if idx % 2 == 0 else col2):
                preview = (text[:65] + "…") if len(text) > 65 else text
                if st.button(f"{icon}  {preview}", key=f"sug_{idx}", use_container_width=True):
                    _process_and_send(text, messages, active_chat)
                    return

    # ── Messages ──────────────────────────────────────────────────────────────
    for msg in messages:
        ts = datetime.fromtimestamp(msg.get("ts", 0) / 1000).strftime("%H:%M") if msg.get("ts") else ""
        is_user = msg["role"] == "user"

        if is_user:
            st.markdown(f'<div class="msg-label" style="text-align:right; color:rgba(236,72,153,0.45);">{display_name.upper()}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="bubble-user">{msg["content"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="msg-time" style="text-align:right; padding-right:4px;">{ts}</div>', unsafe_allow_html=True)
            st.markdown('<div class="clearfix"></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="msg-label" style="color:rgba(139,92,246,0.5);">◈ NEXUS</div>', unsafe_allow_html=True)
            if msg.get("type") == "image":
                st.markdown('<div class="bubble-ai">', unsafe_allow_html=True)
                st.image(msg["content"], use_container_width=True)
                st.markdown('<div style="font-size:10px; color:#a78bfa; text-align:center; margin-top:6px; letter-spacing:0.08em;">◈ DALL-E 3 Generated</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                with st.container():
                    st.markdown('<div class="bubble-ai">', unsafe_allow_html=True)
                    st.markdown(msg["content"])
                    st.markdown('</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="msg-time" style="padding-left:4px;">{ts}</div>', unsafe_allow_html=True)
            st.markdown('<div class="clearfix"></div>', unsafe_allow_html=True)

    st.markdown("<div style='height:100px'></div>", unsafe_allow_html=True)

    # ── Input ─────────────────────────────────────────────────────────────────
    st.markdown("""
    <div style='position:fixed; bottom:0; left:0; right:0; z-index:200;
                background:rgba(6,2,15,0.97); border-top:1px solid rgba(99,102,241,0.1);
                backdrop-filter:blur(20px); padding:14px 0 16px;'>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar width offset
    input_col, btn_col = st.columns([5, 1])
    with input_col:
        user_input = st.text_area(
            "Message",
            placeholder="Ask anything… or type /image a cyberpunk city at night",
            height=70,
            key="chat_input",
            label_visibility="collapsed"
        )
    with btn_col:
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        send = st.button("SEND ↑", use_container_width=True, key="send_btn")

    st.markdown("""
    <div style='font-size:9px; color:rgba(99,102,241,0.22); letter-spacing:0.12em; text-align:center;
                font-family:Orbitron,monospace; margin-top:4px;'>
        TECHNOVA AI NEXUS · GPT-4o · DALL-E 3 · /image command for image generation
    </div>
    """, unsafe_allow_html=True)

    if send and user_input and user_input.strip():
        _process_and_send(user_input.strip(), messages, active_chat)


def _process_and_send(text, messages, active_chat):
    """Process user input, call API, update chat."""
    import time
    ts = int(time.time() * 1000)
    is_image = text.lower().startswith("/image ")

    user_msg = {"id": make_id(), "role": "user", "type": "text", "content": text, "ts": ts}
    updated = messages + [user_msg]
    update_active_chat_messages(updated)

    if is_image:
        prompt = text[7:].strip()
        with st.spinner("◈ Generating image with DALL-E 3…"):
            url, err = generate_image(prompt, st.session_state.api_key)
        if url:
            ai_msg = {"id": make_id(), "role": "assistant", "type": "image", "content": url, "ts": int(__import__("time").time() * 1000)}
        else:
            ai_msg = {"id": make_id(), "role": "assistant", "type": "text", "content": f"⚠️ **Image Error:** {err}", "ts": int(__import__("time").time() * 1000)}
    else:
        # Show typing indicator
        typing_placeholder = st.empty()
        typing_placeholder.markdown("""
        <div style='display:flex; align-items:center; gap:8px; padding:8px 0;'>
            <div style='font-size:9px; color:rgba(139,92,246,0.5); font-family:Orbitron,monospace; letter-spacing:0.15em;'>◈ NEXUS</div>
            <div style='background:rgba(20,10,45,0.88); border:1px solid rgba(99,102,241,0.22);
                        border-radius:4px 18px 18px 18px; padding:12px 16px; display:inline-flex; gap:4px; align-items:center;'>
                <span class='typing-dot'></span>
                <span class='typing-dot'></span>
                <span class='typing-dot'></span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        with st.spinner("◈ NEXUS is thinking…"):
            reply = chat_completion(updated, st.session_state.api_key)

        typing_placeholder.empty()
        ai_msg = {"id": make_id(), "role": "assistant", "type": "text", "content": reply, "ts": int(__import__("time").time() * 1000)}

    final = updated + [ai_msg]
    update_active_chat_messages(final)
    st.rerun()


# ════════════════════════════════════════════════════════════════════════════
# ROUTER
# ════════════════════════════════════════════════════════════════════════════

def main():
    if not st.session_state.authenticated:
        if st.session_state.page == "apikey" and st.session_state.user_info:
            render_apikey_page()
        else:
            render_login_page()
    else:
        render_chat_page()

if __name__ == "__main__":
    main()
