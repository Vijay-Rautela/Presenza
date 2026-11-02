# Presenza

Presenza is a Python desktop Attendance Management System for the BBAT104 Fundamentals of TQM course project. It replaces a paper attendance register with role-based attendance marking, audit trails, leave management, reports, and backups.

## Project details

| Item | Value |
|---|---|
| Course | BBAT104 Fundamentals of TQM, 2026-27 |
| Student roll number | 2414122 |
| Quality goal | Q20: Overall Software Quality |
| Interface | CustomTkinter desktop application |
| Data store | SQLite |

## Key features

- Admin, Teacher, and Student login with one-time account activation.
- PBKDF2 password hashing, role-based portals, and forced admin password change.
- Admin CRUD for students, teachers, courses, subjects, and teaching assignments.
- CSV/Excel bulk import, attendance settings, account reset, and database backup.
- Assignment-scoped attendance marking with duplicate, future-date, and proxy-prevention controls.
- Attendance corrections with mandatory reasons and an audit log.
- Student attendance dashboard, records, leave application, and status tracking.
- Role-scoped reports, defaulter list, CSV export, and Matplotlib subject charts.

## Quality-goal features: Q20

| Feature | Where to demonstrate it |
|---|---|
| Dashboard | Admin, Teacher, and Student home screens |
| Validation | Login, activation, attendance marking, corrections, and leave forms |
| Export reports | Admin or Teacher → Reports → Export CSV |
| Backups | Admin → Backup → Create database backup |
| Role controls | Sign in with each role and observe scoped menus/data |

Full quality-feature evidence is in [docs/QUALITY_FEATURES.md](docs/QUALITY_FEATURES.md).

## Architecture

```text
CustomTkinter UI
      ↓
Service layer: authentication, admin, attendance, student, reports
      ↓
Database helper (parameterized SQLite access)
      ↓
SQLite database + reports / backups / logs
```

The UI never writes SQL. Services hold the validation and permission rules, while `database/db.py` owns connections and transactions.

## Installation

1. Install Python 3.11 or newer from [python.org](https://www.python.org/downloads/). During setup, select **Add Python to PATH**.
2. Open PowerShell in the project folder.
3. Install dependencies:

```powershell
py -m pip install -r requirements.txt
```

4. Start Presenza:

```powershell
py main.py
```

On first run, the application creates `database/ams.db`, applies the schema, and adds safe starter data.

## First-run credentials

| Account | Login ID | Password | Notes |
|---|---|---|---|
| Admin | `admin` | `Admin@123` | Must be changed at first login. |
| Teacher | for example `EMP101` | None initially | Use Activate Account and the seeded DOB. |
| Student | for example `BCA25001` | None initially | Use Activate Account and the seeded DOB. |

Seeded teachers and students are intentionally inactive. The Admin can reset any teacher/student account, after which that user must activate it again.

## User guide

Detailed steps for each portal are in [docs/USER_MANUAL.md](docs/USER_MANUAL.md).

## Tests

Run the focused quality tests after installing Python:

```powershell
py -m unittest discover -s tests -v
```

The tests cover password hashing, password-strength validation, and date validation. Test results must be recorded from real runs only.

Latest verified run: **5 tests passed on 25 October 2026** using Python 3.13. Details are recorded in `docs/DEFECT_CHECKSHEET.csv`.

## Important folders

```text
database/       schema, database helper, seed data, CSV templates
services/       business rules and role checks
ui/             CustomTkinter screens by role
reports/        chart helpers and generated charts
utils/          security, validation, backup, and logging helpers
docs/           PRD, SRS, quality evidence, and user manual
tests/          focused automated tests
```

## Screenshots

Screenshots should be captured from a real local run after Python is installed, then saved to `docs/screenshots/` using these names:

- `login.png`
- `admin-dashboard.png`
- `teacher-mark-attendance.png`
- `student-dashboard.png`
- `reports.png`

No screenshots are included yet because this development computer does not have a runnable Python installation. They must not be fabricated.

## Project documentation

- [Product Requirements Document](docs/PRD.md)
- [Software Requirements Specification](docs/SRS.md)
- [Quality goals](docs/QUALITY_GOALS.md)
- [Quality feature evidence](docs/QUALITY_FEATURES.md)
- [TQM artefacts](docs/SIPOC.md)
- [Viva notes](viva.md)

## License

Academic course-project use only.
