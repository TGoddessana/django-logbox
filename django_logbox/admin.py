from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import ServerLog


@admin.register(ServerLog)
class ServerLogAdmin(admin.ModelAdmin):
    list_display = (
        "method",
        "path",
        "status_code",
        "device",
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
                    "user_agent_details",
                    "status_code",
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

    @admin.display(description=_("User-Agent details"))
    def user_agent_details(self, obj):
        return format_html(
            f"<p>{obj.user_agent}</p>"
            f"<li>Device: {obj.device}</li>"
            f"<li>OS: {obj.os}</li>"
            f"<li>Browser: {obj.browser}</li>"
        )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
