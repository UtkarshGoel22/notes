"""
Main Module
"""

from http import HTTPStatus

from argon2.exceptions import HashingError
from flask import Response, request
from flask.views import MethodView
from marshmallow import Schema, ValidationError

from app.enums import ResponseMessages
from app.exceptions import IncorrectUsernameOrPasswordException, UserAlreadyExistsException
from app.serializers import SigninRequestSchema, SignupRequestSchema
from app.settings import LIMITER, LOGGER
from app.user import CreateUser, LoginUser
from app.utils import make_response


class BaseView(MethodView):
    """
    Base class for views
    """
    
    decorators = [LIMITER.limit("100/hour"), LIMITER.limit("10/minute")]
    payload_schema: Schema = None
    processor_class = None
    success_message: str = None
    
    def handle_request(self, request_data: dict = None, context: dict = None) -> tuple[Response, HTTPStatus]:
        """
        Function to handle request.

        Args:
            request_data (dict, optional): Request data. Defaults to None.
            context (dict, optional): Request args. Defaults to None.

        Returns:
            tuple[Response, HTTPStatus]: Response, status code.
        """
        
        try:
            validated_data: dict = self.payload_schema(context=context).load(request_data or {})
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
    
    def post(self) -> tuple[Response, HTTPStatus]:
        """
        Base post method.

        Returns:
            tuple[Response, HTTPStatus]: Response, status code.
        """
        
        request_data: dict = request.get_json()
        return self.handle_request(request_data=request_data, context={"request_args": request.args})


class BaseAuthView(BaseView):
    """
    Base class for auth views
    """
    
    def post(self) -> tuple[Response, HTTPStatus]:
        
        try:
            return super().post()
        except HashingError as error:
            LOGGER.warning(f"Error while hashing access code: {error.args[0]}")
            return make_response(
                message=ResponseMessages.SOMETHING_WENT_WRONG.value, status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            )


class SignupView(BaseAuthView):
    """
    View class for user signup
    """
    
    payload_schema = SignupRequestSchema
    processor_class = CreateUser
    success_message = ResponseMessages.USER_CREATED_SUCCESSFULLY.value
    
    def post(self) -> tuple[Response, HTTPStatus]:
        """
        This endpoint handles the request for user signup.
        1. Validates incoming request data.
        2. Checks if the user with the given username already exists.
        3. Hash the password.
        3. Creates new user.
        
        Returns:
            tuple[Response, HTTPStatus]: Response, status code.
        """
        
        try:
            return super().post()
        except UserAlreadyExistsException as error:
            LOGGER.warning(f"Error occurred during signup: {error.message}")
            return make_response(message=error.message, status_code=error.status_code)


class SigninView(BaseAuthView):
    """
    View class for user signin
    """
    
    payload_schema = SigninRequestSchema
    processor_class = LoginUser
    success_message = ResponseMessages.USER_LOGGED_IN_SUCCESSFULLY.value
    
    def post(self) -> tuple[Response, HTTPStatus]:
        """
        This endpoint handles the request for user signin.
        1. Validates incoming request data.
        2. Checks if the user with the given username exists.
        3. Verifies the password.
        3. Generates and returns a jwt token.
        
        Returns:
            tuple[Response, HTTPStatus]: Response, status code
        """
        
        try:
            return super().post()
        except IncorrectUsernameOrPasswordException as error:
            LOGGER.warning(f"Error occurred during signin: {error.message}")
            return make_response(message=error.message, status_code=error.status_code)
