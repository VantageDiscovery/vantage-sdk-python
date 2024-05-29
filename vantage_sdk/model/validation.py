from pydantic import BaseModel


class ErrorMessage(BaseModel):
    field_name: str
    error_message: str


class ValidationError(BaseModel):
    document_id: str
    line_number: int
    errors: list[ErrorMessage]
