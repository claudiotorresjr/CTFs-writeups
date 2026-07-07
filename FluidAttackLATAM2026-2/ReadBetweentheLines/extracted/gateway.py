"""
API Gateway — public-facing service that proxies requests
to the internal user profile microservice.
"""
import os

import requests as http_client
from flask import Flask, jsonify

app = Flask(__name__)

BACKEND_HOST = os.environ.get("BACKEND_HOST", "127.0.0.1")
BACKEND_PORT = os.environ.get("BACKEND_PORT", "5001")
BACKEND_URL = f"http://{BACKEND_HOST}:{BACKEND_PORT}"


def sanitize_path(user_input):
    """Neutralize path traversal sequences in user input."""
    cleaned = user_input.replace("../", "")
    cleaned = cleaned.replace("..\\", "")
    return cleaned


@app.route("/")
def index():
    """API documentation page."""
    return jsonify({
        "service": "ProfileHub API Gateway",
        "version": "1.2.0",
        "endpoints": {
            "GET /api/users": "List all users",
            "GET /api/profile/<username>": "Get user profile",
            "GET /health": "Health check",
        },
        "note": "All profile requests are routed through "
                "our secure internal microservice.",
    })


@app.route("/api/users")
def list_users():
    """Proxy user listing to backend."""
    try:
        resp = http_client.get(
            f"{BACKEND_URL}/users",
            timeout=5,
        )
        return jsonify(resp.json()), resp.status_code
    except http_client.RequestException:
        return jsonify({"error": "Backend unavailable"}), 502


@app.route("/api/profile/<path:username>")
def get_profile(username):
    """
    Fetch a user profile from the internal backend service.

    The username is validated and sanitized to prevent
    path traversal before forwarding to the backend.
    """
    if not username or len(username) > 128:
        return jsonify({"error": "Invalid username"}), 400

    safe_username = sanitize_path(username)

    if not safe_username:
        return jsonify({"error": "Invalid username"}), 400

    internal_url = (
        f"{BACKEND_URL}/users/{safe_username}"
    )

    try:
        resp = http_client.get(internal_url, timeout=5)
        data = resp.json()
    except http_client.RequestException:
        return jsonify({"error": "Backend unavailable"}), 502
    except ValueError:
        return jsonify({"error": "Invalid backend response"}), 502

    if resp.status_code == 404:
        return jsonify({"error": "User not found"}), 404

    return jsonify(data), resp.status_code


@app.route("/health")
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy"})


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Not Found",
        "service": "ProfileHub API Gateway",
        "message": "The requested ProfileHub API Gateway route does not exist.",
    }), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
