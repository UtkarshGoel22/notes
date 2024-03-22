"""
Serializers Module
"""

from bson import ObjectId

from marshmallow import EXCLUDE, Schema, ValidationError, fields, post_load, pre_load, validate, validates_schema

from app.constants import REGEX_NAME, REGEX_PASSWORD
from app.enums import ErrorMessages
from app.utils import get_current_datetime


class ObjectIdField(fields.Field):
    """
    ObjectId field
    """

    def _deserialize(self, value: str, attr, obj, **kwargs) -> ObjectId:
        """
        Function to deserialize _id field of mongodb documents.

        Args:
            value (str): Document id.

        Returns:
            ObjectId: ObjectId.
        """

        try:
            return ObjectId(value)
        except Exception as error:
            raise fields.ValidationError(f"Invalid ObjectId: {value}")
        
    def _serialize(self, value: ObjectId, attr, obj, **kwargs) -> str:
        return str(value)


class BaseSchema(Schema):
    """
    Base schema
    """

    class Meta:
        """
        Meta class for BaseSchema. Provides various options for serializing attributes.
        """

        unknown = EXCLUDE
        

class BaseMongoSchema(BaseSchema):
    """
    Base mongo schema
    """
    
    _createdAt = fields.DateTime()
    _lastModifiedAt = fields.DateTime()
    isActive = fields.Boolean(load_default=True)
    
    @post_load
    def transform(self, data: dict, **_) -> dict:
        """
        Add _createdAt and _lastModifiedAt fields in the data.

        Args:
            data (dict): Validated data.

        Returns:
            dict: Validated data with _createdAt and _lastModifiedAt fields.
        """
        
        data["_createdAt"] = data["_lastModifiedAt"] = get_current_datetime()
        return data


class BaseAuthRequestSchema(BaseSchema):
    """
    Base auth request schema
    """

    password = fields.String(
        required=True,
        validate=[
            validate.Length(min=6, error=ErrorMessages.SHORT_PASSWORD.value),
            validate.Regexp(REGEX_PASSWORD, error=ErrorMessages.INVALID_PASSWORD.value),
        ],
    )
    username = fields.Email(required=True)


class SigninRequestSchema(BaseAuthRequestSchema):
    """
    User signin request schema
    """


class SignupRequestSchema(BaseAuthRequestSchema):
    """
    User signup request schema
    """
    
    first_name = fields.String(
        required=True,
        validate=validate.Regexp(REGEX_NAME, error=ErrorMessages.INVALID_NAME.value),
    )
    last_name = fields.String(
        required=True,
        validate=validate.Regexp(REGEX_NAME, error=ErrorMessages.INVALID_NAME.value),
    )


class CreateUserDocumentSchema(BaseMongoSchema):
    """
    Create user document schema
    """
    
    firstName = fields.String(required=True, data_key="first_name")
    lastName = fields.String(required=True, data_key="last_name")
    password = fields.String(required=True)
    username = fields.String(required=True)
    notes = fields.List(ObjectIdField(), load_default=[])
    sharedNotes = fields.List(ObjectIdField(), load_default=[])


class CreateNoteRequestSchema(BaseSchema):
    """
    Create note request schema
    """
    
    body = fields.String(required=True)
    title = fields.String(required=True)    


class CreateNoteDocumentSchema(BaseMongoSchema):
    """
    Create note document schema
    """

    author = ObjectIdField(required=True)
    body = fields.String(required=True)
    title = fields.String(required=True)
