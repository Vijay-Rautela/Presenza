# Presenza — Viva Examination Master Guide & Cheat Sheet

This document is prepared specifically for your **Practical Viva & Project Defense**. It covers both **simple functional questions** (what buttons do, what UI widgets show) and **deep technical questions** (algorithms, database architecture, security, math, and design patterns).

---

## ⚡ Quick Viva Cheat Sheet (Memorize in 2 Minutes)

| Feature | Plain English Answer (Say this in Viva) |
| :--- | :--- |
| **What is Presenza?** | A desktop attendance management system built in Python, CustomTkinter, and SQLite with automated proxy prevention and real-time risk radar. |
| **What Architecture?** | 3-Tier Service-Layer Architecture (UI -> Services -> Database). UI has zero SQL. |
| **What is the 3D Radar?** | An animated tactical visualizer that plots students in polar coordinates. Outer green dots = safe students; inner pulsing red dots = critical defaulters (< 75%). |
| **What is the Waveform?** | A live cyber oscilloscope canvas showing real-time system event telemetry and database bus activity. |
| **How are duplicates stopped?** | Dual protection: Poka-Yoke check in Python service + database `UNIQUE(student_id, subject_id, date)` constraint. |
| **How are passwords stored?** | PBKDF2-HMAC-SHA256 with 100,000 iterations and a unique 16-byte random salt per user. Never plain text. |
| **Why SQLite?** | Zero-configuration, embedded, fast, serverless, and supports atomic transactions via Write-Ahead Logging (WAL). |
| **Demo Admin Login** | Username: `admin` | Default password: `Admin@123` (requires change on first login) |

---

## Part 1: Simple & Functional Viva Questions ("Sir, this is what the UI does")

### Q1: What are the three roles in the system and what can each do?
- **Admin**: The superuser. Manages students, faculty, courses, and subjects. Maps teaching assignments, monitors the 3D Defaulter Radar, runs bulk CSV imports, changes attendance policy, and creates database backups.
- **Teacher**: The attendance operator. Can **only** see classes officially assigned to them. Marks daily attendance registers, corrects records within a grace window (mandatory reason required), and approves/rejects student leave requests.
- **Student**: The viewer. Can **only** see their own attendance percentage, subject breakdown, lecture history, and warning alerts if below the 75% threshold. Can submit leave applications.

---

### Q2: What is that 3D Radar on the Admin Dashboard? What do the green and red dots mean?
**Simple Answer to tell Sir:**
> *"Sir, that is our **3D Defaulter Risk Radar**. It visualizes student attendance compliance in real-time. 
> - The circular elliptical rings represent attendance zones: the outer ring is 100%, the middle dashed ring is our 75% target threshold, and the center core is the danger zone.
> - The green dots rotating on the outer edge represent safe, compliant students who have attendance above 75%.
> - The pulsing red beacons in the center represent **critical defaulters** who have attendance below 75% (for example, the 3 students in our database with only 6.2% attendance).
> - The sweeping line continuously scans 360 degrees, simulating a real-time radar sweep."*

---

### Q3: What is the moving green wave (oscilloscope)? What does it show?
**Simple Answer to tell Sir:**
> *"Sir, that is our **Telemetry Waveform Canvas**. It is an animated digital oscilloscope that represents the live system heartbeat and audit stream. Whenever teachers mark attendance, students apply for leave, or audit revisions occur, it reflects that the database event bus is active and synchronized."*

---

### Q4: Why do the numbers count up when the dashboard opens?
**Simple Answer to tell Sir:**
> *"Sir, that is an **animation easing ticker**. Instead of abruptly flashing static numbers on screen, the numbers smoothly roll up from 0 to their actual value (for example, 0 to 36 students, or 0.0% to 91.8% attendance) over 450 milliseconds using an ease-out cubic curve. It gives the dashboard a polished, high-tech command center feel."*

---

### Q5: What is the colored bar under "Attendance Spectrum"?
**Simple Answer to tell Sir:**
> *"Sir, that is the **proportional attendance spectrum bar**. It divides all attendance logs into three color-coded sections:
> - **Green segment**: Present records (78.6%)
> - **Orange/Amber segment**: Late arrivals (13.2%)
> - **Red segment**: Absent records (8.2%)
> When the dashboard opens, this bar smoothly expands from width 0 to its full proportional width."*

---

### Q6: What was that "dot" on the far right of the top metric cards?
**Simple Answer to tell Sir:**
> *"Sir, previously on standard 1080p laptop screens, all 6 KPI cards were packed horizontally in a single row, so the 6th card (**SYSTEM EVENTS**) was squeezed against the right border into a tiny sliver. 
> We resolved this by building a **dynamic responsive grid**: on standard laptop displays, it automatically organizes the cards into a clean **3 columns by 2 rows** layout so every card has generous breathing room and is 100% visible. If the window is maximized on an ultra-wide screen, it automatically expands to 6 columns across."*

---

### Q7: What are the 6 Rapid Action buttons on the dashboard?
1. **Enroll Student**: Opens a pop-up dialog to register a new student with their roll number, name, DOB, course, semester, section, and email.
2. **Appoint Faculty**: Opens a dialog to register a teacher with employee ID, name, department, DOB, and email.
3. **Map Assignment**: Assigns a teacher to teach a specific subject, course, semester, and section using friendly dropdown menus.
4. **Bulk CSV Ingest**: Opens the bulk import screen to upload a spreadsheet of 100+ students or teachers at once.
5. **DB Snapshot**: Creates an immediate point-in-time backup file of the SQLite database in the `/backups` directory without restarting the app.
6. **Threshold Policy**: Lets the admin adjust the college minimum attendance percentage (e.g., from 75% to 80%).

---

### Q8: What happens when an Admin clicks "Reset Account"?
**Simple Answer to tell Sir:**
> *"If a student or teacher forgets their password or locks themselves out, the Admin clicks 'Reset Account'. The system wipes their password hash and sets `is_active = 0`. The user must then go to the 'Activate Account' screen, verify their identity using their Login ID and Date of Birth, and set a new password."*

---

### Q9: What happens when a teacher marks attendance? Can they mark for tomorrow?
**Simple Answer to tell Sir:**
> *"No, sir. The system enforces **Poka-Yoke (mistake-proofing)**:
> 1. The teacher selects their assigned class from a dropdown.
> 2. The date defaults to today. If a teacher attempts to pick a future date, the system immediately blocks it with a validation error.
> 3. If attendance has already been saved for that class on that date, the system prevents duplicate submission.
> 4. The teacher selects Present, Late, or Absent for each student and saves. The records are saved in SQLite within an atomic transaction."*

---

### Q10: Can a teacher edit attendance after saving? How is cheating prevented?
**Simple Answer to tell Sir:**
> *"Yes, but under two strict security conditions:
> 1. **Edit Window**: It must be within the configured grace period (e.g., within 2 days of the class). After 2 days, records are locked permanently.
> 2. **Mandatory Reason & Audit Log**: The teacher cannot save a correction without entering a valid reason (e.g., 'Late bus verified' or 'Medical slip provided'). 
> The system writes an immutable audit record into `attendance_logs` storing who changed it, the old status, the new status, the timestamp, and the reason. The Admin can see this on the Audit Logs screen."*

---

### Q11: How does student leave work?
**Simple Answer to tell Sir:**
> *"A student submits a leave application with start date, end date, and reason. The status is set to `Pending`. The assigned teacher reviews it in their portal and clicks `Approve` or `Reject`. If approved, any attendance records for that student during that date range are automatically updated to `Leave`."*

---

## Part 2: Technical & Architecture Viva Questions ("Sir, this is how the code works")

### Q12: Explain your System Architecture. Why is there no SQL in the UI files?
**Technical Answer:**
> *"Sir, we implemented a **3-Tier Service-Layer Architecture**:
> 1. **Presentation Layer (`ui/`)**: Built using CustomTkinter and Tkinter Canvas. Its only job is rendering widgets, capturing user inputs, and displaying responses. It contains zero SQL queries.
> 2. **Service Layer (`services/`)**: Contains all business logic, validation, role authorization, and data transformation (`admin_service.py`, `attendance_service.py`, `auth_service.py`, `student_service.py`).
> 3. **Persistence Layer (`database/`)**: Manages the SQLite connection pool, schema migrations, and atomic transactions (`db.py`).
> 
> **Why this matters**: Separation of concerns. If we ever switch our database from SQLite to PostgreSQL, we only modify the database layer. The UI code remains completely untouched."*

---

### Q13: How does the 3D Tactical Radar work under the hood? What is the math?
**Technical Answer:**
> *"Sir, the radar is rendered on a native **Tkinter Canvas** running at approximately 30 frames per second using recursive `after(35, self._schedule_sweep)` scheduling.
> 
> **The Mathematical Implementation**:
> 1. **3D Perspective Projection**: Instead of circles, we draw ellipses by using distinct horizontal and vertical radii ($r_x$ and $r_y$, where $r_y \approx 0.65 \cdot r_x$). This simulates an inclined tactical cockpit display viewed from an angle.
> 2. **Rotating Sweep Vector**: We maintain an angle variable $\theta$ that increments by $3.5^\circ$ each frame. We convert polar coordinates to screen Cartesian coordinates $(x, y)$ using trigonometry:
>    $$x = c_x + r_x \cdot \cos(\theta)$$
>    $$y = c_y + r_y \cdot \sin(\theta)$$
> 3. **Phosphor Trail**: We render three trailing lines at $(\theta - 6^\circ)$ and $(\theta - 12^\circ)$ with darker green shades to simulate an authentic fading phosphor radar trail.
> 4. **Defaulter Blip Pulse**: We use a sinusoidal phase equation $r_{pulse} = 3 + 2 \cdot \sin(\phi)$ to make the red defaulter target beacons expand and contract dynamically."*

---

### Q14: How does the responsive layout work in the Admin Dashboard?
**Technical Answer:**
> *"Sir, we bound the `<Configure>` event on the parent container. Whenever the window is resized:
> 1. It reads the current container width: `w = kpi_container.winfo_width()`.
> 2. It evaluates dynamic breakpoints:
>    - If $w \ge 1260\text{px}$: sets columns = 6.
>    - If $700\text{px} \le w < 1260\text{px}$: sets columns = 3 (creating a balanced 3×2 grid).
>    - If $w < 700\text{px}$: sets columns = 2.
> 3. We configure column weights: `kpi_container.grid_columnconfigure(c, weight=1, uniform='kpi')`.
> 4. We position each card using integer division and modulo:
>    $$\text{row} = i // \text{cols}, \quad \text{col} = i \% \text{cols}$$
> 5. We cache the previous column state (`if cols == last_cols: return`) to prevent redundant re-renders and eliminate CPU overhead."*

---

### Q15: Explain the animation easing formula used for the number tickers.
**Technical Answer:**
> *"Sir, instead of linear interpolation which looks mechanical, we implemented **Ease-Out Cubic Interpolation**:
> $$\text{Progress} = \min\left(1.0, \frac{\text{Elapsed Time}}{\text{Duration (450ms)}}\right)$$
> $$\text{Eased Progress} = 1 - (1 - \text{Progress})^3$$
> $$\text{Current Value} = \text{Target} \times \text{Eased Progress}$$
> 
> In this formula, the value increases rapidly at the beginning and decelerates smoothly near the end, producing a natural physics-based telemetry count."*

---

### Q16: How are passwords secured in the database?
**Technical Answer:**
> *"Sir, we follow industry security standards:
> 1. We never store plain text passwords.
> 2. We use Python's `hashlib.pbkdf2_hmac` with the `SHA256` hashing algorithm.
> 3. We use **100,000 iteration cycles**, which makes brute-force attacks and GPU cracking computationally unfeasible.
> 4. We generate a unique **16-byte cryptographically secure random salt** using `os.urandom(16)` for each user.
> 5. The salt is stored alongside the hash in format `hex(salt)$hex(hash)`, preventing rainbow table lookups."*

---

### Q17: How do you prevent SQL Injection and CSV Formula Injection?
**Technical Answer:**
> *"1. **SQL Injection**: We never concatenate user strings into raw SQL. We strictly use **parameterized queries** with SQLite place-holders (`?`), ensuring user inputs are treated solely as literal values by the SQLite query planner.
> 2. **CSV Formula Injection (CSV Exploitation)**: When exporting reports to CSV via Pandas, malicious users might enter names starting with `=`, `+`, `-`, or `@` to trigger arbitrary code execution in Microsoft Excel. Our `report_service.py` inspects values and prepends a single quote (`'`) to any string starting with formula characters, neutralizing spreadsheet execution."*

---

### Q18: What is SQLite WAL Mode and why did you use it?
**Technical Answer:**
> *"Sir, by default, SQLite uses a rollback journal which locks the entire database file during writes. In `database/db.py`, we execute `PRAGMA journal_mode = WAL;` (Write-Ahead Logging).
> In WAL mode:
> - **Readers do not block writers, and writers do not block readers**.
> - Read operations can occur concurrently while attendance records are being written.
> - Write operations are significantly faster because changes are appended sequentially to a `.wal` file before checkpointing."*

---

### Q19: What is Poka-Yoke and where is it in your project?
**Technical Answer:**
> *"Sir, **Poka-Yoke** is a Japanese Total Quality Management (TQM) principle meaning 'mistake-proofing' — designing a system so that human error is mechanically impossible.
> In Presenza, Poka-Yoke is implemented in three places:
> 1. **Future Date Blocking**: The attendance calendar mechanically rejects dates in the future.
> 2. **Class Verification**: A teacher cannot submit attendance for students not officially enrolled in that section.
> 3. **Database Unique Constraint**: `UNIQUE(student_id, subject_id, date)` guarantees that duplicate attendance can never physically be inserted, even if a user double-clicks submit."*

---

### Q20: What are the main database tables and how are they related?
1. `users`: Stores login credentials (`login_id`, `password_hash`, `role`, `dob`, `is_active`, `must_change_password`).
2. `courses`: Academic programs (`name`, `duration_years`).
3. `subjects`: Course subjects (`code`, `name`, `course_id`, `semester`). Foreign key -> `courses.id`.
4. `teachers`: Faculty records (`emp_id`, `name`, `department`, `email`, `user_id`). Foreign key -> `users.id`.
5. `students`: Enrolled students (`roll_no`, `name`, `course_id`, `semester`, `section`, `email`, `user_id`). Foreign keys -> `users.id`, `courses.id`.
6. `teaching_assignments`: Many-to-many allocation mapping `teacher_id`, `subject_id`, `course_id`, `semester`, `section`.
7. `attendance`: Attendance marks (`student_id`, `subject_id`, `date`, `status`, `marked_by`). Unique constraint on `(student_id, subject_id, date)`.
8. `attendance_logs`: Audit trail for corrections (`attendance_id`, `old_status`, `new_status`, `changed_by`, `changed_at`, `reason`).
9. `leave_requests`: Student leave applications (`student_id`, `from_date`, `to_date`, `reason`, `status`, `approved_by`).
10. `settings`: Key-value system configurations (`min_attendance`, `edit_window_days`).

---

## 🎯 Final Tips for the Viva

1. **Be confident and speak clearly**: You know your system inside and out.
2. **Start with the business problem**: *"Sir, manual registers cause proxy attendance and lost data. Presenza automates attendance with role access and fraud prevention."*
3. **Show, don't just tell**: When talking about the radar or responsive layout, maximize and minimize the window to demonstrate that the cards adapt smoothly.
4. **Use technical terms**: Mention *Poka-Yoke*, *PBKDF2*, *Write-Ahead Logging*, *Service-Layer pattern*, and *Ease-Out Cubic interpolation*. Professors love these keywords!
