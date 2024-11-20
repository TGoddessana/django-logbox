from django.conf import settings

from http import HTTPStatus

DEFAULTS = {
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
    # The number of logs to insert in bulk. The default is 1, which means insert logs instantly.
    "LOGGING_DAEMON_QUEUE_SIZE": 1,
    # The number of seconds between log insertion attempts. The default is 0.
    "LOGGING_DAEMON_INTERVAL": 0,
}


class AppSettings:
    def __init__(self, defaults=None):
        self.defaults = defaults or {}
        self._user_settings = getattr(settings, "LOGBOX_SETTINGS", {})
        self._merged_settings = self._deep_merge(self.defaults, self._user_settings)

    def _deep_merge(self, defaults, user_settings):
        merged = defaults.copy()
        for key, value in user_settings.items():
            if isinstance(value, dict) and key in merged:
                merged[key] = self._deep_merge(merged[key], value)
            else:
                merged[key] = value
        return merged

    def __getattr__(self, name):
        if name not in self._merged_settings:
            raise AttributeError(f"Invalid setting: '{name}'")
        return self._merged_settings[name]


app_settings = AppSettings(DEFAULTS)
