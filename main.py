"""Presenza application entry point."""

from database.db import initialize_database
from utils.logger import get_logger


def main() -> None:
    logger = get_logger()
    try:
        initialize_database()
        # Import after database setup so a first run always has valid starter data.
        from ui.app import PresenzaApp

        app = PresenzaApp()
        app.mainloop()
    except Exception:
        logger.exception("Unexpected application error")
        raise


if __name__ == "__main__":
    main()
