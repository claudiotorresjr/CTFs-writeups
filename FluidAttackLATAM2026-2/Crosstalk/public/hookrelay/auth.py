"""User registration and JWT-based auth helpers."""

import hashlib
import re
import time

import jwt
from flask import Blueprint, jsonify, request

from hookrelay.config import JWT_KID
from hookrelay.jwt_verify import verify
from hookrelay.keys import PRIVATE_KEY

bp = Blueprint("auth", __name__)


@bp.route("/api/auth/register", methods=["POST"])
def register():
    body = request.get_json(silent=True) or {}
    username = body.get("username", "")
    if not isinstance(username, str) or not re.match(
        r"^[a-zA-Z0-9_]{3,32}$", username
    ):
        return jsonify({
            "error": "username must be 3-32 chars [A-Za-z0-9_]",
        }), 400

    user_id = "usr_" + hashlib.sha256(username.encode()).hexdigest()[:12]
    now = int(time.time())
    token = jwt.encode(
        {
            "sub": user_id,
            "username": username,
            "role": "user",
            "iat": now,
            "exp": now + 86400,
        },
        PRIVATE_KEY,
        algorithm="RS256",
        headers={"kid": JWT_KID},
    )
    return jsonify({"user_id": user_id, "token": token})


def require_user_jwt():
    """Return (payload, None) on success, or (None, error_response) on failure."""
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return None, (jsonify({"error": "Missing bearer token"}), 401)
    try:
        payload = verify(auth_header[7:])
    except Exception as e:
        return None, (jsonify({"error": f"Invalid token: {e}"}), 401)
    if payload.get("role") != "user":
        return None, (jsonify({"error": "User role required"}), 403)
    return payload, None
