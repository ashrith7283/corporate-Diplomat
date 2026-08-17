FROM node:20-alpine AS build

WORKDIR /app

COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci

COPY frontend/ ./
RUN npm run build -- --configuration production

FROM nginx:1.27-alpine AS runtime

RUN apk add --no-cache bash gettext

COPY --from=build /app/dist/corporate-diplomat /usr/share/nginx/html
COPY frontend/nginx.conf.template /etc/nginx/conf.d/nginx.conf.template
COPY frontend/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
    CMD wget -qO- http://localhost/ >/dev/null 2>&1 || exit 1

CMD ["/docker-entrypoint.sh"]
