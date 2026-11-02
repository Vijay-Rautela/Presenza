"""Safe, timestamped SQLite database backup helper."""

from datetime import datetime
import shutil

from config import BACKUP_DIR, DATABASE_PATH


def create_database_backup(role: str) -> str:
    """Copy the database to backups without overwriting an earlier snapshot."""
    if role != "Admin":
        raise PermissionError("Only an Admin can create a database backup.")
    if not DATABASE_PATH.exists():
        raise FileNotFoundError("The Presenza database has not been created yet.")
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    name = f"presenza_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
    output = BACKUP_DIR / name
    shutil.copy2(DATABASE_PATH, output)
    return str(output)
