"""Password hashing helpers using Python's built-in PBKDF2 implementation."""

import hashlib
import hmac
import os


ITERATIONS = 260_000


def hash_password(password: str) -> str:
    """Return a salted PBKDF2 hash; never store a plain-text password."""
    salt = os.urandom(16)
    password_hash = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, ITERATIONS)
    return f"pbkdf2_sha256${ITERATIONS}${salt.hex()}${password_hash.hex()}"


def verify_password(password: str, stored_hash: str) -> bool:
    """Safely compare a password with the hash produced by hash_password."""
    try:
        algorithm, iterations, salt_hex, hash_hex = stored_hash.split("$")
        if algorithm != "pbkdf2_sha256":
            return False
        calculated = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), bytes.fromhex(salt_hex), int(iterations)
        )
        return hmac.compare_digest(calculated.hex(), hash_hex)
    except (AttributeError, TypeError, ValueError):
        return False
