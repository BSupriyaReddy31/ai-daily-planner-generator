import streamlit as st
# Switching to the newer recommended SDK
from google import genai 
from datetime import datetime

# --- GEMINI SETUP ---
# Make sure to add "google-genai" to your requirements.txt
client = genai.Client(api_key="YOUR_GEMINI_API_KEY_HERE")

# --- UI COLORS (FIXED) ---
st.set_page_config(page_title="Gemini Plan Generator", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #F0F4F9; color: #1F1F1F; }
    section[data-testid="stSidebar"] { background-color: #E9EEF6 !important; }
    
    .stTextArea textarea {
        background-color: #FFFFFF !important;
        border-radius: 24px !important;
        border: 1px solid #DDE3EA !important;
        padding: 15px !important;
    }

    .task-card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 20px;
        margin-bottom: 12px;
        border: 1px solid #DDE3EA;
    }

    .stButton>button {
        background-color: #0B57D0;
        color: white;
        border-radius: 50px;
        padding: 10px 25px;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True) # FIXED: Changed from unsafe_allow_index to unsafe_allow_html

# --- APP UI ---
st.markdown('<h1 style="font-family: Google Sans; font-weight: 500;">AI Daily Architect</h1>', unsafe_allow_html=True)

with st.sidebar:
    st.title("Settings")
    energy = st.select_slider("Energy Level", options=["Low", "Medium", "High"])

user_prompt = st.text_area("", placeholder="What's on your list today?")

if st.button("Generate Plan"):
    if user_prompt:
        with st.spinner("Gemini is thinking..."):
            # New SDK syntax
            response = client.models.generate_content(
                model="gemini-2.0-flash", 
                contents=f"Create a time-blocked schedule for: {user_prompt}. Energy: {energy}"
            )
            
            st.markdown("### ✨ Your Generated Day")
            st.write(response.text)
    else:
        st.warning("Please enter some tasks!")
