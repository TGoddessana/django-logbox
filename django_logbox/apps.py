from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DjangoLogboxConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "django_logbox"
    verbose_name = _("Logbox")
