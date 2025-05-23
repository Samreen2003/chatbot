import google.generativeai as genai
import streamlit as st

# API Configuration
GOOGLE_API_KEY = "AIzaSyCwLyqVhe-16lDTggXHgzrya6Bc5s8wecc"
genai.configure(api_key=GOOGLE_API_KEY)

# Model Initialization
model = genai.GenerativeModel('gemini-1.5-flash')  # You can also try 'gemini-pro' if needed

# Function to get response from the model
def getResponseFromModel(user_input):
    if not isinstance(user_input, str) or not user_input.strip():
        raise ValueError("Prompt must be a non-empty string.")
    try:
        response = model.generate_content(user_input)
        return response.text
    except Exception as e:
        st.error("❌ Failed to get response from Gemini API.")
        st.error(f"Details: {e}")
        return "Sorry, something went wrong. Please try again later."

# App title and description
st.set_page_config(page_title="AI Chat with Gemini", page_icon="🤖")
st.title("🤖 AI Chatbot")
st.subheader("Welcome, Samreen")
st.write("This chatbot is powered by Gemini API")

# Session state to store chat history
if "history" not in st.session_state:
    st.session_state["history"] = []

# Custom CSS for chat bubbles with background colors and adaptive text colors
st.markdown("""
    <style>
    .user-bubble, .bot-bubble {
        padding: 12px 16px;
        border-radius: 20px;
        margin-bottom: 10px;
        max-width: 80%;
        backdrop-filter: blur(12px);
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        font-family: 'Segoe UI', sans-serif;
    }
    .user-bubble {
        margin-left: 0;
        color: #000;
        background: rgba(220, 248, 198, 0.6);
    }
    .bot-bubble {
        margin-left: auto;
        color: #fff;
        background: rgba(59, 59, 59, 0.7);
    }
    </style>
""", unsafe_allow_html=True)


# Input form for user prompt
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your message here...", max_chars=2000, placeholder="Ask anything!")
    submit_button = st.form_submit_button("Send")

    if submit_button:
        if user_input.strip():
            response = getResponseFromModel(user_input)
            st.session_state["history"].append((user_input, response))
            st.experimental_rerun()
        else:
            st.warning("⚠️ Please enter a valid message.")

# Add a button to clear chat history
if st.session_state["history"]:
    if st.button("🧹 Clear Chat"):
        st.session_state["history"] = []
        st.experimental_rerun()

# Display chat history with styled bubbles
if st.session_state["history"]:
    for user_message, bot_response in st.session_state["history"]:
        st.markdown(f'<div class="user-bubble"><strong>You:</strong> {user_message}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="bot-bubble"><strong>Bot:</strong> {bot_response}</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
