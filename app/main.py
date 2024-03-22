"""
Main Module
"""

from http import HTTPStatus

from flask import Response

from app.base import BaseAuthView, BaseNoteView
from app.enums import ResponseMessages
from app.exceptions import (
    AlreadySharedException,
    CannotShareNoteToYourselfException,
    DocumentNotExistsException,
    ForbiddenAccessException,
    IncorrectUsernameOrPasswordException,
    UserAlreadyExistsException,
)
from app.notes import CreateNote, DeleteNote, GetNotes, ShareNote, UpdateNote
from app.serializers import (
    CreateNoteRequestSchema,
    NoteAPIRequestSchema,
    ShareNoteRequestSchema,
    SigninRequestSchema,
    SignupRequestSchema,
    UpdateNoteRequestSchema,
)
from app.settings import LOGGER
from app.user import CreateUser, LoginUser
from app.utils import make_response


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


class CreateNoteView(BaseNoteView):
    """
    View class for creating a new note
    """

    payload_schema = CreateNoteRequestSchema
    processor_class = CreateNote
    success_message = ResponseMessages.NOTE_CREATED_SUCCESSFULLY.value


class GetNotesView(BaseNoteView):
    """
    View class to get notes of a user
    """

    payload_schema = NoteAPIRequestSchema
    processor_class = GetNotes
    success_message = ResponseMessages.NOTE_FETCHED_SUCCESSFULLY.value
    
    def get(self, note_id: str = None) -> tuple[Response, HTTPStatus]:
        """
        Get method for fetching notes of a user.
        If note_id is present then fetch only that note otherwise fetch all the notes.

        Args:
            note_id (str, optional): Note id. Defaults to None.

        Returns:
            tuple[Response, HTTPStatus]: Response, status code.
        """

        try:
            return super().get(note_id)
        except (DocumentNotExistsException, ForbiddenAccessException) as error:
            LOGGER.warning(f"Error occurred while fetching note(s): {error}")
            return make_response(message=error.message, status_code=error.status_code)


class DeleteNoteView(BaseNoteView):
    """
    View class to delete note of a user
    """

    payload_schema = NoteAPIRequestSchema
    processor_class = DeleteNote
    success_message = ResponseMessages.NOTE_DELETED_SUCCESSFULLY.value
    
    def delete(self, note_id: str) -> tuple[Response, HTTPStatus]:
        """
        Delete method for deleting a note.

        Args:
            note_id (str): Note id.

        Returns:
            tuple[Response, HTTPStatus]: Response, status code.
        """
        
        try:
            return super().delete(note_id)
        except (DocumentNotExistsException, ForbiddenAccessException) as error:
            LOGGER.warning(f"Error occurred while deleting note: {error}")
            return make_response(message=error.message, status_code=error.status_code)


class UpdateNoteView(BaseNoteView):
    """
    View class to update note of a user
    """

    payload_schema = UpdateNoteRequestSchema
    processor_class = UpdateNote
    success_message = ResponseMessages.NOTE_UPDATED_SUCCESSFULLY.value
    
    def put(self, note_id: str) -> tuple[Response, HTTPStatus]:
        """
        Put method for updating a note.

        Args:
            note_id (str): Note id.

        Returns:
            tuple[Response, HTTPStatus]: Response, status code.
        """
        
        try:
            return super().put(note_id)
        except (DocumentNotExistsException, ForbiddenAccessException) as error:
            LOGGER.warning(f"Error occurred while updating note: {error}")
            return make_response(message=error.message, status_code=error.status_code)


class ShareNoteView(BaseNoteView):
    """
    View class to share a note to another user
    """

    payload_schema = ShareNoteRequestSchema
    processor_class = ShareNote
    success_message = ResponseMessages.NOTE_SHARED_SUCCESSFULLY.value
    
    def post(self, note_id: str) -> tuple[Response, HTTPStatus]:
        """
        Post method for sharing note with another user.

        Args:
            note_id (str): Note id.

        Returns:
            tuple[Response, HTTPStatus]: Response, status code.
        """
        
        try:
            return super().post(note_id)
        except (
            AlreadySharedException,
            CannotShareNoteToYourselfException,
            DocumentNotExistsException,
            ForbiddenAccessException,
        ) as error:
            LOGGER.warning(f"Error occurred while sharing note to another user: {error}")
            return make_response(message=error.message, status_code=error.status_code)
