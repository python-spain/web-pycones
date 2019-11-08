# https://hub.docker.com/_/node/
FROM node:11 as nodebuilder
ENV NPM_CONFIG_LOGLEVEL info

WORKDIR /app
COPY docker/build_node.sh /build_node.sh
COPY src/ .
RUN /build_node.sh build

# https://hub.docker.com/_/python/
FROM python:3.7

# Install system-requirements
COPY docker/system-requirements.txt /srv/system-requirements.txt
RUN  \
    apt-get -qq update && \
    xargs apt-get -qq install < /srv/system-requirements.txt

# Requirements and webapp user and group
COPY ./requirements /requirements
RUN pip3 install -r /requirements/production.txt
# TODO: maybe just install on dev environment from other docker image FROM this one.
RUN pip3 install -r /requirements/local.txt

# Source code
COPY --from=nodebuilder /app /app
WORKDIR /app

COPY ./docker/entrypoint.sh /entrypoint.sh
COPY ./docker/uwsgi.ini /etc/uwsgi/uwsgi.ini

RUN DJANGO_SETTINGS_MODULE=config.settings.local python3 manage.py collectstatic --no-input

ENTRYPOINT ["/entrypoint.sh"]
CMD ["run-uwsgi"]