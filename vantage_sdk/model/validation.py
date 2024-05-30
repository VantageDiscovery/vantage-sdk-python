from enum import Enum
from typing import Optional

from pydantic import BaseModel


class CollectionType(Enum):
    """Collection type"""

    USER_PROVIDED_EMBEDDINGS = "UPE"
    OPEN_AI = "OpenAI"
    HUGGING_FACE = "HuggingFace"


class ErrorMessage(BaseModel):
    """
    Validation error message.

    Arguments
    ---------
    field_name: str
        Name of field for which is erroneous.
    error_message: str
        Message describing error details.
    """

    field_name: str
    error_message: str


class ValidationError(BaseModel):
    """
    Validation error for a single document.

    Arguments
    ---------
    document_id: Optional[str]
        Unique id of a document.
    line_number: Optional[int]
        A line/row where document is located in file.
    errors: list[ErrorMessage]
        Validation error messages.
    """

    document_id: Optional[str]
    line_number: Optional[int]
    errors: list[ErrorMessage]
