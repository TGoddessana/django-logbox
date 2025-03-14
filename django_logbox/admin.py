from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from ua_parser import Result, parse

from .models import ServerLog


@admin.register(ServerLog)
class ServerLogAdmin(admin.ModelAdmin):
    list_display = (
        "method",
        "path",
        "status_code",
        "user_agent_summary",
        "timestamp",
        "server_ip",
        "client_ip",
    )

    readonly_fields = (
        "method",
        "path",
        "status_code",
        "user_agent",
        "querystring",
        "request_body",
        "timestamp",
        "exception_type",
        "exception_message",
        "traceback",
        "server_ip",
        "client_ip",
    )

    fieldsets = (
        (
            _("Request Information"),
            {
                "fields": (
                    "timestamp",
                    "method",
                    "path",
                    "status_code",
                    "user_agent_details",
                    "querystring",
                    "request_body",
                ),
            },
        ),
        (
            _("Exception Details"),
            {
                "fields": (
                    "exception_type",
                    "exception_message",
                    "traceback",
                ),
            },
        ),
        (
            _("IP Addresses"),
            {
                "fields": (
                    "server_ip",
                    "client_ip",
                ),
            },
        ),
    )
    list_display_links = (
        "method",
        "path",
    )
    search_fields = (
        "status_code",
        "exception_message",
        "client_ip",
        "server_ip",
    )
    list_filter = (
        "method",
        "status_code",
        "path",
        "timestamp",
    )

    @admin.display(description=_("User-Agent Summary"))
    def user_agent_summary(self, obj):
        if not obj.user_agent:
            return None
        return self._get_useragent_summary(parse(obj.user_agent))

    @admin.display(description=_("User-Agent Details"))
    def user_agent_details(self, obj):
        if not obj.user_agent:
            return None
        _parsed_useragent_result = parse(obj.user_agent)

        _details = self._get_useragent_details(_parsed_useragent_result)

        return format_html(
            f"<p>{obj.user_agent}</p>"
            f"<li>{_details["device"]}</li>"
            f"<li>{_details["os"]}</li>"
            f"<li>{_details["user-agent"]}</li>"
        )

    @staticmethod
    def _get_useragent_summary(parsed_useragent_result: Result):
        device_summary = (
            parsed_useragent_result.device.family
            if parsed_useragent_result.device
            else "X"
        )
        os_summary = (
            parsed_useragent_result.os.family if parsed_useragent_result.os else "X"
        )
        user_agent_summary = (
            parsed_useragent_result.user_agent.family
            if parsed_useragent_result.user_agent
            else "X"
        )
        return f"{device_summary}/{os_summary}/{user_agent_summary}"

    def _get_useragent_details(self, parsed_useragent_result: Result):
        device_details = (
            f"Device: {parsed_useragent_result.device.family}"
            f"("
            f"{parsed_useragent_result.device.brand}, {parsed_useragent_result.device.model}"
            f")"
            if parsed_useragent_result.device
            else _("No device data found.")
        )
        os_details = (
            f"OS: {parsed_useragent_result.os.family}"
            f"("
            f"{self._empty_str_if_none(parsed_useragent_result.os.major)}."
            f"{self._empty_str_if_none(parsed_useragent_result.os.minor)}."
            f"{self._empty_str_if_none(parsed_useragent_result.os.patch)}"
            f")"
            if parsed_useragent_result.os
            else _("No OS data found.")
        )
        user_agent_details = (
            f"User-Agent: {parsed_useragent_result.user_agent.family}"
            f"("
            f"{self._empty_str_if_none(parsed_useragent_result.os.major)}."
            f"{self._empty_str_if_none(parsed_useragent_result.os.minor)}."
            f"{self._empty_str_if_none(parsed_useragent_result.os.patch)}"
            f")"
            if parsed_useragent_result.user_agent
            else _("No User-Agent data found.")
        )

        return {
            "device": device_details,
            "os": os_details,
            "user_agent": user_agent_details,
        }

    @staticmethod
    def _empty_str_if_none(value):
        if value is None:
            return ""
        return value

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
