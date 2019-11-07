# FROM node image install and build gulp for static 
# Install nodejs.
# ENV NPM_CONFIG_LOGLEVEL info
# RUN curl -sL https://deb.nodesource.com/setup_11.x  | bash -
# RUN apt-get -y install nodejs
# RUN npm install
# RUN npm install -g gulp

# https://hub.docker.com/_/python/
FROM python:3.7

ENV PYTHONUNBUFFERED 1

# Install system-requirements
COPY docker/system-requirements.txt /srv/system-requirements.txt
RUN  \
    apt-get -qq update && \
    xargs apt-get -qq install < /srv/system-requirements.txt


# Install nodejs, bower and less
#RUN add-apt-repository ppa:ubuntugis/ubuntugis-unstable && apt-get update

# ¿?
#ENV PYTHONIOENCODING="UTF-8";
#ENV CPLUS_INCLUDE_PATH /usr/include/gdal
#ENV C_INCLUDE_PATH /usr/include/gdal

# ¿?
#RUN ln -s /usr/include/locale.h /usr/include/xlocale.h


# Requirements and webapp user and group
COPY ./requirements /requirements
RUN pip3 install -r /requirements/production.txt
# TODO: maybe just install on dev environment from other docker image FROM this one.
RUN pip3 install -r /requirements/local.txt

# Source code
WORKDIR /app
COPY src/ .

COPY ./docker/entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
CMD ["run-uwsgi"]

