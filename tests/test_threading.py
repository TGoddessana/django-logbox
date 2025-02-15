import pytest

from django_logbox.models import ServerLog
from django_logbox.threading import ServerLogInsertThread


@pytest.mark.django_db(transaction=True)
def test_log_inserted_when_queue_is_full(log_data):
    logbox_thread = ServerLogInsertThread(
        logging_daemon_interval=0,
        logging_daemon_queue_size=1,
    )
    logbox_thread.start()

    for _ in range(3):
        logbox_thread.put_serverlog(log_data)

    assert ServerLog.objects.count() == 3


@pytest.mark.django_db(transaction=True)
def test_log_not_inserted_when_queue_is_not_full(log_data):
    logbox_thread = ServerLogInsertThread(
        logging_daemon_interval=0,
        logging_daemon_queue_size=3,
    )
    logbox_thread.start()

    for _ in range(3):
        logbox_thread.put_serverlog(log_data)

    assert ServerLog.objects.count() == 3
