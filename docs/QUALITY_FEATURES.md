# Q20 Quality-Goal Feature Evidence: Presenza

Selected goal: **Q20 - Overall Software Quality**  
Student roll number: **2414122**  
Selected features: Dashboard, Validation, Export Reports, Backups, Role Controls.

| SRS ID | Feature | Demonstrable implementation | TQM principle | Evidence to show in review |
|---|---|---|---|---|
| SRS-F25 | Dashboard | Admin, Teacher, and Student dashboards show role-relevant counts, assignments, and attendance. | Customer Focus | Sign in with each role and show its workspace. |
| SRS-F26 | Validation | Date, password, duplicate attendance, assignment, future-date, correction-reason, and leave validations give friendly messages. | Poka-Yoke | Attempt an invalid input or duplicate attendance. |
| SRS-F27 | Export Reports | Admin and Teacher report window exports role-scoped report rows as CSV using Pandas. | Fact-Based Decision Making | Load a report, then export it. |
| SRS-F28 | Backups | Admin can create a timestamped copy of `ams.db` in `backups/`. | Reliability | Click Create database backup and show the generated file. |
| SRS-F29 | Role Controls | Login routes roles to separate portals and services apply Admin/Teacher/Student data scopes. | Process-Centric Approach | Log in as different roles and compare visible data. |

## Test record

Automated tests are in `tests/test_quality_basics.py`. They cover password hashing, password validation, and date validation. Run `py -m unittest discover -s tests -v` after Python 3 is installed. The project does not claim any unrun test results.
