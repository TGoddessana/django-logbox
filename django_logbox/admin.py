from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import ServerLog


@admin.register(ServerLog)
class ServerLogAdmin(admin.ModelAdmin):
    list_display = (
        "method",
        "path",
        "status_code",
        "short_user_agent",
        "timestamp",
        "exception_type",
        "exception_message",
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
                    "user_agent",
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

    search_fields = ("status_code", "exception_message")
    list_filter = ("method", "status_code", "timestamp")

    @staticmethod
    @admin.display(description=_("User Agent"))
    def short_user_agent(obj):
        max_length = 30
        return (
            (obj.user_agent[:max_length] + "...")
            if len(obj.user_agent) > max_length
            else obj.user_agent
        )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
