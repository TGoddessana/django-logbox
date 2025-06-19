import os

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DjangoLogboxConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "django_logbox"
    verbose_name = _("Logbox")

    def ready(self):
        if self._is_main_process():
            from django_logbox.threading import logbox_logger_thread

            logbox_logger_thread.start()

    @staticmethod
    def _is_main_process() -> bool:
        """
        Check if the current process is the main process.

        This is used to ensure that the logging thread is started only in the main process.
        """
        return os.environ.get("RUN_MAIN") == "true"
