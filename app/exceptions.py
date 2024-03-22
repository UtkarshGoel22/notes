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
        """
        Initialization Function.

        Args:
            message (str, optional): Exception message. Defaults to None.
            status_code (HTTPStatus, optional): Exception status code. Defaults to None.
        """

        super().__init__()
        self.message = message or self.message
        self.status_code = status_code or self.status_code


class AlreadySharedException(BaseHTTPException):
    """
    Already shared exception
    """

    message = ExceptionMessages.NOTE_ALREADY_SHARED.value
    status_code = HTTPStatus.BAD_REQUEST


class CannotShareNoteToYourselfException(BaseHTTPException):
    """
    Cannot share a note to your self exception
    """

    message = ExceptionMessages.NOTE_CANNOT_BE_SHARED_WITH_YOURSELF.value
    status_code = HTTPStatus.BAD_REQUEST


class DocumentNotExistsException(BaseHTTPException):
    """
    Document not exists in the database exception
    """

    message = ExceptionMessages.DOCUMENT_DOES_NOT_EXIST.value
    status_code = HTTPStatus.BAD_REQUEST


class ForbiddenAccessException(BaseHTTPException):
    """
    Forbidden access exception. When user does not have sufficient permission
    """

    message = ExceptionMessages.INSUFFICIENT_PERMISSIONS.value
    status_code = HTTPStatus.FORBIDDEN


class IncorrectUsernameOrPasswordException(BaseHTTPException):
    """
    Incorrect username or password exception.
    """

    message = ExceptionMessages.INCORRECT_USERNAME_OR_PASSWORD.value
    status_code = HTTPStatus.UNAUTHORIZED


class UnauthorizedAccessException(BaseHTTPException):
    """
    Unauthorized access exception
    """

    message = ExceptionMessages.UNAUTHORIZED_ACCESS.value
    status_code = HTTPStatus.UNAUTHORIZED


class UserAlreadyExistsException(BaseHTTPException):
    """
    User already exists exception
    """

    message = ExceptionMessages.USER_ALREADY_EXISTS.value
    status_code = HTTPStatus.BAD_REQUEST
