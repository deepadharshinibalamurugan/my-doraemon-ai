import streamlit as st
from google import genai

# --- 1. SETTINGS & ICONS ---
st.set_page_config(page_title="Doraemon AI", page_icon="🐱")

# These URLs are direct PNG links that work in Streamlit Cloud
DORAEMON_IMG = "https://cdn-icons-png.flaticon.com/512/281/281031.png"
NOBITA_IMG = "https://cdn-icons-png.flaticon.com/512/4392/4392525.png"

# --- 2. THEME-AWARE STYLING ---
st.markdown("""
    <style>
    /* Light Mode Background Only */
    [data-theme="light"] .stApp { background-color: #f0f8ff !important; }
    
    /* Text color adjusts automatically to theme */
    .stMarkdown p { color: var(--text-color) !important; }
    
    /* Doraemon Blue Title */
    h1 { color: #2986cc !important; text-align: center; }
    
    /* Custom Chat Bubbles */
    .stChatMessage { border-radius: 20px; border: 1px solid #2986cc22; }
    </style>
    """, unsafe_allow_html=True)

st.title("🐱 Doraemon's 4D Study Pocket")

# --- 3. 4D POCKET SIDEBAR (GADGETS) ---
with st.sidebar:
    st.image(DORAEMON_IMG, width=100)
    st.header("🧰 4D Pocket")
    gadget = st.radio(
        "Choose a Gadget:",
        ["Standard Mode", "Computer Pencil ✏️", "Translation Gummy 🍬"],
        help="Switching gadgets changes how Doraemon helps you!"
    )
    
    if st.button("Clear Memory 🧹"):
        st.session_state.messages = []
        st.rerun()

# Logic for Gadgets
if gadget == "Computer Pencil ✏️":
    system_prompt = "You are Doraemon. You are now using the Computer Pencil! Solve math/science problems step-by-step for Nobita."
elif gadget == "Translation Gummy 🍬":
    system_prompt = "You are Doraemon. You just gave Nobita a Translation Gummy! Translate everything to Japanese."
else:
    system_prompt = "You are the helpful robot cat Doraemon. Be encouraging and use gadgets to help Nobita study."

# --- 4. API & CHAT ---
try:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except:
    st.error("🔑 API Key Missing in Secrets!")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history with avatars
for msg in st.session_state.messages:
    avatar = NOBITA_IMG if msg["role"] == "user" else DORAEMON_IMG
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# User Input
if prompt := st.chat_input("Ask Doraemon anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=NOBITA_IMG):
        st.markdown(prompt)

    # Doraemon Response
    with st.chat_message("assistant", avatar=DORAEMON_IMG):
        # We use st.status for a nice 2026 loading effect
        with st.status("Searching 4D Pocket...", expanded=False):
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash", 
                    contents=f"{system_prompt}. User says: {prompt}"
                )
                output = response.text
            except:
                output = "Doraemon's pocket is jammed! Check your API connection."
        
        st.markdown(output)
        st.session_state.messages.append({"role": "assistant", "content": output})
        
        # Surprise: If user says 'thank you', show balloons!
        if "thank" in prompt.lower() or "arigato" in prompt.lower():
            st.balloons()