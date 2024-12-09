import time
from datetime import datetime
from queue import Queue
from unittest.mock import patch, MagicMock

import pytest
from django.test import override_settings

from django_logbox.models import ServerLog
from django_logbox.threading import get_logbox_thread


@pytest.fixture
def logbox_thread(settings):
    thread = get_logbox_thread()
    yield thread


@pytest.fixture
def log_data():
    return {
        "method": "GET",
        "path": "/test-path",
        "status_code": 200,
        "user_agent": "test-agent",
        "querystring": None,
        "request_body": None,
        "timestamp": datetime.fromtimestamp(time.time()),
        "exception_type": None,
        "exception_message": None,
        "traceback": None,
        "server_ip": "127.0.0.1",
        "client_ip": "127.0.0.1",
    }


@pytest.mark.django_db(transaction=True)
def test_put_serverlog(logbox_thread, log_data):
    with patch.object(logbox_thread, "_queue", new_callable=Queue) as mock_queue:
        mock_queue.put = MagicMock()
        logbox_thread.put_serverlog(log_data)
        assert mock_queue.put.called
        args, _ = mock_queue.put.call_args
        assert isinstance(args[0], ServerLog)


@pytest.mark.django_db(transaction=True)
@override_settings(
    LOGBOX_SETTINGS={
        "LOGGING_DAEMON_QUEUE_SIZE": 2,
    }
)
def test_serverlog_inserted_with_max_queue_size(settings, log_data):
    from django_logbox.app_settings import app_settings

    print(app_settings)
    print(settings.LOGBOX_SETTINGS)
    thread = get_logbox_thread()
    print(thread._logging_daemon_queue_size)
