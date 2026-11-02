"""Small, reusable SQLite access layer.

Views must call services, and services use these helpers instead of creating their
own connections. This keeps database setup and safe parameterised SQL consistent.
"""

import sqlite3
from contextlib import contextmanager
from pathlib import Path

from config import DATABASE_PATH


def get_connection() -> sqlite3.Connection:
    """Return an SQLite connection with rows readable by column name."""
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


@contextmanager
def database_session():
    """Commit a successful transaction or roll it back if an error occurs."""
    connection = get_connection()
    try:
        yield connection
        connection.commit()
    except sqlite3.Error:
        connection.rollback()
        raise
    finally:
        connection.close()


def apply_schema() -> None:
    """Create every required table and index. It is safe to call repeatedly."""
    schema_path = Path(__file__).with_name("schema.sql")
    with get_connection() as connection:
        connection.executescript(schema_path.read_text(encoding="utf-8"))


def initialize_database() -> None:
    """Create the schema and add starter data when it is not already present."""
    apply_schema()
    # Imported here to keep seed data separate from the connection helpers.
    from database.seed_data import seed_database

    seed_database()
