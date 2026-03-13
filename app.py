import streamlit as st
import google.generativeai as genai
from datetime import datetime

# --- GEMINI SETUP ---
# On GitHub/Local: Store your API key in a .env file or Streamlit Secrets
API_KEY = "YOUR_GEMINI_API_KEY_HERE" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- REPLICATING THE UI COLORS FROM YOUR IMAGE ---
st.set_page_config(page_title="Gemini Plan Generator", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #F0F4F9; color: #1F1F1F; }
    section[data-testid="stSidebar"] { background-color: #E9EEF6 !important; }
    
    /* Chat-like Text Area */
    .stTextArea textarea {
        background-color: #FFFFFF !important;
        border-radius: 24px !important;
        border: 1px solid #DDE3EA !important;
        padding: 15px !important;
    }

    /* Modern Task Cards */
    .task-card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 20px;
        margin-bottom: 12px;
        border: 1px solid #DDE3EA;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }

    /* Google-style Pill Button */
    .stButton>button {
        background-color: #0B57D0;
        color: white;
        border-radius: 50px;
        padding: 10px 25px;
        border: none;
    }
    </style>
    """, unsafe_allow_index=True)

# --- APP UI ---
st.markdown('<h1 style="font-family: Google Sans; font-weight: 500;">AI Daily Architect</h1>', unsafe_allow_index=True)

with st.sidebar:
    st.title("Settings")
    energy = st.select_slider("Energy Level", options=["Low", "Medium", "High"])
    st.info("This project uses Gemini 2.5 Flash to optimize your schedule.")

user_prompt = st.text_area("", placeholder="List your tasks, e.g., 'Work on Blockchain for 2 hours, Gym at 5 PM, Finish OpenCV script'...")

if st.button("Generate Plan"):
    if user_prompt:
        with st.spinner("Gemini is thinking..."):
            # Crafting the AI Instruction
            full_prompt = f"""
            Act as a productivity coach. Create a time-blocked daily schedule based on these tasks: {user_prompt}. 
            The user has {energy} energy levels. 
            Format each task clearly with a Time, Task Title, and a brief Reason why it's scheduled then.
            """
            
            response = model.generate_content(full_prompt)
            
            # Displaying the AI Response in clean cards
            st.markdown("### ✨ Your Generated Day")
            st.markdown(response.text) # You can further parse this for card styling!
    else:
        st.warning("Please enter your tasks first.")
