#!/bin/sh

set -o errexit
set -o nounset


postgres_ready() {
python << END
import sys
import psycopg2
import urlparse

result = urlparse.urlparse("${DATABASE_URL}")
username = result.username
password = result.password
database = result.path[1:]
hostname = result.hostname

try:
    psycopg2.connect(
        database = database,
        user = username,
        password = password,
        host = hostname
    )
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}

until postgres_ready; do
  >&2 echo 'Waiting for PostgreSQL to become available...'
  sleep 1
done
>&2 echo 'PostgreSQL is available'

exec "$@"
