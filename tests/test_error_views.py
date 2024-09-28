import pytest
from django.test import Client
from django.urls import reverse

from django_logbox.models import ServerLog


@pytest.mark.django_db
def test_error_view_logger(client: Client):
    client.get(reverse("404_view"))
    assert ServerLog.objects.count() == 1


@pytest.mark.django_db
def test_unexpected_error_view_logger(client: Client):
    client.raise_request_exception = False

    client.get(reverse("unexpected_error_view"))
    assert ServerLog.objects.count() == 1
    print(ServerLog.objects.first().traceback)
