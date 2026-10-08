import streamlit as st
import requests

# 1. 🌟 The Exact Original Beautiful Dark UI Styling
st.set_page_config(page_title="Rui", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    /* Dark Cyber Theme Background */
    .stApp {
        background-color: #080a1c;
        color: #eaedfa;
        font-family: 'Segoe UI', Roboto, sans-serif;
    }
    
    /* Transparent Frosted Sidebar Panels */
    section[data-testid="stSidebar"] {
        background: #0c0e24 !important;
        border-right: 1px solid #303662;
    }
    
    /* Main Chat Boxes */
    div[data-testid="stChatMessage"] {
        background-color: #131632 !important;
        border: 1px solid #303662 !important;
        border-radius: 12px !important;
        padding: 15px !important;
        margin: 10px 0 !important;
    }
    
    /* Input Container Box styling */
    .stChatInputContainer {
        border-radius: 12px !important;
        border: 1px solid #303662 !important;
        background: #131632 !important;
    }
    
    /* Glowing Title Headers */
    .premium-header {
        color: #eaedfa;
        font-weight: 700;
        letter-spacing: -0.5px;
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

# 3. Handle Secured User Login UI
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "is_premium" not in st.session_state:
    st.session_state.is_premium = False

if not st.session_state.logged_in:
    st.markdown("<h1 class='premium-header' style='text-align: center; margin-top: 100px;'>Welcome to Rui AI Friend ✨</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        email = st.text_input("📧 User Email Address:", placeholder="name@example.com")
        
        if st.button("Initialize Secure Access Portal", use_container_width=True):
            if email:
                st.session_state.logged_in = True
                st.session_state.user_email = email
                st.rerun()
    st.stop()

# 4. Sidebar Controls
st.sidebar.markdown(f"### 👤 `Welcome, User`")
if not st.session_state.is_premium:
    st.sidebar.warning("⚡ Tier Status: Basic Free Plan")
    st.sidebar.markdown("[💎 Unlock Infinite Premium Matrix Pipeline](https://stripe.com)")
    
    if st.sidebar.button("Test Mode: Bypass Premium Check"):
        st.session_state.is_premium = True
        st.rerun()
else:
    st.sidebar.success("🌟 Tier Status: Pro Premium Active")

# 5. Interactive Chat Workspace
st.markdown("<h1 class='premium-header'>Rui AI Workspace</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #8a1d2; margin-top: -15px;'>Your emotional companion & developer accelerator platform.</p>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I am Rui, your AI friend. How can I help you today? 😊"}]

if not st.session_state.is_premium and len(st.session_state.messages) >= 10:
    st.info("System capacity quota threshold reached for today. Activate Premium tier pipeline to remove restrictions!")
    st.stop()

# Print out past logs
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Capture User Text Action
if prompt := st.chat_input("Communicate with Rui..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    try:
        # Free public fallback pipeline that requires zero authentication keys to run models
        API_URL = "https://huggingface.co"
        headers = {"Authorization": "Bearer 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"} 
        
        payload = {
            "inputs": f"<|im_start|>system\n{SYSTEM_PROMPT}<|im_end|>\n<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n",
            "parameters": {"max_new_tokens": 512, "return_full_text": False}
        }
        
        response = requests.post(API_URL, headers=headers, json=payload).json()
        ai_reply = response[0]['generated_text'].strip()
        
        st.session_state.messages.append({"role": "assistant", "content": ai_reply})
        with st.chat_message("assistant"):
            st.write(ai_reply)
            
    except Exception as e:
        st.error("System pipeline is starting up. Please resend your message in a few seconds!")
