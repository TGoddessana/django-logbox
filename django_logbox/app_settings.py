from django.conf import settings

from http import HTTPStatus

DEFAULTS = {
    # default to all http methods
    "LOGGING_HTTP_METHODS": ["GET", "POST", "PUT", "PATCH", "DELETE"],
    # default to all http status codes
    "LOGGING_STATUS_CODES": [http_code.value for http_code in HTTPStatus],
    # default to all paths
    "LOGGING_PATHS_REGEX": r"^/.*$",
    # default to exclude admin paths
    "LOGGING_EXCLUDE_PATHS_REGEX": r"^/admin/.*$",
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
