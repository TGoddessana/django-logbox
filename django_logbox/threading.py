import logging
import time
import threading
from queue import Queue

from django_logbox.app_settings import app_settings

logger = logging.getLogger("logbox")


class ServerLogInsertThread(threading.Thread):
    def __init__(
        self,
        logging_daemon_interval=app_settings.LOGGING_DAEMON_INTERVAL,
        logging_daemon_queue_size=app_settings.LOGGING_DAEMON_QUEUE_SIZE,
    ):
        super().__init__(daemon=True)
        from django_logbox.models import ServerLog

        self.serverlog_model = ServerLog
        from django.conf import settings

        self._logging_daemon_interval = settings.LOGBOX_SETTINGS.get(
            "LOGGING_DAEMON_INTERVAL", logging_daemon_interval
        )
        self._logging_daemon_queue_size = settings.LOGBOX_SETTINGS.get(
            "LOGGING_DAEMON_QUEUE_SIZE", logging_daemon_queue_size
        )
        self._queue = Queue(maxsize=self._logging_daemon_queue_size)

    def run(self) -> None:
        while True:
            try:
                time.sleep(self._logging_daemon_interval)
                self._start_bulk_insertion()
            except Exception as e:
                logger.error(f"Error occurred while inserting logs: {e}")

    def put_serverlog(self, data) -> None:
        self._queue.put(self.serverlog_model(**data))
        if self._queue.qsize() >= self._logging_daemon_queue_size:
            self._start_bulk_insertion()

    def _start_bulk_insertion(self):
        bulk_item = []
        while not self._queue.empty():
            bulk_item.append(self._queue.get())
        if bulk_item:
            self.serverlog_model.objects.bulk_create(bulk_item)


def get_logbox_thread():
    logger_thread = None
    log_thread_name = "logbox_thread"
    already_exists = False

    for t in threading.enumerate():
        if t.name == log_thread_name:
            already_exists = True
            break

    if not already_exists:
        t = ServerLogInsertThread()
        t.name = log_thread_name
        t.start()
        logger_thread = t

    return logger_thread
