# Presenza — Attendance Management System (AMS)
## Complete Comprehensive Project Presentation & Architectural Walkthrough

---

## 1. Executive Summary & Project Introduction

### 1.1 What is Presenza?
**Presenza** is a high-reliability, desktop-based academic attendance management system engineered in **Python** using **CustomTkinter** and **SQLite**. It replaces manual paper-based attendance registers and fragile spreadsheets with an automated, role-segregated, auditable system.

### 1.2 Core Problem Solved
Traditional college attendance tracking suffers from three major flaws:
1. **Proxy Attendance & Manipulation**: Students marking for absent peers or unauthorized changes after submission.
2. **Delayed Defaulter Identification**: Administrators only discover low attendance at the end of the semester when it is too late for intervention.
3. **Data Loss & Fragmented Records**: Lost paper registers, scattered Excel sheets with broken formulas, and zero audit trails.

### 1.3 Tech Stack & Architecture
- **Language**: Python 3.11+
- **GUI Framework**: CustomTkinter (Modern, DPI-aware desktop widgets) + Tkinter Canvas (for 3D vector graphics and animations)
- **Database Engine**: SQLite 3 with Foreign Key enforcement and Write-Ahead Logging (WAL)
- **Data Analytics & Export**: Pandas & Matplotlib
- **Security**: PBKDF2-HMAC-SHA256 password hashing with individual salt generation
- **Architectural Pattern**: **Service-Layer Architecture (3-Tier)**:
  - **Tier 1: Presentation (UI)**: CustomTkinter views (`ui/admin/`, `ui/teacher/`, `ui/student/`). Pure UI logic; zero raw SQL queries.
  - **Tier 2: Business Logic (Services)**: Validation, role scoping, Poka-Yoke rules (`services/`).
  - **Tier 3: Persistence (Database)**: SQLite connection pool, schema, sessions, and atomic transactions (`database/`).

---

## 2. The 3 Role Portals (Deep Dive)

```
                       +----------------------------------+
                       |           PRESENZA APP           |
                       +----------------------------------+
                                        |
                  +---------------------+---------------------+
                  |                     |                     |
                  v                     v                     v
          [ ADMIN PORTAL ]      [ TEACHER PORTAL ]     [ STUDENT PORTAL ]
          • Master Data & CRUD   • Mark Attendance      • View Percentage
          • 3D Tactical Radar    • Edit Records         • Subject Breakdown
          • Defaulter Scanners   • Approve Leaves       • Defaulter Warnings
          • Ingest CSV & Backup  • Scoped Analytics     • Apply Leave Requests
```

---

## 3. Role 1: Administrator (The System Authority)

The Admin is the institutional superuser responsible for master data integrity, faculty allocations, risk monitoring, database security, and compliance enforcement.

### 3.1 Command Overview Dashboard (The Hero Screen)
The Admin Dashboard is designed as an executive control console:
1. **Live System Beacon & Digital Clock**:
   - Breathing status beacon (`● SYSTEM ONLINE`) oscillating in real-time.
   - Live UTC+05:30 digital clock updating every second.
   - Engine telemetry pill showing active SQLite version, WAL mode, and database file size.
2. **Responsive 6-Card Executive HUD**:
   - **Total Students**: Active enrolled students (e.g. `36 Enrolled`).
   - **Faculty Cadre**: Verified teachers across departments (e.g. `5 Verified Staff`).
   - **Curriculum Matrix**: Total subjects and active teaching allocations (e.g. `6 Subjects`, `12 Allocations`).
   - **Attendance Compliance Rate**: System-wide overall attendance percentage (e.g. `91.8%`, evaluated against target threshold).
   - **Defaulter Risk Radar**: Instant count of students falling below minimum compliance.
   - **System Events**: Real-time log of all attendance marks and audit revisions (e.g. `576 Logged`).
   - *Dynamic Responsiveness*: Automatically wraps from 6 columns on ultra-wide monitors to 3×2 on standard displays and 2×3 on compact screens, ensuring zero cutoff.
3. **Attendance Spectrum Engine**:
   - Segmented horizontal distribution bar illustrating Present (78.6%), Late (13.2%), and Absent (8.2%) with smooth glide animation upon load.
   - Individual status metric chips displaying exact record counts and percentages.
4. **Operations Command Shortcuts (6 Rapid Actions)**:
   - `◈ Enroll Student`: Fast modal to register new student records.
   - `⬡ Appoint Faculty`: Onboard teacher credentials and departments.
   - `⚡ Map Assignment`: Connect teacher, subject, course, semester, and section.
   - `↑ Bulk CSV Ingest`: Open batch spreadsheet ingestion center.
   - `💾 DB Snapshot`: 1-click isolated point-in-time database backup.
   - `⚙ Threshold Policy`: Adjust the institutional minimum attendance percentage.
5. **3D Perspective Tactical Radar (`TacticalRadarCanvas`)**:
   - Real-time animated 3D elliptical radar screen with a continuous rotating sweep beam.
   - Plots students as radar blips in polar coordinates:
     - Outer green blips: Compliant students (> 75%).
     - Inner danger core blips: Critical defaulters (< 75%) with pulsing crimson target beacons.
   - Side-by-side with an interactive Defaulter Intervention list.
6. **Audit Telemetry & Live Security Stream**:
   - Real-time oscilloscope waveform (`TelemetryWaveformCanvas`) visualizing live telemetry.
   - Feed of immutable audit events: shows who modified an attendance record, old status vs. new status, timestamp, and stated reason.

### 3.2 Master Records Management (CRUD)
- **Students**: Create, edit, search, filter, and delete student records. Reset account credentials when a student forgets their password.
- **Teachers**: Manage faculty employee IDs, departments, contact emails, and account reset status.
- **Courses**: Define academic programs (e.g., BCA, B.Tech) and duration in years.
- **Subjects**: Course-linked subjects with assigned semester numbers.
- **Teaching Matrix (Assignments)**: Maps teachers to specific subject-course-semester-section combinations via user-friendly dropdowns.

### 3.3 Bulk Ingestion (CSV / Excel)
- Batch import hundreds of students or teachers in seconds.
- Sanitizes input, checks date-of-birth formats (`YYYY-MM-DD`), normalizes uppercase roll numbers, skips duplicate rows safely, and outputs a detailed row-by-row success and skipped-row log.

### 3.4 Snapshots & Recovery (Backup)
- 1-click non-blocking database snapshot saved into `/backups` with ISO timestamp format: `presenza_backup_YYYYMMDD_HHMMSS.db`.
- Snapshot Vault lists all backups, file sizes, creation timestamps, and file paths.

### 3.5 Governance & System Policy
- Configurable minimum attendance threshold (default: `75%`).
- Configurable teacher correction grace window (default: `2` days).

---

## 4. Role 2: Teacher (The Attendance Operator)

Teachers are the operational backbone. Their portal is strictly scoped so they can **only access and modify data for classes officially assigned to them**.

### 4.1 Scoped Attendance Marking Register
1. **Poka-Yoke Assignment Selection**: Teacher selects their allocated class from a dropdown (e.g., *BCA - Sem 5 - Sec A - Data Structures*).
2. **Date Guardrails**: System defaults to today's date. Future dates are strictly rejected to eliminate fraudulent forward-marking.
3. **One-Click Marking Grid**:
   - Loads all enrolled students in that section.
   - Radio/Toggle buttons for `Present`, `Late`, and `Absent`.
   - "Mark All Present" shortcut for rapid morning registration.
4. **Duplicate Prevention**: If attendance has already been recorded for that subject, class, and date, the system prevents duplicate submission.

### 4.2 Traceable Attendance Corrections
- If a student arrives late with an authorized slip or a teacher makes an error:
  - Teacher opens the **Correction Workspace**.
  - System checks the **Edit Window Rule**: corrections are only allowed within the Admin-configured grace window (e.g., within 2 days of marking).
  - **Mandatory Reason Requirement**: The teacher cannot save without typing a valid reason (e.g., *"Late bus pass verified"*, *"Medical certificate submitted"*).
  - **Immutable Audit Logging**: The system writes a permanent record into `attendance_logs`:
    - `attendance_id`, `old_status`, `new_status`, `changed_by`, `changed_at`, `reason`.

### 4.3 Student Leave Approvals
- Teachers can review leave requests submitted by students in their assigned classes.
- Approving a request automatically converts any existing attendance records within that date range to `Leave`.

### 4.4 Scoped Reports & Analytics
- Teachers can generate attendance percentages, student-wise registers, and defaulter lists **only for the subjects they teach**.
- Includes 1-click CSV export and Matplotlib chart generation.

---

## 5. Role 3: Student (The Consumer & Self-Auditor)

The Student Portal empowers students with transparent, tamper-proof insight into their academic attendance.

### 5.1 Account Privacy & Scope
- When a student signs in, their user ID is extracted directly from their authenticated session token.
- A student cannot query or view any other student's attendance records.

### 5.2 Personal Attendance Dashboard
1. **Overall Metric Card**: Total classes held, total classes attended, and aggregate attendance percentage.
2. **Defaulter Warning Banner**:
   - If aggregate percentage ≥ 75%: displays a green compliance badge (`In Good Standing`).
   - If aggregate percentage < 75%: triggers a high-visibility crimson warning banner (`Defaulter Alert: Attendance Below Minimum Policy`).
3. **Subject-by-Subject Matrix**:
   - Breakdown of attendance in every enrolled course.
   - Shows attended vs. total classes and exact percentage.
4. **Date-Wise Attendance History**:
   - Searchable chronological log of every lecture with date, subject code, teacher name, and status (`Present`, `Late`, `Absent`, `Leave`).

### 5.3 Leave Application Portal
- Students can submit leave applications directly within the application:
  - Fields: `Start Date`, `End Date`, `Reason`.
  - Date validation: Start date must precede End date.
  - Overlap Prevention: Cannot submit a new leave request that overlaps with an existing pending request.
  - Status Tracking: Displays whether the application is `Pending`, `Approved`, or `Rejected`.

---

## 6. End-to-End Operational Lifecycle

```
[ STEP 1: INITIALIZATION ]
  Admin logs in -> Sets minimum attendance threshold (75%) -> Ingests courses, subjects, teachers & students.

[ STEP 2: ALLOCATION ]
  Admin maps Faculty to Subjects & Sections in the Teaching Matrix.

[ STEP 3: ACTIVATION ]
  Teachers and Students activate their accounts by verifying their Login ID + DOB and setting a secure password.

[ STEP 4: DAILY LECTURE ]
  Teacher opens portal -> Selects class -> Marks attendance -> System records entries with unique constraints.

[ STEP 5: STUDENT TRANSPARENCY ]
  Student logs in -> Instantly sees updated attendance % -> Views warning if below 75% -> Submits leave if needed.

[ STEP 6: AUDIT & GOVERNANCE ]
  Admin monitors 3D Tactical Radar -> Detects low-attendance students -> Exports defaulter report -> Takes DB backup.
```

---

## 7. Security, Quality & Engineering Highlights

| Feature | Engineering Mechanism | Architectural Value |
| :--- | :--- | :--- |
| **Password Security** | PBKDF2-HMAC-SHA256 with 100,000 iterations & random 16-byte salt | Protects stored credentials against rainbow tables and brute force. |
| **Poka-Yoke Data Guard** | Database `UNIQUE(student_id, subject_id, date)` constraint | Mechanically eliminates duplicate attendance records. |
| **Injection Protection** | Parameterized SQL queries (`?` place-holders) + CSV formula prefixing (`'`) | Blocks SQL injection and Excel CSV formula execution exploits. |
| **Crash Prevention** | Centralized Service Layer Exception handling | UI never crashes; displays contextual error toasts to users. |
| **Responsive Aesthetics** | CustomTkinter + Canvas Vector Graphics (`math.sin`, `math.cos`) | Dynamic HUD radar and tickers with zero external bloated dependencies. |
| **Disaster Recovery** | Isolated point-in-time SQLite snapshots | Zero-downtime database backup and instantaneous restoration. |
