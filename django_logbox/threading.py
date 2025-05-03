import logging
import threading
import time
from queue import Queue

from django.db import close_old_connections

from django_logbox.app_settings import settings

logger = logging.getLogger("logbox")


class ServerLogInsertThread(threading.Thread):
    def __init__(
        self,
        logging_daemon_interval: int,
        logging_daemon_queue_size: int,
        name: str = "logbox_logger_thread",
    ):
        super().__init__(name=name, daemon=True)
        from django_logbox.models import ServerLog

        self._serverlog_model = ServerLog
        self._logging_daemon_interval = logging_daemon_interval
        self._logging_daemon_queue_size = logging_daemon_queue_size
        self._queue = Queue(maxsize=self._logging_daemon_queue_size)

    def run(self) -> None:
        while True:
            try:
                time.sleep(self._logging_daemon_interval)
                self._start_bulk_insertion()
            except Exception as e:
                logger.error(f"Error occurred while inserting logs: {e}")

    def put_serverlog(self, data) -> None:
        self._queue.put(self._serverlog_model(**data))
        if self._queue.qsize() >= self._logging_daemon_queue_size:
            logger.debug(
                f"Queue is full({self._queue.qsize()}), starting bulk insertion"
            )
            self._start_bulk_insertion()

    def start(self):
        close_old_connections()

        for t in threading.enumerate():
            if t.name == self.name:
                return
        super().start()
        logger.info(f"Logbox logger thread started: {self.name}")

    def _start_bulk_insertion(self):
        bulk_item = []
        while not self._queue.empty():
            bulk_item.append(self._queue.get())
        if bulk_item:
            self._serverlog_model.objects.bulk_create(bulk_item)


logbox_logger_thread = ServerLogInsertThread(
    logging_daemon_interval=settings.LOGBOX_SETTINGS["LOGGING_DAEMON_INTERVAL"],
    logging_daemon_queue_size=settings.LOGBOX_SETTINGS["LOGGING_DAEMON_QUEUE_SIZE"],
)
