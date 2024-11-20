import os
from http import HTTPStatus

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = "LIFE_IS_SUFFERING"

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # install djanog_logbox for testing
    "django_logbox",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    # django_logbox supports i18n
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # add LogboxMiddleware to MIDDLEWARE
    "django_logbox.middlewares.LogboxMiddleware",
]

ROOT_URLCONF = "example_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "example_project.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

STATIC_URL = "/static/"

USE_TZ = True

LOGBOX_SETTINGS = {
    # HTTP methods to log. Default to all
    "LOGGING_HTTP_METHODS": ["GET", "POST", "PUT", "PATCH", "DELETE"],
    # IP addresses to log. Default to all
    "LOGGING_SERVER_IP": ["*"],
    # IP addresses to log. Default to all
    "LOGGING_CLIENT_IP": ["*"],
    # Status codes to log. Default to all
    "LOGGING_STATUS_CODES": [http_code.value for http_code in HTTPStatus],
    # Path regex to log. Default to all
    "LOGGING_PATHS_REGEX": r"^/.*$",
    # Path regex to exclude from logging. Default to exclude admin
    "LOGGING_EXCLUDE_PATHS_REGEX": r"^/admin/.*$",
    # Queue size, 0 if you want to log instantly
    "LOGGING_DAEMON_QUEUE_SIZE": 3,
    # Interval time to log, in seconds. 0 if you want to log instantly
    "LOGGING_DAEMON_INTERVAL": 10,
}
