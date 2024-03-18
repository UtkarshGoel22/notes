"""
Initialization Module
"""

from flask import Flask
from flask_cors import CORS

from app.routes import register_routes
from app.settings import LIMITER, MONGO_CLIENT, MONGO_URI

app = Flask(__name__)
app.url_map.strict_slashes = False  # Includes trailing slashes

LIMITER.init_app(app)

MONGO_CLIENT.init_app(app, uri=MONGO_URI)

CORS(app)

register_routes(app)
