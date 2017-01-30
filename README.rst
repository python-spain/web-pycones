================
PyConES 2017 Web
================

Web page made for PyConES 2017, made with Django with :heart:.


Deploy with Docker
------------------

To deploy using docker, first we've to create a ``.env`` file with the
credentials of the database, secret key, etc.

.. code-block:: bash

    $ cp env.example .env

Then, we've have to use Docker Compose to bring it up.

.. code-block:: bash

    $ docker-compose up

