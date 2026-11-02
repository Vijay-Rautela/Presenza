"""Central configuration for the Presenza desktop application."""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
DATABASE_DIR = PROJECT_ROOT / "database"
DATABASE_PATH = DATABASE_DIR / "ams.db"
BACKUP_DIR = PROJECT_ROOT / "backups"

APP_NAME = "Presenza"
DEFAULT_MIN_ATTENDANCE = "75"
DEFAULT_EDIT_WINDOW_DAYS = "2"

# Shared visual language for the CustomTkinter screens built in later phases.
COLORS = {
    "primary": "#1B874B",
    "primary_dark": "#136A3B",
    "primary_light": "#22C55E",
    "accent": "#C4881C",
    "danger": "#DC3545",
    "danger_dark": "#B02A37",
    "late": "#E08316",
    "late_dark": "#B86609",
    "success": "#1B874B",
    "sand": "#D5CCA6",
    "cove": "#D4DFD7",
    "background": "#F7F5EA",
    "background_alt": "#E3ECE6",
    "surface": "#FFFFFF",
    "text": "#11261B",
    "muted": "#506859",
    "border": "#CFDDD3",
    "sidebar": "#0D2E1F",
    "sidebar_hover": "#174D34",
    "sidebar_active": "#1B874B",
    "sidebar_text": "#F4FAF6",
}
