#!/usr/bin/env python3
import argparse
import hashlib
import json
import random
import re
import time

import requests
from ecdsa import NIST256p
from ecdsa.numbertheory import inverse_mod
from fpylll import IntegerMatrix, LLL
from urllib3.exceptions import InsecureRequestWarning


CURVE = NIST256p
ORDER = CURVE.order
GENERATOR = CURVE.generator
NONCE_BOUND = 1 << 248
SCALE = 256


def _int_hex(value):
    return hex(int(value))


def _point_from_private(private_key):
    return private_key * GENERATOR


def _parse_hex(value):
    if isinstance(value, int):
        return value
    return int(value, 16)


def collect_signatures(session, base_url, count, delay):
    samples = []
    for i in range(count):
        message = json.dumps(
            {"request": i, "type": "standard"},
            separators=(",", ":"),
            sort_keys=True,
        )
        resp = session.post(
            f"{base_url}/api/sign",
            json={"message": message},
            timeout=15,
        )
        if resp.status_code == 429:
            time.sleep(1.05)
            resp = session.post(
                f"{base_url}/api/sign",
                json={"message": message},
                timeout=15,
            )
        resp.raise_for_status()
        data = resp.json()
        r = _parse_hex(data["signature"]["r"])
        s = _parse_hex(data["signature"]["s"])
        z = int(data["hash"], 16)
        samples.append((r, s, z))
        if delay:
            time.sleep(delay)
    return samples


def public_key(session, base_url):
    resp = session.get(f"{base_url}/api/info", timeout=15)
    resp.raise_for_status()
    data = resp.json()
    if "public_key" not in data:
        raise RuntimeError(
            "/api/info did not return a Nonce Upon a Time public key. "
            f"Response was: {json.dumps(data, sort_keys=True)}"
        )
    key = data["public_key"]
    return _parse_hex(key["x"]), _parse_hex(key["y"])


def recover_private_key(samples, public_point=None):
    relations = []
    modulus = ORDER * SCALE
    for r, s, z in samples:
        s_inv = inverse_mod(s, ORDER)
        a = (r * s_inv) % ORDER
        b = (z * s_inv) % ORDER
        relations.append((a, b))

    m = len(relations)
    embedding = SCALE * NONCE_BOUND
    matrix = IntegerMatrix(m + 2, m + 2)

    for i in range(m):
        matrix[i, i] = modulus

    for i, (a, b) in enumerate(relations):
        matrix[m, i] = (a * SCALE) % modulus
        matrix[m + 1, i] = (b * SCALE) % modulus

    matrix[m, m] = 1
    matrix[m + 1, m + 1] = embedding

    LLL.reduction(matrix)

    candidates = set()
    for row_index in range(m + 2):
        row = [matrix[row_index, col] for col in range(m + 2)]
        if abs(row[-1]) == embedding:
            candidates.add(row[-2] % ORDER)
            candidates.add((-row[-2]) % ORDER)

    for candidate in candidates:
        if not candidate:
            continue
        if public_point is None:
            return candidate
        point = _point_from_private(candidate)
        if int(point.x()) == public_point[0] and int(point.y()) == public_point[1]:
            return candidate

    raise RuntimeError("private key recovery failed; collect more signatures")


def sign_token(private_key, token):
    z = int.from_bytes(hashlib.sha256(token.encode("utf-8")).digest(), "big")
    while True:
        k = random.randrange(1, ORDER)
        point = k * GENERATOR
        r = int(point.x()) % ORDER
        if not r:
            continue
        s = (inverse_mod(k, ORDER) * (z + r * private_key)) % ORDER
        if s:
            return r, s


def activate(session, base_url, token, r, s):
    resp = session.post(
        f"{base_url}/api/activate",
        json={"token": token, "r": _int_hex(r), "s": _int_hex(s)},
        timeout=15,
    )
    resp.raise_for_status()
    return resp.json()


def main():
    parser = argparse.ArgumentParser(
        description="Exploit biased ECDSA nonces in Nonce Upon a Time."
    )
    parser.add_argument("base_url", help="Base URL returned by the deployed CTF instance")
    parser.add_argument("--count", type=int, default=55, help="signatures to collect")
    parser.add_argument(
        "--delay",
        type=float,
        default=0.12,
        help="delay between signing requests to respect the 10/s rate limit",
    )
    parser.add_argument(
        "--insecure",
        action="store_true",
        help="disable TLS certificate verification for expired/self-signed CTF certs",
    )
    args = parser.parse_args()
    base_url = args.base_url.rstrip("/")

    if args.insecure:
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

    session = requests.Session()
    session.verify = not args.insecure

    pub = public_key(session, base_url)
    samples = collect_signatures(session, base_url, args.count, args.delay)
    private_key = recover_private_key(samples, pub)

    token = json.dumps(
        {"type": "admin"},
        separators=(",", ":"),
        sort_keys=True,
    )
    r, s = sign_token(private_key, token)
    result = activate(session, base_url, token, r, s)
    print(json.dumps(result, indent=2, sort_keys=True))

    text = json.dumps(result)
    flags = sorted(set(re.findall(r"flag\\{[^}]+\\}|fluidctf\\{[^}]+\\}", text, re.I)))
    if flags:
        print("\nFlag:")
        for flag in flags:
            print(flag)


if __name__ == "__main__":
    main()
