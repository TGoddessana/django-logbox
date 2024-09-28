import pytest
from django.test import Client
from django.urls import reverse

from django_logbox.models import ServerLog


@pytest.mark.django_db
def test_ok_view_log_saved(client: Client):
    client.get(reverse("ok_view"))

    assert ServerLog.objects.count() == 1

    saved_log = ServerLog.objects.first()
    assert saved_log.method == "GET"
    assert saved_log.path == "/ok/"
    assert saved_log.status_code == 200
    assert saved_log.user_agent is None
    assert saved_log.querystring is None
    assert saved_log.request_body is None
    assert saved_log.exception is None
    assert saved_log.traceback is None
    assert saved_log.server_ip == "testserver"
    assert saved_log.client_ip == "127.0.0.1"


@pytest.mark.django_db
def test_ok_view_log_user_agent_saved(client: Client):
    client.get(reverse("ok_view"), HTTP_USER_AGENT="Mozilla/5.0")
    assert ServerLog.objects.count() == 1

    saved_log = ServerLog.objects.first()
    assert saved_log.user_agent == "Mozilla/5.0"


@pytest.mark.django_db
def test_ok_view_log_querystring_saved(client: Client):
    client.get(reverse("ok_view"), {"key": "value", "key2": "value2"})
    assert ServerLog.objects.count() == 1

    saved_log = ServerLog.objects.first()
    assert saved_log.querystring == "key=value&key2=value2"
