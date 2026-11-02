"""Admin-only data-management rules for Presenza Phase 3."""

import sqlite3

from database.db import database_session, get_connection
from utils.security import hash_password
from utils.validators import validate_date_of_birth


class AdminServiceError(Exception):
    """Expected error that the Admin UI can show without crashing."""


def _require_admin(role: str) -> None:
    if role != "Admin":
        raise AdminServiceError("Only an Admin can perform this action.")


def dashboard_counts(role: str) -> dict[str, int]:
    _require_admin(role)
    with get_connection() as connection:
        row = connection.execute(
            """SELECT
                (SELECT COUNT(*) FROM students) AS students,
                (SELECT COUNT(*) FROM teachers) AS teachers,
                (SELECT COUNT(*) FROM subjects) AS subjects,
                (SELECT COUNT(*) FROM attendance WHERE date = date('now')) AS today_attendance"""
        ).fetchone()
        return dict(row)


def list_courses(role: str):
    _require_admin(role)
    with get_connection() as connection:
        return connection.execute("SELECT id, name, duration_years FROM courses ORDER BY name").fetchall()


def save_course(role: str, name: str, duration_years: str, course_id: int | None = None) -> None:
    _require_admin(role)
    if not name.strip() or not duration_years.strip().isdigit() or int(duration_years) < 1:
        raise AdminServiceError("Enter a course name and a valid duration in years.")
    try:
        with database_session() as connection:
            if course_id:
                connection.execute("UPDATE courses SET name = ?, duration_years = ? WHERE id = ?", (name.strip(), int(duration_years), course_id))
            else:
                connection.execute("INSERT INTO courses (name, duration_years) VALUES (?, ?)", (name.strip(), int(duration_years)))
    except sqlite3.IntegrityError as error:
        raise AdminServiceError("A course with that name already exists.") from error


def delete_course(role: str, course_id: int) -> None:
    _require_admin(role)
    try:
        with database_session() as connection:
            connection.execute("DELETE FROM courses WHERE id = ?", (course_id,))
    except sqlite3.IntegrityError as error:
        raise AdminServiceError("This course is in use and cannot be deleted.") from error


def list_subjects(role: str):
    _require_admin(role)
    with get_connection() as connection:
        return connection.execute(
            """SELECT subjects.id, subjects.code, subjects.name, courses.name AS course,
                      subjects.course_id, subjects.semester
               FROM subjects JOIN courses ON courses.id = subjects.course_id
               ORDER BY subjects.code"""
        ).fetchall()


def save_subject(role: str, code: str, name: str, course_id: str, semester: str, subject_id: int | None = None) -> None:
    _require_admin(role)
    if not code.strip() or not name.strip() or not course_id.isdigit() or not semester.isdigit() or int(semester) < 1:
        raise AdminServiceError("Enter subject code, name, course, and a valid semester.")
    try:
        with database_session() as connection:
            values = (code.strip().upper(), name.strip(), int(course_id), int(semester))
            if subject_id:
                connection.execute("UPDATE subjects SET code = ?, name = ?, course_id = ?, semester = ? WHERE id = ?", (*values, subject_id))
            else:
                connection.execute("INSERT INTO subjects (code, name, course_id, semester) VALUES (?, ?, ?, ?)", values)
    except sqlite3.IntegrityError as error:
        raise AdminServiceError("That subject code already exists or its course is invalid.") from error


def delete_subject(role: str, subject_id: int) -> None:
    _require_admin(role)
    try:
        with database_session() as connection:
            connection.execute("DELETE FROM subjects WHERE id = ?", (subject_id,))
    except sqlite3.IntegrityError as error:
        raise AdminServiceError("This subject is in use and cannot be deleted.") from error


def list_teachers(role: str):
    _require_admin(role)
    with get_connection() as connection:
        return connection.execute(
            """SELECT teachers.id, teachers.emp_id, teachers.name, teachers.department,
                      teachers.email, users.dob, users.is_active
               FROM teachers JOIN users ON users.id = teachers.user_id ORDER BY teachers.emp_id"""
        ).fetchall()


def save_teacher(role: str, emp_id: str, name: str, dob: str, department: str, email: str, teacher_id: int | None = None) -> None:
    _require_admin(role)
    if not all((emp_id.strip(), name.strip(), department.strip())) or not validate_date_of_birth(dob):
        raise AdminServiceError("Enter employee ID, name, department, and DOB as YYYY-MM-DD.")
    try:
        with database_session() as connection:
            if teacher_id:
                teacher = connection.execute("SELECT user_id FROM teachers WHERE id = ?", (teacher_id,)).fetchone()
                if teacher is None:
                    raise AdminServiceError("Teacher record was not found.")
                connection.execute("UPDATE users SET login_id = ?, dob = ? WHERE id = ?", (emp_id.strip().upper(), dob.strip(), teacher["user_id"]))
                connection.execute("UPDATE teachers SET emp_id = ?, name = ?, department = ?, email = ? WHERE id = ?", (emp_id.strip().upper(), name.strip(), department.strip(), email.strip(), teacher_id))
            else:
                cursor = connection.execute("INSERT INTO users (login_id, role, dob, is_active) VALUES (?, 'Teacher', ?, 0)", (emp_id.strip().upper(), dob.strip()))
                connection.execute("INSERT INTO teachers (user_id, emp_id, name, department, email) VALUES (?, ?, ?, ?, ?)", (cursor.lastrowid, emp_id.strip().upper(), name.strip(), department.strip(), email.strip()))
    except sqlite3.IntegrityError as error:
        raise AdminServiceError("That employee ID already exists.") from error


def delete_teacher(role: str, teacher_id: int) -> None:
    _require_admin(role)
    try:
        with database_session() as connection:
            record = connection.execute("SELECT user_id FROM teachers WHERE id = ?", (teacher_id,)).fetchone()
            if record:
                connection.execute("DELETE FROM users WHERE id = ?", (record["user_id"],))
    except sqlite3.IntegrityError as error:
        raise AdminServiceError(
            "This teacher has recorded attendance or assignments and cannot be deleted."
        ) from error


def list_students(role: str):
    _require_admin(role)
    with get_connection() as connection:
        return connection.execute(
            """SELECT students.id, students.roll_no, students.name, courses.name AS course,
                      students.course_id, students.semester, students.section, students.email,
                      users.dob, users.is_active
               FROM students JOIN users ON users.id = students.user_id
               JOIN courses ON courses.id = students.course_id ORDER BY students.roll_no"""
        ).fetchall()


def save_student(role: str, roll_no: str, name: str, dob: str, course_id: str, semester: str, section: str, email: str, student_id: int | None = None) -> None:
    _require_admin(role)
    if not all((roll_no.strip(), name.strip(), section.strip())) or not validate_date_of_birth(dob) or not course_id.isdigit() or not semester.isdigit():
        raise AdminServiceError("Enter roll number, name, valid DOB, course, semester, and section.")
    try:
        with database_session() as connection:
            values = (roll_no.strip().upper(), name.strip(), int(course_id), int(semester), section.strip().upper(), email.strip())
            if student_id:
                student = connection.execute("SELECT user_id FROM students WHERE id = ?", (student_id,)).fetchone()
                if student is None:
                    raise AdminServiceError("Student record was not found.")
                connection.execute("UPDATE users SET login_id = ?, dob = ? WHERE id = ?", (values[0], dob.strip(), student["user_id"]))
                connection.execute("UPDATE students SET roll_no = ?, name = ?, course_id = ?, semester = ?, section = ?, email = ? WHERE id = ?", (*values, student_id))
            else:
                cursor = connection.execute("INSERT INTO users (login_id, role, dob, is_active) VALUES (?, 'Student', ?, 0)", (values[0], dob.strip()))
                connection.execute("INSERT INTO students (user_id, roll_no, name, course_id, semester, section, email) VALUES (?, ?, ?, ?, ?, ?, ?)", (cursor.lastrowid, *values))
    except sqlite3.IntegrityError as error:
        raise AdminServiceError("That roll number already exists or the course is invalid.") from error


def delete_student(role: str, student_id: int) -> None:
    _require_admin(role)
    with database_session() as connection:
        record = connection.execute("SELECT user_id FROM students WHERE id = ?", (student_id,)).fetchone()
        if record:
            connection.execute("DELETE FROM users WHERE id = ?", (record["user_id"],))


def list_assignments(role: str):
    _require_admin(role)
    with get_connection() as connection:
        return connection.execute(
            """SELECT teaching_assignments.id, teachers.emp_id, teachers.name AS teacher,
                      subjects.code, subjects.name AS subject, courses.name AS course,
                      teaching_assignments.semester, teaching_assignments.section
               FROM teaching_assignments JOIN teachers ON teachers.id = teaching_assignments.teacher_id
               JOIN subjects ON subjects.id = teaching_assignments.subject_id
               JOIN courses ON courses.id = teaching_assignments.course_id ORDER BY teachers.emp_id, subjects.code"""
        ).fetchall()


def save_assignment(role: str, teacher_id: str, subject_id: str, course_id: str, semester: str, section: str) -> None:
    _require_admin(role)
    if not all(value.isdigit() for value in (teacher_id, subject_id, course_id, semester)) or not section.strip():
        raise AdminServiceError("Choose a teacher, subject, course, semester, and section.")
    try:
        with database_session() as connection:
            connection.execute("INSERT INTO teaching_assignments (teacher_id, subject_id, course_id, semester, section) VALUES (?, ?, ?, ?, ?)", (int(teacher_id), int(subject_id), int(course_id), int(semester), section.strip().upper()))
    except sqlite3.IntegrityError as error:
        raise AdminServiceError("This teaching assignment already exists or contains invalid data.") from error


def delete_assignment(role: str, assignment_id: int) -> None:
    _require_admin(role)
    with database_session() as connection:
        connection.execute("DELETE FROM teaching_assignments WHERE id = ?", (assignment_id,))


def reset_account(role: str, login_id: str) -> None:
    _require_admin(role)
    with database_session() as connection:
        updated = connection.execute("UPDATE users SET password_hash = NULL, is_active = 0, must_change_password = 0 WHERE login_id = ? AND role IN ('Teacher', 'Student')", (login_id.strip(),)).rowcount
        if not updated:
            raise AdminServiceError("Only an existing Teacher or Student account can be reset.")


def get_settings(role: str) -> dict[str, str]:
    _require_admin(role)
    with get_connection() as connection:
        return {row["key"]: row["value"] for row in connection.execute("SELECT key, value FROM settings")}


def save_minimum_attendance(role: str, value: str) -> None:
    _require_admin(role)
    try:
        percentage = float(value)
    except ValueError as error:
        raise AdminServiceError("Minimum attendance must be a number from 0 to 100.") from error
    if not 0 <= percentage <= 100:
        raise AdminServiceError("Minimum attendance must be between 0 and 100.")
    with database_session() as connection:
        connection.execute("UPDATE settings SET value = ? WHERE key = 'min_attendance'", (str(percentage),))


def dashboard_telemetry(role: str) -> dict:
    _require_admin(role)
    with get_connection() as connection:
        counts_row = connection.execute(
            """SELECT
                (SELECT COUNT(*) FROM students) AS students,
                (SELECT COUNT(*) FROM teachers) AS teachers,
                (SELECT COUNT(*) FROM subjects) AS subjects,
                (SELECT COUNT(*) FROM courses) AS courses,
                (SELECT COUNT(*) FROM teaching_assignments) AS assignments,
                (SELECT COUNT(*) FROM attendance) AS total_attendance,
                (SELECT COUNT(*) FROM attendance WHERE date = date('now')) AS today_attendance,
                (SELECT COUNT(*) FROM users WHERE is_active = 1) AS active_users"""
        ).fetchone()
        counts = dict(counts_row)

        status_rows = connection.execute(
            "SELECT status, COUNT(*) AS count FROM attendance GROUP BY status"
        ).fetchall()
        status_map = {row["status"]: row["count"] for row in status_rows}
        present = status_map.get("Present", 0)
        late = status_map.get("Late", 0)
        absent = status_map.get("Absent", 0)
        total_att = present + late + absent
        overall_pct = round(((present + late) / max(total_att, 1)) * 100, 1) if total_att > 0 else 0.0

        breakdown = {
            "present": present,
            "late": late,
            "absent": absent,
            "total": total_att,
            "present_pct": round((present / max(total_att, 1)) * 100, 1),
            "late_pct": round((late / max(total_att, 1)) * 100, 1),
            "absent_pct": round((absent / max(total_att, 1)) * 100, 1),
            "overall_pct": overall_pct,
        }

        setting_row = connection.execute("SELECT value FROM settings WHERE key = 'min_attendance'").fetchone()
        threshold = float(setting_row["value"]) if setting_row else 75.0

        defaulter_rows = connection.execute(
            """SELECT s.roll_no, s.name, c.name AS course, s.semester, s.section,
                      COUNT(a.id) AS total,
                      SUM(CASE WHEN a.status IN ('Present', 'Late') THEN 1 ELSE 0 END) AS attended
               FROM students s
               JOIN courses c ON c.id = s.course_id
               LEFT JOIN attendance a ON a.student_id = s.id
               GROUP BY s.id
               HAVING (CAST(SUM(CASE WHEN a.status IN ('Present', 'Late') THEN 1 ELSE 0 END) AS FLOAT) / MAX(COUNT(a.id), 1)) * 100 < ?
               ORDER BY (CAST(SUM(CASE WHEN a.status IN ('Present', 'Late') THEN 1 ELSE 0 END) AS FLOAT) / MAX(COUNT(a.id), 1)) ASC""",
            (threshold,)
        ).fetchall()

        defaulters = []
        for r in defaulter_rows:
            tot = r["total"] or 0
            att = r["attended"] or 0
            pct = round((att / max(tot, 1)) * 100, 1)
            defaulters.append({
                "roll_no": r["roll_no"],
                "name": r["name"],
                "course": r["course"],
                "semester": r["semester"],
                "section": r["section"],
                "attended": att,
                "total": tot,
                "percentage": pct,
            })

        recent_log_rows = connection.execute(
            """SELECT al.id, al.attendance_id, al.old_status, al.new_status, al.reason, al.changed_at,
                      u.login_id AS changed_by_user
               FROM attendance_logs al
               LEFT JOIN users u ON u.id = al.changed_by
               ORDER BY al.changed_at DESC LIMIT 10"""
        ).fetchall()
        recent_logs = [dict(r) for r in recent_log_rows]

        leave_rows = connection.execute(
            """SELECT lr.id, lr.from_date, lr.to_date, lr.reason, lr.status,
                      s.roll_no, s.name AS student_name
               FROM leave_requests lr
               JOIN students s ON s.id = lr.student_id
               ORDER BY lr.id DESC LIMIT 10"""
        ).fetchall()
        recent_leaves = [dict(r) for r in leave_rows]

        import os
        from config import DATABASE_PATH
        db_size_kb = round(os.path.getsize(DATABASE_PATH) / 1024, 1) if DATABASE_PATH.exists() else 0

        return {
            "counts": counts,
            "breakdown": breakdown,
            "threshold": threshold,
            "defaulters": defaulters,
            "recent_logs": recent_logs,
            "recent_leaves": recent_leaves,
            "db_size_kb": db_size_kb,
            "sqlite_version": sqlite3.sqlite_version,
        }


def list_audit_logs(role: str, limit: int = 100):
    _require_admin(role)
    with get_connection() as connection:
        return connection.execute(
            """SELECT al.id, al.attendance_id, al.old_status, al.new_status, al.reason, al.changed_at,
                      u.login_id AS changed_by_user
               FROM attendance_logs al
               LEFT JOIN users u ON u.id = al.changed_by
               ORDER BY al.changed_at DESC LIMIT ?""",
            (limit,),
        ).fetchall()


def list_leave_requests(role: str):
    _require_admin(role)
    with get_connection() as connection:
        return connection.execute(
            """SELECT lr.id, lr.from_date, lr.to_date, lr.reason, lr.status,
                      s.roll_no, s.name AS student_name
               FROM leave_requests lr
               JOIN students s ON s.id = lr.student_id
               ORDER BY lr.id DESC"""
        ).fetchall()


def update_leave_status(role: str, request_id: int, new_status: str, admin_user_id: int) -> None:
    _require_admin(role)
    if new_status not in ("Approved", "Rejected"):
        raise AdminServiceError("Status must be Approved or Rejected.")
    with database_session() as connection:
        connection.execute(
            "UPDATE leave_requests SET status = ?, approved_by = ? WHERE id = ?",
            (new_status, admin_user_id, request_id),
        )


def list_backups_info(role: str) -> list[dict]:
    _require_admin(role)
    import datetime, os
    from config import BACKUP_DIR
    if not BACKUP_DIR.exists():
        return []
    backups = []
    for file in sorted(BACKUP_DIR.glob("*.db"), key=os.path.getmtime, reverse=True):
        stat = file.stat()
        backups.append({
            "name": file.name,
            "path": str(file),
            "size_kb": round(stat.st_size / 1024, 1),
            "modified": datetime.datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
        })
    return backups

