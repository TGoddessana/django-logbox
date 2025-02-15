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

        if not self._filter_requests(request) or not self._filter_responses(response):
            return response

        if not hasattr(request, "logbox_logged"):
            logbox_logger_thread.put_serverlog(
                get_log_data(
                    timestamp=timestamp,
                    request=request,
                    response=response,
                    exception=None,
                ),
            )
            request.logbox_logged = True

        return response

    def process_exception(self, request: HttpRequest, exception: Exception):
        data = get_log_data(time(), request, None, exception)

        logbox_logger_thread.put_serverlog(data)
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
        return (
            _get_client_ip(request)
            not in settings.LOGBOX_SETTINGS["LOGGING_CLIENT_IPS_TO_EXCLUDE"]
        )

    @staticmethod
    def _filter_server_ip(request: HttpRequest):
        """
        Filter requests based on server IP.

        :return: True if the request should be logged, False otherwise.
        """
        return (
            _get_server_ip(request)
            not in settings.LOGBOX_SETTINGS["LOGGING_SERVER_IPS_TO_EXCLUDE"]
        )

    @staticmethod
    def _filter_path(request: HttpRequest) -> bool:
        """Filter requests based on path patterns."""

        return not any(
            re.match(path, request.path)
            for path in settings.LOGBOX_SETTINGS["LOGGING_PATHS_TO_EXCLUDE"]
        )

    @staticmethod
    def _filter_responses(response: HttpResponse):
        return response.status_code in settings.LOGBOX_SETTINGS["LOGGING_STATUS_CODES"]
