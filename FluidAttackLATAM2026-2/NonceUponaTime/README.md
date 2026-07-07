# Nonce Upon a Time

## Metadata

| Field | Value |
| --- | --- |
| Category | Cryptography |
| Difficulty | Hard |
| Points | 500 |
| Solves | 91 |
| First Blood | serrooT |

## Challenge Description

```text
LicenseForge signs license tokens with ECDSA. Regular users get regular tokens. Admins get the good stuff.

The source shipped to the repo by accident.
```

## Artifacts

The provided file is an encrypted zip. The password is `infected`:

```bash
7z x -pinfected public.zip -oextracted -y
```

After extraction:

```text
public.zip
extracted/server.py
solve_nonce.py
```

`server.py` is the leaked Flask service. `solve_nonce.py` is the exploit script
used to collect signatures, recover the private key, and activate a forged admin
license.

## Recon

The Python script is small enough to read top-to-bottom. The imports classify
the challenge before naming any vulnerability:

```python
from ecdsa import NIST256p, SigningKey
from ecdsa.numbertheory import inverse_mod
from flask import Flask, jsonify, request
```

This is a Flask API that implements ECDSA signing and verification itself. The
route decorators expose the attack surface:

```text
GET  /api/info       exposes curve parameters and the public key
POST /api/sign       signs user-controlled license JSON strings
POST /api/activate   verifies a submitted license token and signature
```

From that API map, the security boundary is clear: normal users can obtain
standard signatures, but the flag requires a verified admin token. This makes
the challenge an ECDSA license-forgery problem.

### Key Lifecycle

After mapping the API, I checked whether the private key was hardcoded or
derived from something predictable. Near the top of `server.py`, before any
route handler, the signing globals are initialized:

```python
from ecdsa import NIST256p, SigningKey

CURVE = NIST256p
ORDER = CURVE.order
GENERATOR = CURVE.generator

SIGNING_KEY = SigningKey.generate(curve=CURVE)
VERIFYING_KEY = SIGNING_KEY.get_verifying_key()
PRIVATE_KEY_INT = SIGNING_KEY.privkey.secret_multiplier
```

I searched `NIST256p` and found that it is an elliptic curve: NIST P-256, also
known as `secp256r1`, commonly used with ECDSA. In this code:

- `CURVE = NIST256p` selects P-256.
- `SigningKey.generate(curve=CURVE)` creates the private key at process start.
- `get_verifying_key()` derives the matching public key.
- `PRIVATE_KEY_INT` stores the private scalar used by the manual signer.

So the private key is not statically leaked in `server.py`; it exists only in
server memory.

## Vulnerability

With the API model and key lifecycle understood, I checked whether the signing
oracle could be used directly for an admin license. It cannot:

```python
if isinstance(parsed, dict) and parsed.get("type") == "admin":
    return jsonify({
        "error": "Admin license tokens cannot be signed via this endpoint"
    }), 403
```

`/api/activate` also verifies the signature before checking whether the token is
admin:

```python
if not _verify_signature(token_bytes, r, s):
    return jsonify({"error": "Invalid signature"}), 401

token_data = json.loads(token_str)
license_type = token_data.get("type", "standard")

if license_type == "admin":
    return jsonify({"flag": FLAG, ...})
```

So the useful target is signature forgery, not JSON parsing.

### Why Nonce Generation Became Suspicious

The source contains a commented RFC 6979 deterministic nonce function:

```python
# def deterministic_nonce(private_key, message_hash):
#     """RFC 6979 deterministic nonce generation.
#
#     Generates k deterministically from the private key and message hash
#     so that nonce reuse is impossible and timing leaks are mitigated.
#     See: https://tools.ietf.org/html/rfc6979
#
#     TODO: switch to RFC 6979 deterministic nonces -- current
#     implementation uses random nonces which should be sufficient
#     for our license activation volume. Tracked in JIRA-4821.
#     """
```

That function is commented and is not the vulnerability. Its value is as a clue:
it points directly at ECDSA nonce safety. The live signer is implemented manually
in `_sign_message`:

```python
msg_hash = hashlib.sha256(message_bytes).digest()
z = int.from_bytes(msg_hash, "big")

k = random.getrandbits(256) >> 8

while k == 0 or k >= ORDER:
    k = random.getrandbits(256) >> 8

point = k * GENERATOR
r = point.x() % ORDER

s = (inverse_mod(k, ORDER) * (z + r * PRIVATE_KEY_INT)) % ORDER
```

The suspicious operation is the bit shift in nonce generation:

```python
k = random.getrandbits(256) >> 8
```

At this point I searched terms like:

```text
ECDSA biased nonce
ECDSA partial nonce leakage
ECDSA hidden number problem
CTF ECDSA biased nonce
```

The references confirmed the direction:

- NIST FIPS 186-5 describes ECDSA's per-message secret number `k` and requires
  it to be generated in `[1, n-1]`; it also notes deterministic ECDSA protects
  against attacks from insufficient randomness.
- Kelby Ludwig's Hidden Number Problem tutorial explains how approximate modular
  relations can be solved with lattice methods.
- Joachim Breitner's Bitcoin ECDSA nonce writeup is a real example of spotting
  nonce structure and turning it into key recovery.
- The TSG CTF 2021 writeup "Cracking Biased Nonces in ECDSA" shows the same
  class of idea in a CTF: weird nonce structure becomes an Extended Hidden
  Number Problem solved with lattice reduction.

The useful lesson from the 2021 CTF writeup was the entropy check: ECDSA `k`
should be uniformly distributed, so low entropy or forced structure in `k` is
suspicious. There the structure came from digit encoding. Here it is simpler:
`>> 8` forces every nonce to have at most 248 bits.

```text
1 <= k < 2^248
```

For P-256, the group order `n` is approximately `2^256`, and a safe nonce should
be uniform in `[1, n-1]`. Here the top 8 bits of every nonce are known to be zero
when `k` is viewed as a 256-bit scalar. That is partial nonce leakage.

## Exploitation

### Manual API Checks

Before automating the attack, I tested the local API with `curl`.

`/api/info` exposes public ECDSA parameters, but not the private key:

```bash
BASE_URL="http://127.0.0.1:8080"
curl -s "$BASE_URL/api/info"
```

Local response from one run. The public key changes when the server restarts
because the key is generated at process start:

```json
{
  "curve": "NIST P-256",
  "generator": {
    "x": "0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296",
    "y": "0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5"
  },
  "order": "0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551",
  "public_key": {
    "x": "0x99071a3efaa3a9b8b800fa4da622b7cc16e10a4d3f725e708caa742ca6a22e4f",
    "y": "0x3a34b777bc2e819141231ed5620f0b424c2a51166a474ad0bc51b3e829706678"
  },
  "public_key_hex": "99071a3efaa3a9b8b800fa4da622b7cc16e10a4d3f725e708caa742ca6a22e4f3a34b777bc2e819141231ed5620f0b424c2a51166a474ad0bc51b3e829706678"
}
```

A normal token can be signed:

```bash
curl -s -X POST "$BASE_URL/api/sign" \
  -H "Content-Type: application/json" \
  --data '{"message":"{\"request\":0,\"type\":\"standard\"}"}'
```

Local response from one run. The signature changes on each request because the
server generates a new ECDSA nonce:

```json
{
  "hash": "86376106d2560a7f855407b7678bca4a71aee4aca20cc4682f27804adfc53c65",
  "message": "{\"request\":0,\"type\":\"standard\"}",
  "public_key": "99071a3efaa3a9b8b800fa4da622b7cc16e10a4d3f725e708caa742ca6a22e4f3a34b777bc2e819141231ed5620f0b424c2a51166a474ad0bc51b3e829706678",
  "signature": {
    "r": "0x15cd9897c63495ced9d8538fb86ac738fb2f03536d6737bf1390086f89cbe4b4",
    "s": "0xcff11bb7e7ddfa9bcca23ac022da26158d70318fe0e281d7dda14cd2edf80de8"
  }
}
```

But admin tokens cannot be signed through the oracle:

```bash
curl -i -s -X POST "$BASE_URL/api/sign" \
  -H "Content-Type: application/json" \
  --data '{"message":"{\"type\":\"admin\"}"}'
```

```text
HTTP/1.1 403 FORBIDDEN

{"error":"Admin license tokens cannot be signed via this endpoint"}
```

Sending an admin token with a fake signature also fails:

```bash
curl -i -s -X POST "$BASE_URL/api/activate" \
  -H "Content-Type: application/json" \
  --data '{"token":"{\"type\":\"admin\"}","r":"0x1","s":"0x1"}'
```

```text
HTTP/1.1 401 UNAUTHORIZED

{"error":"Invalid signature"}
```

These checks show the exploit path: collect valid standard signatures, recover
the private key, then sign an admin token locally.

### Chain

1. Collect standard signatures from `/api/sign`.

   ```json
   {"request":0,"type":"standard"}
   {"request":1,"type":"standard"}
   {"request":2,"type":"standard"}
   ```

   `request` is only an application-level field used to make every message
   different. It is not the vulnerable ECDSA nonce. The vulnerable nonce is the
   internal signing value `k` generated by `_sign_message`.

2. Convert each `(r, s, z)` sample into:

   ```text
   k_i = (r_i*s_i^-1)*d + (z_i*s_i^-1) mod n
   k_i < 2^248
   ```

3. Solve the resulting Hidden Number Problem with LLL.

4. Verify the recovered private key against the public key from `/api/info`.

5. Sign the compact admin token:

   ```json
   {"type":"admin"}
   ```

6. Submit the forged token to `/api/activate`.

## Technical Details

ECDSA over group order `n` signs message hash `z` with private key `d` and nonce
`k` as:

```text
r = x(kG) mod n
s = k^-1 * (z + r*d) mod n
```

Rearrange:

```text
s*k = z + r*d                 mod n
k = (r*s^-1)*d + (z*s^-1)     mod n
```

For each signature `i`:

```text
a_i = r_i * s_i^-1 mod n
b_i = z_i * s_i^-1 mod n
k_i = a_i*d + b_i mod n
```

The private key `d` is the same for every signature. The vulnerable code gives
the nonce bound:

```text
0 < k_i < B
B = 2^248
```

So for every signature there is an integer `q_i` such that:

```text
a_i*d + b_i - q_i*n = k_i
abs(k_i) < 2^248
```

That is the Hidden Number Problem shape.

The exploit builds the relations in `recover_private_key()`:

```python
for r, s, z in samples:
    s_inv = inverse_mod(s, ORDER)
    a = (r * s_inv) % ORDER
    b = (z * s_inv) % ORDER
    relations.append((a, b))
```

Then it builds the lattice:

```python
NONCE_BOUND = 1 << 248
SCALE = 256

modulus = ORDER * SCALE
embedding = SCALE * NONCE_BOUND
matrix = IntegerMatrix(m + 2, m + 2)

for i in range(m):
    matrix[i, i] = modulus

for i, (a, b) in enumerate(relations):
    matrix[m, i] = (a * SCALE) % modulus
    matrix[m + 1, i] = (b * SCALE) % modulus

matrix[m, m] = 1
matrix[m + 1, m + 1] = embedding
```

The useful linear combination is:

```text
d * row_m + row_(m+1) - q_0 * row_0 - ... - q_(m-1) * row_(m-1)
```

Its first coordinates become:

```text
SCALE * (a_i*d + b_i - q_i*n) = SCALE * k_i
```

Because `k_i < 2^248`, those coordinates are bounded by:

```text
256 * 2^248 = 2^256
```

A random coordinate modulo `ORDER * 256` would occupy roughly a `2^264` range,
so the correct vector is unusually short.

After LLL, the exploit scans rows whose last coordinate is `+/- embedding`; the
second-last coordinate is a private-key candidate:

```python
if abs(row[-1]) == embedding:
    candidates.add(row[-2] % ORDER)
    candidates.add((-row[-2]) % ORDER)
```

The candidate is verified against `/api/info`:

```python
point = candidate * GENERATOR
point.x() == public_key.x
point.y() == public_key.y
```

This proves the recovered scalar is the server private key, not just an unrelated
short vector.

## Exploit Artifact

Exploit file:

```text
solve_nonce.py
```

Relevant functions:

- `public_key()` requests `/api/info` and parses the public key.
- `collect_signatures()` requests `/api/sign` and stores `(r, s, z)`.
- `recover_private_key()` builds the HNP lattice and runs `fpylll.LLL`.
- `sign_token()` signs the admin token with the recovered key.
- `activate()` posts the forged token to `/api/activate`.

Run against the remote instance:

```bash
python solve_nonce.py https://ecf6d7f61e4838aa.chal.ctf.ae --insecure
```

I used `--insecure` because the CTF instance served HTTPS with an expired certificate during my run;
without that option, `requests` rejected the connection before reaching `/api/info`.

## Validation

Remote output:

```json
{
  "flag": "flag{e6106e251b448734}",
  "license": "admin",
  "message": "Administrative license activated successfully",
  "status": "activated"
}
```

Local validation:

```bash
FLAG=flag{local_test} python extracted/server.py
```

In another terminal:

```bash
python solve_nonce.py http://127.0.0.1:8080 --count 55 --delay 0.12
```

Local output:

```json
{
  "flag": "flag{local_test}",
  "license": "admin",
  "message": "Administrative license activated successfully",
  "status": "activated"
}
```

## References

- RFC 6979: <https://www.rfc-editor.org/rfc/rfc6979>
- NIST FIPS 186-5: <https://doi.org/10.6028/NIST.FIPS.186-5>
- Hidden Number Problem tutorial: <https://kel.bz/post/hnp/>
- Half-half Bitcoin ECDSA nonces: <https://www.joachim-breitner.de/blog/804-The_curious_case_of_the_half-half_Bitcoin_ECDSA_nonces>
- TSG CTF 2021 biased ECDSA nonces: <https://angmar2722.github.io/2021-10-04-solving-the-extended-hidden-number-problem/>

## Flag

```text
flag{e6106e251b448734}
```
