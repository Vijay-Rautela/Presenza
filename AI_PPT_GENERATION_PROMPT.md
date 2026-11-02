# Master AI Prompt: Generate Clean, Non-AI-Oriented Presentation

Use this prompt in **Gamma App (gamma.app)**, **Claude 3.7 / ChatGPT 4o (with Python-pptx or Marp)**, or **Canva AI**. It includes strict negative constraints based on our engineering principles to eliminate generic AI fluff, purple gradients, and cartoonish clichés.

---

### Copy and Paste the Prompt Below:

```markdown
You are a senior systems architect and presentation designer creating a high-stakes, 12-slide engineering defense slide deck for an academic software project named "Presenza: Attendance Management System".

Follow these STRICT aesthetic and content constraints:

CRITICAL DESIGN & AESTHETIC RULES (DO NOT VIOLATE):
1. NO PURPLE GRADIENTS: Do not use purple, violet, magenta, or dark-neon gamer themes.
2. COLOR PALETTE: Deep slate/charcoal (#0F172A or #1E293B) background, clean off-white (#F8FAFC) text, muted steel gray (#64748B) borders, and a sharp functional emerald green (#10B981) or technical cyan (#0EA5E9) accent for key highlights.
3. NO EMOJIS: Never use emojis anywhere in slide titles, bullets, or headers. No rocket ships, lightbulbs, or sparkles.
4. NO CHEESY STOCK IMAGES OR CARTOONS: Absolutely zero illustrations of 3D floating robot hands, abstract glowing network nodes, or corporate handshake clipart. If visuals are needed, use structured ASCII architecture diagrams, clean 2-column data tables, or database schema snippets.
5. NO BENTO GRIDS OR 3-CARD ROWS: Avoid the standard AI template of 3 identical rounded cards in a row. Use asymmetric editorial layouts: split columns (e.g., 60% data table on the left, 40% technical callout box on the right).
6. NO EM DASHES: Do not use the em dash ("—"). Use colons, parentheses, or periods.
7. NO VAGUE AI BUZZWORDS: Ban words like "synergy", "seamlessly orchestrate", "leverage", "paradigm shift", "empower", "unlock", and "in today's fast-paced digital world". Use concrete engineering terminology: latency, atomicity, Poka-Yoke, PBKDF2-HMAC-SHA256, SQLite WAL mode, polar coordinates, unique constraints.
8. REAL NUMBERS & METRICS: Include tangible data points:
   - 36 enrolled students, 5 faculty, 6 subjects, 91.8% compliance rate, 3 critical defaulters.
   - Screen transition latency: 0.28 seconds.
   - 100-row batch CSV import: 0.84 seconds.
   - Database constraint: UNIQUE(student_id, subject_id, date).

PRESENTATION STRUCTURE (12 SLIDES):

Slide 1: Title & System Overview
- Title: Presenza: Attendance Management System with Automated Defaulter Tracking
- Subtitle: 3-Tier Desktop Architecture with Poka-Yoke Proxy Prevention and Polar Coordinate Risk Radar
- Details: Python 3.11+, CustomTkinter, SQLite3 (WAL mode), TQM Quality Goal Q20.

Slide 2: Problem Statement & Structural Failures
- Topic: Why paper sign-in sheets and manual Excel workbooks fail in universities.
- Layout: 2-column table comparing legacy failure mode (proxies, silent unlogged edits, delayed defaulter detection) against academic consequences.

Slide 3: Total Quality Management (TQM) Principles & Goal Q20
- Topic: Poka-Yoke error prevention, customer-centric transparency, and continuous audit logs.
- Include a 5-point parameter table showing target metrics vs verified implementation (0 duplicate records, 100% audit log coverage).

Slide 4: 3-Tier Service-Oriented Desktop Architecture
- Topic: Clean separation between Presentation Layer (CustomTkinter UI), Service Layer (Business rules & validators), and Persistence Layer (SQLite WAL).
- Include clean text/box diagram showing data flow and strictly zero raw SQL inside UI classes.

Slide 5: Tripartite Role Segregation & Access Boundaries
- Topic: Admin (master data, teaching assignments, backups), Teacher (scoped to assigned subjects only, 48h edit window), Student (read-only self-audit, leave requests).
- Layout: 3-column structured matrix outlining permitted vs prohibited actions.

Slide 6: Poka-Yoke Proxy Prevention Mechanisms
- Topic: Eliminating proxies mechanically at 3 levels: UI future-date blocking, Service-layer teacher assignment validation, and SQLite composite UNIQUE key.
- Include the exact SQL schema snippet for the attendance table.

Slide 7: Admin Command HUD & 3D Tactical Defaulter Radar
- Topic: Real-time executive dashboard featuring a polar coordinate risk radar (green outer ring for >75% attendance; red danger core for <75% defaulters with sweep arm) and telemetry waveform.
- Data: 36 students, 5 faculty, 91.8% compliance, 3 defaulters flagged.

Slide 8: Auditable Corrections & Grace Windows
- Topic: Handling clerical adjustments without data corruption.
- Rules: 48-hour configurable grace period, mandatory justification text requirement, atomic write to attendance_logs.

Slide 9: Security, Cryptography & Disaster Recovery
- Topic: PBKDF2-HMAC-SHA256 password hashing (100,000 rounds, 16-byte random salt), two-factor account activation (ID + DOB), and 1-click isolated SQLite snapshots.

Slide 10: Student Portal & Two-Way Leave Approval Loop
- Topic: Transparent self-auditing and automated leave status synchronization upon teacher approval.

Slide 11: Quantitative System Benchmarks & Performance Verification
- Topic: Empirical test results in a verification table (0.28s navigation latency, 0.84s batch ingestion, 0 duplicate records allowed, 100% audit logging).

Slide 12: Production Readiness & Defense Summary
- Topic: Engineering conclusion, TQM defense readiness, and future hardware integration roadmap (biometrics, barcode scanning, parent SMS triggers).

OUTPUT FORMAT:
Generate the presentation with clean, high-density slides, precise typography, technical tables, and exact engineering details. Maintain a serious, polished, and human-designed aesthetic throughout.
```
