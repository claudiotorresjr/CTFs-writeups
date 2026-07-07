import hashlib
import json
import os
import re
import secrets
import shlex
import time

import jwt
from flask import Flask, Response, jsonify, request

app = Flask(__name__)

BOOT_TIMESTAMP = None
SESSION_SECRET = None
XOR_ENCODED_SECRET = None
API_KEYS = {}

ALLOWED_FILE_EXTENSIONS = (".json", ".yml", ".db")

SANDBOX_BUILTINS = {
    "print": print,
    "range": range,
    "len": len,
    "str": str,
    "int": int,
    "list": list,
    "dict": dict,
    "type": type,
    "getattr": getattr,
    "hasattr": hasattr,
    "chr": chr,
    "ord": ord,
    "bool": bool,
    "tuple": tuple,
    "set": set,
    "float": float,
    "abs": abs,
    "max": max,
    "min": min,
    "sorted": sorted,
    "enumerate": enumerate,
    "zip": zip,
    "map": map,
    "filter": filter,
    "reversed": reversed,
    "isinstance": isinstance,
    "repr": repr,
    "hex": hex,
}

BLOCKED_PATTERNS = [
    r"\bos\b",
    r"\bsubprocess\b",
    r"\b__import__\b",
    r"\bimport\b",
    r"\bopen\b",
    r"\beval\b",
    r"\bexec\b",
    r"\bcompile\b",
    r"\bglobals\b",
    r"\blocals\b",
    r"\bbreakpoint\b",
    r"\binput\b",
]

SAFE_TEMPLATE_CHARS = re.compile(r"^[a-zA-Z0-9 .,!?:;\-_@#()]+$")

ALLOWED_COMMANDS = {"status", "version", "uptime", "help"}


def xor_bytes(data: bytes, key: bytes) -> bytes:
    return bytes(
        d ^ key[i % len(key)] for i, d in enumerate(data)
    )


def init_app():
    global BOOT_TIMESTAMP, SESSION_SECRET, XOR_ENCODED_SECRET

    BOOT_TIMESTAMP = int(time.time())

    SESSION_SECRET = os.urandom(24).hex()

    ts_hash = hashlib.sha256(
        str(BOOT_TIMESTAMP).encode()
    ).digest()
    xor_key = ts_hash[: len(SESSION_SECRET)]
    XOR_ENCODED_SECRET = xor_bytes(
        SESSION_SECRET.encode(), xor_key
    ).hex()

    internal_dir = "/app/.internal"
    os.makedirs(internal_dir, exist_ok=True)
    config = {
        "session_secret": XOR_ENCODED_SECRET,
        "version": "2.1.0",
    }
    config_path = os.path.join(internal_dir, "config.json")
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)

    API_KEYS["viewer"] = secrets.token_hex(16)
    API_KEYS["editor"] = secrets.token_hex(16)


def verify_admin_token():
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return None
    token = auth_header[7:]
    try:
        payload = jwt.decode(
            token, SESSION_SECRET, algorithms=["HS256"]
        )
        if payload.get("role") == "admin":
            return payload
        return None
    except (jwt.InvalidTokenError, jwt.DecodeError):
        return None


def verify_any_token():
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return None
    token = auth_header[7:]
    try:
        return jwt.decode(
            token, SESSION_SECRET, algorithms=["HS256"]
        )
    except (jwt.InvalidTokenError, jwt.DecodeError):
        return None


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify(
        {
            "status": "ok",
            "started_at": BOOT_TIMESTAMP,
            "version": "2.1.0",
            "uptime_seconds": int(time.time()) - BOOT_TIMESTAMP,
        }
    )


@app.route("/api/docs", methods=["GET"])
def docs():
    return jsonify(
        {
            "api": "FlowForge Automation Platform",
            "version": "2.1.0",
            "endpoints": [
                {
                    "path": "/api/health",
                    "method": "GET",
                    "description": "Service health status",
                },
                {
                    "path": "/api/webhooks/trigger",
                    "method": "POST",
                    "description": (
                        "Trigger a workflow via webhook. "
                        "Accepts JSON payload with workflow_id. "
                        "Optionally include a 'files' array of "
                        "{path} objects to attach file metadata; "
                        "only .json, .yml, and .db files are permitted."
                    ),
                },
                {
                    "path": "/api/auth/verify",
                    "method": "POST",
                    "description": "Verify authentication token",
                },
            ],
        }
    )


@app.route("/api/webhooks/trigger", methods=["POST"])
def webhook_trigger():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({"error": "Invalid JSON payload"}), 400

    workflow_id = body.get("workflow_id")
    if not workflow_id:
        return jsonify(
            {"error": "workflow_id is required"}
        ), 400

    files_meta = body.get("files")
    if files_meta and isinstance(files_meta, list):
        results = []
        for entry in files_meta:
            if not isinstance(entry, dict):
                continue
            fpath = entry.get("path", "")
            if not isinstance(fpath, str):
                continue
            fpath = os.path.normpath(fpath)
            if not any(
                fpath.endswith(ext)
                for ext in ALLOWED_FILE_EXTENSIONS
            ):
                results.append(
                    {
                        "path": fpath,
                        "error": (
                            "Unsupported file extension. "
                            "Allowed: .json, .yml, .db"
                        ),
                    }
                )
                continue
            try:
                with open(fpath, "r") as f:
                    content = f.read(4096)
                results.append(
                    {
                        "path": fpath,
                        "metadata": {
                            "size": len(content),
                            "preview": content[:512],
                        },
                    }
                )
            except FileNotFoundError:
                results.append(
                    {"path": fpath, "error": "File not found"}
                )
            except PermissionError:
                results.append(
                    {
                        "path": fpath,
                        "error": "Permission denied",
                    }
                )
        return jsonify(
            {
                "workflow_id": workflow_id,
                "status": "triggered",
                "file_metadata": results,
            }
        )

    return jsonify(
        {
            "workflow_id": workflow_id,
            "status": "triggered",
            "message": "Workflow execution queued",
        }
    )


@app.route("/api/auth/verify", methods=["POST"])
def auth_verify():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({"error": "Invalid request body"}), 400

    token = body.get("token", "")
    if not token:
        return jsonify({"error": "Token is required"}), 400

    try:
        payload = jwt.decode(
            token, SESSION_SECRET, algorithms=["HS256"]
        )
        return jsonify(
            {
                "valid": True,
                "user": payload.get("user", "unknown"),
                "role": payload.get("role", "viewer"),
            }
        )
    except jwt.ExpiredSignatureError:
        return jsonify(
            {"valid": False, "error": "Token expired"}
        ), 401
    except jwt.InvalidTokenError:
        return jsonify(
            {"valid": False, "error": "Invalid token"}
        ), 401


# ── Red herring: looks like command injection but is safe ──
@app.route("/api/workflows/debug", methods=["POST"])
def workflow_debug():
    user = verify_any_token()
    if user is None:
        return jsonify(
            {"error": "Authentication required"}
        ), 403

    body = request.get_json(silent=True)
    if body is None:
        return jsonify({"error": "Invalid request body"}), 400

    command = body.get("command", "").strip()
    if not command:
        return jsonify(
            {"error": "Command is required"}
        ), 400

    sanitized = shlex.quote(command)
    if sanitized.strip("'") not in ALLOWED_COMMANDS:
        return jsonify(
            {
                "error": (
                    f"Unknown command: {sanitized}. "
                    "Allowed: status, version, uptime, help"
                )
            }
        ), 400

    responses = {
        "status": {"status": "running", "pid": 1},
        "version": {"version": "2.1.0", "build": "2026.03"},
        "uptime": {
            "uptime_seconds": int(time.time())
            - BOOT_TIMESTAMP
        },
        "help": {
            "commands": list(ALLOWED_COMMANDS),
            "note": "Debug commands are read-only",
        },
    }
    return jsonify(responses.get(command, {"error": "Unknown"}))


# ── Red herring: SSTI-looking template but properly escaped ──
@app.route("/api/notifications/preview", methods=["POST"])
def notification_preview():
    user = verify_any_token()
    if user is None:
        return jsonify(
            {"error": "Authentication required"}
        ), 403

    body = request.get_json(silent=True)
    if body is None:
        return jsonify({"error": "Invalid request body"}), 400

    template = body.get("template", "")
    if not isinstance(template, str) or len(template) > 200:
        return jsonify(
            {"error": "Template must be a string under 200 chars"}
        ), 400

    if not SAFE_TEMPLATE_CHARS.match(template):
        return jsonify(
            {
                "error": (
                    "Template contains invalid characters. "
                    "Only alphanumeric and basic punctuation "
                    "allowed."
                )
            }
        ), 400

    name = user.get("user", "User")
    safe_name = re.sub(r"[^a-zA-Z0-9 _-]", "", str(name))
    rendered = template.replace("{name}", safe_name)
    rendered = rendered.replace(
        "{date}", time.strftime("%Y-%m-%d")
    )

    return jsonify(
        {
            "preview": rendered,
            "note": "Template variables: {name}, {date}",
        }
    )


# ── Red herring: file upload that looks exploitable ──
@app.route("/api/workflows/import", methods=["POST"])
def workflow_import():
    admin = verify_admin_token()
    if admin is None:
        return jsonify(
            {"error": "Admin authentication required"}
        ), 403

    body = request.get_json(silent=True)
    if body is None:
        return jsonify({"error": "Invalid request body"}), 400

    workflow_data = body.get("workflow")
    if not isinstance(workflow_data, dict):
        return jsonify(
            {
                "error": (
                    "workflow must be a JSON object with "
                    "name, steps, and trigger fields"
                )
            }
        ), 400

    name = workflow_data.get("name", "")
    if not isinstance(name, str) or len(name) > 50:
        return jsonify(
            {"error": "Workflow name must be under 50 chars"}
        ), 400
    if not re.match(r"^[a-zA-Z0-9 _-]+$", name):
        return jsonify(
            {
                "error": (
                    "Workflow name contains invalid characters"
                )
            }
        ), 400

    steps = workflow_data.get("steps", [])
    if not isinstance(steps, list) or len(steps) > 10:
        return jsonify(
            {"error": "Steps must be a list with max 10 entries"}
        ), 400

    for step in steps:
        if not isinstance(step, dict):
            return jsonify(
                {"error": "Each step must be a JSON object"}
            ), 400
        step_type = step.get("type", "")
        if step_type not in ("http", "transform", "filter"):
            return jsonify(
                {
                    "error": (
                        f"Invalid step type: {step_type}. "
                        "Allowed: http, transform, filter"
                    )
                }
            ), 400

    return jsonify(
        {
            "imported": True,
            "workflow_id": f"wf-{secrets.token_hex(4)}",
            "name": name,
            "steps_count": len(steps),
        }
    )


# ── Actual vulnerable endpoint (admin only) ──
@app.route("/api/workflows/evaluate", methods=["POST"])
def workflow_evaluate():
    admin = verify_admin_token()
    if admin is None:
        return jsonify(
            {"error": "Admin authentication required"}
        ), 403

    body = request.get_json(silent=True)
    if body is None:
        return jsonify({"error": "Invalid request body"}), 400

    expression = body.get("expression", "")
    if not isinstance(expression, str) or not expression.strip():
        return jsonify(
            {"error": "Expression is required"}
        ), 400

    if len(expression) > 1000:
        return jsonify(
            {"error": "Expression too long (max 1000 chars)"}
        ), 400

    for pattern in BLOCKED_PATTERNS:
        if re.search(pattern, expression):
            return (
                jsonify(
                    {
                        "error": (
                            "Blocked keyword detected: "
                            f"{pattern.strip(chr(92)).strip('b')}"
                        )
                    }
                ),
                400,
            )

    try:
        collected_output = []

        def sandbox_print(*args, **kwargs):
            collected_output.append(
                " ".join(str(a) for a in args)
            )

        sandbox_builtins = dict(SANDBOX_BUILTINS)
        sandbox_builtins["print"] = sandbox_print

        restricted_globals = {
            "__builtins__": sandbox_builtins
        }
        restricted_locals = {}

        code = compile(expression, "<sandbox>", "exec")
        exec(code, restricted_globals, restricted_locals)

        return jsonify(
            {
                "result": "\n".join(collected_output)
                if collected_output
                else None,
                "variables": {
                    k: repr(v)
                    for k, v in restricted_locals.items()
                    if not k.startswith("_")
                },
            }
        )

    except SyntaxError as e:
        return jsonify(
            {"error": f"Syntax error: {e}"}
        ), 400
    except Exception as e:
        return jsonify(
            {"error": f"Runtime error: {str(e)}"}
        ), 400


@app.route("/api/workflows", methods=["GET"])
def list_workflows():
    admin = verify_admin_token()
    if admin is None:
        return jsonify(
            {"error": "Authentication required"}
        ), 403
    return jsonify(
        {
            "workflows": [
                {
                    "id": "wf-001",
                    "name": "Data Pipeline Sync",
                    "status": "active",
                },
                {
                    "id": "wf-002",
                    "name": "Alert Notification",
                    "status": "paused",
                },
                {
                    "id": "wf-003",
                    "name": "Report Generator",
                    "status": "active",
                },
            ]
        }
    )


@app.route("/api/system/info", methods=["GET"])
def system_info():
    admin = verify_admin_token()
    if admin is None:
        return jsonify(
            {"error": "Authentication required"}
        ), 403
    return jsonify(
        {
            "platform": "FlowForge",
            "version": "2.1.0",
            "python": "3.12",
            "environment": "production",
            "features": [
                "webhook_triggers",
                "expression_eval",
                "scheduled_workflows",
            ],
        }
    )


@app.route("/", methods=["GET"])
def index():
    return Response(
        json.dumps(
            {
                "service": "FlowForge Automation Platform",
                "version": "2.1.0",
                "docs": "/api/docs",
            },
            indent=2,
        ),
        mimetype="application/json",
    )


@app.errorhandler(404)
def not_found(error):
    return Response(
        json.dumps(
            {
                "error": "Not Found",
                "service": "FlowForge Automation Platform",
                "message": (
                    "The requested FlowForge endpoint does not exist; "
                    "see the API documentation for available routes."
                ),
                "docs": "/api/docs",
            },
            indent=2,
        ),
        status=404,
        mimetype="application/json",
    )


# Initialize at import so the app works under gunicorn (single worker keeps
# the in-memory SESSION_SECRET / BOOT_TIMESTAMP consistent across requests).
init_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
