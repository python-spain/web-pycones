#!/bin/bash

echo "→ Installing npm depedencies"
npm install

echo "→ Installing gulp globaly"
npm install -g gulp

echo "→ Building gulp"
gulp $1