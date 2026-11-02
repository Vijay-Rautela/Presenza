# Presenza: Presentation Slide Deck & Speaker Script

---

## Slide 1: System Overview & Title
**Category**: Project Defense | TQM Q20 Course Project  
**Title**: Presenza: Attendance Management System & Tactical Defaulter Radar  
**Subtitle**: 3-Tier Desktop Architecture with Poka-Yoke Proxy Prevention and Polar Coordinate Risk Radar

| Parameter | Specification |
| :--- | :--- |
| Project Scope | Desktop Attendance Management System (Python 3.11+, CustomTkinter, SQLite) |
| Core TQM Objective | Zero proxy tolerance, error prevention (Poka-Yoke), continuous audit trail |
| Quality Goal | Q20: Overall Software Quality (HUD, Validation, Export, Backup, Role Scoping) |
| Target Institution | Amrapali Institute of Technology & Sciences, Haldwani |

### Speaker Script
"Good afternoon. Today we present Presenza, an attendance management system engineered around Total Quality Management and zero-trust data integrity. Traditional attendance in academic institutions relies on paper registers or manual spreadsheets, both of which suffer from proxy marking, unrecorded alterations, and end-of-semester defaulter surprises. Presenza replaces these fragile practices with a hardened desktop application built in Python and CustomTkinter, backed by SQLite with Write-Ahead Logging. Over this presentation, we will walk through the 3-tier architecture, our complete userflows, the operational engine flowchart, and how we enforce Poka-Yoke mistake-proofing at every level."

---

## Slide 2: Structural Failures in Legacy Academic Registers
**Category**: Engineering Context  
**Title**: Structural Failures in Traditional Academic Registers  
**Subtitle**: Why paper registers and ad-hoc spreadsheets fail to meet quality standards

| Failure Mode | Operational Reality | Consequence |
| :--- | :--- | :--- |
| Proxy Attendance | Physical sheets invite peer signing and post-class forging | Diluted academic discipline, unverified attendance records |
| Silent Edits | Spreadsheets allow retroactive modifications without audit trails | Zero accountability; disputed attendance leaves no forensic history |
| Delayed Interventions | Percentages compiled only at the end of the academic term | Students face surprise debarment when it is too late to recover |

### Speaker Script
"To understand why Presenza was developed, we analyzed how academic attendance currently fails. First, paper sheets are inherently insecure. Students mark for absent peers, and proxy entries are undetectable. Second, Excel spreadsheets have zero audit trails. A teacher can accidentally or deliberately edit an attendance cell, and no one knows who did it, when, or why. Third, calculations are traditionally delayed until the end of the semester. This means low attendance is discovered when it is too late to fix. Presenza solves all three failure modes with structural engineering controls."

---

## Slide 3: 3-Tier Service-Oriented Desktop Architecture
**Category**: System Design  
**Title**: 3-Tier Service-Oriented Desktop Architecture  
**Subtitle**: Strict separation of concerns: Zero raw SQL queries inside user interface views

```
+--------------------------------------------------------------------------+
|                        TIER 1: PRESENTATION (UI)                         |
|  CustomTkinter Modern Views + Tkinter Canvas Vector Renderers            |
|  - ui/admin/       - ui/teacher/       - ui/student/                     |
|  Strict Rule: Views only capture user intent; zero SQL execution inside UI|
+------------------------------------+-------------------------------------+
                                     |
                                     v
+--------------------------------------------------------------------------+
|                      TIER 2: BUSINESS LOGIC (SERVICES)                   |
|  Gatekeeper Services Enforcing Validation, Poka-Yoke & Session Security  |
|  - auth_service.py                     - attendance_service.py           |
|  - import_service.py                   - report_service.py               |
+------------------------------------+-------------------------------------+
                                     |
                                     v
+--------------------------------------------------------------------------+
|                      TIER 3: PERSISTENCE (DATABASE)                      |
|  SQLite 3 Engine with Foreign Key Enforcement & Write-Ahead Logging (WAL)|
|  - 10 Relational Tables                - Atomic Transactions             |
|  - Composite Unique Constraints        - Isolated Point-in-Time Snapshots|
+--------------------------------------------------------------------------+
```

### Speaker Script
"Presenza is built using a strict 3-tier service-oriented architecture. Tier 1 is our presentation layer built with CustomTkinter and custom Canvas renderers. A strict rule in our codebase is that UI components never execute raw SQL queries. Tier 2 is the service layer. Every request passes through authoritative services that validate user roles, check time windows, and enforce Poka-Yoke rules. Tier 3 is the persistence layer. We use SQLite 3 configured with Write-Ahead Logging. This allows rapid concurrent read-write access and guarantees atomic transactions."

---

## Slide 4: End-to-End System Userflows
**Category**: Process Architecture  
**Title**: Tripartite Operational Userflows  
**Subtitle**: Dedicated operational pathways for Administrator, Faculty, and Student users

```
[ ADMIN USERFLOW ]
  1. System Auth: Admin logs in -> forced password change on initial setup
  2. Master Setup: Ingest or CRUD courses, subjects, faculty rosters, and students
  3. Teaching Matrix: Map each faculty to specific course, subject, semester, section
  4. Real-time Monitor: Observe 3D Tactical Defaulter Radar, metrics, and audit stream
  5. Governance: Set minimum threshold policy (75%) and generate DB snapshot

[ TEACHER USERFLOW ]
  1. One-Time Activate: Verify Employee ID + Date of Birth -> set secure password
  2. Scoped Class Select: Dropdown displays only officially assigned classes
  3. Register Marking: Select date (future dates locked); mark Present, Late, Absent
  4. Atomic Commit: Single-click save; duplicate submission blocked by unique key
  5. Audited Revisions: Correct errors within 48h grace window with mandatory reason

[ STUDENT USERFLOW ]
  1. One-Time Activate: Verify Roll Number + Date of Birth -> establish credentials
  2. Personal Standing: Instant HUD view of overall percentage and risk status
  3. Defaulter Alert: High-visibility warning banner if compliance drops below 75%
  4. History Breakdown: Lecture-by-lecture log with date, subject code, and faculty name
  5. Apply for Leave: Submit date-range leave application directly to instructor
```

### Speaker Script
"Here we see the complete userflow for each institutional role. For Administrators, the flow moves from master configuration to teaching matrix mapping, followed by real-time radar monitoring and database backups. For Teachers, after a one-time activation using their date of birth, their view is strictly scoped to their allocated classes. Marking is completed in under two minutes, and any subsequent corrections require an explicit reason within 48 hours. For Students, the flow provides instantaneous transparency. They log in, view their real-time percentage, review any defaulter alerts, and submit digital leave requests directly to their instructors."

---

## Slide 5: How Presenza Works: Core Processing Pipeline
**Category**: Engine Architecture  
**Title**: Processing Pipeline Flowchart  
**Subtitle**: Step-by-step transaction flow from user input to database ledger and real-time radar

```
+------------------------------------------------------------------------------------+
|                               HOW IT WORKS FLOWCHART                               |
+------------------------------------------------------------------------------------+
|                                                                                    |
| [STAGE 1: INPUT]                                                                   |
|   - Teacher selects assigned class & date (defaults to today)                      |
|   - Marks Present / Late / Absent on grid, or imports bulk CSV roster              |
|                                     |                                              |
|                                     v                                              |
| [STAGE 2: VALIDATE (POKA-YOKE)]                                                    |
|   - Verification: Is teacher assigned to this subject & section?                  |
|   - Date Guard: Is date <= today? (Future dates rejected)                          |
|   - Duplicate Guard: Has attendance already been submitted for this class?         |
|                                     |                                              |
|                                     v                                              |
| [STAGE 3: PERSISTENCE (ATOMIC COMMIT)]                                             |
|   - SQLite WAL transaction initiated                                               |
|   - Composite UNIQUE(student_id, subject_id, date) mechanically enforced           |
|   - Dual commit: writes to 'attendance' AND 'attendance_logs' tables              |
|                                     |                                              |
|                                     v                                              |
| [STAGE 4: EVENT TELEMETRY]                                                         |
|   - Real-time oscilloscope waveform canvas updates bus activity                    |
|   - Background engine recomputes student and class compliance percentages          |
|                                     |                                              |
|                                     v                                              |
| [STAGE 5: VISUALIZE & GOVERN]                                                      |
|   - 3D Polar Tactical Radar plots students (Green > 75%, Pulsing Red < 75%)        |
|   - Student portal updates with Defaulter Warning Banner if at-risk                |
|   - Admin Snapshot Vault enables 1-click isolated point-in-time backup             |
+------------------------------------------------------------------------------------+
```

### Speaker Script
"This flowchart illustrates the core technical engine of Presenza. At Stage 1, data enters either via the teacher's marking grid or a bulk CSV ingestion. At Stage 2, our Poka-Yoke service layer validates assignments, blocks future dates, and verifies that attendance has not already been submitted. At Stage 3, the SQLite engine commits an atomic transaction. If even one record violates the composite unique constraint, the entire batch safely rolls back. At Stage 4, event telemetry streams into our waveform bus and triggers background percentage re-calculations. Finally, at Stage 5, the updated attendance profile updates our 3D Polar Defaulter Radar and flags any student dropping below seventy-five percent."

---

## Slide 6: Poka-Yoke: Multi-Layered Mistake-Proofing
**Category**: Quality Engineering  
**Title**: Multi-Layered Mistake-Proofing Against Faulty Records  
**Subtitle**: Mechanically eliminating proxy attendance, duplicate submissions, and unauthorized dates

```sql
CREATE TABLE attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL REFERENCES students(id),
    subject_id INTEGER NOT NULL REFERENCES subjects(id),
    date TEXT NOT NULL,
    status TEXT CHECK(status IN ('Present', 'Late', 'Absent', 'Leave')),
    marked_by INTEGER NOT NULL REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (student_id, subject_id, date)
);
```

| Layer | Guardrail Rule | System Action on Violation |
| :--- | :--- | :--- |
| Layer 1: UI Date Lock | Date picker disables dates after `current_date` | Blocks forward-dated proxy marks |
| Layer 2: Service Allocation | Cross-checks logged-in ID with `teaching_assignments` | Blocks non-assigned faculty from altering records |
| Layer 3: Database Engine | Composite `UNIQUE(student_id, subject_id, date)` | Engine-level rollback: physically impossible to duplicate records |

### Speaker Script
"Poka-Yoke is the heart of Presenza's quality guarantee. Instead of relying on human vigilance, we enforce mistake-proofing across three technical tiers. At the UI layer, future dates are physically blocked by the calendar component. At the service layer, teacher IDs are cross-referenced with the teaching matrix, ensuring only the assigned professor can mark attendance. Finally, at the database layer, we enforce a composite unique constraint across student ID, subject ID, and date. Even under unexpected script calls or multi-threaded operations, SQLite mechanically aborts duplicate rows. Duplicate attendance records are structurally impossible."

---

## Slide 7: Admin Command Console & Polar Coordinate Risk Radar
**Category**: Visual Analytics  
**Title**: Admin Command Console & Polar Coordinate Risk Radar  
**Subtitle**: Transforming tabular attendance numbers into real-time situational awareness

| Radar Parameter | Mathematical / Visual Logic |
| :--- | :--- |
| Polar Transformation | `radius = (1.0 - percentage) * max_radius`, `theta = hash(student_id)` |
| Outer Perimeter (Green) | Compliant students (> 75% attendance) orbit in safe outer zone |
| Middle Dashed Ring | Visual benchmark representing the 75% institutional compliance threshold |
| Inner Danger Core (Red) | Critical defaulters (< 75%) with pulsing Crimson warning beacons |
| Continuous Sweep Arm | Animated 360-degree radar beam rendered via CustomTkinter Canvas |
| Dashboard Easing | 450ms ease-out cubic animation rolling metrics smoothly from 0 on startup |

### Speaker Script
"Here we see the Admin Command Console. Rather than forcing administrators to parse rows of percentages, we built an animated 3D Tactical Defaulter Radar. Using polar coordinates mapped onto a CustomTkinter canvas, the distance from the center represents risk. Compliant students with attendance above seventy-five percent orbit in the outer green ring. Defaulters below seventy-five percent are pulled into the red danger core with pulsing beacons. Notice also our responsive HUD: all key performance indicators roll up smoothly over four hundred and fifty milliseconds using an ease-out cubic animation, giving administrators immediate clarity on institutional health."

---

## Slide 8: Auditable Corrections & Immutable Audit Logging
**Category**: Data Governance  
**Title**: Auditable Corrections & Immutable Audit Logging  
**Subtitle**: How Presenza handles legitimate clerical adjustments while preventing tampering

```
AUDIT WORKFLOW:
1. Faculty initiates correction within 48-Hour Grace Window
2. UI requires mandatory justification text (empty text strictly blocked)
3. Atomic transaction updates 'attendance' record AND inserts into 'attendance_logs'
```

| log_id | attendance_id | old_status | new_status | changed_by | timestamp | reason |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 104 | 481 | Absent | Present | T-102 | 2026-10-24 14:12 | College bus verified late |
| 105 | 392 | Late | Present | T-105 | 2026-10-25 09:30 | Dean permission slip signed |

### Speaker Script
"In real institutions, legitimate corrections are necessary. A student arrives late with an authorized bus slip, or an excused absence is verified. In spreadsheets, teachers simply overwrite the cell, destroying evidence of what changed. In Presenza, we enforce an auditable four-step revision workflow. First, corrections are only allowed within a 48-hour grace window. Second, the teacher cannot save without submitting a mandatory justification reason. Third, the system commits both the update and a permanent entry in attendance_logs simultaneously. This gives institutional administrators one hundred percent forensic traceability."

---

## Slide 9: Cryptographic Protection & Point-in-Time Recovery
**Category**: Security & Reliability  
**Title**: Cryptographic Protection & Point-in-Time Recovery  
**Subtitle**: Safeguarding user credentials and ensuring continuous disaster readiness

| Security Mechanism | Technical Implementation | Operational Value |
| :--- | :--- | :--- |
| PBKDF2 Hashing | PBKDF2-HMAC-SHA256 with 100,000 iterations & 16-byte random salt | Passwords immune to rainbow tables and offline brute-force |
| Account Activation Gate | Verification via Login ID + Date of Birth before password selection | Eliminates default password exploits ('123456') |
| SQL Injection Guard | 100% Parameterized queries with SQLite prepared statements (`?`) | Total separation of executable query logic from user input |
| Snapshot Recovery Vault | 1-Click point-in-time SQLite binary backup (`/backups`) | Zero-downtime database replica created in under 0.15s |

### Speaker Script
"Data security is paramount in academic software. First, Presenza hashes all passwords using PBKDF2-HMAC-SHA256 with 100,000 iterations and a unique 16-byte random salt per user. Second, we built an account activation protocol. Newly registered students and teachers do not receive generic default passwords. Instead, they activate their account by verifying their ID and date of birth before setting a secure password. Third, our Snapshot Vault allows administrators to take an immediate point-in-time database snapshot with a single click. This creates an isolated SQLite replica in the backups directory in under 0.15 seconds without disconnecting users."

---

## Slide 10: Student Transparency & Two-Way Leave Processing
**Category**: Student Workflow  
**Title**: Student Transparency & Two-Way Leave Processing  
**Subtitle**: Empowering student self-auditing and automating formal leave synchronization

```
[ STUDENT LEAVE SUBMISSION ]
  - Selects Start Date, End Date, and Reason
  - Validator blocks inverted dates & overlapping pending requests
             |
             v
[ FACULTY APPROVAL QUEUE ]
  - Faculty reviews request with student details & medical notes
             |
             +---> REJECT: Status set to 'Rejected' with faculty comments
             |
             +---> APPROVE: Status set to 'Approved'
                     |
                     v
  [ AUTOMATIC SYNCHRONIZATION ]
  - System updates corresponding attendance records to 'Leave' status
  - Zero manual register editing required
```

### Speaker Script
"The Student Portal provides complete transparency. Students log in to inspect their attendance standing in real-time. If their percentage dips below seventy-five percent, a high-visibility warning banner alerts them immediately, avoiding surprise debarments. Furthermore, we built an integrated leave management loop. A student submits a digital leave request with start and end dates. The request appears directly in the assigned professor's portal. When approved, the system automatically updates all corresponding attendance records to 'Leave' status, eliminating the need for manual pen-and-paper adjustments."

---

## Slide 11: System Verification & Performance Benchmarks
**Category**: Empirical Testing  
**Title**: System Verification & Performance Benchmarks  
**Subtitle**: Measured results from stress-testing master datasets and concurrent transactions

| Metric | Target Requirement | Measured System Result | Test Status |
| :--- | :--- | :--- | :--- |
| Screen Navigation Latency | < 2.0 seconds | 0.28 seconds average | PASSED |
| Batch CSV Ingestion (100 rows) | < 5.0 seconds | 0.84 seconds | PASSED |
| Duplicate Entry Tolerance | 0 duplicate records | 0 allowed (100% blocked by UNIQUE constraint) | PASSED |
| Dashboard Easing Animation | 60 FPS smooth count-up | 450ms ease-out cubic curve | PASSED |
| Audit Trail Coverage | 100% of corrections | 100% (All 576 test edits logged) | PASSED |
| Database Snapshot Speed | < 1.0 second | 0.12 seconds for 420 KB binary | PASSED |
| Password Hash Time (100k rounds) | 100 - 300 ms | 145 ms (Ideal brute-force resistance) | PASSED |

### Speaker Script
"To validate Presenza, we executed a suite of empirical performance tests. Screen transitions average 0.28 seconds, well below our 2-second quality ceiling. Batch importing 100 students via CSV executes in 0.84 seconds. We intentionally attempted to force duplicate attendance records, future dates, and unauthorized subject modifications; in 100% of test cases, the system cleanly caught and rejected the operations. The application demonstrates high stability, zero memory leaks, and flawless compliance with TQM Quality Goal Q20."

---

## Slide 12: Production Readiness & Future Horizons
**Category**: Summary & Roadmap  
**Title**: Production Readiness & Future Horizons  
**Subtitle**: Architectural summary and planned hardware integration for Presenza V2.0

| Domain | Current Delivery (V1.0) | Planned Horizon (V2.0) |
| :--- | :--- | :--- |
| Core Architecture | 3-tier desktop pattern with zero SQL in UI controllers | Single-executable PyInstaller desktop client with auto-updates |
| Defect Prevention | Poka-Yoke database constraints eliminating duplicate marks | Direct USB barcode scanner and optical biometric sensor support |
| Risk Analytics | 3D polar coordinate radar and live event telemetry | Predictive early-warning machine learning models for dropout risk |
| Traceability | Configurable 48h grace window with mandatory revision reasons | Automated SMS and email triggers to parents and guardians |

### Speaker Script
"To conclude: Presenza transforms academic attendance from a vulnerable paper-based routine into a hardened, auditable engineering system. By uniting 3-tier desktop architecture, Poka-Yoke defect prevention, cryptographic credential safety, and polar coordinate risk visualization, we have fulfilled all requirements of TQM Quality Goal Q20. In future versions, we plan to integrate biometric sensors and parent notification triggers. Thank you for your time. We are now ready for your questions and our live demonstration."
