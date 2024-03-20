"""
Helpers Module
"""

from app.settings import MONGO_CLIENT


def fetch_user(username: str) -> dict:
    """
    Function to fetch user from the database.

    Args:
        username (str): Username.

    Returns:
        dict: User document if the user exists in the database.
    """
 
    return MONGO_CLIENT.db.users.find_one({"isActive": True, "username": username}, {"password": 0})
