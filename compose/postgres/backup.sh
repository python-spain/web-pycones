#!/bin/bash
# stop on errors
set -e

# default user for postgres
if [ "$POSTGRES_USER" == "" ]
then
    POSTGRES_USER="postgres"
fi

# host is the service name
POSTGRES_HOST="db"

# export the postgres password so that subsequent commands don't ask for it
export PGPASSWORD=${POSTGRES_PASSWORD}

echo "creating backup"
echo "---------------"

FILENAME=backup_$(date +'%Y_%m_%dT%H_%M_%S').sql.gz
pg_dump -h ${POSTGRES_HOST} -U ${POSTGRES_USER} ${POSTGRES_DB} | gzip > /backups/${FILENAME}

echo "successfully created backup $FILENAME"
