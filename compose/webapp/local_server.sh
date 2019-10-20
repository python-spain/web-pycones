#!/bin/sh

set -o errexit
set -o nounset

export PATH="/usr/src/app/node_modules/.bin:$PATH"

echo "*** Updating node_modules"
npm install --unsafe-perm
echo "*** Setting strict-ssl to false"
npm config set strict-ssl false

python3 manage.py migrate
python3 manage.py runserver 0.0.0.0:8000
