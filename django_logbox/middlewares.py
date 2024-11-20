import re
from time import time

from django.http import HttpRequest, HttpResponse

from django_logbox.app_settings import app_settings
from django_logbox.threading import logger_thread
from django_logbox.utils import get_log_data, _get_client_ip, _get_server_ip


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
    def _filter_requests(request: HttpRequest):
        # filter client ip
        client_ip = _get_client_ip(request)
        logging_client_ips = app_settings.LOGGING_CLIENT_IPS
        if "*" not in logging_client_ips and client_ip not in logging_client_ips:
            return False

        # filter server ip
        server_ip = _get_server_ip(request)
        logging_server_ips = app_settings.LOGGING_SERVER_IPS
        if "*" not in logging_server_ips and server_ip not in logging_server_ips:
            return False

        # filter paths
        logging_paths_regex = re.compile(app_settings.LOGGING_PATHS_REGEX)
        logging_exclude_paths_regex = re.compile(
            app_settings.LOGGING_EXCLUDE_PATHS_REGEX
        )

        return (
            request.method in app_settings.LOGGING_HTTP_METHODS
            and logging_paths_regex.match(request.path)
            and not logging_exclude_paths_regex.match(request.path)
        )

    @staticmethod
    def _filter_responses(response: HttpResponse):
        return response.status_code in app_settings.LOGGING_STATUS_CODES
