from typing import Optional

from pydantic import BaseModel


class ErrorMessage(BaseModel):
    field_name: str
    error_message: str


class ValidationError(BaseModel):
    document_id: Optional[str]
    line_number: Optional[int]
    errors: list[ErrorMessage]
