"""
User Module
"""

from abc import ABC, abstractmethod

from pymongo.results import InsertOneResult

from app.exceptions import UserAlreadyExistsException
from app.serializers import CreateUserDocumentSchema
from app.settings import MONGO_CLIENT
from app.utils import argon2id_hasher


class User(ABC):
    """
    User base class
    """
    
    def __init__(self, validated_data: dict) -> None:
        """
        Initialization function.

        Args:
            validated_data (dict): Validated request data.
        """

        self.request_data = validated_data

    def fetch_user(self) -> dict:
        """
        Function to fetch user from the database.
        
        Returns:
            dict: User document if the user exists in the database.
        """
        
        return MONGO_CLIENT.db.users.find_one({"isActive": True, "username": self.request_data["username"]})

    def hash_password(self) -> str:
        """
        Function to hash password.

        Returns:
            str: Hashed password.
        """
        
        return argon2id_hasher(self.request_data["password"].encode()).hex()
    
    @abstractmethod
    def process(self) -> dict:
        """
        Driver Function for processing the request
        """


class CreateUser(User):
    """
    Class for creating new user.
    """    
        
    def process(self) -> dict:
        """
        Function for creating new user.
        1. Check if user already exists.
        2. Hash the password.
        3. Create user.

        Raises:
            UserAlreadyExistsException: When user with the same username already exists.
            HashingError: When some problem is encountered while hashing password.
        
        Returns:
            dict: Response data containing user id of the newly created user.
        """
        
        if self.fetch_user():
            raise UserAlreadyExistsException()

        self.request_data["password"] = self.hash_password()

        user_data: dict = CreateUserDocumentSchema().load(self.request_data)

        result: InsertOneResult = MONGO_CLIENT.db.users.insert_one(user_data)

        return {"user_id": str(result.inserted_id)}
