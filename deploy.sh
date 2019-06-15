#!/bin/bash

echo "Pull new code from repository"
git pull origin master
echo "Building new docker image"
docker-compose build
echo "Install npm dependencies on new image"
docker-compose run webapp npm install
echo "Run npm build on new image"
docker-compose run webapp npm run build
echo "Collectstatic for new image"
docker-compose run webapp python3 /app/manage.py collectstatic --noinput
echo "Compilemessages"
docker-compose run webapp python3 /app/manage.py compilemessages
echo "Migrate database"
docker-compose run webapp python3 /app/manage.py migrate
echo "Start new docker image"
docker-compose up -d
