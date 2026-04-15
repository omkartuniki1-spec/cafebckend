import os
from pymongo import MongoClient

# 🔐 Get Mongo URL from environment (Render)
MONGO_URL = os.getenv("MONGO_URL")

# ⚠️ Fallback for local development (optional)
if not MONGO_URL:
    MONGO_URL = "mongodb+srv://omkartuniki1_db_user:ezqFTPl6uYrS7aRu@cluster0.afgvuld.mongodb.net/?retryWrites=true&w=majority"

# 🔗 Connect to MongoDB
client = MongoClient(MONGO_URL)

# 📦 Database + Collection
db = client["cafe_db"]
orders_collection = db["orders"]

# ✅ Optional: Test connection (runs once)
try:
    client.admin.command("ping")
    print("✅ MongoDB Connected Successfully")
except Exception as e:
    print("❌ MongoDB Connection Error:", e)