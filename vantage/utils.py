from pydantic_core._pydantic_core import ValidationError

from vantage.core.http.exceptions import (
    ApiAttributeError,
    ApiException,
    ApiKeyError,
    ApiValueError,
    BadRequestException,
    ForbiddenException,
    NotFoundException,
    OpenApiException,
    ServiceException,
    UnauthorizedException,
)
from vantage.exceptions import (
    VantageForbiddenError,
    VantageInvalidRequestError,
    VantageInvalidResponseError,
    VantageNotFoundError,
    VantageServiceError,
    VantageUnauthorizedError,
)


def _parse_exception(exception: Exception, response=None) -> Exception:
    if isinstance(exception, BadRequestException):
        return VantageInvalidRequestError(
            reason=exception.reason,
            status=exception.status,
            response=exception.body,
        )

    if isinstance(exception, NotFoundException):
        return VantageNotFoundError(message=exception.reason)

    if isinstance(exception, UnauthorizedException):
        return VantageUnauthorizedError("")

    if isinstance(exception, ForbiddenException):
        return VantageForbiddenError("")

    if isinstance(exception, ServiceException):
        return VantageServiceError(
            reason=exception.reason,
            status=exception.status,
            response=exception.body,
        )

    if isinstance(exception, ApiValueError):
        return VantageInvalidRequestError(
            reason=exception.reason,
            status=exception.status,
            response=exception.body,
        )

    if isinstance(exception, ApiAttributeError):
        return VantageInvalidRequestError(
            reason=exception.reason,
            status=exception.status,
            response=exception.body,
        )

    if isinstance(exception, ApiKeyError):
        return VantageInvalidRequestError(
            reason=exception.reason,
            status=exception.status,
            response=exception.body,
        )

    if isinstance(exception, ApiException):
        return VantageServiceError(
            reason=exception.reason,
            status=exception.status,
            response=exception.body,
        )

    if isinstance(exception, OpenApiException):
        return VantageServiceError(
            reason=exception.reason,
            status=exception.status,
            response=exception.body,
        )

    if isinstance(exception, ValidationError):
        return VantageInvalidResponseError(
            error_message=exception.title, validation_error=exception
        )

    return exception
