import logging
import threading
import time
from queue import Queue

logger = logging.getLogger("logbox")


class ServerLogInsertThread(threading.Thread):
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(ServerLogInsertThread, cls).__new__(cls)
        return cls._instance

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

    @staticmethod
    def get_instance():
        return ServerLogInsertThread._instance

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
