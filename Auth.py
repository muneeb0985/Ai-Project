import bcrypt
import jwt
from datetime import datetime, timedelta

SECRET_KEY = "MENTAL_AI_SECRET_KEY"

# ---------------- Password Hashing ----------------
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def verify_password(password, hashed):
    if isinstance(hashed, str):  # decode if stored as string
        hashed = hashed.encode()
    return bcrypt.checkpw(password.encode(), hashed)

# ---------------- Token Generation ----------------
def generate_token(username):
    payload = {
        "user": username,
        "exp": datetime.utcnow() + timedelta(hours=2)  # token valid for 2 hours
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

# ---------------- Token Verification ----------------
def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["user"]  # return username if valid
    except jwt.ExpiredSignatureError:
        return None  # token expired
    except jwt.InvalidTokenError:
        return None  # invalid token
