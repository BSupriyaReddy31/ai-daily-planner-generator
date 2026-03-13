import streamlit as st
from google import genai
import os

# --- 1. SET UP THE PAGE ---
st.set_page_config(page_title="Gemini Plan Generator", layout="centered")

# --- 2. LOAD API KEY FROM SECRETS ---
# This is the correct way to handle keys on Streamlit Cloud
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception:
    API_KEY = None

# --- 3. INITIALIZE GEMINI CLIENT ---
if API_KEY:
    # Using the latest google-genai SDK syntax
    client = genai.Client(api_key=API_KEY)
else:
    st.error("🔑 Missing API Key! Go to Streamlit Settings > Secrets and add GEMINI_API_KEY.")
    st.stop()

# --- 4. GEMINI-STYLE UI DESIGN ---
st.markdown("""
    <style>
    .stApp { background-color: #F0F4F9; color: #1F1F1F; }
    
    section[data-testid="stSidebar"] { background-color: #E9EEF6 !important; }

    .stTextArea textarea {
        background-color: #FFFFFF !important;
        border-radius: 20px !important;
        border: 1px solid #DDE3EA !important;
    }

    .stButton>button {
        background-color: #0B57D0;
        color: white;
        border-radius: 50px;
        padding: 10px 25px;
        border: none;
        width: 100%;
    }

    .task-card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 20px;
        margin-top: 20px;
        border: 1px solid #DDE3EA;
        color: #1F1F1F;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 5. APP INTERFACE ---
st.title("⚡ AI Daily Architect")
st.write("Organize your day using Gemini 2.0 Flash")

with st.sidebar:
    st.header("Settings")
    energy = st.select_slider("Energy Level", options=["Low", "Medium", "High"])

user_prompt = st.text_area("What are your tasks today?", placeholder="e.g., OpenCV project for 2 hours, Gym at 6 PM...")

# --- 6. GENERATION LOGIC ---
if st.button("Generate My Schedule"):
    if user_prompt:
        with st.spinner("✨ Gemini is architecting your day..."):
            try:
                # Using 2.0-flash as it is the current stable high-speed model
                response = client.models.generate_content(
                    model="gemini-2.0-flash", 
                    contents=f"User Tasks: {user_prompt}. Energy Level: {energy}. Create a time-blocked daily schedule."
                )
                
                # Displaying the result in a clean card
                st.markdown(f'<div class="task-card">{response.text}</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter some tasks first!")
