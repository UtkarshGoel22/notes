"""
Notes Module
"""

from abc import ABC, abstractmethod

from bson import ObjectId
from pymongo.results import InsertOneResult

from app.exceptions import (
    AlreadySharedException,
    CannotShareNoteToYourselfException,
    DocumentNotExistsException,
    ForbiddenAccessException,
)
from app.helpers import fetch_user
from app.serializers import CreateNoteDocumentSchema, NotesSchema
from app.settings import MONGO_CLIENT
from app.utils import get_current_datetime


class Notes(ABC):
    """
    User base class
    """
    
    def __init__(self, validated_data: dict, user: dict) -> None:
        """
        Initialization function.

        Args:
            validated_data (dict): Validated request data.
            user (dict): User data.
        """

        self.request_data: dict = validated_data
        self.user: dict = user
        
    def fetch_note(self) -> dict:
        """
        Funtion to fetch note.

        Raises:
            DocumentNotExistsException: When the note document does not exist.

        Returns:
            dict: Note document.
        """
        
        note: dict = MONGO_CLIENT.db.notes.find_one({"_id": ObjectId(self.request_data["note_id"]), "isActive": True})
        if not note:
            raise DocumentNotExistsException()
        return note
    
    def has_read_access(self, note: dict) -> None:
        """
        Function to check whether the user has read access of the note.

        Args:
            note (dict): Note document.

        Raises:
            ForbiddenAccessException: When user does not have read access of the note.
        """
        
        if  (self.user["_id"] != note["author"]) and (note["_id"] not in self.user["sharedNotes"]):
            raise ForbiddenAccessException()
        
    def has_write_access(self, note: dict) -> None:
        """
        Function to check whether the user has write access of the note.

        Args:
            note (dict): Note document.

        Raises:
            ForbiddenAccessException: When user does not have write access of the note.
        """
        
        if  self.user["_id"] != note["author"]:
            raise ForbiddenAccessException()
    
    @abstractmethod
    def process(self) -> dict:
        """
        Driver Function for processing the request
        """


class CreateNote(Notes):
    """
    Class for creating a new note
    """
    
    def process(self) -> dict:
        """
        Function for creating new note.
        1. Prepare note data to set on the database.
        2. Create new note document.
        3. Append the note object id in the notes field in user document.

        Returns:
            dict: Containing new note id.
        """
        
        note_data: dict = CreateNoteDocumentSchema().load({**self.request_data, "author": str(self.user["_id"])})

        with MONGO_CLIENT.cx.start_session() as session:
            with session.start_transaction():
                result: InsertOneResult = MONGO_CLIENT.db.notes.insert_one(note_data, session=session)
                note_id: str = result.inserted_id
                MONGO_CLIENT.db.users.update_one(
                    {"_id": self.user["_id"]},
                    {
                        "$push": {"notes": note_id},
                        "$set": {"_lastModifiedAt": get_current_datetime()},
                    },
                    session=session,
                )
                session.commit_transaction()
                return {"note_id": str(note_id)}


class GetNotes(Notes):
    """
    Class for fetching notes
    """
    
    def process(self) -> dict:
        """
        Function for fetching note(s).
        1. If note with the note_id .
            1.1 Check if the note exists.
            1.2 Check whether the user has access to the note.
        2. If note_id is not present then fetch all the notes of the user.
        
        Raises:
            DocumentNotExistsException: When the note document does not exist.
            ForbiddenAccessException: When user does not have read access of the note.

        Returns:
            dict: Containing notes.
        """

        if self.request_data.get("note_id"):
            notes: list[dict] = [self.fetch_note()]
            self.has_read_access(notes[0])
        else:
            notes: list[dict] = list(MONGO_CLIENT.db.notes.find(
                {"_id": {"$in": [*self.user["notes"], *self.user["sharedNotes"]]}, "isActive": True},
            ))
        return NotesSchema().dump({"notes": notes})


class DeleteNote(Notes):
    """
    Class for deleting a note
    """
    
    def process(self):
        """
        Function to soft delete a note.
        1. Check if the note exists.
        2. Check whether the user has access to the note.
        3. Soft delete the note by setting isActive to False.

        Raises:
            DocumentNotExistsException: When the note document does not exist.
            ForbiddenAccessException: When user does not have write access of the note.
        """

        with MONGO_CLIENT.cx.start_session() as session:
            with session.start_transaction():
                note : dict = self.fetch_note()
                self.has_write_access(note)
                MONGO_CLIENT.db.notes.update_one(
                    {"_id": note["_id"], "isActive": True},
                    {"$set": {"isActive": False, "_lastModifiedAt": get_current_datetime()}}
                )
                session.commit_transaction()


class UpdateNote(Notes):
    """
    Class for updating a note
    """
    
    def process(self):
        """
        Function to update a note.
        1. Check if the note exists.
        2. Check whether the user has access to the note.
        3. Update the note.
        
        Raises:
            DocumentNotExistsException: When the note document does not exist.
            ForbiddenAccessException: When user does not have write access of the note.
        """

        with MONGO_CLIENT.cx.start_session() as session:
            with session.start_transaction():
                note : dict = self.fetch_note()
                self.has_write_access(note)
                data_to_update: dict = {key: value for key, value in self.request_data.items() if key != "note_id"}
                MONGO_CLIENT.db.notes.update_one(
                    {"_id": note["_id"], "isActive": True},
                    {
                        "$set": {
                            **data_to_update,
                            "_lastModifiedAt": get_current_datetime(),
                        },
                    },
                )
                session.commit_transaction()


class ShareNote(Notes):
    """
    Class for sharing a note
    """
    
    def check_if_note_can_be_shared(self, note: dict, user_to_share: dict) -> None:
        """
        Function to check if a note can be shared.

        Args:
            note (dict): Note document.
            user_to_share (dict): User document to whom the note is to be shared.

        Raises:
            CannotShareNoteToYourselfException: When the user is trying to share a note to himself.
            AlreadySharedException: When the note is already shared with the user.
        """

        if user_to_share["_id"] == note["author"]:
            raise CannotShareNoteToYourselfException()

        if note["_id"] in user_to_share["sharedNotes"]:
            raise AlreadySharedException()

    def process(self):
        """
        Function to share a note with another user.
        1. Check if the note exists.
        2. Check whether the user has write access to the note.
        3. Check if user is trying to share the note to himself.
        4. Check if the note is already shared.
        5. Share the note with another user.

        Raises:
            DocumentNotExistsException: When the note or the user document does not exist.
            ForbiddenAccessException: When user does not have write access of the note.
            CannotShareNoteToYourselfException: When the user is trying to share a note to himself.
            AlreadySharedException: When the note is already shared with the user.
        """
        
        with MONGO_CLIENT.cx.start_session() as session:
            with session.start_transaction():
                note : dict = self.fetch_note()
                self.has_write_access(note)
                user_to_share: dict = fetch_user(self.request_data["share_with"])
                if not user_to_share:
                    raise DocumentNotExistsException(
                        message="The user you are trying to share the note with doesn't exist."
                    )
                self.check_if_note_can_be_shared(note, user_to_share)
                MONGO_CLIENT.db.users.update_one(
                    {"_id": user_to_share["_id"], "isActive": True},
                    {
                        "$push": {"sharedNotes": note["_id"]},
                        "$set": {"_lastModifiedAt": get_current_datetime()},
                    }
                )
                session.commit_transaction()


class SearchNotes(Notes):
    """
    Class for searching notes
    """

    def process(self) -> dict:
        """
        Function to search notes based on keywords.

        Returns:
            dict: Notes whose title or body contain the keywords.
        """

        notes = list(
            MONGO_CLIENT.db.notes.find({"author": self.user["_id"], "$text": {"$search": self.request_data["q"]}})
        )
        return NotesSchema().dump({"notes": notes})
