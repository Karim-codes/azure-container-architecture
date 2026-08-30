#!/bin/sh
set -eu

domain="${DOMAIN:-cloudproject.coderaxa.com}"
cert_dir="/etc/letsencrypt/live/${domain}"

if [ -f "${cert_dir}/fullchain.pem" ] && [ -f "${cert_dir}/privkey.pem" ]; then
    cp /etc/nginx/conf-available/https.conf /etc/nginx/conf.d/default.conf
else
    cp /etc/nginx/conf-available/http.conf /etc/nginx/conf.d/default.conf
fi
