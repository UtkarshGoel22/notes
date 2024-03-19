"""
Exceptions Module
"""

from http import HTTPStatus

from app.enums import ExceptionMessages


class BaseHTTPException(Exception):
    """
    Base exception
    """

    def __init__(self, message: str = None, status_code: HTTPStatus = None) -> None:
        super().__init__()
        self.message = message or self.message
        self.status_code = status_code or self.status_code


class UserAlreadyExistsException(BaseHTTPException):
    """
    User already exists exception
    """
    
    message = ExceptionMessages.USER_ALREADY_EXISTS.value
    status_code = HTTPStatus.BAD_REQUEST
