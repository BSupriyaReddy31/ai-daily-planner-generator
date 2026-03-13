import streamlit as st
from google import genai
import os

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="AI Daily Architect", page_icon="⚡", layout="centered")

# --- 2. THE "SECRET" CHECK ---
# We use a try-except to handle cases where the secret isn't set yet
try:
    if "GEMINI_API_KEY" in st.secrets:
        API_KEY = st.secrets["GEMINI_API_KEY"]
    else:
        API_KEY = None
except Exception:
    API_KEY = None

# --- 3. UI STYLING (Gemini Modern Light) ---
st.markdown("""
    <style>
    .stApp { background-color: #F0F4F9; color: #1F1F1F; }
    [data-testid="stSidebar"] { background-color: #E9EEF6 !important; }
    .stTextArea textarea {
        background-color: #FFFFFF !important;
        border-radius: 15px !important;
        border: 1px solid #DDE3EA !important;
    }
    .stButton>button {
        background-color: #0B57D0;
        color: white;
        border-radius: 100px;
        width: 100%;
        border: none;
        height: 3em;
        font-weight: bold;
    }
    .task-card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #DDE3EA;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. MAIN INTERFACE ---
st.title("⚡ AI Daily Architect")
st.write("Organize your day with Gemini 2.0 Flash")

with st.sidebar:
    st.image("https://www.gstatic.com/lamda/images/gemini_sparkle_v002_d4735304ef62337744f77.svg", width=40)
    energy = st.select_slider("Energy Level", options=["Low", "Medium", "High"])
    st.divider()
    st.caption("Final Year Project • Powered by Google")

# Fixed the 'label' warning from your logs
user_prompt = st.text_area(
    "Enter your tasks:", 
    placeholder="e.g., OpenCV project for 2 hours, Lunch with mom, Gym at 6 PM...",
    label_visibility="collapsed",
    height=150
)

# --- 5. EXECUTION LOGIC ---
if st.button("Generate My Plan"):
    if not API_KEY:
        st.error("❌ **API Key Missing!** Please go to Streamlit Cloud Settings > Secrets and add: GEMINI_API_KEY = 'your_key'")
    elif not user_prompt:
        st.warning("Please enter some tasks first!")
    else:
        with st.spinner("✨ Architecting your day..."):
            try:
                client = genai.Client(api_key=API_KEY)
                response = client.models.generate_content(
                    model="gemini-2.0-flash", 
                    contents=f"User Tasks: {user_prompt}. Energy: {energy}. Create a clear, time-blocked daily schedule."
                )
                
                st.markdown("### 📅 Your Optimized Blueprint")
                st.markdown(f'<div class="task-card">{response.text}</div>', unsafe_allow_html=True)
                st.balloons()

            except Exception as e:
                # If the API key is invalid, it will show this clearly
                if "API_KEY_INVALID" in str(e):
                    st.error("❌ **Invalid API Key!** The key in your Secrets is not recognized by Google. Please generate a new one at Google AI Studio.")
                else:
                    st.error(f"⚠️ An error occurred: {e}")

st.markdown("---")
st.caption("Created by Supriya Reddy")
