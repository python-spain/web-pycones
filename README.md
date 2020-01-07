# PyConES 2020 Web

Web page made for PyConES 2020, made with Django with :heart:.


## Develop with Docker

``` bash
make up
```

For more help use `make`.

## Continous Integration

Travis CI build and deploy 
[![Build Status](https://travis-ci.org/python-spain/web-pycones.svg?branch=2020)](https://travis-ci.org/python-spain/web-pycones)

## Deploy with Docker

``` bash
$ cp docker-compose.yml.production_template docker-compose.yml
```

The available environment variables are:

  - `DJANGO_SECRET_KEY` Django secret key
  - `DJANGO_SETTINGS_MODULE` Django settings module (eg.
    `config.settings.production`)
  - `DATABASE_URL` Url to connect to the database (eg.
    `config.settings.production`)
  - `DJANGO_ALLOWED_HOSTS` Host names allowed, separated by commas (eg.
    `localhost,2017.es.pycon.org`))
  - `DJANGO_EMAIL_HOST` Host for SMTP server
  - `DJANGO_EMAIL_HOST_USER` User for SMTP server
  - `DJANGO_EMAIL_HOST_PASSWORD` Password for SMTP server
  - `DJANGO_EMAIL_PORT` Port for SMTP server

The default values are ready to run the containers in a development
machine using **production configuration**. Then, we've have to use
Docker Compose to bring it up.

``` bash
$ ./docker/deploy.sh
```

We use an external server deployment to manage the production environment.
The deployment is automated with Travis:
 
https://travis-ci.org/python-spain/web-pycones

## Configuration parameters

Some configuration can be enabled/dissabled on the options admin page:

  - \`activate\_about\_us\`: 1/0 About us page
  - \`activate\_schedule\`: 1/0 Schedule page
  - \`activate\_job\_board\`: 1/0 Job board
  - \`activate\_hotels\`: 1/0 Hotels page
  - \`activate\_blog\`: 1/0 Blog page
  - \`tshirts\_page\_activated\`: 1/0 Tshirst page
  - \`activated\_tickets\_sale\_page\`: 1/0 Tickets option
  - \`info\_available\`: 1/0 availability of the information page
  - \`schedule\_opened\`: 1/0 Determines if the schedule is open or not
