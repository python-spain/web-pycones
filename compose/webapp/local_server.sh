#!/bin/sh

set -o errexit
set -o nounset

export PATH="/usr/src/app/node_modules/.bin:$PATH"

echo "*** Updating node_modules"
npm install --unsafe-perm
echo "*** Setting strict-ssl to false"
npm config set strict-ssl false

npm install -g gulp


gulp build
python3 manage.py migrate
python3 manage.py runserver_plus 0.0.0.0:8000
