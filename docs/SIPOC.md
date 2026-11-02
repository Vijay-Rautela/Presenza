# SIPOC Process Map: Presenza Attendance Management

## Process scope

The SIPOC map covers daily attendance, from prepared master data to reliable attendance information and reports.

| Suppliers | Inputs | Process | Outputs | Customers |
|---|---|---|---|---|
| Admin | Student, teacher, course, subject, and assignment data | 1. Admin creates/imports master data | Valid accounts and class assignments | Admin, Teachers |
| Teacher | Assigned class, subject, date, attendance statuses | 2. Teacher selects assigned class and loads students | One attendance record per student, subject, and date | Students, Admin |
| Student | Login credentials and leave details | 3. System validates date, assignment, duplicate, and access rules | Friendly validation result or safe saved record | Teacher, Student |
| Presenza database | Stored attendance, settings, audit history | 4. Teacher corrects a valid record with reason or decides a leave request | Audit log and approved/rejected leave state | Admin, Teacher |
| Admin / Teacher | Scoped report request | 5. System calculates percentages, defaulters, exports, and backup | Role-scoped report, CSV, chart, or backup | Admin, Teacher, Student |

## TQM interpretation

- **Customer focus:** Teachers receive a quick class register; students see their own status; Admin receives oversight.
- **Poka-Yoke:** Assignment, duplicate, future-date, and required-reason checks prevent common process mistakes.
- **Fact-based decisions:** Reports and defaulter lists are calculated from stored attendance records.
