"""
Routes Module
"""

from flask import Blueprint, Flask

from app.main import signup

api_bp = Blueprint("api_bp", __name__, url_prefix="/api")
auth_bp = Blueprint("auth_bp", __name__, url_prefix="/auth")
notes_bp = Blueprint("notes_bp", __name__, url_prefix="/notes")

def register_routes(app: Flask) -> None:
    """
    Function to register routes

    Args:
        app (Flask): Flask app
    """
    
    # Auth routes
    auth_bp.add_url_rule("/signup", view_func=signup, methods=["POST"])
    
    # Notes routes
    
    api_bp.register_blueprint(auth_bp)
    api_bp.register_blueprint(notes_bp)
    app.register_blueprint(api_bp)
