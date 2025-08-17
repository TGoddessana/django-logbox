import re

from django.http import HttpRequest, HttpResponse

from django_logbox.app_settings import settings
from django_logbox.utils import get_client_ip, get_method, get_server_ip


class LogboxLogFilter:
    @staticmethod
    def should_filter_log(
        request: HttpRequest,
        response: HttpResponse | None,
    ) -> bool:
        """
        Check if the request and response should be logged.

        :return: True if the request and response should be filtered, False otherwise.
        """
        # Check if the request is already logged
        if hasattr(request, "logbox_logged"):
            return True

        # Check if the request and response should be logged
        if not LogboxLogFilter.should_log_request(request=request):
            return True
        if response:
            if not LogboxLogFilter.should_log_response(response=response):
                return True

        return False

    @staticmethod
    def should_log_request(request: HttpRequest) -> bool:
        return (
            LogboxLogFilter.is_client_ip_allowed(
                client_ip=get_client_ip(request=request)
            )
            and LogboxLogFilter.is_server_ip_allowed(
                server_ip=get_server_ip(request=request)
            )
            and LogboxLogFilter.is_method_allowed(
                method=get_method(request=request),
            )
            and LogboxLogFilter.is_path_allowed(
                request_path=request.path,
            )
        )

    @staticmethod
    def is_method_allowed(method: str) -> bool:
        """
        Check if the HTTP method is allowed to be logged.
        """
        return method in settings.LOGBOX_SETTINGS["LOGGING_HTTP_METHODS"]

    @staticmethod
    def is_client_ip_allowed(client_ip: str) -> bool:
        """
        Check if the client IP is allowed to be logged.
        """
        return (
            client_ip not in settings.LOGBOX_SETTINGS["LOGGING_CLIENT_IPS_TO_EXCLUDE"]
        )

    @staticmethod
    def is_server_ip_allowed(server_ip: str) -> bool:
        """
        Check if the server IP is allowed to be logged.
        """
        return (
            server_ip not in settings.LOGBOX_SETTINGS["LOGGING_SERVER_IPS_TO_EXCLUDE"]
        )

    @staticmethod
    def is_path_allowed(request_path: str) -> bool:
        """Filter requests based on path patterns."""

        return not any(
            re.match(path, request_path)
            for path in settings.LOGBOX_SETTINGS["LOGGING_PATHS_TO_EXCLUDE"]
        )

    @staticmethod
    def should_log_response(response: HttpResponse):
        return response.status_code in settings.LOGBOX_SETTINGS["LOGGING_STATUS_CODES"]
