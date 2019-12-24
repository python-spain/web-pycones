#!/bin/bash

set -e


postgres_ready() {
python << END
import sys
import psycopg2
try:
    psycopg2.connect(
        dbname="${POSTGRES_DB}",
        user="${POSTGRES_USER}",
        password="${POSTGRES_PASSWORD}",
        host="${POSTGRES_HOST}",
        port="${POSTGRES_PORT}",
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

case $1 in
    run-uwsgi)
        exec uwsgi --ini=/etc/uwsgi/uwsgi.ini
        ;;

    run-migrations)
        /entrypoint.sh launch-migrations
        exec sleep infinity
        ;;

    run-uwsgitop)
        exec uwsgitop localhost:9090
        ;;

    run-devel)
        export PATH="/app/node_modules/.bin:$PATH"
        /entrypoint.sh launch-migrations
        echo "→ Running as runserver mode"
        exec python manage.py runserver 0.0.0.0:8000
        ;;

    launch-migrations)
        echo "→ Executing migrate"
        exec python manage.py migrate --noinput
        echo "✓ Migrations applied"
        ;;

    launch-liveness-probe)
        exec curl -f localhost:8080/health/ || exit 1
        ;;

    launch-readiness-probe)
        exec python manage.py showmigrations | grep -c "\[ \]" -m 1 | grep -q 0 || exit 1
        ;;

    *)
        exec "$@"
        ;;
esac
