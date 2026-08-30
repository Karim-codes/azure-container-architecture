#!/usr/bin/env sh
set -eu

domain="${1:-cloudproject.coderaxa.com}"
email="${2:-}"

if [ -z "$email" ]; then
    echo "Usage: ./scripts/issue-cert.sh cloudproject.coderaxa.com you@example.com"
    exit 1
fi

mkdir -p certbot/www certbot/conf

docker compose up -d --build nginx_proxy
docker compose run --rm certbot certonly \
    --non-interactive \
    --keep-until-expiring \
    --webroot \
    -w /var/www/certbot \
    -d "$domain" \
    --email "$email" \
    --agree-tos \
    --no-eff-email

docker compose up -d --build nginx_proxy
docker compose exec nginx_proxy nginx -t
