"""Student-scoped attendance and leave-request rules."""

from datetime import date, datetime

from database.db import database_session, get_connection


class StudentServiceError(Exception):
    """Expected Student portal error that can be displayed safely."""


def _student_id(connection, user_id: int) -> int:
    student = connection.execute("SELECT id FROM students WHERE user_id = ?", (user_id,)).fetchone()
    if student is None:
        raise StudentServiceError("The signed-in account is not a Student account.")
    return student["id"]


def _percentage(present: int, total: int) -> float:
    return round((present / total) * 100, 1) if total else 0.0


def dashboard_data(user_id: int) -> dict:
    """Return only the signed-in student's summary and subject percentages."""
    with get_connection() as connection:
        student_id = _student_id(connection, user_id)
        minimum = float(connection.execute("SELECT value FROM settings WHERE key = 'min_attendance'").fetchone()["value"])
        totals = connection.execute(
            """SELECT COUNT(*) AS total,
                      SUM(CASE WHEN status IN ('Present', 'Late') THEN 1 ELSE 0 END) AS present
               FROM attendance WHERE student_id = ?""", (student_id,)
        ).fetchone()
        total = totals["total"]
        present = totals["present"] or 0
        subjects = connection.execute(
            """SELECT subjects.code, subjects.name, COUNT(attendance.id) AS total,
                      SUM(CASE WHEN attendance.status IN ('Present', 'Late') THEN 1 ELSE 0 END) AS present
               FROM attendance JOIN subjects ON subjects.id = attendance.subject_id
               WHERE attendance.student_id = ? GROUP BY subjects.id ORDER BY subjects.code""", (student_id,)
        ).fetchall()
        subject_rows = [{"code": row["code"], "name": row["name"], "total": row["total"], "present": row["present"] or 0, "percentage": _percentage(row["present"] or 0, row["total"])} for row in subjects]
        return {"total": total, "present": present, "percentage": _percentage(present, total), "minimum": minimum, "subjects": subject_rows}


def attendance_records(user_id: int):
    """List attendance records belonging only to the signed-in student."""
    with get_connection() as connection:
        student_id = _student_id(connection, user_id)
        return connection.execute(
            """SELECT attendance.date, subjects.code, subjects.name AS subject, attendance.status
               FROM attendance JOIN subjects ON subjects.id = attendance.subject_id
               WHERE attendance.student_id = ? ORDER BY attendance.date DESC, subjects.code""", (student_id,)
        ).fetchall()


def leave_history(user_id: int):
    """List only the signed-in student's leave applications."""
    with get_connection() as connection:
        student_id = _student_id(connection, user_id)
        return connection.execute(
            """SELECT id, from_date, to_date, reason, status FROM leave_requests
               WHERE student_id = ? ORDER BY id DESC""", (student_id,)
        ).fetchall()


def apply_leave(user_id: int, from_date: str, to_date: str, reason: str) -> None:
    """Create one valid leave request and prevent overlapping pending requests."""
    try:
        start = datetime.strptime(from_date.strip(), "%Y-%m-%d").date()
        end = datetime.strptime(to_date.strip(), "%Y-%m-%d").date()
    except ValueError as error:
        raise StudentServiceError("Use YYYY-MM-DD for both leave dates.") from error
    if end < start:
        raise StudentServiceError("The leave end date must be on or after the start date.")
    if end < date.today():
        raise StudentServiceError("A leave request cannot end in the past.")
    if not reason.strip() or len(reason.strip()) < 5:
        raise StudentServiceError("Enter a clear leave reason of at least 5 characters.")
    with database_session() as connection:
        student_id = _student_id(connection, user_id)
        overlap = connection.execute(
            """SELECT 1 FROM leave_requests WHERE student_id = ? AND status = 'Pending'
               AND from_date <= ? AND to_date >= ? LIMIT 1""", (student_id, end.isoformat(), start.isoformat())
        ).fetchone()
        if overlap:
            raise StudentServiceError("A pending leave request already overlaps these dates.")
        connection.execute(
            """INSERT INTO leave_requests (student_id, from_date, to_date, reason)
               VALUES (?, ?, ?, ?)""", (student_id, start.isoformat(), end.isoformat(), reason.strip()))
