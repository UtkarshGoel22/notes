"""
Notes Module
"""

from abc import ABC, abstractmethod

from bson import ObjectId
from pymongo.results import InsertOneResult

from app.exceptions import DocumentNotExistsException, ForbiddenAccessException
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
