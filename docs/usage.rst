Usage
=====

Once Django-Logbox is installed and configured, it will automatically log HTTP requests to your Django application. This section explains how to view and work with the logs.

Viewing Logs in Django Admin
---------------------------

Django-Logbox integrates with the Django Admin interface, providing a user-friendly way to view and filter logs.

1. Navigate to your Django Admin interface (typically at ``/admin/``)
2. Click on "Server Logs" under the "Django_Logbox" section
3. You'll see a list of all logged requests, sorted by timestamp (most recent first)

Filtering Logs
-------------

The Django Admin interface allows you to filter logs by various criteria:

- **Method**: Filter by HTTP method (GET, POST, etc.)
- **Path**: Filter by request path
- **Status Code**: Filter by HTTP status code
- **Client IP**: Filter by client IP address
- **User**: Filter by authenticated user
- **Timestamp**: Filter by date range

You can also use the search box to search across multiple fields.

Analyzing Log Data
----------------

Django-Logbox provides several methods for analyzing log data through the ``ServerLogQuerySet`` class:

Traffic Analysis
~~~~~~~~~~~~~~

To get traffic data over time:

.. code-block:: python

    from django_logbox.models import ServerLog
    
    # Get traffic data grouped by date
    traffic_data = ServerLog.objects.get_traffic_data()
    
    for entry in traffic_data:
        print(f"Date: {entry['date']}, Count: {entry['count']}")

Status Code Analysis
~~~~~~~~~~~~~~~~~

To analyze status code distribution:

.. code-block:: python

    from django_logbox.models import ServerLog
    
    # Get status code distribution with percentages
    status_data = ServerLog.objects.get_status_code_data()
    
    for entry in status_data:
        print(f"Status: {entry['status_code']}, Count: {entry['count']}, Percentage: {entry['percentage']:.2f}%")

Device Analysis
~~~~~~~~~~~~~

To analyze device usage:

.. code-block:: python

    from django_logbox.models import ServerLog
    
    # Get device distribution
    device_data = ServerLog.objects.get_device_data()
    
    for entry in device_data:
        print(f"Device: {entry['device']}, Count: {entry['count']}, Percentage: {entry['percentage']:.2f}%")

OS Analysis
~~~~~~~~~

To analyze operating system usage:

.. code-block:: python

    from django_logbox.models import ServerLog
    
    # Get OS distribution
    os_data = ServerLog.objects.get_os_data()
    
    for entry in os_data:
        print(f"OS: {entry['os']}, Count: {entry['count']}, Percentage: {entry['percentage']:.2f}%")

Browser Analysis
~~~~~~~~~~~~~~

To analyze browser usage:

.. code-block:: python

    from django_logbox.models import ServerLog
    
    # Get browser distribution
    browser_data = ServerLog.objects.get_browser_data()
    
    for entry in browser_data:
        print(f"Browser: {entry['browser']}, Count: {entry['count']}, Percentage: {entry['percentage']:.2f}%")

Custom Queries
------------

You can also perform custom queries using Django's ORM:

.. code-block:: python

    from django_logbox.models import ServerLog
    
    # Get all 404 errors
    not_found_logs = ServerLog.objects.filter(status_code=404)
    
    # Get all logs for a specific user
    user_logs = ServerLog.objects.filter(user=request.user)
    
    # Get all logs with exceptions
    error_logs = ServerLog.objects.exclude(exception_type=None)
    
    # Get logs for a specific time period
    from django.utils import timezone
    from datetime import timedelta
    
    yesterday = timezone.now() - timedelta(days=1)
    recent_logs = ServerLog.objects.filter(timestamp__gte=yesterday)

Cleaning Up Old Logs
------------------

Over time, the logs table can grow quite large. You may want to periodically clean up old logs:

.. code-block:: python

    from django_logbox.models import ServerLog
    from django.utils import timezone
    from datetime import timedelta
    
    # Delete logs older than 30 days
    thirty_days_ago = timezone.now() - timedelta(days=30)
    ServerLog.objects.filter(timestamp__lt=thirty_days_ago).delete()

You can automate this cleanup using Django's management commands or a task scheduler like Celery.


Integrating with Django-REST-Framework
--------------------------------------

