# Crumble Cookie

## Metadata

| Field | Value |
| --- | --- |
| Category | `cryptography` |
| Difficulty | Easy |
| Points | 100 |
| Solves | 155 |
| First Blood | Jxckal |

## Challenge Description

```text
SecureVault signs every download link so you can't grab the files you're not
meant to. The dev team is very confident about this.
```

## Artifacts

The provided archive contained a small Flask API:

```text
public.zip
extracted/app.py
solve.py
```

The archive password from the challenge notes was:

```text
infected
```

Target used during the solve:

```text
https://bf34e445fdb6153b.chal.ctf.ae
```

## Recon

I started by checking the archive contents:

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

The source was short, so I mapped the routes first:

```text
GET  /
GET  /files
GET  /download
GET  /health
```

The challenge text mentioned signed download links, so `/files` and `/download`
were the important routes. `/files` creates public download tokens:

```python
for filepath in sorted(FILES.keys()):
    token = f"action=download&file={filepath}"
    sig = sign(token.encode())
    encoded_token = quote(token, safe="")
```

A live request showed the concrete token format and signature value:

```bash
curl -k https://bf34e445fdb6153b.chal.ctf.ae/files
```

Representative item:

```json
{
  "path": "public/notes.txt",
  "token": "action=download&file=public/notes.txt",
  "sig": "41f55a0b9d9266ada1dee2e3fe2fd236cc0491fff56c22700b4d2bc858ba6a66"
}
```

Then `/download` takes `token` and `sig`, verifies the signature, parses the
token, and returns the selected file:

```python
token = request.args.get("token", "")
sig = request.args.get("sig", "")
token_bytes = token.encode("latin-1")

expected_sig = sign(token_bytes)
if sig != expected_sig:
    return jsonify({"error": "Invalid signature"}), 403

params = parse_token_params(token_bytes)
filepath = params.get("file")
```

The target file was visible in the same route:

```python
if filepath == "private/flag.txt":
    return jsonify({
        "filename": "private/flag.txt",
        "content": FLAG,
    })
```

So the problem became: can I produce a valid signature for a token that still
starts as an allowed public download but eventually makes `file` equal
`private/flag.txt`?

## Vulnerability

The first vulnerable artifact is the signing function:

```python
def sign(message_bytes):
    """Sign a message using SHA256(SECRET_KEY + message)."""
    return hashlib.sha256(SECRET_KEY.encode() + message_bytes).hexdigest()
```

This is a raw secret-prefix MAC, not HMAC. The source also gives the key length:

```python
# Our 16-character API key secures all download tokens
SECRET_KEY = os.environ.get("SECRET_KEY", "????????????????")
```

At this point I searched for the pattern `SHA256(secret || message) length
extension`. The useful confirmation was that SHA-256 is a Merkle-Damgard hash,
and secret-prefix constructions like `Hash(secret || message)` are vulnerable to
length extension when the attacker knows the original message, the digest, and
the secret length. The SkullSecurity write-up describes exactly this case and
recommends HMAC instead of a home-grown keyed hash.

The second important artifact is the token parser:

```python
for segment in token_str.split("&"):
    if "=" in segment:
        key, _, value = segment.partition("=")
        parts[key] = value
```

Repeated keys overwrite earlier values. That means an appended suffix like this:

```text
&file=private/flag.txt
```

causes the final parsed dictionary to use the private path, even though the
original signed token started with `file=public/notes.txt`.

The vulnerability is therefore a chain:

```text
public token + public signature
        |
        v
SHA-256 length extension on SHA256(secret || token)
        |
        v
append &file=private/flag.txt with a valid forged signature
        |
        v
duplicate file parameter overwrites the original file value
        |
        v
/download returns private/flag.txt
```

## Exploitation

The exploit chain was:

1. Request `/files` and take one public token plus its signature.
2. Use the known 16-byte secret length from the source comment.
3. Treat the original SHA-256 digest as the internal SHA-256 state after hashing
   `SECRET_KEY || original_token`.
4. Build the SHA-256 glue padding for the unknown secret plus the known token.
5. Continue SHA-256 from that state over `&file=private/flag.txt`.
6. Send the forged token and forged signature to `/download`.
7. Let `parse_token_params()` overwrite the first `file` value with the appended
   `private/flag.txt` value.

The final forged token has this logical shape:

```text
action=download&file=public/notes.txt
<sha256 glue padding for SECRET_KEY || original token>
&file=private/flag.txt
```

The padding contains bytes such as `0x80` and `0x00`, so it cannot be pasted as a
normal ASCII query string. The application decodes the query parameter to a
Python string and then re-encodes it with Latin-1:

```python
token_bytes = token.encode("latin-1")
```

The solver therefore decodes the forged bytes as Latin-1 and then URL-encodes
that string:

```python
return quote(token_bytes.decode("latin-1"), safe="")
```

This makes Werkzeug decode the request into Unicode code points that the app can
encode back to the original byte sequence with `latin-1`.

## Technical Details

[solve.py](solve.py) implements the length extension directly, without relying on
an external `hash_extender` binary.

`sha256_padding()` recreates the padding that SHA-256 would have added after the
unknown secret plus the original token:

```python
def sha256_padding(message_len):
    padding = b"\x80"
    padding += b"\x00" * ((56 - (message_len + 1) % 64) % 64)
    padding += struct.pack(">Q", message_len * 8)
    return padding
```

`parse_state()` converts the original 64-hex-character signature into the eight
32-bit SHA-256 state words:

```python
return tuple(int(digest_hex[i:i + 8], 16) for i in range(0, 64, 8))
```

`forge_token()` glues the pieces together:

```python
original = token.encode("latin-1")
suffix_bytes = suffix.encode("latin-1")
glue = sha256_padding(secret_len + len(original))
processed_len = secret_len + len(original) + len(glue)
forged_sig = sha256_continue(suffix_bytes, parse_state(signature), processed_len)
return original + glue + suffix_bytes, forged_sig
```

The server computes:

```text
SHA256(secret || original || glue_padding || suffix)
```

and the attacker computes the same final digest by continuing from the exposed
digest state. The secret itself is never recovered.

## Exploit Artifact

The final artifact is [solve.py](solve.py).

Local usage:

```bash
SECRET_KEY=abcdefghijklmnop FLAG=flag{local_crumble_cookie} \
  extracted/.venv/bin/python extracted/app.py

python3 solve.py http://127.0.0.1:8080
```

Remote usage:

```bash
python3 solve.py --insecure https://bf34e445fdb6153b.chal.ctf.ae
```

`--insecure` only disables TLS certificate validation because the challenge
certificate was expired during validation. It is not part of the vulnerability.

## Validation

Local validation with a controlled flag:

```text
[*] Original token: action=download&file=public/notes.txt
[*] Forged sig:     3c5fed51e3dd73a854e96540dfb9fb7cca986509c28fbb2a51600db9ea7ef5f3
{
  "content": "flag{local_crumble_cookie}",
  "filename": "private/flag.txt"
}
```

Remote validation:

```text
[*] Original token: action=download&file=public/notes.txt
[*] Original sig:   41f55a0b9d9266ada1dee2e3fe2fd236cc0491fff56c22700b4d2bc858ba6a66
[*] Forged sig:     d0879064cb03ba2b82c21160ca5812fee87263a380c95c9c7cd7495aa8f75398
{
  "content": "flag{750624509935c795}",
  "filename": "private/flag.txt"
}
```

## References

- <https://www.skullsecurity.org/2012/everything-you-need-to-know-about-hash-length-extension-attacks>
- <https://en.wikipedia.org/wiki/Length_extension_attack>
- <https://docs.python.org/3/library/hmac.html>

## Flag

```text
flag{750624509935c795}
```
