"""
Base Views Module
"""

from abc import ABC
from http import HTTPStatus

from argon2.exceptions import HashingError
from flask import Response, request
from flask.views import MethodView
from marshmallow import Schema, ValidationError

from app.enums import ResponseMessages
from app.helpers import authenticate_user
from app.settings import LIMITER, LOGGER
from app.utils import make_response


class BaseAuthView(MethodView):
    """
    Base class for auth API views
    """
    
    decorators = [LIMITER.limit("100/hour"), LIMITER.limit("10/minute")]
    payload_schema: Schema = None
    processor_class = None
    success_message: str = None
    
    def post(self) -> tuple[Response, HTTPStatus]:
        """
        Post method for auth API views.

        Returns:
            tuple[Response, HTTPStatus]: Response, status code
        """
        
        request_data: dict = request.get_json()
        
        try:
            validated_data: dict = self.payload_schema().load(request_data)
            data: dict = self.processor_class(validated_data).process()
            return make_response(message=self.success_message, data=data)

        except ValidationError as error:
            error_messages: dict = error.messages if isinstance(error.messages, dict) else error.normalized_messages()
            LOGGER.warning(f"Validation error: {error_messages}")
            return make_response(
                message=ResponseMessages.INVALID_REQUEST_DATA.value,
                errors={"details": error_messages},
                status_code=HTTPStatus.BAD_REQUEST
            )

        except HashingError as error:
            LOGGER.warning(f"Error while hashing access code: {error.args[0]}")
            return make_response(
                message=ResponseMessages.SOMETHING_WENT_WRONG.value, status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            )


class BaseAuthenticationView(MethodView, ABC):
    """
    Base class for view requiring token authentication
    """
    
    decorators = [authenticate_user, LIMITER.limit("100/hour"), LIMITER.limit("10/minute")]
    payload_schema: Schema = None
    processor_class = None
    success_message: str = None
    
    def handle_request(self, request_data: dict, context: dict = None) -> tuple[Response, HTTPStatus]:
        """
        Function to handle request.

        Args:
            request_data (dict): Request data.
            context (dict, optional): Request view args and request args. Defaults to None.

        Returns:
            tuple[Response, HTTPStatus]: Response, status code
        """
        
        user: dict = request.user
        
        try:
            validated_data: dict = self.payload_schema(context=context).load(request_data)
            data: dict = self.processor_class(validated_data, user).process()
            return make_response(message=self.success_message, data=data)

        except ValidationError as error:
            error_messages: dict = error.messages if isinstance(error.messages, dict) else error.normalized_messages()
            LOGGER.warning(f"Validation error: {error_messages}")
            return make_response(
                message=ResponseMessages.INVALID_REQUEST_DATA.value,
                errors={"details": error_messages},
                status_code=HTTPStatus.BAD_REQUEST
            )


class BaseNoteView(BaseAuthenticationView):
    """
    Base class for notes API views.
    """    

    def delete(self, note_id: str) -> tuple[Response, HTTPStatus]:
        """
        Base delete method.

        Args:
            note_id (str): Note id.

        Returns:
            tuple[Response, HTTPStatus]: Response, status code.
        """
        
        return self.handle_request({}, {"note_id": note_id})

    def get(self, note_id: str = None) -> tuple[Response, HTTPStatus]:
        """
        Base get method.

        Args:
            note_id (str, optional): Note id. Defaults to None.

        Returns:
            tuple[Response, HTTPStatus]: Response, status code.
        """
        
        return self.handle_request({}, {"note_id": note_id})

    def post(self, note_id: str = None) -> tuple[Response, HTTPStatus]:
        """
        Base post method.

        Args:
            note_id (str, optional): Note id. Defaults to None.

        Returns:
            tuple[Response, HTTPStatus]: Response, status code.
        """
        
        request_data = request.get_json()
        return self.handle_request(request_data, {"note_id": note_id})

    def put(self, note_id: str) -> tuple[Response, HTTPStatus]:
        """
        Base put method.

        Args:
            note_id (str): Note id.

        Returns:
            tuple[Response, HTTPStatus]: Response, status code.
        """

        request_data = request.get_json()
        return self.handle_request(request_data, {"note_id": note_id})
