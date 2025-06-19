from django.http import HttpRequest

from django_logbox.logging import add_log


class LogboxMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        response = self.get_response(request)

        add_log(
            request=request,
            response=response,
            exception=None,
        )

        return response

    def process_exception(self, request: HttpRequest, exception: Exception):
        add_log(
            request=request,
            response=None,
            exception=exception,
        )
