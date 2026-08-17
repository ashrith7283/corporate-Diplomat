#!/bin/sh
set -e

: "${BACKEND_URL:?BACKEND_URL must be set, e.g. https://corporate-diplomat-backend.onrender.com}"

envsubst '${BACKEND_URL}' < /etc/nginx/conf.d/nginx.conf.template > /etc/nginx/conf.d/default.conf

exec nginx -g 'daemon off;'
