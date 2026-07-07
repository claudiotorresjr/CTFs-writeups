"""Webhook subscription store and management endpoints."""

import secrets
import threading
import time
from typing import Iterator

from flask import Blueprint, jsonify, request

from hookrelay.auth import require_user_jwt

bp = Blueprint("subscriptions", __name__)

ALLOWED_FILTERS = {
    "user.*",
    "user.created",
    "user.updated",
    "webhook.*",
    "webhook.delivered",
    "webhook.failed",
}

_lock = threading.Lock()
_STORE: list[dict] = []


def iter_subscriptions() -> Iterator[dict]:
    with _lock:
        return iter(list(_STORE))


@bp.route("/api/v2/subscriptions", methods=["POST"])
def create_subscription():
    payload, err = require_user_jwt()
    if err:
        return err

    body = request.get_json(silent=True) or {}
    name = body.get("name", "")
    url_template = body.get("url_template", "")
    filter_ = body.get("filter", "user.*")

    if not isinstance(name, str) or not name:
        return jsonify({"error": "name required"}), 400
    if not isinstance(url_template, str) or not url_template.startswith(
        "https://"
    ):
        return jsonify({"error": "url_template must start with https://"}), 400
    if filter_ not in ALLOWED_FILTERS:
        return jsonify({
            "error": (
                "filter must be one of: " + ", ".join(sorted(ALLOWED_FILTERS))
            ),
        }), 400

    sub = {
        "id": "sub_" + secrets.token_hex(6),
        "owner": payload["sub"],
        "name": name,
        "url_template": url_template,
        "filter": filter_,
        "created_at": int(time.time()),
    }
    with _lock:
        _STORE.append(sub)

    public = {k: sub[k] for k in (
        "id", "name", "url_template", "filter", "created_at",
    )}
    return jsonify(public), 201


@bp.route("/api/v2/subscriptions", methods=["GET"])
def list_subscriptions():
    payload, err = require_user_jwt()
    if err:
        return err
    with _lock:
        owned = [s for s in _STORE if s["owner"] == payload["sub"]]
    return jsonify([
        {k: s[k] for k in (
            "id", "name", "url_template", "filter", "created_at",
        )}
        for s in owned
    ])
