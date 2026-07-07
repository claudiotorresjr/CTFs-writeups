import base64
import json
import os
import time

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from flask import Flask, make_response, redirect, request, url_for

app = Flask(__name__)

SECRET_KEY = get_random_bytes(32)
FLAG = os.environ.get("FLAG", "flag{placeholder}")

USERS = {
    "guest": {"password": "guest123", "role": "viewer"},
}


def encrypt_session(data: dict) -> str:
    plaintext = json.dumps(data).encode()
    nonce = get_random_bytes(12)
    cipher = AES.new(SECRET_KEY, AES.MODE_GCM, nonce=nonce)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)
    blob = nonce + tag + ciphertext
    return base64.b64encode(blob).decode()


def decrypt_session(cookie: str) -> dict:
    try:
        raw = base64.b64decode(cookie)
        nonce = raw[:12]
        tag = raw[12:28]
        ciphertext = raw[28:]
        cipher = AES.new(SECRET_KEY, AES.MODE_GCM, nonce=nonce)
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        return json.loads(plaintext)
    except Exception:
        session_data = json.loads(base64.b64decode(cookie))
        return session_data


@app.route("/")
def index():
    return redirect(url_for("login"))


@app.route("/health")
def health():
    return "ok", 200


@app.route("/login", methods=["GET", "POST"])
def login():
    error = ""
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        if username in USERS and USERS[username]["password"] == password:
            session_data = {
                "user": username,
                "role": USERS[username]["role"],
                "iat": int(time.time()),
            }
            token = encrypt_session(session_data)
            resp = make_response(redirect(url_for("dashboard")))
            resp.set_cookie(
                "session_token",
                token,
                httponly=True,
                samesite="Lax",
            )
            return resp
        error = "Invalid username or password."

    error_html = ""
    if error:
        error_html = f'<div class="error-msg">{error}</div>'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>SecureVault - Sign In</title>
</head>
<body>
<h1>SecureVault Login</h1>
{error_html}
<p>Guest access: guest / guest123</p>
<form method="POST" action="/login">
  <label>Username</label>
  <input type="text" name="username">
  <label>Password</label>
  <input type="password" name="password">
  <button type="submit">Sign In</button>
</form>
</body>
</html>"""


@app.route("/dashboard")
def dashboard():
    cookie = request.cookies.get("session_token")
    if not cookie:
        return redirect(url_for("login"))

    try:
        session_data = decrypt_session(cookie)
    except Exception:
        return redirect(url_for("login"))

    user = session_data.get("user", "unknown")
    role = session_data.get("role", "viewer")

    if role == "admin":
        flag_section = f"<p><b>Admin Recovery Key:</b> {FLAG}</p>"
    else:
        flag_section = "<p>Admin privileges required to view recovery keys.</p>"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>SecureVault - Dashboard</title>
</head>
<body>
<h1>Dashboard</h1>
<p>User: {user} | Role: {role}</p>
{flag_section}
</body>
</html>"""


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
