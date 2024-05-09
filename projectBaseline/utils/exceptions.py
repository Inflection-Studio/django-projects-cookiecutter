from typing import Any

from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR  # isort:skip


class AbstractException(Exception):
    def __init__(
        self,
        error_msg: str,
        status: int = HTTP_400_BAD_REQUEST,
        extra: dict[str, Any] = None,
    ):
        """
        :error_msg: The error message
        :status: HTTP status of the response
        :extra: any extra message
        """

        self.error_msg = error_msg
        self.status = status
        self.extra = extra

        super().__init__(error_msg, status)


class ServiceException(AbstractException):
    """
    An exception type that services and tasks can raise,
    defines the generic exception to raised by the system
    """


class InternalServerException(AbstractException):
    def __init__(
        self,
        error_msg: str,
        status=HTTP_500_INTERNAL_SERVER_ERROR,
        extra=None,
    ):
        super().__init__(error_msg, status, extra)
