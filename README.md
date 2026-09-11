 AI Student Stress Prediction & Medical Recommendation System

An end-to-end machine learning and full-stack web application designed to monitor, predict, and mitigate stress levels among students. The system collects comprehensive behavioral, academic, and psychological survey data from over 1,000 students, classifies their stress state into distinct categories using a trained Logistic Regression model, and delivers personalized, actionable medical and lifestyle recommendations.

---

## 🚀 Key Features

* **Student Stress Assessment Questionnaire:** Multi-factor questionnaire assessing academic workload, sleep patterns, social interactions, and physical health metrics.
* **Multi-Class Stress Classification:** Utilizes a robust **Logistic Regression** machine learning model to categorize student stress into four distinct levels:
  * 🟢 **Normal**
  * 🟡 **Low Stress**
  * 🟠 **Mid Stress**
  * 🔴 **High Stress**
* **Personalized Recommendations:** Generates targeted medical, psychological, and lifestyle guidance based on the student's predicted stress category.
* **Secure Authentication:** Robust user signup and login system secured via JSON Web Tokens (JWT) for authentication and role management.
* **Interactive Web Dashboard:** Clean, responsive user interface built for real-time assessments and historical stress tracking.

---

## 🛠️ Technology Stack

### Frontend
* **Streamlit**: Provides a fast, interactive, and Python-native web user interface for student surveys, score visualizations, and recommendation dashboards.

### Backend & API
* **Python**: Core programming language for business logic and data processing.
* **FastAPI**: High-performance asynchronous web framework powering RESTful API endpoints.
* **TensorFlow / Keras**: Utilized for supplementary data preprocessing pipelines and feature extraction.
* **JWT (JSON Web Tokens)**: Secures authentication endpoints for user login, session management, and authorization.

### Machine Learning & Data Science
* **Scikit-Learn**: Implements the core **Logistic Regression** classifier alongside preprocessing and evaluation pipelines.
* **Pandas & NumPy**: Data cleaning, wrangling, and exploratory data analysis over the 1,000+ student dataset.

---

## 📂 Project Architecture

```text
ai-student-stress-prediction/
│
├── backend/
│   ├── app/
│   │   ├── api/              # FastAPI routers (auth, predict, recommendations)
│   │   ├── core/             # JWT security, configuration, database settings
│   │   ├── models/           # SQLAlchemy database models & Pydantic schemas
│   │   └── ml/               # Trained Logistic Regression model & inference scripts
│   ├── data/                 # Student dataset (1000+ records)
│   ├── requirements.txt      # Python backend dependencies
│   └── main.py               # FastAPI application entry point
│
├── frontend/
│   ├── app.py                # Streamlit user interface entry point
│   ├── auth.py               # Authentication & session state management
│   ├── components/           # Reusable UI widgets & charts
│   └── requirements.txt      # Streamlit frontend dependencies
│
└── README.md
```

---

## 📊 Dataset Overview

The underlying dataset comprises survey responses from **1,000+ students**, capturing key determinants of academic stress:
* **Academic Factors:** Daily study hours, assignment pressures, exam anxiety, and perceived academic performance.
* **Lifestyle Factors:** Average hours of sleep, physical activity frequency, and screen time.
* **Psychological & Environmental Factors:** Social support systems, financial concerns, and living conditions.

---

## ⚙️ Installation & Setup

### Prerequisites
* Python 3.10 or higher
* Pip & Virtualenv

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/ai-student-stress-prediction.git
cd ai-student-stress-prediction
```

### 2. Backend Setup (FastAPI)
```bash
cd backend
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

Run the FastAPI development server:
```bash
uvicorn main:app --reload --port 8000
```
*API documentation will be available at `http://localhost:8000/docs`.*

### 3. Frontend Setup (Streamlit)
Open a new terminal window/tab:
```bash
cd frontend
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

Run the Streamlit application:
```bash
streamlit run app.py
```
*Access the web interface at `http://localhost:8501`.*

---

## 🔒 Authentication Flow (JWT)

1. **Signup / Registration**: Users register with credentials; passwords are securely hashed before storage.
2. **Login**: Authenticated users receive a signed **JWT token** containing session claims.
3. **Authorized Requests**: Subsequent requests from the frontend pass the JWT token in the HTTP `Authorization: Bearer <token>` header to access prediction history and secure endpoints.

---

## 🤖 Model Performance & Evaluation

The Logistic Regression classifier was chosen for its interpretability, stability, and strong baseline performance on multi-class categorical surveys. 
* **Evaluation Metrics:** Accuracy, Precision, Recall, and F1-Score across all four stress categories (Normal, Low, Mid, High).
* **Validation:** 5-fold cross-validation performed on the 1,000+ student dataset to prevent overfitting.
