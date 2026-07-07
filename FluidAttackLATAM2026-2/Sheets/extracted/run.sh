#!/bin/sh
export PATH="/app/.venv/bin:$PATH"

echo $FLAG > /app/flag$(head -c 16 /dev/urandom | od -An -tx1 | tr -d ' ').txt
unset FLAG

uv run -- fastapi run --host 0.0.0.0 --port 5000 src/main.py