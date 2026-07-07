import secrets
import base64
from typing import Literal

from pydantic import BaseModel


class SessionData(BaseModel):
    username: str = "guest"
    role: Literal["guest", "admin"] = "guest"


class TableData(BaseModel):
    header: list[object]
    rows: list[list[object]]


def generate_session_id() -> str:
    return secrets.token_hex(32)


def validate_session_id(session_id: str | None) -> str | Literal[False]:
    if (
        session_id
        and type(session_id) is str
        and len(session_id) == 64
        and all(c in "0123456789abcdef" for c in session_id)
    ):
        return session_id

    return False


admin_session_id = generate_session_id()
api_write_key = base64.b32encode(secrets.token_bytes(32)).decode()
