#!/bin/bash
set -euo pipefail

FLAG_RAND=$(head -c 8 /dev/urandom | xxd -p)
FLAG_FILE="/flag_${FLAG_RAND}.txt"
echo -n "$FLAG" > "$FLAG_FILE"
chmod 444 "$FLAG_FILE"

chown -R flowforge:flowforge /app/.internal

unset FLAG

exec gosu flowforge gunicorn \
    --workers 1 --threads 8 --timeout 60 \
    --bind 0.0.0.0:8080 app:app
