import traceback

from django.http import HttpRequest, HttpResponse
from ua_parser import Result

########################
# Django request utils #
########################


def get_method(request: HttpRequest):
    return request.method


def get_path(request: HttpRequest):
    return request.path


def get_status_code(response: HttpResponse):
    return response.status_code


def get_user_agent(request: HttpRequest) -> str | None:
    return request.META.get("HTTP_USER_AGENT", None)


def get_querystring(request: HttpRequest):
    return (
        None
        if request.META.get("QUERY_STRING", None) == ""
        else request.META.get("QUERY_STRING", None)
    )


def get_request_body(request: HttpRequest):
    return request.body.decode("utf-8") if request.body else None


def get_exception_type(exception: Exception) -> str:
    return exception.__class__.__name__


def get_traceback(exception: Exception) -> str:
    return "".join(traceback.format_tb(exception.__traceback__))


def get_server_ip(request: HttpRequest):
    return request.get_host()


def get_client_ip(request: HttpRequest):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


############################
# User-Agent parsing utils #
#############################


def device_str(parsed_useragent: Result) -> str | None:
    """
    extract device data from parsed useragent.

    for example: Mac(Apple, Mac), Samsung SM-S711N(Samsung, SM-S711N)
    """
    if not parsed_useragent.device:
        return None

    family = parsed_useragent.device.family if parsed_useragent.device.family else ""

    brand = parsed_useragent.device.brand if parsed_useragent.device.brand else ""
    model = parsed_useragent.device.model if parsed_useragent.device.model else ""

    return f"{family}({brand}, {model})" if brand and model else family


def os_str(parsed_useragent: Result) -> str | None:
    """
    extract OS data from parsed useragent.

    for example: Windows(10), Mac OS X(10.15.7), SomeOS
    """
    if not parsed_useragent.os:
        return None

    family = parsed_useragent.os.family if parsed_useragent.os.family else ""

    version_information = [
        parsed_useragent.os.major,
        parsed_useragent.os.minor,
        parsed_useragent.os.patch,
        parsed_useragent.os.patch_minor,
    ]
    version_suffix = ".".join(list(filter(None, version_information)))

    return f"{family}({version_suffix})" if version_suffix else family


def browser_str(parsed_useragent: Result) -> str | None:
    """
    extract browser data from parsed useragent.

    for example: Chrome(86), Safari(13.1.2), SomeBrowser
    """
    if not parsed_useragent.user_agent:
        return None

    family = (
        parsed_useragent.user_agent.family if parsed_useragent.user_agent.family else ""
    )

    version_information = [
        parsed_useragent.user_agent.major,
        parsed_useragent.user_agent.minor,
        parsed_useragent.user_agent.patch,
        parsed_useragent.user_agent.patch_minor,
    ]
    version_suffix = ".".join(list(filter(None, version_information)))

    return f"{family}({version_suffix})" if version_suffix else family
