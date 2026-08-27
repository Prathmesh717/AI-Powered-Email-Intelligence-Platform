"""JWT-based authentication for Smartai."""

from Smartai.auth.jwt import (
    JWTError,
    create_access_token,
    decode_access_token,
)

__all__ = ["JWTError", "create_access_token", "decode_access_token"]
