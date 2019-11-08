# https://hub.docker.com/_/node/
FROM node:11 as nodebuilder
ENV NPM_CONFIG_LOGLEVEL info

WORKDIR /app
COPY docker/build_node.sh /build_node.sh
COPY src/ .
RUN /build_node.sh build
VOLUME /app