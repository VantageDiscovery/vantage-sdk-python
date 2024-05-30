from enum import Enum
from typing import Optional

from pydantic import BaseModel


class CollectionType(Enum):
    USER_PROVIDED_EMBEDDINGS = "UPE"
    OPEN_AI = "OpenAI"
    HUGGING_FACE = "HuggingFace"


class ErrorMessage(BaseModel):
    field_name: str
    error_message: str


class ValidationError(BaseModel):
    document_id: Optional[str]
    line_number: Optional[int]
    errors: list[ErrorMessage]
