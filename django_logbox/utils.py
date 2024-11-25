import traceback
from datetime import datetime
from http import HTTPStatus

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.utils.timezone import make_aware


def get_log_data(
    timestamp,
    request: HttpRequest,
    response: HttpResponse | None,
    exception: Exception | None = None,
) -> dict:
    data = {
        "method": _get_method(request),
        "path": _get_path(request),
        "user_agent": _get_user_agent(request),
        "querystring": _get_querystring(request),
        "request_body": _get_request_body(request),
        "timestamp": _get_timestamp(timestamp),
        "server_ip": _get_server_ip(request),
        "client_ip": _get_client_ip(request),
        "status_code": (
            # if response is None, return status code 500
            _get_status_code(response) if response else HTTPStatus.INTERNAL_SERVER_ERROR
        ),
    }

    if exception:
        exception_data = {
            "exception_type": _get_exception_type(exception),
            "exception_message": str(exception),
            "traceback": _get_traceback(exception),
        }
        data.update(exception_data)

    return data


def _get_method(request: HttpRequest):
    return request.method


def _get_path(request: HttpRequest):
    return request.path


def _get_status_code(response: HttpResponse):
    return response.status_code


def _get_user_agent(request: HttpRequest):
    return request.META.get("HTTP_USER_AGENT", None)


def _get_querystring(request: HttpRequest):
    return (
        None
        if request.META.get("QUERY_STRING", None) == ""
        else request.META.get("QUERY_STRING", None)
    )


def _get_request_body(request: HttpRequest):
    return request.body.decode("utf-8") if request.body else None


def _get_timestamp(unix_timestamp: float) -> datetime:
    return (
        make_aware(datetime.fromtimestamp(unix_timestamp))
        if settings.USE_TZ
        else datetime.fromtimestamp(unix_timestamp)
    )


def _get_exception_type(exception: Exception) -> str:
    return exception.__class__.__name__


def _get_traceback(exception: Exception) -> str:
    return "".join(traceback.format_tb(exception.__traceback__))


def _get_server_ip(request: HttpRequest):
    return request.get_host()


def _get_client_ip(request: HttpRequest):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip
