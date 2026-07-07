"""Control-plane endpoint."""

import hmac

from flask import Blueprint, jsonify, request

from hookrelay.config import FLAG, HEARTBEAT_TOKEN

bp = Blueprint("control", __name__)


@bp.route("/api/v2/admin/control", methods=["GET"])
def admin_control():
    token = request.headers.get("X-Heartbeat-Token", "")
    if not token:
        return jsonify({"error": "Missing X-Heartbeat-Token header"}), 401
    if not hmac.compare_digest(token, HEARTBEAT_TOKEN):
        return jsonify({"error": "Invalid heartbeat token"}), 403
    return jsonify({
        "flag": FLAG,
        "endpoint": "control_plane",
        "version": "v2",
    })
