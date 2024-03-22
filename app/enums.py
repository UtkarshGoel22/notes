"""
Enums Module
"""

from enum import Enum

# Argon2 hashing. Do not change these value. Changing the following 
# values will result in generation of different hash for same input.

class Argon2IdHash(Enum):
    """
    Enum for argon2id hashing constants
    """

    TIME_COST = 8
    MEMORY_COST = 16
    PARALLELISM = 2
    HASH_LENGTH = 16


class ErrorMessages(Enum):
    """
    Enum for error messages
    """

    INVALID_NAME = "Only A-Z letters and non-consecutive apostrophes(') and/or dashes(-) are allowed."
    INVALID_PASSWORD = "Password should be alphanumeric with at least one special character."
    SHORT_PASSWORD = "Password should contain at least 6 characters."


class ExceptionMessages(Enum):
    """
    Enum for exception messages
    """

    DOCUMENT_DOES_NOT_EXIST = "Document does not exists."
    INCORRECT_USERNAME_OR_PASSWORD = "Incorrect username or password."
    INSUFFICIENT_PERMISSIONS = "Insufficient permissions."
    UNAUTHORIZED_ACCESS = "Unauthorized access."
    USER_ALREADY_EXISTS = "User already exists."


class ResponseMessages(Enum):
    """
    Enum for response messages
    """

    INVALID_REQUEST_DATA = "Invalid request data."
    NOTE_CREATED_SUCCESSFULLY = "Note created successfully."
    NOTE_DELETED_SUCCESSFULLY = "Note deleted successfully."
    NOTE_FETCHED_SUCCESSFULLY = "Note(s) fetched successfully."
    SOMETHING_WENT_WRONG = "Something went wrong, please try again."
    USER_CREATED_SUCCESSFULLY = "User created successfully."
    USER_LOGGED_IN_SUCCESSFULLY = "User logged in successfully."
