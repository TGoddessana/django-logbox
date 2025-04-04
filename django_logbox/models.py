from django.conf import settings
from django.db.models import (
    SET_NULL,
    CharField,
    Count,
    DateTimeField,
    F,
    FloatField,
    ForeignKey,
    GenericIPAddressField,
    IntegerField,
    Model,
    QuerySet,
    TextField,
)
from django.db.models.functions import Cast, TruncDate
from django.utils.translation import gettext_lazy as _


class ServerLogQuerySet(QuerySet):
    def get_traffic_data(self):
        return (
            ServerLog.objects.annotate(date=TruncDate("timestamp"))
            .values("date")
            .annotate(count=Count("id"))
            .order_by("date")
        )

    def get_status_code_data(self):
        total_count = ServerLog.objects.aggregate(total=Count("id"))["total"]

        queryset = (
            ServerLog.objects.values("status_code")
            .annotate(count=Count("id"))
            .annotate(percentage=Cast(F("count"), FloatField()) * 100.0 / total_count)
            .order_by("status_code")
        )
        return queryset

    def get_device_data(self):
        total_count = ServerLog.objects.aggregate(total=Count("id"))["total"]

        queryset = (
            ServerLog.objects.values("device")
            .annotate(count=Count("id"))
            .annotate(percentage=Cast(F("count"), FloatField()) * 100.0 / total_count)
            .order_by("-count")[:10]
        )
        return queryset

    def get_os_data(self):
        total_count = ServerLog.objects.aggregate(total=Count("id"))["total"]

        queryset = (
            ServerLog.objects.values("os")
            .annotate(count=Count("id"))
            .annotate(percentage=Cast(F("count"), FloatField()) * 100.0 / total_count)
            .order_by("-count")[:10]
        )
        return queryset

    def get_browser_data(self):
        total_count = ServerLog.objects.aggregate(total=Count("id"))["total"]

        queryset = (
            ServerLog.objects.values("browser")
            .annotate(count=Count("id"))
            .annotate(percentage=Cast(F("count"), FloatField()) * 100.0 / total_count)
            .order_by("-count")[:10]
        )
        return queryset


class ServerLog(Model):
    # http
    method = CharField(
        _("method"),
        help_text=_("HTTP method used for the request, e.g., 'GET', 'POST', 'PUT'."),
        max_length=10,
    )
    path = CharField(
        _("path"),
        help_text=_(
            "The endpoint path requested, excluding the domain, e.g., '/api/v1/users/'."
        ),
        max_length=255,
    )
    status_code = IntegerField(
        _("status_code"),
        help_text=_("HTTP status code of the response, e.g., 200, 404, 500."),
    )
    user_agent = TextField(
        _("user_agent"),
        help_text=_(
            "User-Agent string from the client's request header, providing browser and OS details."
        ),
        max_length=255,
        null=True,
    )

    # for example: Mac(Apple, Mac) , Samsung SM-S711N(Samsung, SM-S711N)
    device = CharField(
        _("device"),
        help_text=_("Device data parsed from User-Agent request header."),
        max_length=255,
        null=True,
        blank=True,
    )
    # for example: Android(14), iOS(13.2.3), Windows(10)
    os = CharField(
        _("os"),
        help_text=_("OS data parsed from User-Agent request header."),
        max_length=255,
        null=True,
        blank=True,
    )
    # for example: Yeti(10), Mobile Safari(13.2.3)
    browser = CharField(
        _("browser"),
        help_text=_("Browser data parsed from User-Agent request header."),
        max_length=255,
        null=True,
        blank=True,
    )

    querystring = TextField(
        _("querystring"),
        help_text=_(
            "Query parameters of the request as a URL-encoded string, e.g., 'param1=value1&ampparam2=value2'."
        ),
        null=True,
    )
    request_body = TextField(
        _("request_body"),
        help_text=_(
            "Body content of the request, usually JSON or form data. Null if no body was sent."
        ),
        null=True,
    )

    # log
    timestamp = DateTimeField(
        _("timestamp"),
        help_text=_("Date and time when this log entry was created."),
    )
    exception_type = CharField(
        _("exception_type"),
        help_text=_("Class name or type of the exception, if any occurred."),
        max_length=255,
        null=True,
    )
    exception_message = TextField(
        _("exception_message"),
        help_text=_("Detailed message provided by the exception."),
        null=True,
    )
    traceback = TextField(
        _("traceback"),
        help_text=_("Full traceback of the exception for debugging purposes."),
        null=True,
    )

    # ip
    server_ip = GenericIPAddressField(
        _("server_ip"), help_text=_("IP address of the server handling the request.")
    )
    client_ip = GenericIPAddressField(
        _("client_ip"), help_text=_("IP address of the client making the request.")
    )

    # user
    user = ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=SET_NULL,
        null=True,
        blank=True,
        related_name="server_logs",
        help_text=_("User associated with the request, if authenticated."),
    )

    # object manager
    objects = ServerLogQuerySet.as_manager()

    def __str__(self) -> str:
        return f"{self.timestamp} {self.method} {self.path} {self.status_code}"

    class Meta:
        verbose_name = _("Server Log")
        verbose_name_plural = _("Server Logs")
        ordering = ("-timestamp",)
