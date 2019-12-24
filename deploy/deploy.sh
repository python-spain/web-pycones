#!/bin/bash

echo "### Show my local dir"
pwd
echo "### And files"
ls -ltr
echo "### Last commit deployed"
git log --stat -1
echo "### Building new docker image"
docker-compose build
echo "### Migrate database"
docker-compose run --rm web python3 /app/manage.py migrate
echo "### Start new docker image"
docker-compose up -d