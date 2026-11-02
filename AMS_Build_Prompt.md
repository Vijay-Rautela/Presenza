# Master Prompt: Build the Attendance Management System (BBAT104 TQM Project)

## Role

You are a senior Python developer. Build a complete, working **Attendance Management System** desktop application for a college TQM course project. Work in phases, and wait for my confirmation after each phase before starting the next. Commit to Git after every phase with a meaningful message (the project needs at least 30 commits overall).

## Session Protocol (read this first, every time)

This project uses a memory file called `CODEX.md` in the project root.

1. At the start of every session, before doing anything else, read `CODEX.md` fully. It tells you what is done, what is pending, the decisions already made, and the rules of the project. Also read `docs/PRD.md` and `docs/SRS.md` once for the full requirements.
2. If `CODEX.md` does not exist, create it from the template given in the file I provided, then continue.
3. Treat `CODEX.md` as the source of truth for project state. If it conflicts with your assumptions, follow `CODEX.md` and tell me.
4. After finishing every phase, and after any meaningful change, update `CODEX.md`: tick off the phase in the status table, list files added or changed, record new decisions, known bugs, and what to do next, and add one line to the changelog with the date.
5. Never delete history from the changelog. Keep `CODEX.md` short, accurate, and current.
6. Before ending a session, make sure `CODEX.md` matches the real state of the code.

## Project Context

- Course: BBAT104 Fundamentals of TQM, Course Project 2026-27
- Core TQM goal: automate attendance tracking and minimize proxy entries
- Review 1 and Review 2 happen together, so the base system, CRUD, and architecture must be clean and demo-ready
- My assigned Quality Goal: Q__ (to be filled by me). Leave a clean place in the code for 5 quality-goal features, which I will specify later.

## Tech Stack (strict)

- Python 3.x
- CustomTkinter for the GUI
- SQLite3 for the database (use parameterized queries only)
- Pandas for CSV import and reports
- Matplotlib / Seaborn for charts
- hashlib (PBKDF2) or bcrypt for password hashing
- Do not use any web framework, React, or any other stack

## Cleanup Rule

Before and during the build, inspect the existing project folder. Remove every file, folder, table, function, and feature that is not required by this prompt. Keep only what this prompt needs. Tell me what you removed.

## Roles and Portals

One login screen, three role-based portals:

1. **Admin**: sets up everything
2. **Teacher**: marks and manages attendance for assigned classes
3. **Student**: views own attendance and applies for leave

## Account Activation Flow (important)

Teachers and students do not get ready-made passwords.

1. Admin imports teachers and students (single form or bulk CSV). Each record has a login ID and date of birth. For teachers the ID is the employee ID. For students it is the roll number.
2. The account is created as **inactive** with no password.
3. On the login screen there is an **Activate Account** option. The user enters ID and date of birth.
4. If both match an inactive account, the user is asked to create a password (minimum 8 characters, at least one letter and one number, with confirm field).
5. The password is stored only as a hash, the account becomes active, and the user logs in normally.
6. Wrong ID or DOB, or an already activated account, shows a clear friendly error.
7. Admin can reset a user's account to inactive so they can activate again.
8. Admin has a default seeded account (username `admin`) that must change its password on first login.

## Database Design

Create `database/schema.sql` and `database/db.py` with these tables:

- `users`: id, login_id (unique), role, dob, password_hash (nullable), is_active, created_at
- `courses`: id, name, duration_years
- `students`: id, user_id, roll_no (unique), name, course_id, semester, section, email
- `teachers`: id, user_id, emp_id (unique), name, department, email
- `subjects`: id, code, name, course_id, semester
- `teaching_assignments`: id, teacher_id, subject_id, course_id, semester, section (this decides which teacher marks which class)
- `attendance`: id, student_id, subject_id, date, status (Present/Absent/Late/Leave), marked_by, created_at, with `UNIQUE(student_id, subject_id, date)`
- `attendance_logs`: id, attendance_id, old_status, new_status, changed_by, changed_at, reason
- `leave_requests`: id, student_id, from_date, to_date, reason, status (Pending/Approved/Rejected), approved_by
- `settings`: key, value (for example `min_attendance = 75`, `edit_window_days = 2`)

Add indexes on attendance (student_id, subject_id, date).

## Seed Data (write it with a Python script)

Create `database/seed_data.py` that runs once and inserts all starting data, so I do not have to enter anything manually:

- 1 admin account (username `admin`, default password to be changed on first login)
- 1 course: BCA (3 years), with semesters 1 to 6 available
- 6 to 8 subjects for BCA Semester 5 (for example Python Programming, DBMS, Web Technologies, Computer Networks, Software Engineering, TQM)
- 5 teachers with employee IDs, DOB, department, **inactive** accounts
- 30 to 40 dummy students (roll numbers, names, DOB, Semester 5, Section A and B), **inactive** accounts
- `teaching_assignments` linking each teacher to subjects and sections
- Settings: minimum attendance 75
- Optional demo attendance for the last 3 to 4 weeks with realistic variation (some students below 75%) so that reports, charts, and defaulter lists show real data

Also generate two template files: `sample_students.csv` and `sample_teachers.csv`. The seed script must be safe to re-run (do not create duplicates).

## Bulk Import

Admin can upload a CSV or Excel file for students and teachers using Pandas. Validate required columns, skip and report duplicates, and show a summary (added, skipped, errors). Accounts are created inactive as per the activation flow.

## Features by Portal

**Admin**
- Dashboard with counts (students, teachers, subjects, today's attendance)
- CRUD for students, teachers, courses, subjects
- Bulk import (CSV/Excel)
- Teaching assignments: assign teacher to subject, course, semester, section
- Reset account activation
- Set minimum attendance percentage
- View all reports, defaulter list, audit logs
- One-click database backup

**Teacher**
- Sees only assigned subjects and classes
- Select subject, class, and date; the student list loads automatically from the assignment
- Mark Present, Absent, Late; include a "Mark all present" option
- Edit attendance within the allowed window, with a mandatory reason (log saved)
- Approve or reject student leave requests
- Class-wise and subject-wise reports, defaulter list for own classes

**Student**
- Dashboard with overall attendance percentage and warning if below minimum
- Subject-wise percentage and date-wise records
- Apply for leave and see its status
- Can see only own data

## Proxy Control and Error Prevention (Poka-Yoke)

- One record per student, subject, and date (database constraint plus a friendly message)
- A teacher can mark only subjects assigned to them
- Future dates are rejected
- Edits only within the allowed window and always with a reason
- Every edit is logged in `attendance_logs`
- Strict input validation and friendly error alerts everywhere
- Wrap database and file operations in exception handling so the app never crashes

## Reports and Charts

- Student-wise, subject-wise, and monthly attendance percentage
- Defaulter list (below the minimum percentage)
- CSV export
- Matplotlib charts (attendance by subject, monthly trend)

## Folder Structure

```
BBAT104_TQM_[RegNo]/
  main.py
  config.py
  database/      (db.py, schema.sql, seed_data.py, ams.db)
  models/
  services/      (auth_service.py, attendance_service.py, import_service.py, report_service.py)
  ui/            (login_view.py, activate_view.py, admin/, teacher/, student/)
  utils/         (validators.py, security.py, backup.py, logger.py)
  reports/       (charts.py, exports/)
  tests/
  docs/          (PRD.md, SRS.md, SIPOC, CTQ tree, FMEA, Pareto, Fishbone, checksheet, PDCA log)
  CODEX.md
  README.md
```

Keep UI, business logic, and database code separate. Add clear comments.

## Phases

1. Project cleanup, folder structure, `schema.sql`, `db.py`, `seed_data.py`, sample CSVs
2. Login, account activation, role-based routing, password hashing
3. Admin portal: CRUD, bulk import, teaching assignments, settings
4. Teacher portal: attendance marking, proxy control, edit with audit log, leave approval
5. Student portal: dashboard, records, leave application
6. Reports, charts, defaulter list, CSV export, backup
7. Quality-goal features (I will provide the 5 features), unit tests, error handling polish
8. README.md with setup steps, screenshots, user manual, and final cleanup
9. TQM documents for later reviews, saved in `docs/` and generated with Python where possible: SIPOC diagram, CTQ tree, FMEA matrix with RPN (Severity x Occurrence x Detection), defect checksheet and log, Pareto chart (Matplotlib), Fishbone diagram, and PDCA log

## How the System Works (manual)

1. **First run:** `python main.py` creates `ams.db`, runs the schema, and runs the seed data if the database is empty. Only the `admin` account is active; everyone else is inactive.
2. **Admin setup:** admin logs in, changes the default password, then reviews courses, subjects, teachers, students, and teaching assignments (loaded by seed or bulk import).
3. **Activation:** a teacher or student opens Activate Account, enters ID and date of birth, creates a password, and from then on logs in with ID and password.
4. **Daily attendance:** teacher logs in, picks one of their assigned subjects, class, and date; the student list loads from the assignment; teacher marks Present, Absent, or Late and submits. The service layer checks the teacher, the date, and duplicates before saving.
5. **Corrections:** teacher edits within the allowed window with a reason; the change is written to `attendance_logs`.
6. **Leave:** student applies; teacher or admin approves or rejects; approved leave shows as Leave.
7. **Reports:** Pandas reads the data, calculates percentages, Matplotlib draws charts, and the defaulter list shows students below the minimum. Reports export to CSV.
8. **Backup:** admin clicks backup and the database file is copied with a timestamp.

Layers: UI (CustomTkinter views) calls services; services hold all rules and talk to the database through `db.py`; the UI never writes SQL.

## Testing Checklist (run after each phase)

- App starts without errors on a fresh database and on an existing one
- Seed script can be re-run without duplicates
- Wrong ID or DOB, already activated account, and weak password show clear messages
- Duplicate attendance, future date, and non-assigned subject are blocked
- Edit without a reason is blocked and every edit appears in `attendance_logs`
- A student cannot see another student's data; a teacher cannot see another teacher's classes
- Reports, charts, CSV export, and backup work

## Working Rules

- At the end of each phase, give me a short summary, list the files changed, tell me how to run and test it, and then wait.
- Do not add features that are not in this prompt.
- Ask me only if something is truly blocking; otherwise make a sensible choice and tell me.
- Update `CODEX.md` at the end of every phase before you stop.
