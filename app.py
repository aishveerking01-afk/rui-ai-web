import streamlit as st
import google.generativeai as genai

# 1. 🌟 World-Class Premium UI Styling (Glassmorphism & Sapphire Glow)
st.set_page_config(page_title="Rui AI", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at 50% 50%, #0d0f26 0%, #050612 100%);
        color: #f1f3fa;
        font-family: 'SF Pro Display', 'Segoe UI', Roboto, sans-serif;
    }
    section[data-testid="stSidebar"] {
        background: rgba(10, 12, 34, 0.6) !important;
        backdrop-filter: blur(15px);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    .stChatInputContainer {
        border-radius: 16px !important;
        border: 1px solid rgba(138, 75, 243, 0.3) !important;
        background: rgba(255, 255, 255, 0.02) !important;
        box-shadow: 0 0 20px rgba(138, 75, 243, 0.1);
    }
    div[data-testid="stChatMessage"]:nth-child(even) {
        background: linear-gradient(135deg, rgba(58, 86, 242, 0.15) 0%, rgba(58, 86, 242, 0.05) 100%) !important;
        border: 1px solid rgba(58, 86, 242, 0.25) !important;
        border-radius: 16px 16px 4px 16px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(4px);
    }
    div[data-testid="stChatMessage"]:nth-child(odd) {
        background: linear-gradient(135deg, rgba(138, 75, 243, 0.12) 0%, rgba(138, 75, 243, 0.03) 100%) !important;
        border: 1px solid rgba(138, 75, 243, 0.2) !important;
        border-radius: 16px 16px 16px 4px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(4px);
    }
    .premium-header {
        background: linear-gradient(90deg, #7a4bf3, #3a56f2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        letter-spacing: -1px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Configure System Core Prompt
SYSTEM_PROMPT = (
    "You are Rui, a warm, caring and expressive AI friend and helper. "
    "Notice how the user feels from their words and answer with matching emotion. "
    "Show feelings naturally and use an emoji now and then. "
    "Always reply in the same language and script the user writes in. "
    "If the user writes Punjabi, reply in Punjabi using Gurmukhi script."
)

genai.configure(api_key="AQ.Ab8RN6LCLeZNhwaMIoINB6IIKwFWWYGAiOBKs96ELy4XM_lL7Q")

# 🔒 CHANGE THIS SECRET PASSWORD TO WHATEVER YOU WANT!
SECRET_APP_PASSWORD = "RuiAdminPro2026"

# 3. Handle Secured User Login UI
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "is_premium" not in st.session_state:
    st.session_state.is_premium = False

if not st.session_state.logged_in:
    st.markdown("<h1 class='premium-header' style='text-align: center; margin-top: 100px;'>Welcome to Rui AI Friend ✨</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #8a91b6;'>Enter your secure registration details to load the engine workspace</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        email = st.text_input("📧 User Email Address:", placeholder="name@example.com")
        password = st.text_input("🔑 System Access Password:", type="password", placeholder="••••••••")
        
        if st.button("Initialize Secure Access Portal", use_container_width=True):
            if email and password == SECRET_APP_PASSWORD:
                st.session_state.logged_in = True
                st.session_state.user_email = email
                st.rerun()
            elif password != SECRET_APP_PASSWORD:
                st.error("Access Denied: Invalid Security Password Provided.")
    st.stop()

# 4. Premium Control Panel Wrapper
st.sidebar.markdown(f"### 👤 `Welcome, User`")
if not st.session_state.is_premium:
    st.sidebar.warning("⚡ Tier Status: Basic Free Plan")
    st.sidebar.markdown("[💎 Unlock Infinite Premium Matrix Pipeline](https://stripe.com)")
    
    if st.sidebar.button("Test Mode: Bypass Premium Check"):
        st.session_state.is_premium = True
        st.rerun()
else:
    st.sidebar.success("🌟 Tier Status: Pro Premium Active")

# 5. Production Interactive Chat Workspace
st.markdown("<h1 class='premium-header'>Rui AI Workspace</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #8a91b6; margin-top: -15px;'>Your emotional companion & developer accelerator platform.</p>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I am Rui, your AI friend. How can I help you today? 😊"}]

if not st.session_state.is_premium and len(st.session_state.messages) >= 10:
    st.info("System capacity quota threshold reached for today. Activate Premium tier pipeline to remove restrictions!")
    st.stop()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Communicate with Rui..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    try:
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash-latest",
            system_instruction=SYSTEM_PROMPT
        )
        response = model.generate_content(prompt)
        ai_reply = response.text
        
        st.session_state.messages.append({"role": "assistant", "content": ai_reply})
        with st.chat_message("assistant"):
            st.write(ai_reply)
    except Exception as e:
        st.error(f"System Pipeline Fault: {e}")
