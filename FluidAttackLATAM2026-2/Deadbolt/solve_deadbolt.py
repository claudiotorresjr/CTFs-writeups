#!/usr/bin/env python3
import argparse
import json
import ssl
import urllib.error
import urllib.request
from pathlib import Path
from hashlib import pbkdf2_hmac

from cryptography.hazmat.primitives.ciphers.aead import AESGCM


SEED = "fluidvault_master_seed_2026"
DEFAULT_DEVICE_ID = "DEFAULT_DEVICE_ID"
SALT = bytes.fromhex("a915c3e00dbb5a55ba13d7cdaf3a126e")
ITERATIONS = 10000
KEY_LENGTH_BYTES = 32
IV_LENGTH = 12


def java_string_hashcode(value: str) -> int:
    result = 0
    for char in value:
        result = (31 * result + ord(char)) & 0xffffffff
    return result


def derive_key(serial: str = DEFAULT_DEVICE_ID) -> tuple[str, str, bytes]:
    device_hash = java_string_hashcode(serial)
    device_id = format(device_hash, "x")
    passphrase = SEED + device_id
    key = pbkdf2_hmac(
        "sha256",
        passphrase.encode(),
        SALT,
        ITERATIONS,
        KEY_LENGTH_BYTES,
    )
    return device_id, passphrase, key


def decrypt_backup(key: bytes, backup_path: Path) -> dict:
    blob = backup_path.read_bytes()
    iv = blob[:IV_LENGTH]
    ciphertext_and_tag = blob[IV_LENGTH:]
    plaintext = AESGCM(key).decrypt(iv, ciphertext_and_tag, None)
    return json.loads(plaintext.decode())


def save_json(evidence_dir: Path | None, name: str, data) -> None:
    if not evidence_dir:
        return
    evidence_dir.mkdir(parents=True, exist_ok=True)
    (evidence_dir / name).write_text(
        json.dumps(data, indent=2, sort_keys=True) + "\n",
    )


def request_json(base_url: str, path: str, data=None, context=None):
    headers = {"Accept": "application/json"}
    body = None
    method = "GET"
    if data is not None:
        body = json.dumps(data).encode()
        headers["Content-Type"] = "application/json"
        method = "POST"
    req = urllib.request.Request(
        base_url.rstrip("/") + path,
        data=body,
        headers=headers,
        method=method,
    )
    try:
        with urllib.request.urlopen(req, timeout=20, context=context) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode(errors="replace")
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            parsed = raw
        raise RuntimeError(f"{method} {path} returned HTTP {exc.code}: {parsed}") from exc


def find_admin_password(vault: dict) -> str:
    for entry in vault.get("entries", []):
        if entry.get("name") == "Admin Portal" and entry.get("username") == "admin":
            return entry["password"]
    raise RuntimeError("Admin Portal entry not found in decrypted vault")


def main():
    parser = argparse.ArgumentParser(
        description="Solve Deadbolt/FluidVault from the encrypted backup and decompiled crypto code.",
    )
    parser.add_argument(
        "--backup",
        default="extracted/vault_backup.enc",
        help="Path to vault_backup.enc.",
    )
    parser.add_argument(
        "--target",
        help="Optional remote base URL, for example https://host.",
    )
    parser.add_argument(
        "--insecure",
        action="store_true",
        help="Disable TLS certificate validation for the optional remote target.",
    )
    parser.add_argument(
        "--evidence-dir",
        help="Directory where JSON evidence files will be written.",
    )
    args = parser.parse_args()

    evidence_dir = Path(args.evidence_dir) if args.evidence_dir else None
    backup_path = Path(args.backup)

    print("[+] Deriving fallback device id and AES-256 key")
    device_id, passphrase, key = derive_key()
    derivation = {
        "serial": DEFAULT_DEVICE_ID,
        "device_id": device_id,
        "passphrase": passphrase,
        "salt_hex": SALT.hex(),
        "iterations": ITERATIONS,
        "key_hex": key.hex(),
    }
    save_json(evidence_dir, "01_key_derivation.json", derivation)
    print(f"[+] device_id = {device_id}")
    print(f"[+] key       = {key.hex()}")

    print("[+] Decrypting vault backup")
    vault = decrypt_backup(key, backup_path)
    save_json(evidence_dir, "02_decrypted_vault.json", vault)
    admin_password = find_admin_password(vault)
    save_json(evidence_dir, "03_admin_credential.json", {
        "username": "admin",
        "master_password": admin_password,
    })
    print(f"[+] Admin master password = {admin_password}")

    if args.target:
        context = ssl._create_unverified_context() if args.insecure else None
        print("[+] Reading remote vault info")
        info = request_json(args.target, "/api/vault/info", context=context)
        save_json(evidence_dir, "04_vault_info.json", info)

        print("[+] Submitting admin master password")
        response = request_json(
            args.target,
            "/api/vault/admin",
            data={"master_password": admin_password},
            context=context,
        )
        save_json(evidence_dir, "05_admin_response.json", response)
        print(json.dumps(response, indent=2, sort_keys=True))
    else:
        print(json.dumps(vault, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
