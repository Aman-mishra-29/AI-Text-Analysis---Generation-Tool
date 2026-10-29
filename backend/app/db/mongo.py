from pymongo import MongoClient
from app.config import settings

# Connect using settings
client = MongoClient(settings.MONGO_URI)
db = client[settings.DATABASE_NAME]

# Test connection
try:
    client.admin.command("ping")
    print("✅ MongoDB Connected Successfully")
except Exception as e:
    print("❌ MongoDB Connection Failed:", e)

# Collections
summaries_collection = db["summaries"]
plagiarism_collection = db["plagiarism"]
autocorrect_collection = db["autocorrect"]