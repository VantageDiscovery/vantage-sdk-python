from typing import Optional

from pydantic import ValidationError


class VantageException(Exception):
    """The base exception class for all Vantage client exceptions."""


class VantageNotFoundError(VantageException):
    def __init__(self, message: str):
        self.message = message


class VantageValueError(VantageException, ValueError):
    def __init__(self, error_msg: str):
        super(VantageValueError, self).__init__(error_msg)


class VantageFileUploadError(VantageException):
    def __init__(self, error_msg: str, status_code: int):
        super(VantageFileUploadError, self).__init__(error_msg, status_code)


class VantageServiceError(VantageException):
    def __init__(self, reason: str, status: int, response: str):
        self.reason = reason
        self.status = status
        self.response = response


class VantageInvalidRequestError(VantageException):
    def __init__(self, reason: str, status: int, response: str):
        self.reason = reason
        self.status = status
        self.response = response


class VantageInvalidResponseError(VantageException):
    def __init__(
        self,
        error_message: str,
        validation_error: Optional[ValidationError] = None,
    ):
        self.error_message = error_message
        self.validation_error = validation_error


class VantageUnauthorizedError(VantageException):
    def __init__(self, error_msg: str):
        super(VantageUnauthorizedError, self).__init__(error_msg)


class VantageForbiddenError(VantageException):
    def __init__(self, error_msg: str):
        super(VantageForbiddenError, self).__init__(error_msg)
