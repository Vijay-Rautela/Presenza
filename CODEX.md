# CODEX.md - Project Memory: Attendance Management System

This file is the single source of truth for project state. Read it fully at the start of every session. Update it at the end of every phase and after any meaningful change. Never delete changelog history.

## 1. Project Summary

- Project: Attendance Management System (AMS)
- Course: BBAT104 Fundamentals of TQM, Course Project 2026-27
- Baseline system: Attendance Management System (roll number ending in 0)
- Core TQM goal: automate attendance tracking and minimize proxy entries
- Assigned Quality Goal: Q20 - Overall Software Quality. Five features: Dashboard, Validation, Export Reports, Backups, Role Controls.
- Repo name: BBAT104_TQM_[RegNo] (public GitHub repo, at least 30 meaningful commits)
- Reviews: Review 1 and Review 2 are held together (2:00 PM to 3:00 PM, 2 minutes to present). Attendance Management is scheduled on 26-Oct-2026.

## 2. Tech Stack (strict)

Python 3.x, CustomTkinter, SQLite3 (parameterized queries only), Pandas, Matplotlib/Seaborn, hashlib PBKDF2 or bcrypt. No web framework, no React, no Node.

## 3. Key Decisions

- Desktop app, not web (course guidelines require Python and Tkinter/CustomTkinter).
- Three roles: Admin, Teacher, Student, one login screen, role-based portals.
- Login IDs: employee ID for teachers, roll number for students, `admin` for admin.
- Account activation: teachers and students are created inactive with no password. They activate once with ID and date of birth, then set a password (minimum 8 characters, letter and number). DOB is never used as the password afterwards.
- Admin is seeded with a default account and must change the password on first login.
- One teacher can have many subjects and one subject can have many teachers, through `teaching_assignments` (teacher, subject, course, semester, section).
- Starting data comes from `database/seed_data.py`; later data from forms or CSV/Excel bulk import.
- Proxy control: unique (student, subject, date), only the assigned teacher can mark, no future dates, edits only within a window and with a reason, every edit logged.
- Minimum attendance default is 75 percent, stored in `settings`.

## 4. Database Tables

users, courses, students, teachers, subjects, teaching_assignments, attendance (UNIQUE student_id, subject_id, date), attendance_logs, leave_requests, settings. Full field list is in `database/schema.sql` and `docs/SRS.md`.

## 5. Folder Map

```
main.py, config.py
database/   db.py, schema.sql, seed_data.py, ams.db
models/
services/   auth_service.py, attendance_service.py, import_service.py, report_service.py
ui/         login_view.py, activate_view.py, admin/, teacher/, student/
utils/      validators.py, security.py, backup.py, logger.py
reports/    charts.py, exports/
tests/
docs/       PRD.md, SRS.md, SIPOC, CTQ tree, FMEA, Pareto, Fishbone, checksheet, PDCA log
CODEX.md, README.md
```

## 6. Phase Status

| Phase | Description | Status |
|---|---|---|
| 1 | Cleanup, folder structure, schema, db.py, seed_data.py, sample CSVs | Done |
| 2 | Login, activation, role routing, password hashing | Done |
| 3 | Admin portal: CRUD, bulk import, assignments, settings | Done |
| 4 | Teacher portal: marking, proxy control, edit with audit log, leave approval | Done |
| 5 | Student portal: dashboard, records, leave application | Done |
| 6 | Reports, charts, defaulters, CSV export, backup | Done |
| 7 | Quality-goal features, unit tests, error handling polish | Done |
| 8 | README, screenshots, user manual, final cleanup | Done |
| 9 | TQM documents: SIPOC, CTQ tree, FMEA, Pareto, Fishbone, checksheet, PDCA | Done |

Status values: Not started, In progress, Done, Blocked.

## 7. Conventions

- UI never writes SQL; services hold rules; `db.py` handles connections.
- Clear comments in code, friendly error messages, no unhandled exceptions.
- Commit after every phase with a meaningful message.
- Do not add features that are not in the prompt, PRD, or SRS.

## 8. How to Run

```
py -m pip install customtkinter pandas matplotlib seaborn
py main.py
```

(Update this section if dependencies or commands change.)

## 9. Known Issues

- The Teacher attendance syntax error reported on 2026-10-25 was repaired. Full Python syntax compilation and five focused unit tests now pass with Python 3.13.
- Live GUI workflow testing, screenshots, and real attendance/backup test evidence are still pending.

## 10. Open Items

- Confirm registration number for the repo name.

## 11. Next Steps

All planned build phases are complete. Next practical steps are installing Python, running the application/tests, collecting real checksheet evidence, generating the Pareto chart, and capturing screenshots.

## 11A. Phase 1 Files Added or Changed

- Added `config.py` with the supplied Presenza colour palette and shared database settings.
- Added `database/schema.sql`, `database/db.py`, `database/seed_data.py`, and database package setup.
- Added `database/sample_students.csv` and `database/sample_teachers.csv` for the later bulk-import feature.
- Added `utils/security.py` with salted PBKDF2 password hashing helpers.
- Added `main.py` as the Phase 1 database bootstrap entry point.
- Added `viva.md` with a plain-language Phase 1 explanation and viva answers.
- Organised project documents as `docs/PRD.md`, `docs/SRS.md`, `docs/QUALITY_GOALS.md`, and `docs/SIR_REQUIREMENTS.md`; renamed the design checklist to `NOT_VIBE_CODED.md`.
- Created the planned `models`, `services`, `ui`, `reports`, `tests`, and supporting folder structure for later phases.

## 11B. Phase 1 Decisions

- Presenza uses the required CustomTkinter-ready Python desktop architecture; no web or React files were retained because they conflict with the master prompt.
- Added `must_change_password` to `users` to implement the required first-login admin password change in Phase 2.
- Seed data includes BCA Semester 5, six subjects, five inactive teachers, 36 inactive students, teaching assignments, settings, and deterministic recent demo attendance.
- The supplied green, caramel, beige, and off-white palette is stored centrally in `config.py` for all future UI work.

## 11C. Phase 2 Files Added or Changed

- Added `services/auth_service.py` for all login, activation, password-change, and role-routing rules.
- Added `utils/validators.py` for password and date-of-birth validation.
- Added `ui/app.py`, `ui/login_view.py`, `ui/activate_view.py`, and `ui/dashboard_view.py` for the CustomTkinter sign-in experience and role shells.
- Updated `main.py` to initialise the database before opening the CustomTkinter application.
- Added `pahs.md`, the brief self-contained handoff prompt for the next phase.
- Updated `viva.md` and this project memory file with Phase 2 details.

## 11D. Phase 2 Decisions

- Authentication rules are kept in `auth_service.py`; UI screens never query or modify SQLite directly.
- Account activation is restricted to inactive Teacher and Student accounts, using exact login ID plus `YYYY-MM-DD` date of birth verification.
- Passwords must have at least eight characters, one letter, and one number. They are always stored as PBKDF2 hashes.
- A first-time Admin login is routed to a mandatory password-change screen before the Admin portal shell.
- Each role currently reaches only its own portal shell; full role-specific functions are intentionally delivered in Phases 3 to 5.

## 11E. Phase 3 Files Added or Changed

- Added `services/admin_service.py` for protected Admin CRUD, dashboard statistics, teaching assignments, account resets, and attendance settings.
- Added `services/import_service.py` for Pandas CSV/Excel imports with required-column checks, duplicate skipping, and row-level errors.
- Added `ui/admin/portal.py`, a CustomTkinter Admin workspace with dashboard, master-data screens, assignments, imports, and settings.
- Updated `ui/app.py` so a verified Admin reaches the Admin workspace instead of the temporary role shell.
- Replaced the single handoff prompt in `pahs.md` with prompts for every remaining phase.
- Updated `viva.md` and this project memory file with Phase 3 notes.

## 11F. Phase 3 Decisions

- Every Admin database mutation accepts the user's role and rejects non-Admin access in the service layer.
- Creating a teacher or student also creates an inactive user account; it can only become active through the existing activation flow.
- Deleting a student or teacher deletes its linked user through the defined foreign-key relationship.
- Imports accept `.csv`, `.xlsx`, and `.xls` and report added, skipped, and the first five row errors.
- The Admin interface uses readable tables and simple record forms. Course IDs are intentionally shown in the Courses table and used when creating or editing related subjects and students.

## 11G. Phase 4 Files Added or Changed

- Added `services/attendance_service.py` for assigned-class checks, marking, duplicate prevention, correction audit logs, and leave decisions.
- Added `ui/teacher/portal.py`, a CustomTkinter Teacher workspace for marking, corrections, and leave requests.
- Updated `ui/app.py` to route Teachers to their dedicated workspace.
- Removed the completed Phase 4 handoff prompt from `pahs.md`.
- Updated `viva.md` and this project memory file with Phase 4 notes.

## 11H. Phase 4 Decisions

- A Teacher can retrieve and mark only assignments that belong to their authenticated account.
- Attendance submission must contain exactly the students in the selected class. Future dates and any existing class/subject/date records are rejected before insertion.
- Corrections require a changed status and non-empty reason, honour `edit_window_days`, and write old value, new value, user, timestamp, and reason to `attendance_logs`.
- A Teacher can see and decide only pending leave requests from their assigned class. Approval changes the Teacher's existing records in the approved range to `Leave`.

## 11I. Phase 5 Files Added or Changed

- Added `services/student_service.py` for private attendance summaries, records, and leave-request rules.
- Added `ui/student/portal.py`, a CustomTkinter Student workspace with dashboard, records, and leave application screens.
- Updated `ui/app.py` to route Students to their dedicated workspace.
- Removed the completed Phase 5 handoff prompt from `pahs.md`.
- Updated `viva.md` and this project memory file with Phase 5 notes.

## 11J. Phase 5 Decisions

- Every Student query begins by resolving the signed-in user's linked student ID, so no service accepts an arbitrary student ID from the UI.
- Overall and subject attendance percentages count `Present` and `Late` as attended classes.
- Student leave forms reject invalid date order, leave ending in the past, unclear reasons, and overlapping pending requests.
- The dashboard displays a visible warning when the student's overall percentage is below the Admin-configured minimum.

## 11K. Phase 6 Files Added or Changed

- Added `services/report_service.py` for role-scoped student, subject, monthly, and defaulter reports plus Pandas CSV export.
- Added `reports/charts.py` for real Matplotlib subject-attendance charts.
- Added `utils/backup.py` for Admin-only timestamped SQLite backups.
- Added `ui/report_window.py` and linked reports to both Admin and Teacher workspaces.
- Added the Admin backup screen in `ui/admin/portal.py`.
- Removed the completed Phase 6 handoff prompt from `pahs.md`.
- Updated `viva.md` and this project memory file with Phase 6 notes.

## 11L. Phase 6 Decisions

- Admin reports include all attendance data; Teacher reports use the same assignment checks as marking and include only their permitted classes.
- Defaulters are calculated from the live `min_attendance` setting, not a hard-coded number.
- CSV export receives only the already role-scoped report rows.
- Charts are generated from actual database report values and saved under `reports/generated/` when requested.
- Database backup is available only to Admin and copies the SQLite file into a timestamped `backups/` file.

## 11M. Phase 7 Files Added or Changed

- Confirmed Q20 - Overall Software Quality and recorded the selected five features in `docs/QUALITY_GOALS.md`.
- Updated SRS-F25 through SRS-F29 in `docs/SRS.md`.
- Added `docs/QUALITY_FEATURES.md` as the review/viva evidence map for each quality feature.
- Added `utils/logger.py` and application-level unexpected-error logging in `main.py`.
- Added focused unit tests in `tests/test_quality_basics.py`.
- Removed the completed Phase 7 handoff prompt from `pahs.md`.
- Updated `viva.md` and this project memory file with Phase 7 notes.

## 11N. Phase 7 Decisions

- Q20 was selected with the user's permission because it gives the strongest balanced quality story for an Attendance Management System.
- The five Q20 features are visible and already integrated across completed phases: dashboards, validations, CSV export, Admin backups, and role controls.
- Tests are deliberately documented as pending execution because Python 3 is not installed on the current development machine; no unverified test result is recorded as a pass.

## 11O. Phase 8 Files Added or Changed

- Added `README.md` with setup, architecture, first-run credentials, features, tests, documentation links, and an honest screenshot-capture checklist.
- Added `docs/USER_MANUAL.md` with Admin, Teacher, Student, validation, and recovery instructions.
- Added `requirements.txt` for CustomTkinter, Pandas, Matplotlib, and Seaborn.
- Added `.gitignore` to exclude local databases, backups, logs, generated charts, screenshots, virtual environments, and Python cache files.
- Removed the completed Phase 8 handoff prompt from `pahs.md`.
- Updated `viva.md` and this project memory file with Phase 8 notes.

## 11P. Phase 8 Decisions

- Screenshots are intentionally not added until the application can be run on a computer with Python installed; the README names the required real screenshots and target folder.
- The README uses `requirements.txt` as the single dependency-installation command.
- Local operational files are excluded from Git so commits contain code and documentation rather than personal database data or generated outputs.

## 11Q. Phase 9 Files Added or Changed

- Added `docs/SIPOC.md`, `docs/CTQ_TREE.md`, and `docs/ARCHITECTURE_FLOWCHART.md`.
- Added `docs/FMEA.md` with calculated pre-release RPN values and mitigation actions.
- Added `docs/DEFECT_CHECKSHEET.csv`, `docs/DEFECT_LOG.md`, `docs/FISHBONE.md`, and `docs/PDCA_LOG.md`.
- Added `reports/generate_pareto.py`, which generates a Pareto chart only from logged, real failed tests.
- Updated `README.md` with the TQM documentation link.
- Removed the completed Phase 9 handoff prompt from `pahs.md`.
- Updated `viva.md` and this project memory file with Phase 9 notes.

## 11R. Phase 9 Decisions

- FMEA numbers are documented as pre-release risk-assessment ratings, not historical defect measurements.
- The defect log and checksheet remain explicitly empty until real local test results exist.
- The Pareto script stops without output if there are no real failed-test categories, preventing invented SQC evidence.
- PDCA cycles are marked Pending real test until Plan, Do, Check, and Act evidence is actually recorded.

## 11S. Post-Phase Verification and Repair

- Repaired a missing closing quote in `services/attendance_service.py` that prevented the Teacher portal from importing.
- Replaced the leave-status update query with a less error-prone concatenated SQL string.
- Verified the entire project with Python 3.13 compilation.
- Ran `python -m unittest discover -s tests -v`: 3 tests passed (password hashing, password validation, date validation).
- Recorded the verified test outcomes in `docs/DEFECT_CHECKSHEET.csv` and completed the related validation PDCA cycle.

## 11T. Admin and UI Reliability Patch

- Rebuilt `ui/admin/portal.py` to fix the backup AttributeError, provide dashboard cards, persistent feedback banners, double-click record editing, course dropdown mappings, and human-readable assignment dropdowns.
- Added red Absent and orange Late status selectors in the Teacher attendance/correction views.
- Added Teacher-deletion integrity handling with a friendly message.
- Added spreadsheet DOB/semester normalisation and CSV formula-injection protection.
- Expanded tests for import normalisation and CSV export protection; all five focused tests pass with Python 3.13.

## 12. Changelog

| Date | Change |
|---|---|
| 2026-10-24 | CODEX.md created. PRD, SRS, and build prompt prepared. No code written yet. |
| 2026-10-25 | Phase 1 completed: project structure, SQLite schema, database bootstrap, repeatable seed data, CSV templates, colour configuration, and viva notes added. |
| 2026-10-25 | Phase 2 completed: CustomTkinter login, account activation, PBKDF2 authentication, forced admin password replacement, role routing, and next-phase handoff prompt added. |
| 2026-10-25 | Phase 3 completed: Admin dashboard, CRUD services and screens, CSV/Excel imports, assignments, account reset, and attendance settings added. |
| 2026-10-25 | Phase 4 completed: Teacher attendance marking, Poka-Yoke checks, correction audit logs, and class-scoped leave decisions added. |
| 2026-10-25 | Phase 5 completed: Student dashboard, private attendance records, warning threshold, and leave application/status tracking added. |
| 2026-10-25 | Phase 6 completed: role-scoped reports, defaulters, CSV export, Matplotlib charts, and Admin database backup added. |
| 2026-10-25 | Phase 7 completed: Q20 quality-goal mapping, feature evidence, validation/security tests, and centralized error logging added. |
| 2026-10-25 | Phase 8 completed: README, user manual, dependency list, Git ignore rules, and screenshot-capture checklist added. |
| 2026-10-25 | Phase 9 completed: SIPOC, CTQ, FMEA, architecture flowchart, fishbone, evidence-based defect tools, PDCA log, and Pareto generator added. |
| 2026-10-25 | Repaired Teacher portal syntax error; project syntax compilation passed and 3 focused Python 3.13 unit tests passed. |
| 2026-10-25 | Rebuilt Admin portal and attendance status styling; fixed backup, foreign-key editing, assignment mapping, import/export hardening, and verified 5 focused tests. |
