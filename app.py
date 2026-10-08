import streamlit as st
from openai import OpenAI

# 1. 🌟 World-Class Premium UI Styling (Glassmorphism & Neon Glow)
st.set_page_config(page_title="Rui AI", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    /* Premium Cyber Space Background */
    .stApp {
        background: radial-gradient(circle at 50% 50%, #0d0f26 0%, #050612 100%);
        color: #f1f3fa;
        font-family: 'SF Pro Display', 'Segoe UI', Roboto, sans-serif;
    }
    
    /* Transparent Frosted Sidebar Wrapper */
    section[data-testid="stSidebar"] {
        background: rgba(10, 12, 34, 0.6) !important;
        backdrop-filter: blur(15px);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Neon Gradient Chat Input Box */
    .stChatInputContainer {
        border-radius: 16px !important;
        border: 1px solid rgba(138, 75, 243, 0.3) !important;
        background: rgba(255, 255, 255, 0.02) !important;
        box-shadow: 0 0 20px rgba(138, 75, 243, 0.1);
    }
    
    /* User Message Style - Sapphire Glass */
    div[data-testid="stChatMessage"]:nth-child(even) {
        background: linear-gradient(135deg, rgba(58, 86, 242, 0.15) 0%, rgba(58, 86, 242, 0.05) 100%) !important;
        border: 1px solid rgba(58, 86, 242, 0.25) !important;
        border-radius: 16px 16px 4px 16px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(4px);
    }
    
    /* Rui AI Message Style - Amethyst Glass */
    div[data-testid="stChatMessage"]:nth-child(odd) {
        background: linear-gradient(135deg, rgba(138, 75, 243, 0.12) 0%, rgba(138, 75, 243, 0.03) 100%) !important;
        border: 1px solid rgba(138, 75, 243, 0.2) !important;
        border-radius: 16px 16px 16px 4px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(4px);
    }
    
    /* Luxury Glow Dashboard Card Headers */
    .premium-header {
        background: linear-gradient(90deg, #7a4bf3, #3a56f2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        letter-spacing: -1px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Configure System Core Options
SYSTEM_PROMPT = (
    "You are Rui, a warm, caring and expressive AI friend and helper. "
    "Notice how the user feels from their words and answer with matching emotion. "
    "Show feelings naturally and use an emoji now and then. "
    "Always reply in the same language and script the user writes in. "
    "If the user writes Punjabi, reply in Punjabi using Gurmukhi script."
)

# Active OpenAI Infrastructure Instance
client = OpenAI(api_key="sk-proj-RUIAIKEY1029384756564738291010293847565647382910")

# 3. Secure Gate & Custom Identity UI
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "is_premium" not in st.session_state:
    st.session_state.is_premium = False

if not st.session_state.logged_in:
    st.markdown("<h1 class='premium-header' style='text-align: center; margin-top: 100px;'>Welcome to Rui AI Friend ✨</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #8a91b6;'>Enter your workspace terminal access token below</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        email = st.text_input("🔑 Email Address Account:", label_visibility="collapsed", placeholder="name@example.com")
        if st.button("Initialize Secure Access Portal", use_container_width=True):
            if email:
                st.session_state.logged_in = True
                st.session_state.user_email = email
                st.rerun()
    st.stop()

# 4. Premium Control Panel Wrapper
st.sidebar.markdown(f"### 👤 `{st.session_state.user_email}`")
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
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I am Rui, your AI friend. How are you feeling today? 😊"}]

# Limit system resource depletion for non-paying consumers
if not st.session_state.is_premium and len(st.session_state.messages) >= 10:
    st.info("System capacity quota threshold reached for today. Activate Premium tier pipeline to remove restrictions!")
    st.stop()

# Draw operational thread entries
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Capture live keystroke input events
if prompt := st.chat_input("Communicate with Rui..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ]
        )
        ai_reply = response.choices.message.content
        
        st.session_state.messages.append({"role": "assistant", "content": ai_reply})
        with st.chat_message("assistant"):
            st.write(ai_reply)
    except Exception as e:
        st.error(f"System Pipeline Fault: {e}")
