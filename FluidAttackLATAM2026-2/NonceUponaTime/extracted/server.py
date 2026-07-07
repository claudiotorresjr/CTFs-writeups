import hashlib
import json
import os
import random
import time

from ecdsa import NIST256p, SigningKey
from ecdsa.numbertheory import inverse_mod
from flask import Flask, jsonify, request

app = Flask(__name__)

FLAG = os.environ.get("FLAG", "flag{REDACTED}")

CURVE = NIST256p
ORDER = CURVE.order
GENERATOR = CURVE.generator

SIGNING_KEY = SigningKey.generate(curve=CURVE)
VERIFYING_KEY = SIGNING_KEY.get_verifying_key()
PRIVATE_KEY_INT = SIGNING_KEY.privkey.secret_multiplier


RATE_LIMIT_WINDOW = 1.0
MAX_REQUESTS_PER_WINDOW = 10
request_timestamps = []


# def deterministic_nonce(private_key, message_hash):
#     """RFC 6979 deterministic nonce generation.
#
#     Generates k deterministically from the private key and message hash
#     so that nonce reuse is impossible and timing leaks are mitigated.
#     See: https://tools.ietf.org/html/rfc6979
#
#     TODO: switch to RFC 6979 deterministic nonces -- current
#     implementation uses random nonces which should be sufficient
#     for our license activation volume. Tracked in JIRA-4821.
#     """
#     import hmac
#     v = b'\x01' * 32
#     k_hmac = b'\x00' * 32
#     priv_bytes = private_key.to_bytes(32, 'big')
#     msg_bytes = message_hash
#     k_hmac = hmac.new(
#         k_hmac, v + b'\x00' + priv_bytes + msg_bytes, hashlib.sha256
#     ).digest()
#     v = hmac.new(k_hmac, v, hashlib.sha256).digest()
#     k_hmac = hmac.new(
#         k_hmac, v + b'\x01' + priv_bytes + msg_bytes, hashlib.sha256
#     ).digest()
#     v = hmac.new(k_hmac, v, hashlib.sha256).digest()
#     v = hmac.new(k_hmac, v, hashlib.sha256).digest()
#     return int.from_bytes(v, 'big') % ORDER


def _rate_limit_check():
    """Enforce rate limiting on signature requests."""
    global request_timestamps
    now = time.time()
    request_timestamps = [
        t for t in request_timestamps if now - t < RATE_LIMIT_WINDOW
    ]
    if len(request_timestamps) >= MAX_REQUESTS_PER_WINDOW:
        return False
    request_timestamps.append(now)
    return True


def _sign_message(message_bytes):
    """Sign a message using ECDSA with P-256.

    Returns (r, s, hash_hex) tuple.
    """
    msg_hash = hashlib.sha256(message_bytes).digest()
    z = int.from_bytes(msg_hash, "big")

    k = random.getrandbits(256) >> 8

    while k == 0 or k >= ORDER:
        k = random.getrandbits(256) >> 8

    point = k * GENERATOR
    r = point.x() % ORDER
    if r == 0:
        return _sign_message(message_bytes)

    s = (inverse_mod(k, ORDER) * (z + r * PRIVATE_KEY_INT)) % ORDER
    if s == 0:
        return _sign_message(message_bytes)

    return (r, s, msg_hash.hex())


def _verify_signature(message_bytes, r, s):
    """Verify an ECDSA signature against the server public key."""
    try:
        msg_hash = hashlib.sha256(message_bytes).digest()
        z = int.from_bytes(msg_hash, "big")

        if not (1 <= r < ORDER and 1 <= s < ORDER):
            return False

        w = inverse_mod(s, ORDER)
        u1 = (z * w) % ORDER
        u2 = (r * w) % ORDER
        point = u1 * GENERATOR + u2 * VERIFYING_KEY.pubkey.point
        return (point.x() % ORDER) == r
    except Exception:
        return False


@app.route("/")
def index():
    return jsonify({
        "service": "LicenseForge Activation Server",
        "version": "2.4.1",
        "endpoints": [
            "/api/info",
            "/api/sign",
            "/api/activate"
        ]
    })


@app.route("/api/info")
def info():
    """Return the public key and curve parameters."""
    pub_point = VERIFYING_KEY.pubkey.point
    return jsonify({
        "curve": "NIST P-256",
        "order": hex(ORDER),
        "generator": {
            "x": hex(GENERATOR.x()),
            "y": hex(GENERATOR.y())
        },
        "public_key": {
            "x": hex(pub_point.x()),
            "y": hex(pub_point.y())
        },
        "public_key_hex": VERIFYING_KEY.to_string().hex()
    })


@app.route("/api/sign", methods=["POST"])
def sign():
    """Sign a license activation request.

    Accepts JSON: {"message": "..."}
    Returns signed message with ECDSA signature.
    """
    if not _rate_limit_check():
        return jsonify({"error": "Rate limit exceeded. Try again shortly."}), 429

    data = request.get_json(silent=True)
    if not data or "message" not in data:
        return jsonify({
            "error": "Missing 'message' field",
            "usage": {"message": "your license data as JSON string"}
        }), 400

    message = data["message"]
    if not isinstance(message, str):
        return jsonify({"error": "'message' must be a string"}), 400

    if len(message) > 1024:
        return jsonify({"error": "Message too long (max 1024 chars)"}), 400

    try:
        parsed = json.loads(message)
    except (json.JSONDecodeError, TypeError):
        return jsonify({
            "error": "Message must be valid JSON",
            "example": '{"user": "alice", "type": "standard"}'
        }), 400

    if isinstance(parsed, dict) and parsed.get("type") == "admin":
        return jsonify({
            "error": "Admin license tokens cannot be signed via this endpoint"
        }), 403

    message_bytes = message.encode("utf-8")
    r, s, msg_hash = _sign_message(message_bytes)

    return jsonify({
        "message": message,
        "hash": msg_hash,
        "signature": {
            "r": hex(r),
            "s": hex(s)
        },
        "public_key": VERIFYING_KEY.to_string().hex()
    })


@app.route("/api/activate", methods=["POST"])
def activate():
    """Activate a license token.

    Accepts JSON: {"token": "json_string", "r": "hex", "s": "hex"}
    If the token type is "admin" and signature is valid, returns the flag.
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid JSON body"}), 400

    token_str = data.get("token")
    r_hex = data.get("r")
    s_hex = data.get("s")

    if not all([token_str, r_hex, s_hex]):
        return jsonify({
            "error": "Missing required fields",
            "required": ["token", "r", "s"]
        }), 400

    try:
        r = int(r_hex, 16)
        s = int(s_hex, 16)
    except (ValueError, TypeError):
        return jsonify({"error": "r and s must be hex strings"}), 400

    token_bytes = token_str.encode("utf-8")

    if not _verify_signature(token_bytes, r, s):
        return jsonify({"error": "Invalid signature"}), 401

    try:
        token_data = json.loads(token_str)
    except (json.JSONDecodeError, TypeError):
        return jsonify({"error": "Token must be valid JSON"}), 400

    license_type = token_data.get("type", "standard")

    if license_type == "admin":
        return jsonify({
            "status": "activated",
            "license": "admin",
            "message": "Administrative license activated successfully",
            "flag": FLAG
        })

    return jsonify({
        "status": "activated",
        "license": license_type,
        "message": f"License type '{license_type}' activated"
    })


@app.route("/health")
def health():
    return "OK", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
