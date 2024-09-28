from django.urls import path
from django.http import HttpResponse


def _404_view(request):
    return HttpResponse(status=404, content="Not found")


def _200_view(request):
    return HttpResponse(status=200, content="OK")


def _500_view(request):
    raise Exception("Unexpected error")


urlpatterns = [
    path("error/", _404_view, name="404_view"),
    path("ok/", _200_view, name="ok_view"),
    path("unexpected_error/", _500_view, name="unexpected_error_view"),
]
