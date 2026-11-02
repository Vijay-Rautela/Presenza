"""Role-scoped attendance reporting and CSV export."""

from pathlib import Path

from database.db import get_connection


class ReportServiceError(Exception):
    """Expected report error that can be shown to the user."""


def _scope_clause(role: str, user_id: int) -> tuple[str, tuple]:
    if role == "Admin":
        return "", ()
    if role == "Teacher":
        return """AND EXISTS (
            SELECT 1 FROM teaching_assignments ta JOIN teachers t ON t.id = ta.teacher_id
            WHERE t.user_id = ? AND ta.subject_id = attendance.subject_id
              AND ta.course_id = students.course_id AND ta.semester = students.semester
              AND ta.section = students.section)""", (user_id,)
    raise ReportServiceError("Reports are available to Admin and Teacher accounts only.")


def _percentage(present: int, total: int) -> float:
    return round((present / total) * 100, 1) if total else 0.0


def student_report(role: str, user_id: int) -> list[dict]:
    """Student-wise attendance, restricted to the caller's allowed records."""
    clause, parameters = _scope_clause(role, user_id)
    with get_connection() as connection:
        rows = connection.execute(
            f"""SELECT students.roll_no, students.name, COUNT(attendance.id) AS total,
                       SUM(CASE WHEN attendance.status IN ('Present', 'Late') THEN 1 ELSE 0 END) AS present
                FROM attendance JOIN students ON students.id = attendance.student_id
                WHERE 1 = 1 {clause} GROUP BY students.id ORDER BY students.roll_no""", parameters
        ).fetchall()
    return [{"roll_no": row["roll_no"], "name": row["name"], "attended": row["present"] or 0, "total": row["total"], "percentage": _percentage(row["present"] or 0, row["total"])} for row in rows]


def subject_report(role: str, user_id: int) -> list[dict]:
    """Subject-wise attendance percentages in the caller's permitted scope."""
    clause, parameters = _scope_clause(role, user_id)
    with get_connection() as connection:
        rows = connection.execute(
            f"""SELECT subjects.code, subjects.name, COUNT(attendance.id) AS total,
                       SUM(CASE WHEN attendance.status IN ('Present', 'Late') THEN 1 ELSE 0 END) AS present
                FROM attendance JOIN subjects ON subjects.id = attendance.subject_id
                JOIN students ON students.id = attendance.student_id
                WHERE 1 = 1 {clause} GROUP BY subjects.id ORDER BY subjects.code""", parameters
        ).fetchall()
    return [{"code": row["code"], "subject": row["name"], "attended": row["present"] or 0, "total": row["total"], "percentage": _percentage(row["present"] or 0, row["total"])} for row in rows]


def monthly_report(role: str, user_id: int) -> list[dict]:
    """Month-by-month attendance percentages for the allowed scope."""
    clause, parameters = _scope_clause(role, user_id)
    with get_connection() as connection:
        rows = connection.execute(
            f"""SELECT substr(attendance.date, 1, 7) AS month, COUNT(attendance.id) AS total,
                       SUM(CASE WHEN attendance.status IN ('Present', 'Late') THEN 1 ELSE 0 END) AS present
                FROM attendance JOIN students ON students.id = attendance.student_id
                WHERE 1 = 1 {clause} GROUP BY month ORDER BY month""", parameters
        ).fetchall()
    return [{"month": row["month"], "attended": row["present"] or 0, "total": row["total"], "percentage": _percentage(row["present"] or 0, row["total"])} for row in rows]


def defaulter_report(role: str, user_id: int) -> list[dict]:
    """Student-wise list below the live Admin-configured threshold."""
    with get_connection() as connection:
        minimum = float(connection.execute("SELECT value FROM settings WHERE key = 'min_attendance'").fetchone()["value"])
    return [row | {"minimum": minimum} for row in student_report(role, user_id) if row["percentage"] < minimum]


def export_csv(rows: list[dict], destination: str) -> Path:
    """Export report rows through Pandas, creating the chosen parent folder."""
    if not rows:
        raise ReportServiceError("There is no report data to export.")
    try:
        import pandas as pd
        path = Path(destination)
        path.parent.mkdir(parents=True, exist_ok=True)
        safe_rows = []
        for row in rows:
            safe_row = {}
            for key, value in row.items():
                text = str(value) if value is not None else ""
                safe_row[key] = f"'{text}" if text.startswith(("=", "+", "-", "@")) else value
            safe_rows.append(safe_row)
        pd.DataFrame(safe_rows).to_csv(path, index=False)
        return path
    except Exception as error:
        raise ReportServiceError(f"Could not export the CSV: {error}") from error
