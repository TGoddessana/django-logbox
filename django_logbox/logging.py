from datetime import datetime
from http import HTTPStatus

from django.http import HttpRequest, HttpResponse
from django.utils import timezone
from ua_parser import parse

from django_logbox.filtering import LogboxLogFilter
from django_logbox.threading import logbox_logger_thread
from django_logbox.utils import (
    browser_str,
    device_str,
    get_client_ip,
    get_exception_type,
    get_method,
    get_path,
    get_querystring,
    get_request_body,
    get_server_ip,
    get_status_code,
    get_traceback,
    get_user_agent,
    os_str,
)


def add_log(
    request: HttpRequest,
    response: HttpResponse | None,
    exception: Exception | None = None,
) -> None:
    """
    Add log data to the serverlog.
    add queue to the server log thread and mark the request as logged.
    """
    if LogboxLogFilter.should_filter_log(request, response):
        return

    logbox_logger_thread.put_serverlog(
        data=get_log_data(
            timestamp=timezone.now(),
            request=request,
            response=response,
            exception=exception,
        )
    )
    request.logbox_logged = True


def get_log_data(
    timestamp: datetime,
    request: HttpRequest,
    response: HttpResponse | None,
    exception: Exception | None = None,
) -> dict:
    _raw_user_agent = get_user_agent(request)

    data = {
        "method": get_method(request),
        "path": get_path(request),
        "user_agent": _raw_user_agent,
        "device": device_str(parse(_raw_user_agent)) if _raw_user_agent else None,
        "os": os_str(parse(_raw_user_agent)) if _raw_user_agent else None,
        "browser": browser_str(parse(_raw_user_agent)) if _raw_user_agent else None,
        "querystring": get_querystring(request),
        "request_body": get_request_body(request),
        "timestamp": timestamp,
        "server_ip": get_server_ip(request),
        "client_ip": get_client_ip(request),
        "status_code": (
            # if response is None, return status code 500.
            # This happens when an exception occurs and response is not set from middleware.process_exception
            get_status_code(response) if response else HTTPStatus.INTERNAL_SERVER_ERROR
        ),
        "user": request.user if request.user.is_authenticated else None,
    }

    if exception:
        exception_data = {
            "exception_type": get_exception_type(exception),
            "exception_message": str(exception),
            "traceback": get_traceback(exception),
        }
        data.update(exception_data)

    return data
