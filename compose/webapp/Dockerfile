# Dockerfile for PyConES Web App
FROM ubuntu:18.04
ENV PYTHONUNBUFFERED 1


RUN apt-get update && apt-get install -y \
    software-properties-common \
    build-essential \
    git \
    libpq-dev \
    python3 \
    python3-dev \
    python3-pip \
    python3-setuptools \
    python-psycopg2 \
    libjpeg-dev \
    jpegoptim \
    optipng \
    gettext \
    curl \
    libproj-dev \
    binutils \
    gdal-bin

# Install nodejs, bower and less
RUN add-apt-repository ppa:ubuntugis/ubuntugis-unstable && apt-get update


ENV PYTHONIOENCODING="UTF-8";
ENV CPLUS_INCLUDE_PATH /usr/include/gdal
ENV C_INCLUDE_PATH /usr/include/gdal


RUN ln -s /usr/include/locale.h /usr/include/xlocale.h

# Install nodejs.
ENV NPM_CONFIG_LOGLEVEL info
RUN curl -sL https://deb.nodesource.com/setup_11.x  | bash -
RUN apt-get -y install nodejs
RUN npm install
RUN npm install -g gulp


# Requirements and webapp user and group
COPY ./requirements /requirements
RUN pip3 install -U pip
RUN pip3 install -r /requirements/local.txt \
    && pip3 install -r /requirements/production.txt \
    && groupadd -r webapp \
    && useradd -r -g webapp webapp

# Source code
COPY . /app
RUN chown -R webapp /app

# Creates entrypoint and start scripts
COPY ./compose/webapp/gunicorn.sh /gunicorn.sh
COPY ./compose/webapp/entrypoint.sh /entrypoint.sh
COPY ./compose/webapp/local_server.sh /local_server.sh

RUN sed -i 's/\r//' /entrypoint.sh \
    && sed -i 's/\r//' /gunicorn.sh \
    && sed -i 's/\r//' /local_server.sh \
    && chmod +x /entrypoint.sh \
    && chown webapp /entrypoint.sh \
    && chmod +x /gunicorn.sh \
    && chmod +x /local_server.sh \
    && chown webapp /gunicorn.sh

WORKDIR /app
ENTRYPOINT ["/entrypoint.sh"]
