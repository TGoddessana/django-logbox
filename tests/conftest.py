from datetime import datetime

import django
import pytest
from django.test import RequestFactory


def pytest_configure(config):
    from django.conf import settings

    settings.configure(
        DEBUG=True,
        DEBUG_PROPAGATE_EXCEPTIONS=False,  # we need this to be False to test 500 errors
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": ":memory:",
            },
        },
        SECRET_KEY="life is suffering",
        STATIC_URL="/static/",
        ROOT_URLCONF="tests.urls",
        TEMPLATES=[
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "APP_DIRS": True,
                "OPTIONS": {
                    "debug": True,
                },
            },
        ],
        MIDDLEWARE=(
            "django.middleware.security.SecurityMiddleware",
            "django.contrib.sessions.middleware.SessionMiddleware",
            "django.middleware.common.CommonMiddleware",
            "django.middleware.csrf.CsrfViewMiddleware",
            "django.contrib.auth.middleware.AuthenticationMiddleware",
            "django.contrib.messages.middleware.MessageMiddleware",
            "django.middleware.clickjacking.XFrameOptionsMiddleware",
            "django_logbox.middlewares.LogboxMiddleware",
        ),
        INSTALLED_APPS=(
            "django.contrib.admin",
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sessions",
            "django.contrib.sites",
            "django.contrib.staticfiles",
            "django_logbox",
            "tests",
        ),
        PASSWORD_HASHERS=("django.contrib.auth.hashers.MD5PasswordHasher",),
    )

    django.setup()


@pytest.fixture
def factory():
    return RequestFactory()


@pytest.fixture
def log_data():
    return {
        "method": "GET",
        "path": "/test-path",
        "status_code": 200,
        "user_agent": "test-agent",
        "querystring": None,
        "request_body": None,
        "timestamp": datetime(2001, 12, 24, 0, 0, 0),
        "exception_type": None,
        "exception_message": None,
        "traceback": None,
        "server_ip": "127.0.0.1",
        "client_ip": "127.0.0.1",
    }
