import traceback
from datetime import datetime
from time import time

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.utils.timezone import make_aware

from django_logbox.models import ServerLog


class LogboxMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self._data = {}

    def __call__(self, request: HttpRequest):
        start_timestamp = time()
        response = self.get_response(request)
        end_timestamp = time()

        data = {
            "method": self._get_method(request),
            "path": self._get_path(request),
            "user_agent": self._get_user_agent(request),
            "querystring": self._get_querystring(request),
            "request_body": self._get_request_body(request),
            "timestamp": self._get_timestamp(start_timestamp),
            "duration": self._get_duration(start_timestamp, end_timestamp),
            "server_ip": self._get_server_ip(request),
            "client_ip": self._get_client_ip(request),
            "status_code": self._get_status_code(response),
        }
        self._data.update(data)

        ServerLog.objects.create(**self._data)

        return response

    def process_exception(self, request: HttpRequest, exception: Exception):
        exception_data = {
            "exception": self._get_exception_type(exception),
            "traceback": self._get_traceback(exception),
        }
        self._data = exception_data
        return None

    @staticmethod
    def _get_method(request: HttpRequest):
        return request.method

    @staticmethod
    def _get_path(request: HttpRequest):
        return request.path

    @staticmethod
    def _get_status_code(response: HttpResponse):
        return response.status_code

    @staticmethod
    def _get_user_agent(request: HttpRequest):
        return request.META.get("HTTP_USER_AGENT", None)

    @staticmethod
    def _get_querystring(request: HttpRequest):
        return None if request.META.get("QUERY_STRING", None) == "" else request.META.get("QUERY_STRING", None)

    @staticmethod
    def _get_request_body(request: HttpRequest):
        return request.body.decode("utf-8") if request.body else None

    @staticmethod
    def _get_timestamp(unix_timestamp: float) -> datetime:
        return make_aware(datetime.fromtimestamp(unix_timestamp)) if settings.USE_TZ else datetime.fromtimestamp(
            unix_timestamp)

    @staticmethod
    def _get_duration(start_timestamp: float, end_timestamp: float) -> float:
        return end_timestamp - start_timestamp

    @staticmethod
    def _get_exception_type(exception: Exception) -> str:
        return exception.__class__.__name__

    @staticmethod
    def _get_traceback(exception: Exception) -> str:
        return ''.join(traceback.format_tb(exception.__traceback__))

    @staticmethod
    def _get_server_ip(request: HttpRequest):
        return request.get_host()

    @staticmethod
    def _get_client_ip(request: HttpRequest):
        return request.META.get("REMOTE_ADDR", None)
