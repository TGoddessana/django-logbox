import signal
import threading
import time
from unittest import mock

import pytest

from django_logbox.threading import ServerLogInsertThread


@pytest.fixture
def fake_serverlog_model():
    class FakeServerLog:
        objects = mock.Mock()

        def __init__(self, **kwargs):
            self.data = kwargs

    return FakeServerLog


@pytest.fixture
def thread(fake_serverlog_model):
    thread = ServerLogInsertThread(
        logging_daemon_interval=0.01,
        logging_daemon_queue_size=2,
    )
    thread._serverlog_model = fake_serverlog_model
    return thread


def test_put_serverlog_and_bulk_insert(thread):
    thread._serverlog_model.objects.bulk_create.reset_mock()
    thread.put_serverlog({"foo": "bar"})
    assert thread._queue.qsize() == 1
    thread.put_serverlog({"foo": "baz"})
    thread._serverlog_model.objects.bulk_create.assert_called_once()
    assert thread._queue.qsize() == 0


def test_start_bulk_insertion(thread):
    thread._serverlog_model.objects.bulk_create.reset_mock()
    thread.put_serverlog({"foo": "a"})
    thread.put_serverlog({"foo": "b"})
    thread._start_bulk_insertion()
    thread._serverlog_model.objects.bulk_create.assert_called_once()
    assert thread._queue.qsize() == 0


def test_exit_gracefully(thread):
    thread._serverlog_model.objects.bulk_create.reset_mock()
    thread.put_serverlog({"foo": "a"})
    with mock.patch("django_logbox.threading.exit", side_effect=SystemExit) as m_exit:
        with pytest.raises(SystemExit):
            thread._exit_gracefully(signal.SIGTERM, None)
    thread._serverlog_model.objects.bulk_create.assert_called_once()
    assert thread._stop_event.is_set()
    m_exit.assert_called_once_with(0)


def test_run_bulk_insertion_called(thread, monkeypatch):
    thread._serverlog_model.objects.bulk_create.reset_mock()
    thread.put_serverlog({"foo": "bar"})

    # stop 이벤트를 짧은 시간 후 set하도록 패치
    original_sleep = time.sleep

    def fake_sleep(interval):
        thread._stop_event.set()
        original_sleep(0)

    monkeypatch.setattr(time, "sleep", fake_sleep)

    thread.run()
    thread._serverlog_model.objects.bulk_create.assert_called()


def test_run_logs_error_on_exception(thread, monkeypatch):
    thread.put_serverlog({"foo": "bar"})
    # bulk_create가 예외를 발생시키도록 설정
    thread._serverlog_model.objects.bulk_create.side_effect = Exception("DB Error")

    # logger.error를 mock
    with mock.patch("django_logbox.threading.logger") as mock_logger:

        def fake_sleep(interval):
            thread._stop_event.set()

        monkeypatch.setattr(time, "sleep", fake_sleep)

        thread.run()
        # logger.error가 호출되었는지 확인
        assert mock_logger.error.called
        assert (
            "Error occurred while inserting logs" in mock_logger.error.call_args[0][0]
        )
