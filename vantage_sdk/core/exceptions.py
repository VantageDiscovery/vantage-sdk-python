from typing import Optional

from pydantic import ValidationError


class VantageException(Exception):
    """The base exception class for all Vantage client exceptions."""


class VantageNotFoundError(VantageException):
    """Thrown if requested resource is not found."""

    def __init__(self, message: str):
        self.message = message


class VantageValueError(VantageException, ValueError):
    """Thrown if value(s) passed to the API are incorrect in given context."""

    def __init__(self, error_msg: str):
        super(VantageValueError, self).__init__(error_msg)


class VantageFileUploadError(VantageException):
    """Thrown if error occurs while uploading a file."""

    def __init__(self, error_msg: str, status_code: int):
        super(VantageFileUploadError, self).__init__(error_msg, status_code)


class VantageServiceError(VantageException):
    """
    Thrown if the API server reports a HTTP 500 error during normal usage.
    """

    def __init__(self, reason: str, status: int, response: str):
        self.reason = reason
        self.status = status
        self.response = response


class VantageInvalidRequestError(VantageException):
    """Thrown if user sends invalid request to the API."""

    def __init__(self, reason: str, status: int, response: str):
        self.reason = reason
        self.status = status
        self.response = response


class VantageInvalidResponseError(VantageException):
    """Thrown if server returns invalid response."""

    def __init__(
        self,
        error_message: str,
        validation_error: Optional[ValidationError] = None,
    ):
        self.error_message = error_message
        self.validation_error = validation_error


class VantageUnauthorizedError(VantageException):
    """Thrown if user tries to access the API without valid authorization."""

    def __init__(self, error_msg: str):
        super(VantageUnauthorizedError, self).__init__(error_msg)


class VantageForbiddenError(VantageException):
    """Thrown if unauthenticated user tries to access the API."""

    def __init__(self, error_msg: str):
        super(VantageForbiddenError, self).__init__(error_msg)
