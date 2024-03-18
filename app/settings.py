"""
Settings Module
"""

import os

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_pymongo import PyMongo

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017")

REDIS_URI = os.environ.get("REDIS_URI", "redis://localhost:6379")

LIMITER = Limiter(
    key_func=get_remote_address,
    storage_uri=REDIS_URI,
    storage_options={"socket_connect_timeout": 30},
)

MONGO_CLIENT = PyMongo()
