-- Presenza database schema. SQLite foreign-key checks are enabled by db.py.

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    login_id TEXT NOT NULL UNIQUE,
    role TEXT NOT NULL CHECK (role IN ('Admin', 'Teacher', 'Student')),
    dob TEXT NOT NULL,
    password_hash TEXT,
    is_active INTEGER NOT NULL DEFAULT 0 CHECK (is_active IN (0, 1)),
    must_change_password INTEGER NOT NULL DEFAULT 0 CHECK (must_change_password IN (0, 1)),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    duration_years INTEGER NOT NULL CHECK (duration_years > 0)
);

CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL UNIQUE,
    roll_no TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    course_id INTEGER NOT NULL,
    semester INTEGER NOT NULL CHECK (semester >= 1),
    section TEXT NOT NULL,
    email TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS teachers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL UNIQUE,
    emp_id TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    department TEXT NOT NULL,
    email TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    course_id INTEGER NOT NULL,
    semester INTEGER NOT NULL CHECK (semester >= 1),
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS teaching_assignments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    teacher_id INTEGER NOT NULL,
    subject_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    semester INTEGER NOT NULL,
    section TEXT NOT NULL,
    UNIQUE (teacher_id, subject_id, course_id, semester, section),
    FOREIGN KEY (teacher_id) REFERENCES teachers(id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    subject_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('Present', 'Absent', 'Late', 'Leave')),
    marked_by INTEGER NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (student_id, subject_id, date),
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE RESTRICT,
    FOREIGN KEY (marked_by) REFERENCES users(id) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS attendance_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    attendance_id INTEGER NOT NULL,
    old_status TEXT NOT NULL,
    new_status TEXT NOT NULL,
    changed_by INTEGER NOT NULL,
    changed_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    reason TEXT NOT NULL,
    FOREIGN KEY (attendance_id) REFERENCES attendance(id) ON DELETE CASCADE,
    FOREIGN KEY (changed_by) REFERENCES users(id) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS leave_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    from_date TEXT NOT NULL,
    to_date TEXT NOT NULL,
    reason TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'Pending' CHECK (status IN ('Pending', 'Approved', 'Rejected')),
    approved_by INTEGER,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (approved_by) REFERENCES users(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_attendance_student_subject_date
    ON attendance (student_id, subject_id, date);
CREATE INDEX IF NOT EXISTS idx_attendance_subject_date
    ON attendance (subject_id, date);
