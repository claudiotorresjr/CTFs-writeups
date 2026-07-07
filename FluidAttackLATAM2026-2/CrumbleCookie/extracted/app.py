import hashlib
import os
from urllib.parse import quote

from flask import Flask, jsonify, request

app = Flask(__name__)

# Our 16-character API key secures all download tokens
SECRET_KEY = os.environ.get("SECRET_KEY", "????????????????")
FLAG = os.environ.get("FLAG", "flag{????????????????}")

FILES = {
    "public/welcome.txt": (
        "Welcome to SecureVault File Sharing!\n"
        "\n"
        "This platform provides cryptographically signed\n"
        "download links to ensure file integrity and access\n"
        "control. Only authorized files can be retrieved.\n"
        "\n"
        "Available files:\n"
        "  - public/welcome.txt\n"
        "  - public/notes.txt\n"
    ),
    "public/notes.txt": (
        "Project meeting notes - Q2 2026\n"
        "================================\n"
        "- Migrate API auth to HMAC-based tokens\n"
        "- Review file access control policies\n"
        "- Update signing mechanism (pending)\n"
    ),
}


def sign(message_bytes):
    """Sign a message using SHA256(SECRET_KEY + message)."""
    return hashlib.sha256(SECRET_KEY.encode() + message_bytes).hexdigest()


def parse_token_params(token_bytes):
    """Parse key=value pairs separated by '&' from token bytes."""
    parts = {}
    try:
        token_str = token_bytes.decode("latin-1")
    except Exception:
        return parts

    for segment in token_str.split("&"):
        if "=" in segment:
            key, _, value = segment.partition("=")
            parts[key] = value
    return parts


@app.route("/")
def index():
    return jsonify({
        "service": "SecureVault File Sharing API",
        "version": "1.2.0",
        "endpoints": {
            "/files": "List available files with signed download tokens",
            "/download": "Download a file using a signed token",
        },
    })


@app.route("/files")
def list_files():
    file_list = []
    for filepath in sorted(FILES.keys()):
        token = f"action=download&file={filepath}"
        sig = sign(token.encode())
        encoded_token = quote(token, safe="")
        file_list.append({
            "path": filepath,
            "token": token,
            "sig": sig,
            "download": f"/download?token={encoded_token}&sig={sig}",
        })
    return jsonify({"files": file_list})


@app.route("/download")
def download():
    token = request.args.get("token", "")
    sig = request.args.get("sig", "")

    if not token or not sig:
        return jsonify({"error": "Missing token or sig parameter"}), 400

    token_bytes = token.encode("latin-1")

    expected_sig = sign(token_bytes)
    if sig != expected_sig:
        return jsonify({"error": "Invalid signature"}), 403

    params = parse_token_params(token_bytes)
    filepath = params.get("file")

    if not filepath:
        return jsonify({"error": "No file specified in token"}), 400

    if filepath == "private/flag.txt":
        return jsonify({
            "filename": "private/flag.txt",
            "content": FLAG,
        })

    if filepath in FILES:
        return jsonify({
            "filename": filepath,
            "content": FILES[filepath],
        })

    return jsonify({"error": "File not found"}), 404


@app.route("/health")
def health():
    return "ok"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
