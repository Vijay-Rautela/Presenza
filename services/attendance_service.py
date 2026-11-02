"""Teacher attendance, correction, and leave-approval rules."""

from datetime import date, datetime, timedelta
import sqlite3

from database.db import database_session, get_connection


class AttendanceServiceError(Exception):
    """Expected Teacher workflow error, safe to show in the UI."""


VALID_STATUSES = {"Present", "Absent", "Late"}


def _as_date(value: str) -> date:
    try:
        return datetime.strptime(value.strip(), "%Y-%m-%d").date()
    except ValueError as error:
        raise AttendanceServiceError("Use date format YYYY-MM-DD.") from error


def _teacher_id(connection, user_id: int) -> int:
    teacher = connection.execute("SELECT id FROM teachers WHERE user_id = ?", (user_id,)).fetchone()
    if teacher is None:
        raise AttendanceServiceError("The signed-in account is not a Teacher account.")
    return teacher["id"]


def _assignment_for_teacher(connection, user_id: int, assignment_id: int):
    teacher_id = _teacher_id(connection, user_id)
    assignment = connection.execute(
        """SELECT * FROM teaching_assignments
           WHERE id = ? AND teacher_id = ?""", (assignment_id, teacher_id)
    ).fetchone()
    if assignment is None:
        raise AttendanceServiceError("You are not assigned to this class and subject.")
    return assignment


def list_assignments(user_id: int):
    """Return only the subject/class combinations assigned to this teacher."""
    with get_connection() as connection:
        teacher_id = _teacher_id(connection, user_id)
        return connection.execute(
            """SELECT teaching_assignments.id, subjects.code, subjects.name AS subject,
                      courses.name AS course, teaching_assignments.semester,
                      teaching_assignments.section
               FROM teaching_assignments JOIN subjects ON subjects.id = teaching_assignments.subject_id
               JOIN courses ON courses.id = teaching_assignments.course_id
               WHERE teaching_assignments.teacher_id = ?
               ORDER BY subjects.code, teaching_assignments.section""", (teacher_id,)
        ).fetchall()


def students_for_assignment(user_id: int, assignment_id: int):
    """Load only the students belonging to a teacher's assigned class."""
    with get_connection() as connection:
        assignment = _assignment_for_teacher(connection, user_id, assignment_id)
        return connection.execute(
            """SELECT id, roll_no, name FROM students
               WHERE course_id = ? AND semester = ? AND section = ? ORDER BY roll_no""",
            (assignment["course_id"], assignment["semester"], assignment["section"]),
        ).fetchall()


def existing_attendance(user_id: int, assignment_id: int, attendance_date: str):
    """Load existing records for correction, scoped to the teacher's assignment."""
    class_date = _as_date(attendance_date)
    with get_connection() as connection:
        assignment = _assignment_for_teacher(connection, user_id, assignment_id)
        return connection.execute(
            """SELECT attendance.id, students.id AS student_id, students.roll_no, students.name,
                      attendance.status, attendance.date
               FROM attendance JOIN students ON students.id = attendance.student_id
               WHERE attendance.subject_id = ? AND attendance.date = ?
                 AND students.course_id = ? AND students.semester = ? AND students.section = ?
               ORDER BY students.roll_no""",
            (assignment["subject_id"], class_date.isoformat(), assignment["course_id"], assignment["semester"], assignment["section"]),
        ).fetchall()


def mark_attendance(user_id: int, assignment_id: int, attendance_date: str, records: list[tuple[int, str]]) -> int:
    """Insert one full attendance list after all Poka-Yoke checks pass."""
    class_date = _as_date(attendance_date)
    if class_date > date.today():
        raise AttendanceServiceError("Attendance cannot be marked for a future date.")
    if not records:
        raise AttendanceServiceError("Load the class and choose at least one attendance status.")
    if any(status not in VALID_STATUSES for _, status in records):
        raise AttendanceServiceError("Attendance status must be Present, Absent, or Late.")

    try:
        with database_session() as connection:
            assignment = _assignment_for_teacher(connection, user_id, assignment_id)
            valid_students = {row["id"] for row in connection.execute(
                "SELECT id FROM students WHERE course_id = ? AND semester = ? AND section = ?",
                (assignment["course_id"], assignment["semester"], assignment["section"]),
            )}
            submitted_students = {student_id for student_id, _ in records}
            if submitted_students != valid_students:
                raise AttendanceServiceError("The submitted list does not match this assigned class.")
            duplicate = connection.execute(
                """SELECT 1 FROM attendance WHERE subject_id = ? AND date = ?
                   AND student_id IN (SELECT id FROM students WHERE course_id = ? AND semester = ? AND section = ?)
                   LIMIT 1""", (assignment["subject_id"], class_date.isoformat(), assignment["course_id"], assignment["semester"], assignment["section"]),
            ).fetchone()
            if duplicate:
                raise AttendanceServiceError("Attendance already exists for this class, subject, and date. Use Corrections if needed.")
            connection.executemany(
                """INSERT INTO attendance (student_id, subject_id, date, status, marked_by)
                   VALUES (?, ?, ?, ?, ?)""",
                [(student_id, assignment["subject_id"], class_date.isoformat(), status, user_id) for student_id, status in records],
            )
            return len(records)
    except sqlite3.IntegrityError as error:
        raise AttendanceServiceError("A duplicate attendance record was blocked. Refresh and try again.") from error


def edit_attendance(user_id: int, attendance_id: int, new_status: str, reason: str) -> None:
    """Correct one record inside the configured time window and add an audit entry."""
    if new_status not in VALID_STATUSES:
        raise AttendanceServiceError("Choose Present, Absent, or Late.")
    if not reason.strip():
        raise AttendanceServiceError("A reason is required for every attendance correction.")
    with database_session() as connection:
        record = connection.execute(
            """SELECT attendance.id, attendance.status, attendance.date, attendance.subject_id,
                      students.course_id, students.semester, students.section
               FROM attendance JOIN students ON students.id = attendance.student_id
               WHERE attendance.id = ?""", (attendance_id,)
        ).fetchone()
        if record is None:
            raise AttendanceServiceError("Attendance record not found.")
        teacher_id = _teacher_id(connection, user_id)
        allowed = connection.execute(
            """SELECT 1 FROM teaching_assignments WHERE teacher_id = ? AND subject_id = ?
               AND course_id = ? AND semester = ? AND section = ?""",
            (teacher_id, record["subject_id"], record["course_id"], record["semester"], record["section"]),
        ).fetchone()
        if not allowed:
            raise AttendanceServiceError("You can edit only attendance from your assigned classes.")
        edit_days = int(connection.execute("SELECT value FROM settings WHERE key = 'edit_window_days'").fetchone()["value"])
        if date.today() - _as_date(record["date"]) > timedelta(days=edit_days):
            raise AttendanceServiceError(f"The {edit_days}-day correction window for this record has closed.")
        if record["status"] == new_status:
            raise AttendanceServiceError("Choose a different status to make a correction.")
        connection.execute("UPDATE attendance SET status = ? WHERE id = ?", (new_status, attendance_id))
        connection.execute(
            """INSERT INTO attendance_logs (attendance_id, old_status, new_status, changed_by, reason)
               VALUES (?, ?, ?, ?, ?)""", (attendance_id, record["status"], new_status, user_id, reason.strip())
        )


def pending_leave_requests(user_id: int):
    """Show a teacher only requests from students in their assigned classes."""
    with get_connection() as connection:
        teacher_id = _teacher_id(connection, user_id)
        return connection.execute(
            """SELECT DISTINCT leave_requests.id, students.roll_no, students.name,
                      leave_requests.from_date, leave_requests.to_date, leave_requests.reason,
                      leave_requests.status
               FROM leave_requests JOIN students ON students.id = leave_requests.student_id
               JOIN teaching_assignments ON teaching_assignments.course_id = students.course_id
                   AND teaching_assignments.semester = students.semester
                   AND teaching_assignments.section = students.section
               WHERE teaching_assignments.teacher_id = ? AND leave_requests.status = 'Pending'
               ORDER BY leave_requests.from_date""", (teacher_id,)
        ).fetchall()


def decide_leave_request(user_id: int, leave_id: int, decision: str) -> None:
    """Approve or reject a visible leave request. Approval marks existing class records Leave."""
    if decision not in {"Approved", "Rejected"}:
        raise AttendanceServiceError("Leave decision must be Approved or Rejected.")
    with database_session() as connection:
        teacher_id = _teacher_id(connection, user_id)
        leave = connection.execute(
            """SELECT leave_requests.*, students.course_id, students.semester, students.section
               FROM leave_requests JOIN students ON students.id = leave_requests.student_id
               WHERE leave_requests.id = ? AND leave_requests.status = 'Pending'""", (leave_id,)
        ).fetchone()
        if leave is None:
            raise AttendanceServiceError("That leave request is no longer pending.")
        assignments = connection.execute(
            """SELECT subject_id FROM teaching_assignments WHERE teacher_id = ? AND course_id = ?
               AND semester = ? AND section = ?""", (teacher_id, leave["course_id"], leave["semester"], leave["section"])
        ).fetchall()
        if not assignments:
            raise AttendanceServiceError("You can approve leave only for your assigned classes.")
        connection.execute("UPDATE leave_requests SET status = ?, approved_by = ? WHERE id = ?", (decision, user_id, leave_id))
        if decision == "Approved":
            for assignment in assignments:
                connection.execute(
                    "UPDATE attendance SET status = 'Leave' "
                    "WHERE student_id = ? AND subject_id = ? AND date BETWEEN ? AND ?",
                    (
                        leave["student_id"],
                        assignment["subject_id"],
                        leave["from_date"],
                        leave["to_date"],
                    ),
                )
