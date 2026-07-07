#!/usr/bin/env python3
"""FluidVault backup decryption helper.

Decrypts the ``vault_backup.enc`` file exported by the FluidVault Android
app. The backup is a raw binary blob laid out exactly as the
``/api/vault/info`` endpoint documents:

    [ 12-byte IV ][ ciphertext ][ 16-byte GCM tag ]

encrypted with AES-256-GCM.

Usage:
    python3 vault_decrypt.py <key_hex>

where ``<key_hex>`` is the 64-character hex AES-256 key. Recover the key
by re-implementing the PBKDF2 derivation found in the decompiled
``CryptoManager.java`` source (decompiled/com/fluidvault/crypto/).

Requires the ``cryptography`` package (``pip install cryptography``).
"""
import sys
from pathlib import Path

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

BACKUP_FILE = Path(__file__).resolve().parent / "vault_backup.enc"
IV_LENGTH = 12


def decrypt(key: bytes, blob: bytes) -> bytes:
    """Decrypt an AES-256-GCM blob laid out as iv || ciphertext || tag."""
    iv = blob[:IV_LENGTH]
    ciphertext_and_tag = blob[IV_LENGTH:]
    return AESGCM(key).decrypt(iv, ciphertext_and_tag, None)


def main() -> int:
    """Parse the key argument, decrypt vault_backup.enc, print the JSON."""
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} <key_hex>", file=sys.stderr)
        return 2

    key_hex = sys.argv[1].strip().lower()
    try:
        key = bytes.fromhex(key_hex)
    except ValueError:
        print("error: key must be hexadecimal", file=sys.stderr)
        return 2

    if len(key) != 32:
        print(
            "error: AES-256 key must be 32 bytes (64 hex chars)",
            file=sys.stderr,
        )
        return 2

    if not BACKUP_FILE.exists():
        print(
            f"error: {BACKUP_FILE.name} not found next to this script",
            file=sys.stderr,
        )
        return 1

    blob = BACKUP_FILE.read_bytes()
    try:
        plaintext = decrypt(key, blob)
    except Exception as exc:  # InvalidTag and friends
        print(
            f"error: decryption failed ({exc}) -- wrong key?",
            file=sys.stderr,
        )
        return 1

    print(plaintext.decode("utf-8"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
