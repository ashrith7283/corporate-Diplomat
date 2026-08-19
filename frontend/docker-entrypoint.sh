#!/bin/sh
set -e

: "${BACKEND_URL:?BACKEND_URL must be set (default http://backend:8000 is used by docker-compose.yml)}"

BACKEND_HOST=$(echo "$BACKEND_URL" | sed -E 's#^https?://##; s#/.*$##')
export BACKEND_HOST

envsubst '${BACKEND_URL} ${BACKEND_HOST}' < /etc/nginx/conf.d/nginx.conf.template > /etc/nginx/conf.d/default.conf

echo "==> proxy_pass ${BACKEND_URL} (host: ${BACKEND_HOST})"

exec nginx -g 'daemon off;'
