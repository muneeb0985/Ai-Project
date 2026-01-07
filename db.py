from pymongo import MongoClient
# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
# Create / use database
db = client["mental_ai"]
# Collections
users_col = db["users"]
history_col = db["history"]
