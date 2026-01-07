import streamlit as st
from db import users_col
from Auth import hash_password
from PIL import Image

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Mental Wellbeing AI - Sign Up", layout="centered")

# ------------------ STYLING (UI ONLY) ------------------
st.markdown("""
<style>
/* Page background gradient */
body { 
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* Transparent container with shadow */
.auth-container { 
    max-width: 450px; 
    margin: 80px auto; 
    padding: 50px 40px 40px 40px; 
    border-radius: 20px; 
    box-shadow:0px 20px 40px rgba(0,0,0,0.25); 
    background: rgba(255,255,255,0.0); /* fully transparent */
    color: white;
}

/* Title & subtitle */
.auth-title { 
    text-align:center; 
    font-size:34px; 
    font-weight:700; 
    margin-bottom:6px; 
    color:white; 
}
.auth-subtitle { 
    text-align:center; 
    color:#e0e0e0; 
    margin-bottom:30px; 
    font-size:16px; 
}

/* Input fields */
.stTextInput>div>div>input {
    border-radius: 12px;
    padding: 12px;
    font-size: 16px;
}

/* Buttons styling */
.stButton>button { 
    border-radius:12px; 
    padding:14px; 
    font-size:16px; 
    background:#667eea; 
    color:white; 
    font-weight:600; 
    border:none; 
    cursor:pointer; 
}
.stButton>button:hover { 
    background:#5a67d8; 
}

/* Image styling */
.auth-image { 
    display:block; 
    margin-left:auto; 
    margin-right:auto; 
    margin-bottom:25px; 
    width:300px; 
    height:160px; 
    object-fit:contain; 
}

/* Inline buttons container */
.button-row {
    display: flex;
    justify-content: space-between;
    gap: 10px;
    margin-top: 15px;
}
.button-row .stButton>button {
    flex: 1;
}
</style>
""", unsafe_allow_html=True)

# ------------------ UI ------------------
st.markdown("<div class='auth-container'>", unsafe_allow_html=True)

# --- Image ---
image = Image.open("image/mental02.png")
image = image.resize((300, 160))
st.image(image)

# --- Title & Subtitle ---
st.markdown("<div class='auth-title'>🧠 Mental Wellbeing AI</div>", unsafe_allow_html=True)
st.markdown("<div class='auth-subtitle'>Create a new account</div>", unsafe_allow_html=True)

# --- Sign-up Form ---
username = st.text_input("Username", placeholder="Enter your username")
password = st.text_input("Password", type="password", placeholder="Enter your password")
username = username.strip().lower()

# --- Inline Buttons ---
col1, col2 = st.columns([1,1])
with col1:
    if st.button("Create Account"):
        if not username or not password:
            st.error("Username and password required")
        elif users_col.find_one({"username": username}):
            st.error("Username already exists")
        else:
            users_col.insert_one({
                "username": username,
                "password": hash_password(password)
            })
            st.success("Account created successfully! Please login.")
            st.button("Go to Login", on_click=lambda: st.switch_page("pract05.py"))

with col2:
    if st.button("Already have an account? Login"):
        st.switch_page("pract05.py")

st.markdown("</div>", unsafe_allow_html=True)
