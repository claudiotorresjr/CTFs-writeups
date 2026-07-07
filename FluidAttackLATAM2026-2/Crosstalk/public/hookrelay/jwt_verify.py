"""Custom JWT verifier supporting RS256 and HS256."""

import base64
import hashlib
import hmac
import json
import time

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

from hookrelay.keys import PUBLIC_KEY, PUBLIC_KEY_PEM

SUPPORTED_ALGORITHMS = ["RS256", "HS256"]


def _b64url_decode(data: str) -> bytes:
    padded = data + "=" * (4 - len(data) % 4)
    return base64.urlsafe_b64decode(padded)


def b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def verify(token_str: str) -> dict:
    parts = token_str.split(".")
    if len(parts) != 3:
        raise ValueError("Malformed token")

    header_b64, payload_b64, signature_b64 = parts
    header = json.loads(_b64url_decode(header_b64))
    alg = header.get("alg")

    if alg not in SUPPORTED_ALGORITHMS:
        raise ValueError(f"Unsupported algorithm: {alg}")

    signing_input = f"{header_b64}.{payload_b64}".encode()
    signature = _b64url_decode(signature_b64)

    if alg == "RS256":
        PUBLIC_KEY.verify(
            signature,
            signing_input,
            padding.PKCS1v15(),
            hashes.SHA256(),
        )
    elif alg == "HS256":
        expected = hmac.new(
            PUBLIC_KEY_PEM,
            signing_input,
            hashlib.sha256,
        ).digest()
        if not hmac.compare_digest(signature, expected):
            raise ValueError("Invalid signature")

    payload = json.loads(_b64url_decode(payload_b64))
    for field in ("sub", "role", "exp"):
        if field not in payload:
            raise ValueError(f"Missing required claim: {field}")
    if payload.get("exp", 0) < time.time():
        raise ValueError("Token expired")

    return payload
