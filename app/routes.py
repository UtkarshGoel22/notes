"""
Routes Module
"""

from flask import Blueprint, Flask

from app.main import CreateNoteView, DeleteNoteView, GetNotesView, SigninView, SignupView

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
    auth_bp.add_url_rule("/signup", view_func=SignupView.as_view("signup_view"), methods=["POST"])
    auth_bp.add_url_rule("/signin", view_func=SigninView.as_view("signin_view"), methods=["POST"])
    
    # Notes routes
    notes_bp.add_url_rule("/", view_func=CreateNoteView.as_view("create_note"), methods=["POST"])
    notes_bp.add_url_rule("/", view_func=GetNotesView.as_view("get_notes"), methods=["GET"])
    notes_bp.add_url_rule("/<note_id>", view_func=GetNotesView.as_view("get_note"), methods=["GET"])
    notes_bp.add_url_rule("/<note_id>", view_func=DeleteNoteView.as_view("delete_note"), methods=["DELETE"])
    
    api_bp.register_blueprint(auth_bp)
    api_bp.register_blueprint(notes_bp)
    app.register_blueprint(api_bp)
