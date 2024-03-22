"""
Helpers Module
"""

import jwt
from flask import request
from jwt.exceptions import PyJWTError

from app.exceptions import UnauthorizedAccessException
from app.settings import JWT_SECRET_KEY, LOGGER, MONGO_CLIENT
from app.utils import make_response


def fetch_user(username: str) -> dict:
    """
    Function to fetch user from the database.

    Args:
        username (str): Username.

    Returns:
        dict: User document if the user exists in the database.
    """
 
    return MONGO_CLIENT.db.users.find_one({"isActive": True, "username": username}, {"password": 0})


def authenticate_user(func):
    """
    Decorator for authenticating user.
    """
    
    def wrapper(*args, **kwargs):
        """
        Wrapper function for authenticating user.
        """
        
        try:
            token: str = request.headers.get("Authorization")
            if not token or not token.startswith("Bearer "):
                raise UnauthorizedAccessException()
            token = token.split("Bearer ")[1]
            
            try:
                decoded_token: dict = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
            except PyJWTError as error:
                LOGGER.warning(f"Error occurred while decoding token: {error}")
                raise UnauthorizedAccessException() from error
            
            user: dict = fetch_user(decoded_token["username"])
            if not user:
                raise UnauthorizedAccessException()

            setattr(request, "user", user)
        
        except UnauthorizedAccessException as error:
            LOGGER.warning(error.message)
            return make_response(message=error.message, status_code=error.status_code)

        return func(*args, **kwargs)
    
    return wrapper
