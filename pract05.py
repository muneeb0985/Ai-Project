import streamlit as st
from db import users_col
from Auth import verify_password, generate_token, verify_token
from PIL import Image

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Mental Wellbeing AI", layout="centered")

# ------------------ SESSION INIT ------------------
if "auth" not in st.session_state:
    st.session_state.auth = False

# ------------------ AUTO-LOGIN ------------------
if "token" in st.session_state:
    username_from_token = verify_token(st.session_state.token)
    if username_from_token:
        st.session_state.username = username_from_token
        st.session_state.auth = True
        st.success(f"Welcome back, {username_from_token}!")
        st.button("Go to Assessment", on_click=lambda: st.switch_page("pages/Page3.py"))

# ------------------ STYLING (UI ONLY) ------------------
st.markdown("""
<style>
body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
.auth-container { max-width: 450px; margin: 80px auto; padding: 50px 40px 40px 40px; border-radius: 20px; background: transparent; box-shadow:none; }
.auth-title { text-align:center; font-size:34px; font-weight:700; margin-bottom:6px; color:white; }
.auth-subtitle { text-align:center; color:#e0e0e0; margin-bottom:30px; font-size:16px; }
.stButton>button { width:100%; border-radius:12px; padding:14px; font-size:16px; background:#667eea; color:white; font-weight:600; border:none; cursor:pointer; }
.stButton>button:hover { background:#5a67d8; }
.auth-image { display:block; margin-left:auto; margin-right:auto; margin-bottom:25px; width:300px; height:160px; object-fit:contain; }
.sign-up-link { text-align:center; color:white; font-weight:600; cursor:pointer; font-size:15px; }
.sign-up-link:hover { text-decoration:underline; }
</style>
""", unsafe_allow_html=True)

# ------------------ UI ------------------
st.markdown("<div class='auth-container'>", unsafe_allow_html=True)

# --- Image (CENTERED) ---
image = Image.open("image/mental02.png")
image = image.resize((300, 160))
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    st.write("")
with col2:
    st.image(image)
with col3:
    st.write("")

# --- Title & Subtitle ---
st.markdown("<div class='auth-title'>🧠 Mental Wellbeing AI</div>", unsafe_allow_html=True)
st.markdown("<div class='auth-subtitle'>Sign in to continue</div>", unsafe_allow_html=True)

# --- Login Form ---
username = st.text_input("Username", placeholder="Enter your username")
password = st.text_input("Password", type="password", placeholder="Enter your password")
username = username.strip().lower()

# --- Buttons Side by Side ---
col_login, col_signup = st.columns(2)

with col_login:
    if st.button("Login"):
        if not username or not password:
            st.error("Username and password required")
        else:
            user = users_col.find_one({"username": username})
            if user and verify_password(password, user["password"]):
                token = generate_token(username)
                st.session_state.auth = True
                st.session_state.username = username
                st.session_state.token = token
                users_col.update_one({"username": username}, {"$set": {"token": token}})
                st.success("Login successful")
                st.switch_page("pages/Page3.py")  # Go to assessment page
            else:
                st.error("Invalid credentials")

with col_signup:
    if st.button("New user? Sign up"):
        st.switch_page("pages/Page1.py")  # Navigate to signup page

st.markdown("</div>", unsafe_allow_html=True)
