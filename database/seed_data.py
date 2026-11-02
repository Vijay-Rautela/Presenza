"""Repeatable starter data for Presenza.

Run directly with `python database/seed_data.py`, or let main.py run it on start.
All inserts use INSERT OR IGNORE or existence checks, so no duplicates are made.
"""

from datetime import date, timedelta

from config import DEFAULT_EDIT_WINDOW_DAYS, DEFAULT_MIN_ATTENDANCE
from database.db import database_session
from utils.security import hash_password


TEACHERS = [
    ("EMP101", "Dr. Anjali Sharma", "Computer Applications", "anjali.sharma@presenza.edu", "1985-04-12"),
    ("EMP102", "Mr. Rohan Verma", "Computer Applications", "rohan.verma@presenza.edu", "1988-09-21"),
    ("EMP103", "Ms. Kavita Joshi", "Computer Applications", "kavita.joshi@presenza.edu", "1987-01-15"),
    ("EMP104", "Mr. Deepak Rawat", "Computer Applications", "deepak.rawat@presenza.edu", "1984-06-30"),
    ("EMP105", "Ms. Neha Kapoor", "Computer Applications", "neha.kapoor@presenza.edu", "1989-11-08"),
]

SUBJECTS = [
    ("BCA501", "Python Programming"),
    ("BCA502", "Database Management Systems"),
    ("BCA503", "Web Technologies"),
    ("BCA504", "Computer Networks"),
    ("BCA505", "Software Engineering"),
    ("BCA506", "Total Quality Management"),
]


def _student_rows() -> list[tuple[str, str, str, str, str]]:
    """Generate 36 readable dummy student records, split across Sections A and B."""
    first_names = ["Aarav", "Aditi", "Arjun", "Bhavya", "Dev", "Diya", "Ishaan", "Kavya", "Manav", "Meera", "Nikhil", "Pooja", "Riya", "Saksham", "Tanvi", "Varun", "Yash", "Zoya"]
    rows = []
    for number in range(1, 37):
        section = "A" if number <= 18 else "B"
        name = f"{first_names[(number - 1) % len(first_names)]} Student {number:02d}"
        roll_no = f"BCA25{number:03d}"
        dob = f"200{(number % 3) + 3}-{(number % 12) + 1:02d}-{(number % 27) + 1:02d}"
        email = f"{roll_no.lower()}@student.presenza.edu"
        rows.append((roll_no, name, dob, section, email))
    return rows


def _id_for(connection, table: str, field: str, value: str) -> int:
    row = connection.execute(f"SELECT id FROM {table} WHERE {field} = ?", (value,)).fetchone()
    if row is None:
        raise RuntimeError(f"Missing seeded {table} record for {value}.")
    return row["id"]


def _seed_demo_attendance(connection, course_id: int) -> None:
    """Add deterministic recent data for later report and defaulter demonstrations."""
    teacher_user_id = connection.execute(
        "SELECT user_id FROM teachers WHERE emp_id = ?", ("EMP101",)
    ).fetchone()["user_id"]
    students = connection.execute(
        "SELECT id FROM students WHERE course_id = ? ORDER BY id", (course_id,)
    ).fetchall()
    subject_id = _id_for(connection, "subjects", "code", "BCA501")
    weekday_dates = []
    current_day = date.today() - timedelta(days=1)
    while len(weekday_dates) < 15:
        if current_day.weekday() < 5:
            weekday_dates.append(current_day.isoformat())
        current_day -= timedelta(days=1)

    for class_date in weekday_dates:
        for position, student in enumerate(students, start=1):
            status = "Absent" if position % 11 == 0 else "Late" if position % 7 == 0 else "Present"
            connection.execute(
                """INSERT OR IGNORE INTO attendance
                   (student_id, subject_id, date, status, marked_by)
                   VALUES (?, ?, ?, ?, ?)""",
                (student["id"], subject_id, class_date, status, teacher_user_id),
            )


def seed_database() -> None:
    """Insert starter data without changing existing data."""
    with database_session() as connection:
        # The default password is intentionally simple for first-run demonstration.
        # Phase 2 will require this account to set a new one at its first login.
        connection.execute(
            """INSERT OR IGNORE INTO users
               (login_id, role, dob, password_hash, is_active, must_change_password)
               VALUES (?, 'Admin', ?, ?, 1, 1)""",
            ("admin", "2000-01-01", hash_password("Admin@123")),
        )
        connection.execute("INSERT OR IGNORE INTO courses (name, duration_years) VALUES (?, ?)", ("BCA", 3))
        course_id = _id_for(connection, "courses", "name", "BCA")

        for code, name in SUBJECTS:
            connection.execute(
                """INSERT OR IGNORE INTO subjects (code, name, course_id, semester)
                   VALUES (?, ?, ?, ?)""",
                (code, name, course_id, 5),
            )

        for emp_id, name, department, email, dob in TEACHERS:
            connection.execute(
                """INSERT OR IGNORE INTO users (login_id, role, dob, is_active)
                   VALUES (?, 'Teacher', ?, 0)""",
                (emp_id, dob),
            )
            user_id = _id_for(connection, "users", "login_id", emp_id)
            connection.execute(
                """INSERT OR IGNORE INTO teachers (user_id, emp_id, name, department, email)
                   VALUES (?, ?, ?, ?, ?)""",
                (user_id, emp_id, name, department, email),
            )

        for roll_no, name, dob, section, email in _student_rows():
            connection.execute(
                """INSERT OR IGNORE INTO users (login_id, role, dob, is_active)
                   VALUES (?, 'Student', ?, 0)""",
                (roll_no, dob),
            )
            user_id = _id_for(connection, "users", "login_id", roll_no)
            connection.execute(
                """INSERT OR IGNORE INTO students
                   (user_id, roll_no, name, course_id, semester, section, email)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (user_id, roll_no, name, course_id, 5, section, email),
            )

        # Teacher EMP101 teaches two subjects. The other four each teach one.
        assignment_plan = [
            ("EMP101", "BCA501"), ("EMP101", "BCA502"), ("EMP102", "BCA503"),
            ("EMP103", "BCA504"), ("EMP104", "BCA505"), ("EMP105", "BCA506"),
        ]
        for emp_id, subject_code in assignment_plan:
            teacher_id = _id_for(connection, "teachers", "emp_id", emp_id)
            subject_id = _id_for(connection, "subjects", "code", subject_code)
            for section in ("A", "B"):
                connection.execute(
                    """INSERT OR IGNORE INTO teaching_assignments
                       (teacher_id, subject_id, course_id, semester, section)
                       VALUES (?, ?, ?, ?, ?)""",
                    (teacher_id, subject_id, course_id, 5, section),
                )

        connection.execute("INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)", ("min_attendance", DEFAULT_MIN_ATTENDANCE))
        connection.execute("INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)", ("edit_window_days", DEFAULT_EDIT_WINDOW_DAYS))
        _seed_demo_attendance(connection, course_id)


if __name__ == "__main__":
    seed_database()
    print("Presenza starter data is ready.")
