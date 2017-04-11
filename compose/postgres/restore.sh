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

# check that we have an argument for a filename candidate
if [[ $# -eq 0 ]] ; then
    echo 'usage:'
    echo '    docker-compose run postgres restore <backup-file>'
    echo ''
    echo 'to get a list of available backups, run:'
    echo '    docker-compose run postgres list-backups'
    exit 1
fi

# set the backupfile variable
BACKUPFILE=/backups/$1

# check that the file exists
if ! [ -f ${BACKUPFILE} ]; then
    echo "backup file not found"
    echo 'to get a list of available backups, run:'
    echo '    docker-compose run postgres list-backups'
    exit 1
fi

echo "beginning restore from $1"
echo "-------------------------"

# delete the db
# deleting the db can fail. Spit out a comment if this happens but continue since the db
# is created in the next step
echo "deleting old database $POSTGRES_DB"
if dropdb -h ${POSTGRES_HOST} -U ${POSTGRES_USER} ${POSTGRES_DB}
then echo "deleted $POSTGRES_DB database"
else echo "database $POSTGRES_DB does not exist, continue"
fi

# create a new database
echo "creating new database $POSTGRES_DB"
createdb -h ${POSTGRES_HOST} -U ${POSTGRES_USER} ${POSTGRES_DB} -O ${POSTGRES_USER}

# restore the database
echo "restoring database $POSTGRES_USER"
gunzip -c ${BACKUPFILE} | psql -h ${POSTGRES_HOST} -U ${POSTGRES_USER} -d ${POSTGRES_DB}
