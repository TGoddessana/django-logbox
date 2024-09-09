from django.db.models import (
    Model,
    TextField,
    DateTimeField,
    CharField,
    GenericIPAddressField,
)
from django.utils.translation import gettext_lazy as _


class ServerLog(Model):
    # http
    method = CharField(_("method"), max_length=10)
    path = CharField(_("path"), max_length=255)
    status_code = CharField(_("status_code"), max_length=3)
    user_agent = CharField(_("user_agent"), max_length=255)
    querystring = TextField(_("querystring"), null=True)
    request_body = TextField(_("request_body"), null=True)

    # log
    level = CharField(_("level"), max_length=10)
    message = TextField(_("message"))
    timestamp = DateTimeField(_("timestamp"))
    exception = TextField(_("exception"), null=True)
    traceback = TextField(_("traceback"), null=True)

    # server
    server_ip = GenericIPAddressField(_("server_ip"))
    client_ip = GenericIPAddressField(_("client_ip"))

    def __str__(self):
        return f"{self.level} {self.timestamp}"
