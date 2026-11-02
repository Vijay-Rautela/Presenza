"""Small validation helpers shared by services and later forms."""

from datetime import datetime
import re


def validate_password(password: str, confirm_password: str) -> str | None:
    """Return a friendly error, or None when a new password is acceptable."""
    if password != confirm_password:
        return "The two passwords do not match."
    if len(password) < 8:
        return "Password must have at least 8 characters."
    if not re.search(r"[A-Za-z]", password):
        return "Password must include at least one letter."
    if not re.search(r"\d", password):
        return "Password must include at least one number."
    return None


def validate_date_of_birth(value: str) -> bool:
    """Check the standard YYYY-MM-DD date format used by account activation."""
    try:
        datetime.strptime(value.strip(), "%Y-%m-%d")
        return True
    except ValueError:
        return False
