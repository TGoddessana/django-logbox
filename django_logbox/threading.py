import logging
import signal
import threading
import time
from queue import Queue
from types import FrameType

from django_logbox.app_settings import settings

logger = logging.getLogger("logbox")


class ServerLogInsertThread(threading.Thread):
    def __init__(
        self,
        logging_daemon_interval: int,
        logging_daemon_queue_size: int,
    ):
        super().__init__(
            name="logbox_logger_thread",
            daemon=True,
        )
        from django_logbox.models import ServerLog

        self._serverlog_model = ServerLog
        self._logging_daemon_interval = logging_daemon_interval
        self._logging_daemon_queue_size = logging_daemon_queue_size
        self._queue = Queue(maxsize=self._logging_daemon_queue_size)

        self._stop_event = threading.Event()
        signal.signal(signal.SIGINT, self._exit_gracefully)
        signal.signal(signal.SIGTERM, self._exit_gracefully)

    def run(self) -> None:
        """
        Continuously runs the logging thread, periodically inserting logs in bulk.

        This method sleeps for the specified interval (`_logging_daemon_interval`)
        and then triggers the bulk insertion of logs from the queue. If an exception
        occurs during the process, it logs the error.
        """
        while not self._stop_event.is_set():
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

    def _start_bulk_insertion(self):
        bulk_item = []
        while not self._queue.empty():
            bulk_item.append(self._queue.get())
        if bulk_item:
            self._serverlog_model.objects.bulk_create(bulk_item)

    def _exit_gracefully(
        self,
        sig: int,
        frame: FrameType | None,
    ) -> None:
        logger.info(f"Received signal {sig}. Exiting gracefully...")
        self._stop_event.set()
        self._start_bulk_insertion()
        logger.info("All logs have been inserted. Exiting.")
        exit(0)


logbox_logger_thread = ServerLogInsertThread(
    logging_daemon_interval=settings.LOGBOX_SETTINGS["LOGGING_DAEMON_INTERVAL"],
    logging_daemon_queue_size=settings.LOGBOX_SETTINGS["LOGGING_DAEMON_QUEUE_SIZE"],
)
