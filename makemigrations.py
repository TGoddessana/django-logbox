import django
from django.conf import settings
from django.core.management import call_command

settings.configure(
    DEBUG=True,
    INSTALLED_APPS=(
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django_logbox",
    ),
)

django.setup()
call_command("makemigrations", "django_logbox")
