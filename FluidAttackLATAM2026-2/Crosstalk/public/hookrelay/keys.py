"""PEM key loading."""

from cryptography.hazmat.primitives.serialization import (
    load_pem_private_key,
    load_pem_public_key,
)

from hookrelay.config import PRIVATE_KEY_PATH, PUBLIC_KEY_PATH

PRIVATE_KEY_PEM = open(PRIVATE_KEY_PATH, "rb").read()
PUBLIC_KEY_PEM = open(PUBLIC_KEY_PATH, "rb").read()
PRIVATE_KEY = load_pem_private_key(PRIVATE_KEY_PEM, password=None)
PUBLIC_KEY = load_pem_public_key(PUBLIC_KEY_PEM)
