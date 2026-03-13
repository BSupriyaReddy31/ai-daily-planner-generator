import streamlit as st
from google import genai
from groq import Groq
import os

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="AI Daily Architect", page_icon="⚡", layout="centered")

# --- 2. LOAD SECRETS ---
# Ensure you add both GEMINI_API_KEY and GROQ_API_KEY to Streamlit Secrets
GEMINI_KEY = st.secrets.get("GEMINI_API_KEY")
GROQ_KEY = st.secrets.get("GROQ_API_KEY")

# --- 3. UI STYLING (Gemini Modern Light) ---
st.markdown("""
    <style>
    .stApp { background-color: #F0F4F9; color: #1F1F1F; }
    [data-testid="stSidebar"] { background-color: #E9EEF6 !important; }
    .stTextArea textarea { background-color: #FFFFFF !important; border-radius: 15px !important; }
    .stButton>button {
        background-color: #0B57D0; color: white; border-radius: 100px;
        width: 100%; border: none; font-weight: bold; height: 3em;
    }
    .task-card {
        background-color: #FFFFFF; padding: 20px; border-radius: 15px;
        border: 1px solid #DDE3EA; box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. APP INTERFACE ---
st.title("⚡ AI Daily Architect")
st.write("Intelligent scheduling with multi-model backup.")

with st.sidebar:
    st.image("https://www.gstatic.com/lamda/images/gemini_sparkle_v002_d4735304ef62337744f77.svg", width=40)
    energy = st.select_slider("Energy Level", options=["Low", "Medium", "High"])
    st.divider()
    if GEMINI_KEY and GROQ_KEY:
        st.success("✅ Systems Ready")
    else:
        st.warning("⚠️ Some API keys are missing in Secrets.")

user_prompt = st.text_area("What are your tasks?", placeholder="e.g. OpenCV project, Gym at 6 PM...", height=150, label_visibility="collapsed")

# --- 5. DUAL-ENGINE GENERATION ---
if st.button("Generate My Plan"):
    if not user_prompt:
        st.warning("Please enter your tasks first!")
    else:
        with st.spinner("✨ Architecting your day..."):
            success = False
            
            # --- TRY GEMINI FIRST ---
            if GEMINI_KEY:
                try:
                    client = genai.Client(api_key=GEMINI_KEY)
                    response = client.models.generate_content(
                        model="gemini-1.5-flash", 
                        contents=f"Tasks: {user_prompt}. Energy: {energy}. Create a time-blocked schedule."
                    )
                    output = response.text
                    engine_used = "Gemini 1.5 Flash"
                    success = True
                except Exception as e:
                    if "429" in str(e):
                        st.info("🔄 Gemini is busy... switching to Backup Engine (Groq).")
                    else:
                        st.error(f"Gemini Error: {e}")

            # --- FALLBACK TO GROQ ---
            if not success and GROQ_KEY:
                try:
                    groq_client = Groq(api_key=GROQ_KEY)
                    chat_completion = groq_client.chat.completions.create(
                        messages=[{"role": "user", "content": f"Create a daily schedule for: {user_prompt}. Energy: {energy}"}],
                        model="llama-3.3-70b-versatile",
                    )
                    output = chat_completion.choices[0].message.content
                    engine_used = "Llama 3.3 (via Groq)"
                    success = True
                except Exception as e:
                    st.error(f"Backup Engine failed too: {e}")

            # --- DISPLAY RESULT ---
            if success:
                st.markdown(f"### 📅 Your Blueprint (via {engine_used})")
                st.markdown(f'<div class="task-card">{output}</div>', unsafe_allow_html=True)
                st.balloons()

st.markdown("---")
st.caption("Developed by Supriya Reddy")
