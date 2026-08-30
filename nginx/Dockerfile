FROM nginx:1.27-alpine

COPY nginx.conf /etc/nginx/conf-available/http.conf
COPY nginx.https.conf /etc/nginx/conf-available/https.conf
COPY nginx/select-config.sh /docker-entrypoint.d/10-select-config.sh

RUN chmod +x /docker-entrypoint.d/10-select-config.sh
