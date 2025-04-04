import re
from time import time

from django.conf import settings
from django.http import HttpRequest, HttpResponse

from django_logbox.threading import ServerLogInsertThread
from django_logbox.utils import _get_client_ip, _get_server_ip, get_log_data

logbox_logger_thread = ServerLogInsertThread.get_instance()


class LogboxMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        timestamp = time()
        response = self.get_response(request)

        if self._should_filter_log(request, response):
            return response

        data = get_log_data(
            timestamp=timestamp,
            request=request,
            response=response,
            exception=None,
        )
        logbox_logger_thread.put_serverlog(data=data)
        request.logbox_logged = True

        return response

    def process_exception(self, request: HttpRequest, exception: Exception):
        if self._should_filter_log(request, None):
            return None

        data = get_log_data(
            timestamp=time(),
            request=request,
            response=None,
            exception=exception,
        )
        logbox_logger_thread.put_serverlog(data=data)
        request.logbox_logged = True

    def _should_filter_log(
        self, request: HttpRequest, response: HttpResponse | None
    ) -> bool:
        """
        Check if the request and response should be logged.

        :param request: The HTTP request object.
        :param response: The HTTP response object.
        :return: True if the request and response should be filtered, False otherwise.
        """
        # Check if the request is already logged
        if hasattr(request, "logbox_logged"):
            return True

        # Check if the request and response should be logged
        if not self._should_log_request(request):
            return True
        if response:
            if not self._should_log_response(response):
                return True

        return False

    @staticmethod
    def _should_log_request(request: HttpRequest) -> bool:
        return (
            LogboxMiddleware._is_client_ip_allowed(request)
            and LogboxMiddleware._is_server_ip_allowed(request)
            and LogboxMiddleware._is_path_allowed(request)
        )

    @staticmethod
    def _is_client_ip_allowed(request: HttpRequest) -> bool:
        """
        Filter requests based on client IP.

        :return: True if the request should be logged, False otherwise.
        """
        return (
            _get_client_ip(request)
            not in settings.LOGBOX_SETTINGS["LOGGING_CLIENT_IPS_TO_EXCLUDE"]
        )

    @staticmethod
    def _is_server_ip_allowed(request: HttpRequest):
        """
        Filter requests based on server IP.

        :return: True if the request should be logged, False otherwise.
        """
        return (
            _get_server_ip(request)
            not in settings.LOGBOX_SETTINGS["LOGGING_SERVER_IPS_TO_EXCLUDE"]
        )

    @staticmethod
    def _is_path_allowed(request: HttpRequest) -> bool:
        """Filter requests based on path patterns."""

        return not any(
            re.match(path, request.path)
            for path in settings.LOGBOX_SETTINGS["LOGGING_PATHS_TO_EXCLUDE"]
        )

    @staticmethod
    def _should_log_response(response: HttpResponse):
        return response.status_code in settings.LOGBOX_SETTINGS["LOGGING_STATUS_CODES"]
