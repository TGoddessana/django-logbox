from django.db.models import (
    Model,
    TextField,
    DateTimeField,
    CharField,
    GenericIPAddressField,
    IntegerField, DecimalField,
)
from django.utils.translation import gettext_lazy as _


class ServerLog(Model):
    # http
    method = CharField(_("method"), max_length=10)
    path = CharField(_("path"), max_length=255)
    status_code = IntegerField(_("status_code"))
    user_agent = CharField(_("user_agent"), max_length=255, null=True)
    querystring = TextField(_("querystring"), null=True)
    request_body = TextField(_("request_body"), null=True)

    # log
    timestamp = DateTimeField(_("timestamp"))
    duration = DecimalField(_("duration"), max_digits=10, decimal_places=6)
    exception = TextField(_("exception"), null=True)
    traceback = TextField(_("traceback"), null=True)

    # server
    server_ip = GenericIPAddressField(_("server_ip"))
    client_ip = GenericIPAddressField(_("client_ip"))

    def __str__(self) -> str:
        return f"{self.method} {self.path}"
