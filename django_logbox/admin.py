from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from ua_parser import parse

from .models import ServerLog


@admin.register(ServerLog)
class ServerLogAdmin(admin.ModelAdmin):
    list_display = (
        "method",
        "path",
        "status_code",
        "user_agent_summary",
        "timestamp",
        "exception_type",
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
    list_display_links = ("method", "path")
    search_fields = ("status_code", "exception_message")
    list_filter = ("method", "status_code", "path", "timestamp")

    @staticmethod
    @admin.display(description=_("User-Agent Summary"))
    def user_agent_summary(obj):
        if not obj.user_agent:
            return None
        _parsed_useragent_result = parse(obj.user_agent)

        device_summary = (
            _parsed_useragent_result.device.family
            if _parsed_useragent_result.device
            else "X"
        )
        os_summary = (
            _parsed_useragent_result.os.family
            if _parsed_useragent_result.device
            else "X"
        )
        user_agent_summary = (
            _parsed_useragent_result.user_agent.family
            if _parsed_useragent_result.os
            else "X"
        )

        return f"{device_summary}, {os_summary}, {user_agent_summary}"

    @staticmethod
    @admin.display(description=_("User-Agent Details"))
    def user_agent_details(obj):
        if not obj.user_agent:
            return None
        _parsed_useragent_result = parse(obj.user_agent)

        device_details = (
            f"Device: {_parsed_useragent_result.device.family}({_parsed_useragent_result.device.brand}, {_parsed_useragent_result.device.model})"
            if _parsed_useragent_result.device
            else _("No device data found.")
        )
        os_details = (
            f"OS: {_parsed_useragent_result.os.family}({_parsed_useragent_result.os.major}.{_parsed_useragent_result.os.minor}.{_parsed_useragent_result.os.patch})"
            if _parsed_useragent_result.os
            else _("No OS data fount.")
        )
        user_agent_details = (
            f"User-Agent: {_parsed_useragent_result.user_agent.family}({_parsed_useragent_result.os.major}.{_parsed_useragent_result.os.minor}.{_parsed_useragent_result.os.patch})"
            if _parsed_useragent_result.os
            else _("No User-Agent data found.")
        )

        return format_html(
            f"<p>{obj.user_agent}</p>"
            f"<li>{device_details}</li>"
            f"<li>{os_details}</li>"
            f"<li>{user_agent_details}</li>"
        )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
