import hashlib


def _normalize_password(password: str) -> str:
    if password is None:
        return ""
    # You can still truncate if you want, but SHA-256 has no 72-byte limit.
    return str(password)


def get_password_hash(password: str) -> str:
    password = _normalize_password(password)
    # SHA-256 hash, hex string
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    plain_password = _normalize_password(plain_password)
    return get_password_hash(plain_password) == hashed_password
