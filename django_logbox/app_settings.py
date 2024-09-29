from django.conf import settings

DEFAULTS = {
    "LOGGING_HTTP_METHODS": ["GET", "POST", "PUT", "PATCH", "DELETE"],
}


class AppSettings:
    def __init__(self, defaults=None):
        self.defaults = defaults or {}
        self._user_settings = getattr(settings, "GLOBALRESPONSE_SETTINGS", {})
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
