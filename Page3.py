import streamlit as st
import numpy as np
from PIL import Image
from datetime import datetime
import joblib
from db import history_col
from Auth import verify_token

# ------------------------- LOAD AI MODEL -------------------------
@st.cache_resource
def load_model():
    return joblib.load("pages/recommendation_model.pkl")
ai_model = load_model()
# ------------------------- UI STYLING -------------------------
st.markdown("""
    <style>
    .main-title {
        font-size: 34px !important;
        font-weight: 700;
        text-align: center;
        color: White;
        margin-bottom: 20px;
    }
    .question-box {
        padding: 20px;
        border-radius: 12px;
        background-color: #f7f9fc;
        border: 1px solid #e0e6ed;
        margin-bottom: 20px;
        color: black !important;
        font-size: 18px;
        font-weight: 600;
    }
    .result-box {
        padding: 20px;
        border-radius: 12px;
        background-color: black;
        border: 1px solid #90CAF9;
        margin-bottom: 20px;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# ------------------------- AUTO LOGIN -------------------------
if "token" in st.session_state and not st.session_state.get("auth", False):
    username_from_token = verify_token(st.session_state.token)
    if username_from_token:
        st.session_state.username = username_from_token
        st.session_state.auth = True

# ------------------------- ACCESS CONTROL -------------------------
if not st.session_state.get("auth", False):
    st.error("Access Denied! Please login first.")
    st.stop()

# ------------------------- HEADER -------------------------
st.title(f"Welcome, {st.session_state.username} 👋")
image = Image.open("image/mental03.png")
st.image(image.resize((560, 280)), use_container_width=True)

# ------------------------- MAPPINGS -------------------------
pss_map = {'Never':0,'Almost Never':1,'Sometimes':2,'Fairly Often':3,'Very Often':4}
gad_map = {'Not at all':0,'Several days':1,'More than half the days':2,'Nearly every day':3}

pss_column = [
    'Q.1 In the last month, how often have you been upset because of something that happened unexpectedly?',
    'Q.2 In the last month, how often have you felt that you were unable to control the important things in your life?',
    'Q.3 In the last month, how often have you felt nervous and stressed?',
    'Q.4 In the last month, how often have you felt confident about your ability to handle your personal problems?',
    'Q.5 In the last month, how often have you felt that things were going your way?',
    'Q.6 In the last month, how often have you found that you could not cope with all the things that you had to do?',
    'Q.7 In the last month, how often have you been able to control irritations in your life?',
    'Q.8 In the last month, how often have you felt that you were on top of things?',
    'Q.9 In the last month, how often have you been angered because of things that happened that were outside of your control?',
    'Q.10 In the last month, how often have you felt difficulties were piling up so high that you could not overcome them?'
]

gad_column = [
    'Q1 Feeling nervous, anxious, or on edge',
    'Q2 Not being able to stop worrying',
    'Q3 Worrying too much about different things',
    'Q4 Trouble relaxing',
    'Q5 Restless or cannot sit still',
    'Q6 Becoming easily annoyed or irritable',
    'Q7 Feeling afraid as if something awful might happen'
]

# ------------------------- SESSION STATE -------------------------
if "pss_index" not in st.session_state:
    st.session_state.pss_index = 0
if "gad_index" not in st.session_state:
    st.session_state.gad_index = 0
if "pss_answers" not in st.session_state:
    st.session_state.pss_answers = []
if "gad_answers" not in st.session_state:
    st.session_state.gad_answers = []
if "stage" not in st.session_state:
    st.session_state.stage = "pss"

# ------------------------- NEXT QUESTION -------------------------
def next_question(answer):
    if st.session_state.stage == "pss":
        st.session_state.pss_answers.append(pss_map[answer])
        st.session_state.pss_index += 1
        if st.session_state.pss_index >= len(pss_column):
            st.session_state.stage = "gad"
    else:
        st.session_state.gad_answers.append(gad_map[answer])
        st.session_state.gad_index += 1
        if st.session_state.gad_index >= len(gad_column):
            st.session_state.stage = "result"

# ------------------------- QUESTIONS -------------------------
if st.session_state.stage == "pss":
    st.progress((st.session_state.pss_index + 1) / len(pss_column))
    st.markdown(f"<div class='question-box'>{pss_column[st.session_state.pss_index]}</div>", unsafe_allow_html=True)
    ans = st.selectbox("Select your answer:", list(pss_map.keys()))
    st.button("Next ➜", on_click=lambda: (next_question(ans), st.rerun()))

elif st.session_state.stage == "gad":
    st.progress((st.session_state.gad_index + 1) / len(gad_column))
    st.markdown(f"<div class='question-box'>{gad_column[st.session_state.gad_index]}</div>", unsafe_allow_html=True)
    ans = st.selectbox("Select your answer:", list(gad_map.keys()))
    st.button("Next ➜", on_click=lambda: (next_question(ans), st.rerun()))

# ------------------------- RESULTS -------------------------
else:
    reverse_idx = [3,4,6,7]
    stress_scores = st.session_state.pss_answers.copy()
    for i in reverse_idx:
        stress_scores[i] = 4 - stress_scores[i]

    gad_scores = st.session_state.gad_answers

    stress_total = sum(stress_scores)
    anxiety_total = sum(gad_scores)

    stress_level = "Low" if stress_total <= 13 else "Moderate" if stress_total <= 19 else "High"
    anxiety_level = "Minimal" if anxiety_total <= 4 else "Mild" if anxiety_total <= 9 else "Moderate" if anxiety_total <= 14 else "Severe"

    # ---------------- AI PREDICTION (FIXED) ----------------
    combined_scores = stress_scores + gad_scores
    ai_input = np.array(
        combined_scores[:ai_model.n_features_in_]
    ).reshape(1, -1)

    ai_recommendation = ai_model.predict(ai_input)[0]

    # ---------------- DISPLAY ----------------
    st.markdown("<h3>📊 Your Assessment Result</h3>", unsafe_allow_html=True)
    st.markdown(f"<div class='result-box'><b>🧘 Stress Level:</b> {stress_level}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='result-box'><b>😟 Anxiety Level:</b> {anxiety_level}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='result-box'><b>🤖 AI Recommendation:</b><br>💡 {ai_recommendation}</div>", unsafe_allow_html=True)

    history_col.insert_one({
        "username": st.session_state.username,
        "stress_level": stress_level,
        "stress_score": stress_total,
        "anxiety_level": anxiety_level,
        "anxiety_score": anxiety_total,
        "ai_recommendation": ai_recommendation,
        "timestamp": datetime.now()
    })

    st.markdown("### 🕒 Your Past Assessments")
    history = list(history_col.find({"username": st.session_state.username}).sort("timestamp", -1))
    for h in history:
        st.markdown(
            f"- {h['timestamp'].strftime('%Y-%m-%d %H:%M')} | "
            f"Stress: {h['stress_level']} ({h['stress_score']}) | "
            f"Anxiety: {h['anxiety_level']} ({h['anxiety_score']}) | "
            f"AI: {h.get('ai_recommendation','')}"
        )

    if st.button("🔄 Restart Assessment"):
        for k in ["pss_index","gad_index","pss_answers","gad_answers","stage"]:
            del st.session_state[k]
        st.rerun()
