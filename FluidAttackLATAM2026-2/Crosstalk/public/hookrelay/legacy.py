"""Legacy v1 surface kept for backwards compatibility.

This module exposes the deprecated GraphQL gateway, the public-key
endpoint, the v1 admin endpoint (superseded by the v2 control plane in
3.2), and a deprecated SQLite-backed product search. New integrations
should use the v2 API.
"""

import hashlib
import json
import os
import random
import sqlite3
import time

import jwt
from ariadne import MutationType, QueryType, make_executable_schema
from flask import Blueprint, jsonify, request
from graphql import graphql_sync

from hookrelay.config import (
    JWT_KID,
    RATE_LIMIT_MAX,
    RATE_LIMIT_WINDOW,
)
from hookrelay.jwt_verify import verify as verify_jwt_token
from hookrelay.keys import PRIVATE_KEY, PUBLIC_KEY_PEM

bp = Blueprint("legacy", __name__)

ADMIN_PIN = str(random.randint(1000, 9999))

_request_timestamps: dict[str, list[float]] = {}
_issued_session_nonces: set[str] = set()


def _check_rate_limit(client_ip: str) -> bool:
    now = time.time()
    if client_ip not in _request_timestamps:
        _request_timestamps[client_ip] = []
    _request_timestamps[client_ip] = [
        ts
        for ts in _request_timestamps[client_ip]
        if now - ts < RATE_LIMIT_WINDOW
    ]
    if len(_request_timestamps[client_ip]) >= RATE_LIMIT_MAX:
        return False
    _request_timestamps[client_ip].append(now)
    return True


_type_defs = """
    type Query {
        health: String!
        webhookStats: WebhookStats!
    }

    type Mutation {
        verifyPin(pin: String!): PinResult!
    }

    type PinResult {
        success: Boolean!
        token: String
        message: String!
    }

    type WebhookStats {
        totalDelivered: Int!
        totalFailed: Int!
        uptime: Float!
    }
"""

_query = QueryType()
_mutation = MutationType()


@_query.field("health")
def _resolve_health(*_):
    return "operational"


@_query.field("webhookStats")
def _resolve_webhook_stats(*_):
    return {
        "totalDelivered": 148392,
        "totalFailed": 237,
        "uptime": 99.84,
    }


@_mutation.field("verifyPin")
def _resolve_verify_pin(_, info, pin):
    if pin == ADMIN_PIN:
        nonce = hashlib.sha256(os.urandom(32)).hexdigest()[:16]
        _issued_session_nonces.add(nonce)
        token = jwt.encode(
            {
                "sub": "admin",
                "role": "admin",
                "session_nonce": nonce,
                "iat": int(time.time()),
                "exp": int(time.time()) + 3600,
            },
            PRIVATE_KEY,
            algorithm="RS256",
            headers={"kid": JWT_KID},
        )
        return {
            "success": True,
            "token": token,
            "message": "Authentication successful.",
        }
    return {
        "success": False,
        "token": None,
        "message": "Invalid PIN.",
    }


_schema = make_executable_schema(_type_defs, _query, _mutation)


def _execute_operation(operation):
    return graphql_sync(
        _schema,
        operation.get("query", ""),
        variable_values=operation.get("variables"),
        context_value={"request": request},
    )


def _format_result(result):
    response = {}
    if result.data is not None:
        response["data"] = result.data
    if result.errors:
        response["errors"] = [{"message": str(e)} for e in result.errors]
    return response


@bp.route("/graphql", methods=["POST"])
def graphql_endpoint():
    if not _check_rate_limit(request.remote_addr):
        return jsonify({
            "errors": [{
                "message": "Rate limit exceeded. Maximum 3 requests per minute.",
            }],
        }), 429

    if "application/json" not in (request.content_type or ""):
        return jsonify({
            "errors": [{"message": "Content-Type must be application/json"}],
        }), 400

    body = request.get_json(silent=True)
    if body is None:
        return jsonify({
            "errors": [{"message": "Invalid JSON body"}],
        }), 400

    if isinstance(body, list):
        return jsonify([_format_result(_execute_operation(op)) for op in body])
    return jsonify(_format_result(_execute_operation(body)))


@bp.route("/api/public-key", methods=["GET"])
def public_key():
    return PUBLIC_KEY_PEM.decode(), 200, {
        "Content-Type": "application/x-pem-file",
    }


@bp.route("/api/admin/flag", methods=["GET"])
def admin_flag_v1():
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return jsonify({"error": "Missing or invalid authorization"}), 401

    try:
        payload = verify_jwt_token(auth_header[7:])
    except Exception as e:
        return jsonify({"error": f"Invalid token: {e}"}), 401

    if payload.get("role") != "superadmin":
        return jsonify({
            "error": "Insufficient privileges. Superadmin role required.",
        }), 403

    nonce = payload.get("session_nonce")
    if not nonce or nonce not in _issued_session_nonces:
        return jsonify({
            "error": "Invalid session. Authenticate via the platform first.",
        }), 403

    return jsonify({
        "message": "Webhook admin panel — legacy v1 endpoint. Deprecated.",
    })


@bp.route("/api/v1/legacy/search", methods=["GET"])
def legacy_search():
    q = request.args.get("q", "")

    if not q:
        return jsonify({
            "warning": "Legacy endpoint — will be removed in v2.",
            "results": [],
        })

    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA journal_mode=WAL")
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS legacy_products ("
        "id INTEGER PRIMARY KEY, name TEXT, category TEXT, status TEXT)"
    )
    cursor.executemany(
        "INSERT OR IGNORE INTO legacy_products VALUES (?, ?, ?, ?)",
        [
            (1, "Webhook Router v1", "integration", "deprecated"),
            (2, "Event Dispatcher", "integration", "active"),
            (3, "Log Aggregator", "monitoring", "deprecated"),
            (4, "Alert Manager v2", "monitoring", "active"),
            (5, "API Gateway Legacy", "networking", "deprecated"),
        ],
    )
    conn.commit()

    try:
        query_str = (
            "SELECT id, name, category, status "
            "FROM legacy_products "
            f"WHERE name LIKE '%{q}%' OR category LIKE '%{q}%'"
        )
        cursor.execute(query_str)
        rows = cursor.fetchall()
    except sqlite3.OperationalError:
        conn.close()
        return jsonify({
            "warning": "Legacy endpoint — will be removed in v2.",
            "error": "Query failed.",
            "results": [],
        })

    results = [
        {"id": r[0], "name": r[1], "category": r[2], "status": r[3]}
        for r in rows
    ]
    conn.close()
    return jsonify({
        "warning": "Legacy endpoint — will be removed in v2.",
        "results": results,
    })
