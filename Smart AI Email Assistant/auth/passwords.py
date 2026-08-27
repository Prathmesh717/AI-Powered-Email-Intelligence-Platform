_hasher = PasswordHasher()


def hash_password(plaintext: str) -> str:
    """Return an Argon2id encoded hash (includes salt + params)."""
    return _hasher.hash(plaintext)


def verify_password(encoded_hash: str | None, plaintext: str) -> bool:
    """Constant-time verify. Returns False (never raises) on any mismatch or
    malformed/absent hash, so callers can branch without leaking which failed."""
    if not encoded_hash:
        return False
    try:
        return _hasher.verify(encoded_hash, plaintext)
    except (VerifyMismatchError, InvalidHashError, Exception):  # noqa: BLE001
        return False


def needs_rehash(encoded_hash: str) -> bool:
    """True when the stored hash used weaker params than the current policy."""
    try:
        return _hasher.check_needs_rehash(encoded_hash)
    except Exception:  # noqa: BLE001
        return False
