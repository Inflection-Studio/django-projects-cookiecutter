import logging
import warnings
from abc import ABC, abstractmethod
from http.client import HTTPException
from urllib.parse import urljoin, urlparse

import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

logger = logging.getLogger(__name__)


class {{ cookiecutter.class_name_prefix }}HTTPClient(ABC):
    """
    Base class for making HTTP calls using Requests library.
    """

    REQUEST_TIMEOUT = 5
    EXCEPTION_CLASS = HTTPException
    # Endpoint name to path
    ENDPOINTS = {}
    BASE_URL = None
    LOG_PREFIX = "bridge_lab.utils.http.{{ cookiecutter.class_name_prefix }}HTTPClient"

    def __init__(self):
        self.session = requests.Session()

    def perform_call(self, http_method, url, json=None, **kwargs):
        """
        Perform an HTTP call with the specified method, URL, and optional JSON data.

        Args:
            http_method (str): The HTTP method to use (e.g., 'GET', 'POST').
            url (str): The URL to make the request to.
            json (dict, optional): JSON data to send in the request body.
            **kwargs: Additional keyword arguments to pass to the requests library.

        Raises:
            HTTPException: If an error occurs during the request.

        Returns:
            requests.Response: The response object.
        """
        request_headers = self.default_headers()
        call_headers = kwargs.pop("headers", {})
        request_headers.update(call_headers)

        if hasattr(requests, "Session") and hasattr(self.session, "mount"):
            self.session.mount(
                url,
                HTTPAdapter(
                    max_retries=Retry(
                        total=3,
                        connect=3,
                        backoff_factor=1,
                    )
                ),
            )
        try:
            response = getattr(requests, http_method)(
                url=url,
                json=json,
                timeout=self.REQUEST_TIMEOUT,
                headers=request_headers,
                **kwargs,
            )
        except requests.Timeout as exc:
            prefix = f"{self.LOG_PREFIX}.timeout"
            logger.warning(
                f"{self.__class__.__name__}.timeout",
                extra={"exception": str(exc), "call_made_from": prefix},
            )
            raise
        except requests.RequestException as exc:
            prefix = f"{self.LOG_PREFIX}.connection_error"
            logger.warning(
                f"{self.__class__.__name__}.connection_error",
                extra={"exception": str(exc), "call_made_from": prefix},
            )
            raise self.EXCEPTION_CLASS(
                f"An error occurred performing {http_method} request: {exc}"
            )
        except Exception as exc:
            prefix = f"{self.LOG_PREFIX}.exception"
            logger.warning(
                f"{self.__class__.__name__}.exception",
                extra={"exception": str(exc), "call_made_from": prefix},
            )
            raise self.EXCEPTION_CLASS(f"Something went wrong: {exc}")

        if not response.ok:
            return self._process_http_error_response(response)
        else:
            return self._process_http_response(response)

    @abstractmethod
    def _process_http_response(self, response: requests.Response):
        raise NotImplementedError()

    @abstractmethod
    def _process_http_error_response(self, response: requests.Response):
        raise NotImplementedError()

    def url(self, method) -> str:
        return urljoin(self.BASE_URL, self.ENDPOINTS[method])

    def default_headers(self):
        return {}


def celery_broker_url(url, default_scheme="redis"):
    res = urlparse(url)
    if res.netloc == "":
        warnings.warn(
            "The URL scheme of the Broker URL should be specified.",
            stacklevel=2,
        )
        res = urlparse(default_scheme + "://" + url)
    return res.geturl()
