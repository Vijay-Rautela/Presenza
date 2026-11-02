# Software Requirements Specification: Attendance Management System

Course: BBAT104 Fundamentals of TQM, Course Project 2026-27
Institute: Amrapali Institute of Technology & Sciences, Haldwani
Version: 1.0

## 1. Introduction

### 1.1 Purpose
This document specifies the requirements of the Attendance Management System (AMS) for the project guide, reviewers, and the developer.

### 1.2 Scope
AMS is a Python desktop application to mark, store, correct, and report student attendance with role-based access for Admin, Teacher, and Student. It automates tracking and minimizes proxy entries.

### 1.3 Definitions

| Term | Meaning |
|---|---|
| AMS | Attendance Management System |
| SRS | Software Requirements Specification |
| CRUD | Create, Read, Update, Delete |
| CTQ | Critical to Quality |
| Proxy entry | Attendance marked for an absent student or by an unauthorized person |
| Poka-Yoke | Error prevention built into the design |

### 1.4 References
- BBAT104 Course Project Guidelines, Session 2026-27
- IEEE Std 830-1998
- Besterfield et al., Total Quality Management, Pearson

## 2. Overall Description

### 2.1 Product Perspective
A standalone desktop application: CustomTkinter UI, Python service layer, SQLite3 database, Pandas and Matplotlib for reports.

### 2.2 Product Functions
Login, master data management, subject assignment, attendance marking, proxy control, correction with audit log, leave management, reports and charts, defaulter list, backup.

### 2.3 User Classes

| User | Description |
|---|---|
| Admin | Configures the system and views all data |
| Teacher | Marks and reviews attendance for assigned subjects |
| Student | Views own attendance and applies for leave |

### 2.4 Operating Environment
- OS: Windows 10 or above
- Python 3.x with Tkinter/CustomTkinter, SQLite3, Pandas, Matplotlib, Seaborn
- No internet required

### 2.5 Constraints
- Role-based access on all screens.
- Passwords stored as hashes only.
- Only one attendance record per student, subject, and date.
- Developed in VS Code and version controlled on GitHub (at least 30 commits).

### 2.6 Assumptions
- Starting data is loaded by a seed script; later data is added by the Admin through forms or bulk import.
- Minimum attendance is 75% unless the Admin changes it.

## 3. Specific Requirements

### 3.1 Functional Requirements

**Authentication**
- SRS-F1: The system shall authenticate users by login ID and password (employee ID for teachers, roll number for students, username for admin).
- SRS-F2: Teachers and students shall activate their account once by entering ID and date of birth, then setting a password (minimum 8 characters with at least one letter and one number). Passwords are stored only as hashes.
- SRS-F3: The system shall show only the screens permitted for the user role. The seeded admin account must change its password on first login.

**Master Data (Admin)**
- SRS-F4: Admin shall create, view, update, and delete students.
- SRS-F5: Admin shall create, view, update, and delete teachers.
- SRS-F6: Admin shall manage courses and subjects.
- SRS-F7: Admin shall assign one or more subjects to a teacher, and one or more teachers to a subject, per section.

**Attendance Marking (Teacher)**
- SRS-F8: Teacher shall select class, subject, and date to load the student list.
- SRS-F9: Teacher shall mark each student as Present, Absent, or Late.
- SRS-F10: The system shall provide a "mark all present" option.
- SRS-F11: The system shall reject duplicate attendance for the same student, subject, and date.
- SRS-F12: The system shall allow marking only for subjects assigned to the logged-in teacher.
- SRS-F13: The system shall reject marking for future dates.

**Correction and Audit**
- SRS-F14: Teacher shall edit a record only with a mandatory reason.
- SRS-F15: The system shall log user, time, old value, new value, and reason for each edit.

**Leave Management**
- SRS-F16: Student shall submit a leave request with dates and reason.
- SRS-F17: Teacher or Admin shall approve or reject the request.

**Reports**
- SRS-F18: The system shall calculate attendance percentage per student per subject.
- SRS-F19: The system shall generate student-wise, subject-wise, and monthly reports.
- SRS-F20: The system shall export reports to CSV.
- SRS-F21: The system shall list students below the minimum percentage.
- SRS-F22: The system shall show attendance charts using Matplotlib.
- SRS-F23: Students shall view only their own attendance.

**Backup**
- SRS-F24: Admin shall be able to back up the database with one click.

**Account Reset and Bulk Import**
- SRS-F30: Admin shall reset a user's account to inactive so the user can activate it again.
- SRS-F31: Admin shall import students and teachers from CSV or Excel; the system shall validate columns, skip duplicates, and show a summary (added, skipped, errors). Imported accounts are created inactive.

**Assigned Quality Goal Features**
- Assigned goal: Q20 - Overall Software Quality (selected for roll number 2414122's Presenza project).
- SRS-F25: The system shall provide role-relevant dashboard overviews for Admin, Teacher, and Student users.
- SRS-F26: The system shall validate passwords, dates, duplicate attendance, assignment access, correction reasons, and leave requests with friendly messages.
- SRS-F27: Admin and Teacher users shall export their role-scoped attendance reports to CSV.
- SRS-F28: Admin shall create timestamped database backups.
- SRS-F29: The system shall restrict portal navigation and service data access by user role.

### 3.2 External Interface Requirements

- User interface: desktop windows with consistent navigation, dropdowns, date pickers, and clear validation messages.
- Software interface: Python sqlite3 module for the database, Pandas for data handling, Matplotlib for charts.
- Hardware interface: standard computer with keyboard and mouse.

### 3.3 Non-Functional Requirements

| ID | Category | Requirement |
|---|---|---|
| NFR1 | Performance | Screens open within 2 seconds; reports within 5 seconds |
| NFR2 | Security | Hashed passwords, role checks, parameterized SQL queries |
| NFR3 | Reliability | Backup option; safe handling of database and file errors |
| NFR4 | Usability | A new teacher can mark attendance within 3 tries |
| NFR5 | Maintainability | Modular folder structure, comments in code |
| NFR6 | Scalability | Handles at least 1000 students and 50 teachers |
| NFR7 | Auditability | All attendance changes are traceable |

### 3.4 Data Requirements

| Table | Key fields |
|---|---|
| users | id, login_id, role, dob, password_hash (empty until activation), is_active |
| students | id, user_id, roll_no, name, course_id, semester, section, email |
| teachers | id, user_id, emp_id, name, department, email |
| courses | id, name, duration |
| subjects | id, code, name, course_id, semester |
| teaching_assignments | id, teacher_id, subject_id, course_id, semester, section |
| attendance | id, student_id, subject_id, date, status (Present/Absent/Late/Leave), marked_by |
| leave_requests | id, student_id, from_date, to_date, reason, status, approved_by |
| attendance_logs | id, attendance_id, old_status, new_status, changed_by, changed_at, reason |
| settings | key, value (for example min_attendance = 75) |

Constraint: UNIQUE (student_id, subject_id, date) on attendance.

### 3.5 Use Cases

| ID | Use case | Actor | Main flow |
|---|---|---|---|
| UC1 | Login | All | Enter credentials, verify, open role dashboard |
| UC2 | Manage master data | Admin | Open module, add or edit or delete, save |
| UC3 | Mark attendance | Teacher | Select class, subject, date, mark students, submit |
| UC4 | Correct attendance | Teacher | Open record, change status, enter reason, save, log created |
| UC5 | Apply for leave | Student | Fill form, submit |
| UC6 | Approve leave | Teacher/Admin | Open request, approve or reject |
| UC7 | View report | All (scoped) | Choose filters, view, export |
| UC8 | Backup | Admin | Click backup, file saved |

## 4. Quality Traceability (TQM)

| CTQ / Quality objective | Related requirements |
|---|---|
| Accuracy | SRS-F11, SRS-F13, SRS-F15 |
| Proxy prevention | SRS-F11, SRS-F12, SRS-F13, SRS-F15 |
| Speed | SRS-F10, NFR1 |
| Report time | SRS-F18, SRS-F19, NFR1 |
| Reliability | SRS-F24, NFR3 |
| Traceability | SRS-F15, NFR7 |

## 5. Acceptance Criteria

- All CRUD operations work for master data.
- Attendance can be marked; duplicates and unauthorized marking are blocked.
- Edits are logged with reason.
- Percentage and defaulter list match sample data.
- Reports export to CSV and charts display.
- Five quality-goal features work as demonstrated.
