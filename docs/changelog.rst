Change Log
==========

This document outlines the changes made in each version of Django-Logbox.

Versioning Scheme
-----------------

Django-Logbox follows `Semantic Versioning <https://semver.org/>`_:

- **MAJOR** version for incompatible API changes
- **MINOR** version for new functionality in a backward-compatible manner
- **PATCH** version for backward-compatible bug fixes

Version 1.1.1
-------------------------
Released on: 2025-09-25

- Replace the dependency(`0007_serverlog_user_alter_serverlog_querystring.py`) with a swappable_dependency. (Covers cases using custom user models.)

Version 1.1.0
-------------------------

Released on: 2025-09-20

- When storing the server's IP, we retrieve it using `socket` instead of `get_host()`
- `server_host`, `server_ip`, `server_port` are stored separately. The existing `server_ip` field is split into these three fields for storage.
- On the admin page, tracebacks are loaded in a more readable format using <pre> tags

Version 1.0.0
-------------------------

This is the first version for recording the changelog. Since it is being used in a production environment,
we are releasing the new version as 1.0.0.