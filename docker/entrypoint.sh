#!/bin/bash

set -e

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