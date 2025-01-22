import re
from time import time

from django.http import HttpRequest, HttpResponse

from django_logbox.app_settings import app_settings
from django_logbox.threading import get_logbox_thread
from django_logbox.utils import get_log_data, _get_client_ip, _get_server_ip

logger_thread = get_logbox_thread()


class LogboxMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        timestamp = time()
        response = self.get_response(request)

        if not self._filter_requests(request) or not self._filter_responses(response):
            return response

        if logger_thread:
            # Avoid logging the same request twice from process_exception
            if not hasattr(request, "logbox_logged"):
                logger_thread.put_serverlog(
                    get_log_data(timestamp, request, response),
                )
                request.logbox_logged = True

        return response

    def process_exception(self, request: HttpRequest, exception: Exception):
        data = get_log_data(time(), request, None, exception)

        if logger_thread:
            logger_thread.put_serverlog(data)
            request.logbox_logged = True

        return None

    @staticmethod
    def _filter_requests(request: HttpRequest) -> bool:
        return (
            LogboxMiddleware._filter_client_ip(request)
            and LogboxMiddleware._filter_server_ip(request)
            and LogboxMiddleware._filter_path(request)
        )

    @staticmethod
    def _filter_client_ip(request: HttpRequest) -> bool:
        """
        Filter requests based on client IP.

        :return: True if the request should be logged, False otherwise.
        """
        return _get_client_ip(request) not in app_settings.LOGGING_CLIENT_IPS_TO_EXCLUDE

    @staticmethod
    def _filter_server_ip(request: HttpRequest):
        """
        Filter requests based on server IP.

        :return: True if the request should be logged, False otherwise.
        """
        return _get_server_ip(request) not in app_settings.LOGGING_SERVER_IPS_TO_EXCLUDE

    @staticmethod
    def _filter_path(request: HttpRequest) -> bool:
        """Filter requests based on path patterns."""

        return not any(
            re.match(path, request.path)
            for path in app_settings.LOGGING_PATHS_TO_EXCLUDE
        )

    @staticmethod
    def _filter_responses(response: HttpResponse):
        return response.status_code in app_settings.LOGGING_STATUS_CODES
