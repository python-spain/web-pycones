#!/bin/bash

echo "### Show my local dir"
pwd
echo "### And files"
ls -ltr
echo "### Building new docker image"
docker-compose build
# Not necessary by the moment:
# echo "### Install npm dependencies on new image"
# docker-compose run webapp npm install
# echo "### Run npm build on new image"
# docker-compose run webapp npm run build
echo "### Collectstatic for new image"
docker-compose run webapp python3 /app/manage.py collectstatic --noinput
# @aaloy: Subimos compilados los messages
#echo "### Compilemessages"
#docker-compose run webapp python3 /app/manage.py compilemessages
echo "### Migrate database"
docker-compose run webapp python3 /app/manage.py migrate
echo "### Start new docker image"
docker-compose up -d
docker-compose restart caddy
