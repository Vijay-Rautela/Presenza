"""Authentication and account-activation rules for Presenza."""

from dataclasses import dataclass

from database.db import database_session, get_connection
from utils.security import hash_password, verify_password
from utils.validators import validate_date_of_birth, validate_password


class AuthenticationError(Exception):
    """An expected authentication error that can be shown safely in the UI."""


@dataclass(frozen=True)
class AuthenticatedUser:
    """The small, safe user object passed from login to a role dashboard."""

    id: int
    login_id: str
    role: str
    display_name: str
    must_change_password: bool


def _display_name(connection, user_id: int, role: str, login_id: str) -> str:
    """Read the person's name without exposing any extra database details."""
    if role == "Teacher":
        row = connection.execute("SELECT name FROM teachers WHERE user_id = ?", (user_id,)).fetchone()
        return row["name"] if row else login_id
    if role == "Student":
        row = connection.execute("SELECT name FROM students WHERE user_id = ?", (user_id,)).fetchone()
        return row["name"] if row else login_id
    return "Administrator"


def login(login_id: str, password: str) -> AuthenticatedUser:
    """Verify active credentials and return the user's permitted role."""
    if not login_id.strip() or not password:
        raise AuthenticationError("Enter both your login ID and password.")

    with get_connection() as connection:
        user = connection.execute(
            """SELECT id, login_id, role, password_hash, is_active, must_change_password
               FROM users WHERE login_id = ?""",
            (login_id.strip(),),
        ).fetchone()
        if user is None:
            raise AuthenticationError("No account was found with that login ID.")
        if not user["is_active"]:
            raise AuthenticationError("This account is inactive. Please choose Activate Account first.")
        if not user["password_hash"] or not verify_password(password, user["password_hash"]):
            raise AuthenticationError("The login ID or password is incorrect.")
        return AuthenticatedUser(
            id=user["id"],
            login_id=user["login_id"],
            role=user["role"],
            display_name=_display_name(connection, user["id"], user["role"], user["login_id"]),
            must_change_password=bool(user["must_change_password"]),
        )


def activate_account(login_id: str, dob: str, password: str, confirm_password: str) -> None:
    """Activate an inactive teacher or student account after DOB verification."""
    clean_id = login_id.strip()
    clean_dob = dob.strip()
    if not clean_id or not clean_dob:
        raise AuthenticationError("Enter your login ID and date of birth.")
    if not validate_date_of_birth(clean_dob):
        raise AuthenticationError("Use date of birth format YYYY-MM-DD.")
    password_error = validate_password(password, confirm_password)
    if password_error:
        raise AuthenticationError(password_error)

    with database_session() as connection:
        user = connection.execute(
            "SELECT id, role, dob, is_active FROM users WHERE login_id = ?", (clean_id,)
        ).fetchone()
        if user is None or user["role"] == "Admin" or user["dob"] != clean_dob:
            raise AuthenticationError("The login ID and date of birth do not match our records.")
        if user["is_active"]:
            raise AuthenticationError("This account is already active. Please log in instead.")
        connection.execute(
            """UPDATE users SET password_hash = ?, is_active = 1, must_change_password = 0
               WHERE id = ?""",
            (hash_password(password), user["id"]),
        )


def change_password(user_id: int, password: str, confirm_password: str) -> None:
    """Save a validated password and remove the first-login password-change flag."""
    password_error = validate_password(password, confirm_password)
    if password_error:
        raise AuthenticationError(password_error)
    with database_session() as connection:
        connection.execute(
            "UPDATE users SET password_hash = ?, must_change_password = 0 WHERE id = ?",
            (hash_password(password), user_id),
        )
