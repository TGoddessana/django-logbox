Installation
============

Requirements
-----------

Django-Logbox requires:

* Python 3.8 or higher
* Django 3.2 or higher

Installation Steps
----------------

1. Install the package using pip:

   .. code-block:: bash

      pip install django-logbox

2. Add ``django_logbox`` to your ``INSTALLED_APPS`` in your Django settings file:

   .. code-block:: python

      INSTALLED_APPS = [
          # ...
          'django.contrib.admin',
          'django.contrib.auth',
          'django.contrib.contenttypes',
          'django.contrib.sessions',
          'django.contrib.messages',
          'django.contrib.staticfiles',
          # ...
          'django_logbox',
          # ...
      ]

3. Add the Django-Logbox middleware to your ``MIDDLEWARE`` setting:

   .. code-block:: python

      MIDDLEWARE = [
          # ...
          'django.middleware.security.SecurityMiddleware',
          'django.contrib.sessions.middleware.SessionMiddleware',
          'django.middleware.common.CommonMiddleware',
          'django.middleware.csrf.CsrfViewMiddleware',
          'django.contrib.auth.middleware.AuthenticationMiddleware',
          'django.contrib.messages.middleware.MessageMiddleware',
          'django.middleware.clickjacking.XFrameOptionsMiddleware',
          # ...
          'django_logbox.middlewares.LogboxMiddleware',
          # ...
      ]

   .. note::
      The position of the middleware in the list matters. For capturing all possible exceptions, 
      it's recommended to place the LogboxMiddleware after Django's built-in middlewares.

4. Run migrations to create the necessary database tables:

   .. code-block:: bash

      python manage.py migrate django_logbox

5. (Optional) Configure Django-Logbox settings in your Django settings file:

   .. code-block:: python

      LOGBOX_SETTINGS = {
          # Your custom settings here
          # See the Settings section for available options
      }

Verifying Installation
---------------------

To verify that Django-Logbox is properly installed and working:

1. Start your Django development server:

   .. code-block:: bash

      python manage.py runserver

2. Make a request to any page in your application.

3. Check the Django admin interface at ``/admin/django_logbox/serverlog/`` to see if the request was logged.

Upgrading
---------

To upgrade Django-Logbox to the latest version:

.. code-block:: bash

   pip install --upgrade django-logbox

After upgrading, always run migrations to apply any database changes:

.. code-block:: bash

   python manage.py migrate django_logbox