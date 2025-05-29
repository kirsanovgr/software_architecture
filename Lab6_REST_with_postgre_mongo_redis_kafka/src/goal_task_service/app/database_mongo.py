from pymongo import MongoClient
import os

MONGO_HOST = os.getenv("MONGO_HOST", "task_files_db")
MONGO_PORT = os.getenv("MONGO_PORT", "27017")
MONGO_USER = os.getenv("MONGO_USER", "admin")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD", "password")

MONGO_URL = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/"

client = MongoClient(MONGO_URL)
db = client["task_files"]

# Коллекции
image_collection = db["images"]
text_collection = db["text"]
office_collection = db["office365"]

