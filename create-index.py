"""
Create Index Module
"""

import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

mongo_uri = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
mongo_client = MongoClient(mongo_uri)
db = mongo_client.notes

db.notes.create_index({"title": "text", "body": "text"})
