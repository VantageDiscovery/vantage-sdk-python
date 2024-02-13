class VantageException(Exception):
    """The base exception class for all Vantage client exceptions."""


class VantageNotFoundException(VantageException):
    def __init__(self, error_msg: str):
        super(VantageNotFoundException, self).__init__(error_msg)


class VantageValueError(VantageException, ValueError):
    def __init__(self, error_msg: str):
        super(VantageValueError, self).__init__(error_msg)


class VantageFileUploadException(VantageException):
    def __init__(self, error_msg: str, status_code: int):
        super(VantageFileUploadException, self).__init__(
            error_msg, status_code
        )


class VantageServiceError(VantageException):
    def __init__(self, error_msg: str, status_code: int):
        super(VantageFileUploadException, self).__init__(
            error_msg, status_code
        )


class VantageInvalidRequest(VantageException):
    def __init__(self, error_msg: str):
        super(VantageValueError, self).__init__(error_msg)


class VantageInvalidResponse(VantageException):
    def __init__(self, error_msg: str):
        super(VantageValueError, self).__init__(error_msg)
