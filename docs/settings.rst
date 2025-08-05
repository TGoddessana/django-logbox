Settings
========

Django-Logbox provides several customization options that can be configured in your Django settings file. These settings allow you to control which requests are logged, how they are processed, and more.

Configuration
------------

To customize Django-Logbox, add a ``LOGBOX_SETTINGS`` dictionary to your Django settings file:

.. code-block:: python

    LOGBOX_SETTINGS = {
        # Your custom settings here
    }

Available Settings
----------------

The following settings are available for customization:

LOGGING_HTTP_METHODS
~~~~~~~~~~~~~~~~~~~

A list of HTTP methods to log. By default, all methods are logged.

.. code-block:: python

    LOGBOX_SETTINGS = {
        "LOGGING_HTTP_METHODS": ["GET", "POST", "PUT", "PATCH", "DELETE"],
    }

To log only specific methods, provide a list of the methods you want to log:

.. code-block:: python

    LOGBOX_SETTINGS = {
        "LOGGING_HTTP_METHODS": ["POST", "PUT", "PATCH", "DELETE"],  # Don't log GET requests
    }

LOGGING_SERVER_IPS_TO_EXCLUDE
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A list of server IP addresses to exclude from logging. By default, no IPs are excluded.

.. code-block:: python

    LOGBOX_SETTINGS = {
        "LOGGING_SERVER_IPS_TO_EXCLUDE": ["127.0.0.1", "192.168.1.100"],
    }

LOGGING_CLIENT_IPS_TO_EXCLUDE
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A list of client IP addresses to exclude from logging. By default, no IPs are excluded.

.. code-block:: python

    LOGBOX_SETTINGS = {
        "LOGGING_CLIENT_IPS_TO_EXCLUDE": ["127.0.0.1", "192.168.1.100"],
    }

LOGGING_STATUS_CODES
~~~~~~~~~~~~~~~~~~

A list of HTTP status codes to log. By default, all status codes are logged.

.. code-block:: python

    LOGBOX_SETTINGS = {
        "LOGGING_STATUS_CODES": [200, 201, 400, 401, 403, 404, 500],
    }

To log only error responses:

.. code-block:: python

    LOGBOX_SETTINGS = {
        "LOGGING_STATUS_CODES": [400, 401, 403, 404, 500],  # Only log error responses
    }

LOGGING_PATHS_TO_EXCLUDE
~~~~~~~~~~~~~~~~~~~~~~

A list of path regex patterns to exclude from logging. By default, no paths are excluded.

.. code-block:: python

    LOGBOX_SETTINGS = {
        "LOGGING_PATHS_TO_EXCLUDE": [r"^/static/", r"^/media/", r"^/admin/"],
    }

LOGGING_DAEMON_QUEUE_SIZE
~~~~~~~~~~~~~~~~~~~~~~~

The number of logs to insert in bulk. The default is 1, which means logs are inserted instantly.

Setting a higher value can improve performance by reducing database operations, but it means logs will be inserted in batches rather than immediately.

.. code-block:: python

    LOGBOX_SETTINGS = {
        "LOGGING_DAEMON_QUEUE_SIZE": 10,  # Insert logs in batches of 10
    }

LOGGING_DAEMON_INTERVAL
~~~~~~~~~~~~~~~~~~~~~

The number of seconds between log insertion attempts. The default is 0.

This setting is useful when combined with a higher ``LOGGING_DAEMON_QUEUE_SIZE`` to control how frequently batches of logs are inserted.

.. code-block:: python

    LOGBOX_SETTINGS = {
        "LOGGING_DAEMON_QUEUE_SIZE": 10,
        "LOGGING_DAEMON_INTERVAL": 5,  # Insert logs every 5 seconds or when queue size reaches 10
    }

Default Settings
--------------

Here are the default settings used by Django-Logbox if not overridden:

.. code-block:: python

    DEFAULT_LOGBOX_SETTINGS = {
        # HTTP methods to log. Default to all
        "LOGGING_HTTP_METHODS": ["GET", "POST", "PUT", "PATCH", "DELETE"],
        # exclude server IPs from logging. Default to not exclude any
        "LOGGING_SERVER_IPS_TO_EXCLUDE": [],
        # exclude client IPs from logging. Default to not exclude any
        "LOGGING_CLIENT_IPS_TO_EXCLUDE": [],
        # Status codes to log. Default to all
        "LOGGING_STATUS_CODES": [http_code.value for http_code in HTTPStatus],
        # Path regex to exclude from logging. Default to not exclude any
        "LOGGING_PATHS_TO_EXCLUDE": [],
        # The number of logs to insert in bulk. The default is 1, which means insert logs instantly.
        "LOGGING_DAEMON_QUEUE_SIZE": 1,
        # The number of seconds between log insertion attempts. The default is 0.
        "LOGGING_DAEMON_INTERVAL": 0,
    }