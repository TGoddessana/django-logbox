from django.db.models import (
    CharField,
    DateTimeField,
    GenericIPAddressField,
    IntegerField,
    Model,
    TextField,
)
from django.utils.translation import gettext_lazy as _


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
            "User agent string from the client's request header, providing browser and OS details."
        ),
        max_length=255,
        null=True,
    )
    querystring = TextField(
        _("querystring"),
        help_text=_(
            "Query parameters of the request as a URL-encoded string, e.g., 'param1=value1&param2=value2'."
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

    def __str__(self) -> str:
        return f"{self.timestamp} {self.method} {self.path} {self.status_code}"

    class Meta:
        verbose_name = _("Server Log")
        verbose_name_plural = _("Server Logs")
        ordering = ("-timestamp",)
