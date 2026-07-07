"""Process-wide configuration values."""

import os
import secrets

FLAG = os.environ.get("FLAG", "flag{missing}")

# Internal control-plane signing material. Persists for the lifetime of
# the process and is required by /api/v2/admin/control as the
# X-Heartbeat-Token header value.
HEARTBEAT_TOKEN = secrets.token_hex(24)

PRIVATE_KEY_PATH = "/app/keys/private.pem"
PUBLIC_KEY_PATH = "/app/keys/public.pem"

JWT_KID = "webhook-platform-key-1"

# v1 rate limiter knobs.
RATE_LIMIT_WINDOW = 60
RATE_LIMIT_MAX = 3
