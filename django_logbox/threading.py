import logging
import time
import threading
from queue import Queue

from django_logbox.app_settings import app_settings

logger = logging.getLogger("logbox")


class ServerLogInsertThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from django_logbox.models import ServerLog

        self.serverlog_model = ServerLog
        self.daemon = True
        self._daemon_interval = app_settings.LOGGING_DAEMON_INTERVAL
        self._queue_size = app_settings.LOGGING_DAEMON_QUEUE_SIZE
        self._queue = Queue(maxsize=self._queue_size)

    def run(self) -> None:
        while True:
            try:
                time.sleep(self._daemon_interval)
                self._start_bulk_insertion()
            except Exception as e:
                logger.error(f"Error occurred while inserting logs: {e}")

    def put_serverlog(self, data) -> None:
        self._queue.put(self.serverlog_model(**data))

        if self._queue.qsize() >= self._queue_size:
            self._start_bulk_insertion()

    def _start_bulk_insertion(self):
        bulk_item = []
        while not self._queue.empty():
            bulk_item.append(self._queue.get())
        if bulk_item:
            self.serverlog_model.objects.bulk_create(bulk_item)


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
