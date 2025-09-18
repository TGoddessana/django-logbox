API Reference
=============

This section provides detailed information about Django-Logbox's API, including models, middleware, and utility functions.

Models
------

ServerLog
~~~~~~~~~

.. code-block:: python

    class ServerLog(Model):
        # HTTP fields
        method = CharField(max_length=10)
        path = CharField(max_length=255)
        status_code = IntegerField()
        user_agent = TextField(max_length=255, null=True)
        device = CharField(max_length=255, null=True, blank=True)
        os = CharField(max_length=255, null=True, blank=True)
        browser = CharField(max_length=255, null=True, blank=True)
        querystring = TextField(null=True)
        request_body = TextField(null=True)
        
        # Log fields
        timestamp = DateTimeField()
        exception_type = CharField(max_length=255, null=True)
        exception_message = TextField(null=True)
        traceback = TextField(null=True)
        
        # IP fields
        server_ip = GenericIPAddressField()
        client_ip = GenericIPAddressField()
        server_host = CharField(max_length=255, null=True, blank=True)
        server_port = IntegerField(null=True, blank=True)
        
        # User field
        user = ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=SET_NULL, null=True, blank=True, related_name="server_logs")

The ``ServerLog`` model stores detailed information about HTTP requests. Each field captures a specific aspect of the request:

- **method**: The HTTP method used (GET, POST, etc.)
- **path**: The requested URL path
- **status_code**: The HTTP status code of the response
- **user_agent**: The User-Agent string from the request header
- **device**: The device type parsed from the User-Agent
- **os**: The operating system parsed from the User-Agent
- **browser**: The browser parsed from the User-Agent
- **querystring**: The query parameters as a URL-encoded string
- **request_body**: The body content of the request (usually JSON or form data)
- **timestamp**: When the log entry was created
- **exception_type**: The type of exception, if any occurred
- **exception_message**: The message from the exception
- **traceback**: The full traceback of the exception
- **server_ip**: The IP address of the server
- **client_ip**: The IP address of the client
- **server_host**: The hostname of the server
- **server_port**: The port number the server is running on
- **user**: The authenticated user associated with the request

ServerLogQuerySet
~~~~~~~~~~~~~~~~

.. code-block:: python

    class ServerLogQuerySet(QuerySet):
        def get_traffic_data(self)
        def get_status_code_data(self)
        def get_device_data(self)
        def get_os_data(self)
        def get_browser_data(self)

The ``ServerLogQuerySet`` provides methods for analyzing log data:

- **get_traffic_data()**: Returns traffic data grouped by date
- **get_status_code_data()**: Returns status code distribution with percentages
- **get_device_data()**: Returns device usage statistics
- **get_os_data()**: Returns operating system usage statistics
- **get_browser_data()**: Returns browser usage statistics

Middleware
---------

LogboxMiddleware
~~~~~~~~~~~~~~~

.. code-block:: python

    class LogboxMiddleware:
        def __init__(self, get_response)
        def __call__(self, request)
        def process_exception(self, request, exception)

The ``LogboxMiddleware`` intercepts HTTP requests and responses to log them:

- **__call__(request)**: Processes the request, gets the response, and logs it
- **process_exception(request, exception)**: Logs exceptions that occur during request processing

Utility Functions
---------------

Logging Functions
~~~~~~~~~~~~~~~

.. code-block:: python

    def add_log(request, response, exception=None)
    def get_log_data(timestamp, request, response, exception=None)

- **add_log()**: Adds a log entry to the queue for processing
- **get_log_data()**: Extracts and formats log data from request, response, and exception objects

Utility Functions
~~~~~~~~~~~~~~~

.. code-block:: python

    def get_client_ip(request)
    def get_server_ip()
    def get_method(request)
    def get_path(request)
    def get_querystring(request)
    def get_request_body(request)
    def get_user_agent(request)
    def get_status_code(response)
    def get_exception_type(exception)
    def get_traceback(exception)
    def get_server_host(request)
    def get_server_port(request)
    def device_str(user_agent)
    def os_str(user_agent)
    def browser_str(user_agent)

These utility functions extract specific information from request, response, and exception objects:

- **get_client_ip()**: Gets the client's IP address from the request
- **get_server_ip()**: Gets the server's IP address using socket information
- **get_method()**: Gets the HTTP method from the request
- **get_path()**: Gets the request path
- **get_querystring()**: Gets the query parameters from the request
- **get_request_body()**: Gets the request body content
- **get_user_agent()**: Gets the User-Agent string from the request
- **get_status_code()**: Gets the HTTP status code from the response
- **get_exception_type()**: Gets the exception type name
- **get_traceback()**: Gets the formatted exception traceback
- **get_server_host()**: Gets the server hostname from the request
- **get_server_port()**: Gets the server port number from the request
- **device_str()**: Parses device information from User-Agent (family, brand, model)
- **os_str()**: Parses OS information from User-Agent (family, version)
- **browser_str()**: Parses browser information from User-Agent (family, version)

Threading
--------

ServerLogInsertThread
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    class ServerLogInsertThread(Thread):
        def __init__(self, logging_daemon_interval=0, logging_daemon_queue_size=1)
        def put_serverlog(self, data)
        def run()
        def _start_bulk_insertion()
        def _exit_gracefully(self, signum, frame)

The ``ServerLogInsertThread`` manages the asynchronous insertion of logs into the database:

- **put_serverlog()**: Adds a log entry to the queue
- **run()**: The main thread loop that processes the queue
- **_start_bulk_insertion()**: Inserts queued logs into the database
- **_exit_gracefully()**: Ensures logs are saved when the application shuts down

Filtering
--------

LogboxLogFilter
~~~~~~~~~~~~~

.. code-block:: python

    class LogboxLogFilter:
        @staticmethod
        def should_filter_log(request, response)

The ``LogboxLogFilter`` determines whether a request should be logged based on the configured settings:

- **should_filter_log()**: Returns True if the request should be filtered out (not logged)