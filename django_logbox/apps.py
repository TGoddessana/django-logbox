from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DjangoLogboxConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "django_logbox"
    verbose_name = _("Logbox")

    def ready(self):
        from django_logbox.app_settings import settings
        from django_logbox.threading import ServerLogInsertThread

        logbox_thread = ServerLogInsertThread(
            logging_daemon_interval=settings.LOGBOX_SETTINGS["LOGGING_DAEMON_INTERVAL"],
            logging_daemon_queue_size=settings.LOGBOX_SETTINGS[
                "LOGGING_DAEMON_QUEUE_SIZE"
            ],
        )
        logbox_thread.start()
