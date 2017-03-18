.. _ref-tutorial:

===========================
Getting Started with cfblog
===========================

Installation
============

Use you python package manager to install the app from PyPI

Example:

.. code-block:: bash

    $ pip install cfblog


Configuration
=============

Apps
----

Add cfblog to your ``INSTALLED_APPS`` setting in your settings file (usually ``settings.py``)

Example:

.. code-block:: python

    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'cfblog',
    )


Urls
----

Add the cfblog url-patterns to your main ``urls.py`` file.

.. code-block:: python

    urlpatterns = [
        url(r'^admin/', include(admin.site.urls)),
        url(r'^blog/', include('cfblog.urls')),
    ]

.. note::

    cfblog ``url_patterns`` contains a catchall url. Hence these urls should be the last entry.

Middleware
----------

Add the cfblog middleware to the ``MIDDLEWARE_CLASSES`` setting in your settings file

.. code-block:: python

    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'django.middleware.security.SecurityMiddleware',
        'cfblog.Middleware',
    )

.. note::

    This setting is only required if you want to serve the cms pages on a url that matches with a url pattern before cfblog.

Static Files
------------

After configuring run the following command to collect the static files of cfblog.

.. code-block:: bash

    $ python manage.py collectstatic

Testing
=======

Start the devserver and login to your admin site

.. code-block:: bash

    $ python manage.py runserver <IP-address>:<port>

Creating a Page
---------------

* In the admin panel, go to cfblog section and click on add beside contents.
* Add url, template, title and author.
* After saving go to the url or click on ``view on site`` button.

Now, you should be able to see a blank page with text "default body" and a toolbar loaded on the right side.

To create your own editable templates, see :ref:`template syntax<syntax>`
