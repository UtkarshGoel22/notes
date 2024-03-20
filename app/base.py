"""
Base Views Module
"""

from http import HTTPStatus

from argon2.exceptions import HashingError
from flask import Response, request
from flask.views import MethodView
from marshmallow import Schema, ValidationError

from app.enums import ResponseMessages
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
