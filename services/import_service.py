"""Pandas-based, duplicate-aware Admin imports for students and teachers."""

from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path

from services import admin_service


@dataclass
class ImportSummary:
    added: int = 0
    skipped: int = 0
    errors: list[str] = field(default_factory=list)


REQUIRED_COLUMNS = {
    "students": {"roll_no", "name", "dob", "course", "semester", "section", "email"},
    "teachers": {"emp_id", "name", "dob", "department", "email"},
}


def _normalise_value(value, column: str, pandas_module) -> str:
    """Convert spreadsheet values into the strings expected by service validators."""
    if pandas_module.isna(value):
        return ""
    if column == "semester":
        try:
            return str(int(float(value)))
        except (TypeError, ValueError):
            return str(value).strip()
    if column == "dob":
        try:
            parsed = pandas_module.to_datetime(value, errors="raise")
            return parsed.date().isoformat()
        except (TypeError, ValueError, OverflowError):
            return str(value).strip()
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    return str(value).strip()


def import_file(role: str, file_path: str, record_type: str) -> ImportSummary:
    """Import an Admin-selected CSV or Excel file and return a clear summary."""
    if record_type not in REQUIRED_COLUMNS:
        raise admin_service.AdminServiceError("Choose Students or Teachers for import.")
    try:
        import pandas as pd
        path = Path(file_path)
        data = pd.read_excel(path) if path.suffix.lower() in {".xlsx", ".xls"} else pd.read_csv(path)
    except Exception as error:
        raise admin_service.AdminServiceError(f"Could not read that file: {error}") from error
    data.columns = [str(column).strip().lower() for column in data.columns]
    missing = REQUIRED_COLUMNS[record_type] - set(data.columns)
    if missing:
        raise admin_service.AdminServiceError("Missing required columns: " + ", ".join(sorted(missing)))
    summary = ImportSummary()
    courses = {row["name"].lower(): str(row["id"]) for row in admin_service.list_courses(role)}
    for row_number, row in data.iterrows():
        values = {
            column: _normalise_value(row[column], column, pd)
            for column in REQUIRED_COLUMNS[record_type]
        }
        try:
            if record_type == "students":
                course_id = courses.get(values["course"].lower())
                if not course_id:
                    raise admin_service.AdminServiceError(f"Unknown course '{values['course']}'.")
                admin_service.save_student(role, values["roll_no"], values["name"], values["dob"], course_id, values["semester"], values["section"], values["email"])
            else:
                admin_service.save_teacher(role, values["emp_id"], values["name"], values["dob"], values["department"], values["email"])
            summary.added += 1
        except admin_service.AdminServiceError as error:
            summary.skipped += 1
            summary.errors.append(f"Row {row_number + 2}: {error}")
    return summary
