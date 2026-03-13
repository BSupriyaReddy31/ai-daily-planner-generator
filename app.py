import streamlit as st
from groq import Groq

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="AI Daily Architect", page_icon="⚡", layout="centered")

# --- 2. LOAD GROQ SECRET ---
# Ensure you have GROQ_API_KEY in your Streamlit Cloud Secrets
GROQ_KEY = st.secrets.get("GROQ_API_KEY")

# --- 3. UI STYLING (Modern Light Theme) ---
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
        color: #1F1F1F;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. APP INTERFACE ---
st.title("⚡ AI Daily Architect")
st.write("Fast, intelligent scheduling powered by Groq.")

with st.sidebar:
    st.image("https://www.gstatic.com/lamda/images/gemini_sparkle_v002_d4735304ef62337744f77.svg", width=40)
    energy = st.select_slider("Energy Level", options=["Low", "Medium", "High"])
    st.divider()
    if GROQ_KEY:
        st.success("✅ Groq Engine Ready")
    else:
        st.error("❌ Missing GROQ_API_KEY in Secrets")

user_prompt = st.text_area(
    "Enter your tasks:", 
    placeholder="e.g. OpenCV project, Gym at 6 PM, IEEE paper abstract...", 
    height=150, 
    label_visibility="collapsed"
)

# --- 5. GENERATION LOGIC ---
if st.button("Generate My Plan"):
    if not GROQ_KEY:
        st.error("Please add your Groq API Key to Streamlit Secrets.")
    elif not user_prompt:
        st.warning("Please enter your tasks first!")
    else:
        with st.spinner("✨ Architecting your day via Groq..."):
            try:
                client = Groq(api_key=GROQ_KEY)
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "system", 
                            "content": "You are a professional productivity coach. Create clear, time-blocked daily schedules based on user tasks and energy levels."
                        },
                        {
                            "role": "user", 
                            "content": f"Tasks: {user_prompt}. Energy: {energy}."
                        }
                    ],
                    model="llama-3.3-70b-versatile",
                )
                
                output = chat_completion.choices[0].message.content
                
                # Display Result
                st.markdown("### 📅 Your Optimized Blueprint")
                st.markdown(f'<div class="task-card">{output}</div>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Generation failed: {e}")

st.markdown("---")
st.caption("Developed by Supriya Reddy")
