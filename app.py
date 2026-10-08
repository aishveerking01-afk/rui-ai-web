import streamlit as st
import google.generativeai as genai

# 1. Setup Page Layout and Styles
st.set_page_config(page_title="Rui AI", layout="centered")

# Dark UI Styling to match your original theme
st.markdown("""
    <style>
    .stApp { background-color: #080a1c; color: #eaedfa; }
    .stChatMessage { background-color: #131632; border-radius: 10px; padding: 10px; margin: 10px 0; }
    </style>
""", unsafe_allow_html=True)

# 2. Configure the AI System Prompt (from your original script)
SYSTEM_PROMPT = (
    "You are Rui, a warm, caring and expressive AI friend and helper. "
    "Notice how the user feels from their words and answer with matching emotion. "
    "Show feelings naturally and use an emoji now and then. "
    "Always reply in the same language and script the user writes in. "
    "If the user writes Punjabi, reply in Punjabi using Gurmukhi script."
)

# Configured for standard v1 production endpoint
genai.configure(api_key="AQ.Ab8RN6LCLeZNhwaMIoINB6IIKwFWWYGAiOBKs96ELy4XM_lL7Q")

# 3. Handle User Accounts & Paywall UI
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "is_premium" not in st.session_state:
    st.session_state.is_premium = False

if not st.session_state.logged_in:
    st.title("Welcome to Rui AI Friend ✨")
    email = st.text_input("Enter your Email to Log In:")
    if st.button("Log In / Sign Up"):
        if email:
            st.session_state.logged_in = True
            st.session_state.user_email = email
            st.rerun()
    st.stop()

# 4. Premium Paywall Check
st.sidebar.title(f"👤 {st.session_state.user_email}")
if not st.session_state.is_premium:
    st.sidebar.warning("You are on the Free Plan (10 chats/day max)")
    st.sidebar.markdown("[💎 Upgrade to Premium for Unlimited Chats](https://stripe.com)")
    
    # Simple manual bypass button for you to test during development
    if st.sidebar.button("Test: Simulate Successful Payment"):
        st.session_state.is_premium = True
        st.rerun()
else:
    st.sidebar.success("💎 Premium Active")

# 5. Core Chat Logic
st.title("Rui AI Companion")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I am Rui, your AI friend. How are you feeling today? 😊"}]

# Limit free users to 10 total history elements for demonstration
if not st.session_state.is_premium and len(st.session_state.messages) >= 10:
    st.info("You have reached your daily free chat limit. Please upgrade in the sidebar to continue talking to Rui!")
    st.stop()

# Display past messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Accept user input
if prompt := st.chat_input("Message Rui..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Updated to stable production version layout
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
        st.error(f"AI Error: {e}")
