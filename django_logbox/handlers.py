import logging

from django.core.handlers.wsgi import WSGIRequest


class DBLogHandler(logging.Handler):
    def emit(self, record: logging.LogRecord):
        request: WSGIRequest | None = getattr(record, "request", None)
        if request:
            method = request.method
            path = request.path
            status_code = str(getattr(record, "status_code", ""))
            user_agent = request.META.get("HTTP_USER_AGENT", "")
            querystring = request.META.get("QUERY_STRING", "")
            request_body = request.body.decode("utf-8") if request.body else ""
            level = record.levelname
            message = record.getMessage()
            timestamp = record.created
            exception = str(record.exc_info[1]) if record.exc_info else ""
            traceback = record.exc_text if record.exc_text else ""
            server_ip = request.get_host()
            client_ip = request.META.get("REMOTE_ADDR", "")

            print(f"method: {method}")
            print(f"path: {path}")
            print(f"status_code: {status_code}")
            print(f"user_agent: {user_agent}")
            print(f"querystring: {querystring}")
            print(f"request_body: {request_body}")
            print(f"level: {level}")
            print(f"message: {message}")
            print(f"timestamp: {timestamp}")
            print(f"exception: {exception}")
            print(f"traceback: {traceback}")
            print(f"server_ip: {server_ip}")
            print(f"client_ip: {client_ip}")
            print()
