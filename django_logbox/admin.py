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

        result = parse(obj.user_agent)
        return f"{result.device.family}, {result.os.family}, {result.user_agent.family}"

    @staticmethod
    @admin.display(description=_("User-Agent Details"))
    def user_agent_details(obj):
        if not obj.user_agent:
            return None
        result = parse(obj.user_agent)

        device_details = f"Device: {result.device.family}({result.device.brand}, {result.device.model})"
        os_details = f"OS: {result.os.family}({result.os.major}.{result.os.minor}.{result.os.patch})"
        user_agent_details = f"User-Agent: {result.user_agent.family}({result.os.major}.{result.os.minor}.{result.os.patch})"

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
