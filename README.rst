================
PyConES 2017 Web
================

Web page made for PyConES 2017, made with Django with :heart:.

.. image:: https://travis-ci.org/python-spain/PyConES-2017.svg?branch=master
    :target: https://travis-ci.org/python-spain/PyConES-2017

Deploy with Docker
------------------

To deploy using docker, first we've to create a ``.env`` file with the
credentials of the database, secret key, etc.

.. code-block:: bash

    $ cp env.example .env

The available environment variables are:

- ``POSTGRES_PASSWORD`` Postgres database password
- ``POSTGRES_DB`` Postgres database name
- ``DJANGO_SECRET_KEY`` Django secret key
- ``DJANGO_SETTINGS_MODULE`` Django settings module (eg. ``config.settings.production``)
- ``DATABASE_URL`` Url to connect to the database (eg. ``config.settings.production``)
- ``DJANGO_ALLOWED_HOSTS`` Host names allowed, separated by commas (eg. ``localhost,2017.es.pycon.org``))
- ``DJANGO_EMAIL_HOST`` Host for SMTP server
- ``DJANGO_EMAIL_HOST_USER`` User for SMTP server
- ``DJANGO_EMAIL_HOST_PASSWORD`` Password for SMTP server
- ``DJANGO_EMAIL_PORT`` Port for SMTP server

The default values are ready to run the containers in a development machine using **production
configuration**. Then, we've have to use Docker Compose to bring it up.

.. code-block:: bash

    $ docker-compose up

