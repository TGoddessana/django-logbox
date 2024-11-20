from django.http import HttpRequest, HttpResponse


def ok_view(request: HttpRequest) -> HttpResponse:
    return HttpResponse("OK")


def handled_error_view(request: HttpRequest) -> HttpResponse:
    return HttpResponse("ERROR", status=500)


def unhandled_error_view(request: HttpRequest) -> HttpResponse:
    1 / 0
    return HttpResponse("ERROR")
