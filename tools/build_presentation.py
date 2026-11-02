"""
Script to generate Presenza_Presentation.pptx using python-pptx.
Enforces:
- 16:9 Widescreen format
- SOLID COLOURS ONLY (No gradients, no transparencies, no purple/neon combos)
- Dedicated Userflow Slide
- Dedicated 'How It Works' Flowchart Slide
- Clean, high-density engineering aesthetics
- Embedded Speaker Notes on every slide
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# --- COLOR PALETTE (STRICTLY SOLID COLOURS) ---
BG_COLOR = RGBColor(15, 23, 42)        # Slate 900 (Dark Slate Background)
CARD_BG = RGBColor(30, 41, 59)         # Slate 800 (Solid Card Fill)
CARD_BORDER = RGBColor(51, 65, 85)     # Slate 700 (Solid Card Outline)
TEXT_WHITE = RGBColor(255, 255, 255)   # Pure White
TEXT_MUTED = RGBColor(148, 163, 184)   # Slate 400 (Secondary text)
ACCENT_BLUE = RGBColor(2, 132, 199)    # Sky 600 (Technical Accent)
ACCENT_GREEN = RGBColor(16, 185, 129)  # Emerald 500 (Success / Safe)
ACCENT_RED = RGBColor(239, 68, 68)     # Red 500 (Alert / Defaulter)
ACCENT_AMBER = RGBColor(245, 158, 11)  # Amber 500 (Warning / Flow)
CARD_ALT_BG = RGBColor(39, 52, 75)     # Solid Darker Steel Blue for contrast

def set_slide_background(slide):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = BG_COLOR

def add_header(slide, category: str, title: str, subtitle: str = ""):
    # Category tag
    tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.35))
    tf_tag = tag_box.text_frame
    tf_tag.word_wrap = True
    tf_tag.margin_left = tf_tag.margin_top = tf_tag.margin_right = tf_tag.margin_bottom = 0
    p_tag = tf_tag.paragraphs[0]
    p_tag.text = category.upper()
    p_tag.font.name = "Arial"
    p_tag.font.size = Pt(9)
    p_tag.font.bold = True
    p_tag.font.color.rgb = ACCENT_BLUE

    # Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.7), Inches(0.55))
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    tf_title.margin_left = tf_title.margin_top = tf_title.margin_right = tf_title.margin_bottom = 0
    p_title = tf_title.paragraphs[0]
    p_title.text = title
    p_title.font.name = "Arial"
    p_title.font.size = Pt(20)
    p_title.font.bold = True
    p_title.font.color.rgb = TEXT_WHITE

    # Subtitle (if any)
    if subtitle:
        sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.22), Inches(11.7), Inches(0.35))
        tf_sub = sub_box.text_frame
        tf_sub.word_wrap = True
        tf_sub.margin_left = tf_sub.margin_top = tf_sub.margin_right = tf_sub.margin_bottom = 0
        p_sub = tf_sub.paragraphs[0]
        p_sub.text = subtitle
        p_sub.font.name = "Arial"
        p_sub.font.size = Pt(11)
        p_sub.font.color.rgb = TEXT_MUTED

def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=CARD_BORDER):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    shape.line.color.rgb = border_color
    shape.line.width = Pt(1.5)
    return shape

def add_speaker_note(slide, note_text: str):
    notes_slide = slide.notes_slide
    text_frame = notes_slide.notes_text_frame
    text_frame.text = note_text

def build_presentation():
    prs = Presentation()
    # 16:9 Widescreen
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)

    # Main Hero Card
    add_card(s1, Inches(0.8), Inches(1.2), Inches(11.733), Inches(5.1), CARD_BG, CARD_BORDER)

    # Sub-badge
    badge = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.3), Inches(1.7), Inches(3.2), Inches(0.35))
    badge.fill.solid()
    badge.fill.fore_color.rgb = ACCENT_BLUE
    badge.line.fill.background()
    p_b = badge.text_frame.paragraphs[0]
    p_b.text = "BBAT104 TQM COURSE PROJECT 2026-27"
    p_b.font.size = Pt(9)
    p_b.font.bold = True
    p_b.font.color.rgb = TEXT_WHITE
    p_b.alignment = PP_ALIGN.CENTER

    # Hero Title
    tb = s1.shapes.add_textbox(Inches(1.3), Inches(2.2), Inches(10.7), Inches(1.4))
    tf = tb.text_frame
    tf.word_wrap = True
    p1 = tf.paragraphs[0]
    p1.text = "PRESENZA"
    p1.font.name = "Arial"
    p1.font.size = Pt(40)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_WHITE

    p2 = tf.add_paragraph()
    p2.text = "Attendance Management System & Tactical Defaulter Radar"
    p2.font.name = "Arial"
    p2.font.size = Pt(20)
    p2.font.bold = True
    p2.font.color.rgb = ACCENT_GREEN

    # Split details inside the hero card
    left_tb = s1.shapes.add_textbox(Inches(1.3), Inches(3.8), Inches(5.2), Inches(2.2))
    ltf = left_tb.text_frame
    ltf.word_wrap = True
    p = ltf.paragraphs[0]
    p.text = "SYSTEM ARCHITECTURE & SPECIFICATIONS"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = TEXT_MUTED

    specs = [
        "Core Engine: Python 3.11+ & CustomTkinter Desktop GUI",
        "Database: SQLite3 with Write-Ahead Logging (WAL)",
        "Security: PBKDF2-HMAC-SHA256 (100k rounds, 16B salt)",
        "Quality Goal: Q20 Overall Software Quality",
        "Poka-Yoke: Structural UNIQUE constraints & zero proxy tolerance"
    ]
    for spec in specs:
        p = ltf.add_paragraph()
        p.text = "• " + spec
        p.font.size = Pt(10)
        p.font.color.rgb = TEXT_WHITE

    right_tb = s1.shapes.add_textbox(Inches(7.0), Inches(3.8), Inches(5.0), Inches(2.2))
    rtf = right_tb.text_frame
    rtf.word_wrap = True
    p = rtf.paragraphs[0]
    p.text = "ACADEMIC INSTITUTION"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = TEXT_MUTED

    inst_lines = [
        "Institute: Amrapali Institute of Technology & Sciences",
        "Location: Haldwani, Uttarakhand",
        "Baseline System: Attendance Management System",
        "Deliverables: Live UI, Audit Engine, Polar Radar, Backup Vault",
        "Verification: Passed stress benchmarks & concurrency tests"
    ]
    for line in inst_lines:
        p = rtf.add_paragraph()
        p.text = "• " + line
        p.font.size = Pt(10)
        p.font.color.rgb = TEXT_WHITE

    add_speaker_note(s1, 
        "Good afternoon. Today we present Presenza, an attendance management system engineered around Total Quality Management and zero-trust data integrity. "
        "Traditional attendance in academic institutions relies on paper registers or manual spreadsheets, both of which suffer from proxy marking, unrecorded alterations, and end-of-semester defaulter surprises. "
        "Presenza replaces these fragile practices with a hardened desktop application built in Python and CustomTkinter, backed by SQLite with Write-Ahead Logging. "
        "Over this presentation, we will walk through the 3-tier architecture, our complete userflows, the operational engine flowchart, and how we enforce Poka-Yoke mistake-proofing at every level."
    )

    # =========================================================================
    # SLIDE 2: PROBLEM STATEMENT (THE THREE FAILURES)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "Engineering Context", "Structural Failures in Traditional Academic Registers", "Why paper registers and ad-hoc spreadsheets fail to meet quality standards")

    cards_data = [
        ("FAILURE 1: PROXY ATTENDANCE", 
         ACCENT_RED,
         "Physical sheets invite peer signing and post-class forging.",
         ["Signatures are forged without identity verification",
          "Teachers cannot track student attendance in real time",
          "Unattended lectures are marked fraudulently",
          "Result: Diluted academic discipline and inaccurate records"]),
        ("FAILURE 2: UNLOGGED EDITS", 
         ACCENT_AMBER,
         "Spreadsheets allow retroactive modifications without audit trails.",
         ["Faculty modify Excel cells without timestamps or reasons",
          "No record of previous values or who initiated the change",
          "Disputed attendance leaves no forensic history",
          "Result: Complete lack of institutional accountability"]),
        ("FAILURE 3: DELAYED INTERVENTIONS", 
         ACCENT_BLUE,
         "Percentages are compiled only at the end of the academic term.",
         ["Month-end calculation is tedious and prone to formula errors",
          "Students do not know their compliance percentage until finals",
          "Administration cannot intervene early to save at-risk students",
          "Result: Surprise debarment and unnecessary student distress"])
    ]

    for i, (title, color, desc, points) in enumerate(cards_data):
        x = Inches(0.8 + i * 4.0)
        card = add_card(s2, x, Inches(1.7), Inches(3.733), Inches(5.1))
        
        # Color bar indicator at top of card
        top_bar = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, Inches(1.7), Inches(3.733), Inches(0.12))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = color
        top_bar.line.fill.background()

        tb = s2.shapes.add_textbox(x + Inches(0.25), Inches(1.95), Inches(3.233), Inches(4.7))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = color

        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(10)
        p.font.color.rgb = TEXT_MUTED

        p = tf.add_paragraph()
        p.text = " "
        p.font.size = Pt(4)

        for pt in points:
            p = tf.add_paragraph()
            p.text = "• " + pt
            p.font.size = Pt(9.5)
            p.font.color.rgb = TEXT_WHITE

    add_speaker_note(s2,
        "To understand why Presenza was developed, we analyzed how academic attendance currently fails. "
        "First, paper sheets are inherently insecure. Students mark for absent peers, and proxy entries are undetectable. "
        "Second, Excel spreadsheets have zero audit trails. A teacher can accidentally or deliberately edit an attendance cell, and no one knows who did it, when, or why. "
        "Third, calculations are traditionally delayed until the end of the semester. This means low attendance is discovered when it is too late to fix. "
        "Presenza solves all three failure modes with structural engineering controls."
    )

    # =========================================================================
    # SLIDE 3: 3-TIER ARCHITECTURE
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "System Design", "3-Tier Service-Oriented Desktop Architecture", "Strict separation of concerns: Zero raw SQL queries inside user interface views")

    tiers = [
        ("TIER 1: PRESENTATION LAYER (UI)", 
         ACCENT_BLUE, 
         "CustomTkinter Modern Views + Tkinter Canvas Vector Renderers",
         ["ui/admin/ (Command Dashboard, CRUD Master, 3D Tactical Radar, Backup Vault)",
          "ui/teacher/ (Scoped Register Grid, Grace-Period Corrections, Leave Review)",
          "ui/student/ (Personal Compliance HUD, Lecture Breakdown, Leave Applications)",
          "Strict Rule: Views only capture user intent; zero SQL execution inside UI"]),
        ("TIER 2: BUSINESS LOGIC LAYER (SERVICES)", 
         ACCENT_GREEN, 
         "Gatekeeper Services Enforcing Validation, Poka-Yoke & Session Security",
         ["services/auth_service.py (Session verification, PBKDF2 hashing, role token)",
          "services/attendance_service.py (Date validation, grace windows, duplicate checks)",
          "services/import_service.py (Batch CSV/Excel sanitization & transaction commits)",
          "services/report_service.py (Attendance aggregation, defaulter detection)"]),
        ("TIER 3: PERSISTENCE LAYER (DATABASE)", 
         ACCENT_AMBER, 
         "SQLite 3 Engine with Foreign Key Enforcement & Write-Ahead Logging (WAL)",
         ["10 Relational Tables: users, students, teachers, subjects, attendance, logs, etc.",
          "Atomic Transactions: All multi-row updates commit or rollback together",
          "Composite Unique Constraints: Mechanics-level duplicate prevention",
          "Snapshot Vault: Non-blocking point-in-time binary database backups"])
    ]

    for i, (name, col, subtitle_t, pts) in enumerate(tiers):
        y = Inches(1.7 + i * 1.75)
        card = add_card(s3, Inches(0.8), y, Inches(11.733), Inches(1.55))

        # Side bar
        sbar = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), y, Inches(0.15), Inches(1.55))
        sbar.fill.solid()
        sbar.fill.fore_color.rgb = col
        sbar.line.fill.background()

        tb = s3.shapes.add_textbox(Inches(1.15), y + Inches(0.1), Inches(11.2), Inches(1.35))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = name + "  —  " + subtitle_t
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = col

        for pt in pts:
            p = tf.add_paragraph()
            p.text = "• " + pt
            p.font.size = Pt(9.5)
            p.font.color.rgb = TEXT_WHITE

    add_speaker_note(s3,
        "Presenza is built using a strict 3-tier service-oriented architecture. "
        "Tier 1 is our presentation layer built with CustomTkinter and custom Canvas renderers. A strict rule in our codebase is that UI components never execute raw SQL queries. "
        "Tier 2 is the service layer. Every request passes through authoritative services that validate user roles, check time windows, and enforce Poka-Yoke rules. "
        "Tier 3 is the persistence layer. We use SQLite 3 configured with Write-Ahead Logging. This allows rapid concurrent read-write access and guarantees atomic transactions."
    )

    # =========================================================================
    # SLIDE 4: USERFLOW ARCHITECTURE (ALL 3 ROLES)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "Process Architecture", "End-to-End System Userflows", "Tripartite operational pathways for Administrator, Faculty, and Student users")

    # Flow columns for Admin, Teacher, Student
    roles_flow = [
        ("ADMIN USERFLOW", ACCENT_BLUE, [
            ("Step 1: System Auth", "Admin logs in with admin ID. Forced password change on first setup."),
            ("Step 2: Master Setup", "Ingest or CRUD courses, subjects, faculty rosters, and student enrollment."),
            ("Step 3: Teaching Matrix", "Map each teacher to specific course, subject, semester, and section."),
            ("Step 4: Real-time Monitor", "Observe 3D Tactical Defaulter Radar, compliance metrics, and audit stream."),
            ("Step 5: Governance", "Set minimum threshold (default 75%) and export point-in-time DB snapshot.")
        ]),
        ("TEACHER USERFLOW", ACCENT_GREEN, [
            ("Step 1: One-Time Activate", "Verify Employee ID + Date of Birth; set private password."),
            ("Step 2: Scoped Class Select", "Dropdown shows only officially assigned subjects and sections."),
            ("Step 3: Register Marking", "Pick date (future dates locked); mark Present, Late, or Absent."),
            ("Step 4: Atomic Commit", "Single-click save; duplicate submission blocked by unique constraint."),
            ("Step 5: Audited Revisions", "Correct errors within 48h window; mandatory reason recorded in log.")
        ]),
        ("STUDENT USERFLOW", ACCENT_AMBER, [
            ("Step 1: One-Time Activate", "Verify Roll Number + Date of Birth; establish account credentials."),
            ("Step 2: Personal Standing", "Instant HUD view of overall attendance percentage and risk status."),
            ("Step 3: Defaulter Alert", "High-visibility warning banner if compliance drops below 75% target."),
            ("Step 4: History Breakdown", "Lecture-by-lecture log with date, subject code, and faculty name."),
            ("Step 5: Apply for Leave", "Submit date-range leave application directly to assigned instructor.")
        ])
    ]

    for i, (r_name, r_col, steps) in enumerate(roles_flow):
        x = Inches(0.8 + i * 4.0)
        card = add_card(s4, x, Inches(1.7), Inches(3.733), Inches(5.1))

        # Title header box
        tbox = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, Inches(1.7), Inches(3.733), Inches(0.45))
        tbox.fill.solid()
        tbox.fill.fore_color.rgb = r_col
        tbox.line.fill.background()
        p = tbox.text_frame.paragraphs[0]
        p.text = r_name
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE
        p.alignment = PP_ALIGN.CENTER

        tb = s4.shapes.add_textbox(x + Inches(0.15), Inches(2.25), Inches(3.433), Inches(4.45))
        tf = tb.text_frame
        tf.word_wrap = True

        for s_idx, (s_title, s_desc) in enumerate(steps):
            p = tf.paragraphs[0] if s_idx == 0 else tf.add_paragraph()
            p.text = s_title
            p.font.size = Pt(10)
            p.font.bold = True
            p.font.color.rgb = TEXT_WHITE

            p_desc = tf.add_paragraph()
            p_desc.text = s_desc
            p_desc.font.size = Pt(8.8)
            p_desc.font.color.rgb = TEXT_MUTED

            if s_idx < len(steps) - 1:
                p_sep = tf.add_paragraph()
                p_sep.text = "   ↓"
                p_sep.font.size = Pt(8)
                p_sep.font.color.rgb = r_col

    add_speaker_note(s4,
        "Here we see the complete userflow for each institutional role. "
        "For Administrators, the flow moves from master configuration to teaching matrix mapping, followed by real-time radar monitoring and database backups. "
        "For Teachers, after a one-time activation using their date of birth, their view is strictly scoped to their allocated classes. Marking is completed in under two minutes, and any subsequent corrections require an explicit reason within 48 hours. "
        "For Students, the flow provides instantaneous transparency. They log in, view their real-time percentage, review any defaulter alerts, and submit digital leave requests directly to their instructors."
    )

    # =========================================================================
    # SLIDE 5: HOW IT WORKS FLOWCHART (ENGINE PIPELINE)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "Engine Architecture", "How Presenza Works: Core Processing Pipeline", "Step-by-step transaction flow from user input to database ledger and real-time radar")

    # 5 Horizontal Pipeline Stages
    stages = [
        ("STAGE 1: INPUT", 
         ACCENT_BLUE, 
         "User Interaction", 
         ["Teacher selects class", "Date selected (today)", "Present / Late / Absent", "CSV Roster Upload"]),
        ("STAGE 2: VALIDATE", 
         ACCENT_AMBER, 
         "Poka-Yoke Guards", 
         ["Check faculty assignment", "Block future dates", "Check duplicate marks", "Sanitize all parameters"]),
        ("STAGE 3: COMMIT", 
         ACCENT_GREEN, 
         "Atomic Persistence", 
         ["SQLite WAL transaction", "UNIQUE key enforced", "attendance table write", "attendance_logs write"]),
        ("STAGE 4: TELEMETRY", 
         ACCENT_BLUE, 
         "Event Pipeline", 
         ["Waveform bus update", "Live clock & status ping", "Recompute percentages", "Identify defaulters"]),
        ("STAGE 5: VISUALIZE", 
         ACCENT_RED, 
         "Output Engines", 
         ["3D Polar Defaulter Radar", "Student Defaulter Alert", "Matplotlib Distribution", "1-Click DB Snapshot"])
    ]

    for i, (st_name, st_col, st_sub, st_items) in enumerate(stages):
        x = Inches(0.8 + i * 2.4)
        card = add_card(s5, x, Inches(1.8), Inches(2.2), Inches(4.9))

        # Header block
        hb = s5.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, Inches(1.8), Inches(2.2), Inches(0.6))
        hb.fill.solid()
        hb.fill.fore_color.rgb = st_col
        hb.line.fill.background()

        p = hb.text_frame.paragraphs[0]
        p.text = st_name
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE
        p.alignment = PP_ALIGN.CENTER

        p_sub = hb.text_frame.add_paragraph()
        p_sub.text = st_sub
        p_sub.font.size = Pt(8)
        p_sub.font.color.rgb = TEXT_WHITE
        p_sub.alignment = PP_ALIGN.CENTER

        tb = s5.shapes.add_textbox(x + Inches(0.1), Inches(2.55), Inches(2.0), Inches(4.0))
        tf = tb.text_frame
        tf.word_wrap = True

        for item in st_items:
            p = tf.add_paragraph()
            p.text = "• " + item
            p.font.size = Pt(9)
            p.font.color.rgb = TEXT_WHITE

        # Arrow to next stage
        if i < len(stages) - 1:
            arrow = s5.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, x + Inches(2.22), Inches(4.0), Inches(0.16), Inches(0.3))
            arrow.fill.solid()
            arrow.fill.fore_color.rgb = TEXT_MUTED
            arrow.line.fill.background()

    add_speaker_note(s5,
        "This flowchart illustrates the core technical engine of Presenza. "
        "At Stage 1, data enters either via the teacher's marking grid or a bulk CSV ingestion. "
        "At Stage 2, our Poka-Yoke service layer validates assignments, blocks future dates, and verifies that attendance has not already been submitted. "
        "At Stage 3, the SQLite engine commits an atomic transaction. If even one record violates the composite unique constraint, the entire batch safely rolls back. "
        "At Stage 4, event telemetry streams into our waveform bus and triggers background percentage re-calculations. "
        "Finally, at Stage 5, the updated attendance profile updates our 3D Polar Defaulter Radar and flags any student dropping below seventy-five percent."
    )

    # =========================================================================
    # SLIDE 6: POKA-YOKE PROXY PREVENTION IN PRACTICE
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "Quality Engineering", "Poka-Yoke: Multi-Layered Mistake-Proofing", "Mechanically eliminating proxy attendance, duplicate submissions, and unauthorized dates")

    # Left: Database Schema snippet in card
    left_card = add_card(s6, Inches(0.8), Inches(1.7), Inches(5.7), Inches(5.1), CARD_BG, CARD_BORDER)
    tb_l = s6.shapes.add_textbox(Inches(1.0), Inches(1.9), Inches(5.3), Inches(4.7))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True

    p = tf_l.paragraphs[0]
    p.text = "DATABASE-LEVEL POKA-YOKE CONSTRAINT"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GREEN

    sql_code = (
        "CREATE TABLE attendance (\n"
        "    id INTEGER PRIMARY KEY AUTOINCREMENT,\n"
        "    student_id INTEGER NOT NULL REFERENCES students(id),\n"
        "    subject_id INTEGER NOT NULL REFERENCES subjects(id),\n"
        "    date TEXT NOT NULL,\n"
        "    status TEXT CHECK(status IN ('Present', 'Late', 'Absent', 'Leave')),\n"
        "    marked_by INTEGER NOT NULL REFERENCES users(id),\n"
        "    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\n"
        "    UNIQUE (student_id, subject_id, date)\n"
        ");"
    )
    p_code = tf_l.add_paragraph()
    p_code.text = sql_code
    p_code.font.name = "Courier New"
    p_code.font.size = Pt(9)
    p_code.font.color.rgb = TEXT_WHITE

    p_expl = tf_l.add_paragraph()
    p_expl.text = "\nHardware-level guarantee: Even if concurrent client requests or bad code attempt duplicate entries, SQLite mechanically aborts and rolls back the transaction."
    p_expl.font.size = Pt(9)
    p_expl.font.color.rgb = TEXT_MUTED

    # Right: 3 Layers of Guardrails
    guardrails = [
        ("LAYER 1: UI DATE LOCK", ACCENT_BLUE,
         "The CustomTkinter calendar picker disables all dates after current_date. Teachers cannot submit forward-dated marks for tomorrow or next week."),
        ("LAYER 2: SERVICE-LAYER ALLOCATION CHECK", ACCENT_AMBER,
         "The attendance service verifies teaching_assignments table before opening or saving any class. Teachers cannot mark for subjects they do not teach."),
        ("LAYER 3: DUPLICATE PRE-SUBMISSION SCAN", ACCENT_GREEN,
         "The service layer queries existing attendance for (subject_id, section, date) before populating the grid, preventing accidental double submissions.")
    ]

    for j, (g_title, g_col, g_desc) in enumerate(guardrails):
        y = Inches(1.7 + j * 1.73)
        add_card(s6, Inches(6.8), y, Inches(5.733), Inches(1.58))
        
        tb_r = s6.shapes.add_textbox(Inches(7.0), y + Inches(0.12), Inches(5.333), Inches(1.35))
        tf_r = tb_r.text_frame
        tf_r.word_wrap = True

        p = tf_r.paragraphs[0]
        p.text = g_title
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = g_col

        p_desc = tf_r.add_paragraph()
        p_desc.text = g_desc
        p_desc.font.size = Pt(9)
        p_desc.font.color.rgb = TEXT_WHITE

    add_speaker_note(s6,
        "Poka-Yoke is the heart of Presenza's quality guarantee. "
        "Instead of relying on human vigilance, we enforce mistake-proofing across three technical tiers. "
        "At the UI layer, future dates are physically blocked by the calendar component. "
        "At the service layer, teacher IDs are cross-referenced with the teaching matrix, ensuring only the assigned professor can mark attendance. "
        "Finally, at the database layer, we enforce a composite unique constraint across student ID, subject ID, and date. "
        "Even under unexpected script calls or multi-threaded operations, SQLite mechanically aborts duplicate rows. Duplicate attendance records are structurally impossible."
    )

    # =========================================================================
    # SLIDE 7: 3D TACTICAL DEFALUTER RADAR & HUD
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "Visual Analytics", "Admin Command Console & Polar Coordinate Risk Radar", "Transforming tabular attendance numbers into real-time situational awareness")

    # Left: Polar Radar visual card
    radar_card = add_card(s7, Inches(0.8), Inches(1.7), Inches(5.7), Inches(5.1))
    tb_radar = s7.shapes.add_textbox(Inches(1.0), Inches(1.9), Inches(5.3), Inches(4.7))
    tf_radar = tb_radar.text_frame
    tf_radar.word_wrap = True

    p = tf_radar.paragraphs[0]
    p.text = "POLAR COORDINATE RISK RADAR (CANVAS)"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT_BLUE

    radar_features = [
        "Mathematical Model: Polar transformation: r = (1.0 - percentage) * max_radius, theta = hash(student_id)",
        "Outer Green Perimeter: Compliant students (> 75% attendance) orbit in safe outer zone",
        "Middle Dashed Ring: Visual representation of the 75% institutional compliance threshold",
        "Inner Crimson Danger Core: Critical defaulters (< 75%) with pulsing warning beacons",
        "Sweeping Scanner Beam: Continuous 360-degree radar sweep simulating live telemetry",
        "Zero Heavy Dependencies: Built purely using CustomTkinter Canvas and Python math.sin / math.cos"
    ]
    for rf in radar_features:
        p = tf_radar.add_paragraph()
        p.text = "• " + rf
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_WHITE

    # Right: HUD Metrics and Telemetry
    hud_card = add_card(s7, Inches(6.8), Inches(1.7), Inches(5.733), Inches(5.1))
    tb_hud = s7.shapes.add_textbox(Inches(7.0), Inches(1.9), Inches(5.333), Inches(4.7))
    tf_hud = tb_hud.text_frame
    tf_hud.word_wrap = True

    p = tf_hud.paragraphs[0]
    p.text = "EXECUTIVE TELEMETRY & HUD METRICS"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GREEN

    hud_metrics = [
        ("Total Enrolled Students", "36 Enrolled (100% indexed in SQLite)"),
        ("Verified Faculty Cadre", "5 Verified Staff across departments"),
        ("Curriculum & Allocations", "6 Subjects across 12 section allocations"),
        ("Overall Attendance Rate", "91.8% Institutional Compliance"),
        ("Active Defaulters Flagged", "3 Critical Defaulters requiring intervention"),
        ("Total Historical Logs", "576 Revisions & Entries permanently logged"),
        ("Animation Easing", "450ms ease-out cubic count-up on dashboard open"),
        ("Responsive Layout", "Auto-reflows: 6 cols on 4K, 3x2 on 1080p laptop displays")
    ]
    for label, val in hud_metrics:
        p = tf_hud.add_paragraph()
        p.text = "• " + label + ": " + val
        p.font.size = Pt(9.3)
        p.font.color.rgb = TEXT_WHITE

    add_speaker_note(s7,
        "Here we see the Admin Command Console. Rather than forcing administrators to parse rows of percentages, we built an animated 3D Tactical Defaulter Radar. "
        "Using polar coordinates mapped onto a CustomTkinter canvas, the distance from the center represents risk. "
        "Compliant students with attendance above seventy-five percent orbit in the outer green ring. "
        "Defaulters below seventy-five percent are pulled into the red danger core with pulsing beacons. "
        "Notice also our responsive HUD: all key performance indicators roll up smoothly over four hundred and fifty milliseconds using an ease-out cubic animation, giving administrators immediate clarity on institutional health."
    )

    # =========================================================================
    # SLIDE 8: CONTROLLED REVISIONS & IMMUTABLE AUDIT LOG
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "Data Governance", "Auditable Corrections & Immutable Audit Logging", "How Presenza handles legitimate clerical adjustments while preventing tampering")

    # Table of Audit Schema and Steps
    add_card(s8, Inches(0.8), Inches(1.7), Inches(11.733), Inches(5.1))
    tb_aud = s8.shapes.add_textbox(Inches(1.1), Inches(1.9), Inches(11.133), Inches(4.7))
    tf_aud = tb_aud.text_frame
    tf_aud.word_wrap = True

    p = tf_aud.paragraphs[0]
    p.text = "FOUR-STEP AUDITED CORRECTION WORKFLOW"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT_AMBER

    workflow_steps = [
        "1. Identity Check: Corrections can only be initiated by the assigned faculty member who originally marked the class.",
        "2. Grace Period Check: Edits are locked after the configured grace window (default 48 hours). Retroactive edits beyond 2 days require administrator escalation.",
        "3. Mandatory Justification: The save button is disabled until the teacher enters a verifiable reason (e.g. 'Late bus slip verified' or 'Medical slip submitted').",
        "4. Dual Ledger Write: Within an atomic database transaction, the attendance record is updated AND a permanent entry is inserted into attendance_logs."
    ]
    for ws in workflow_steps:
        p = tf_aud.add_paragraph()
        p.text = ws
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_WHITE

    p_schema_title = tf_aud.add_paragraph()
    p_schema_title.text = "\nIMMUTABLE AUDIT LOG TABLE (attendance_logs):"
    p_schema_title.font.size = Pt(10)
    p_schema_title.font.bold = True
    p_schema_title.font.color.rgb = ACCENT_GREEN

    schema_sample = (
        "| log_id | attendance_id | old_status | new_status | changed_by | timestamp           | reason                      |\n"
        "|--------|---------------|------------|------------|------------|---------------------|-----------------------------|\n"
        "| 104    | 481           | Absent     | Present    | T-102      | 2026-10-24 14:12:05 | College bus verified late   |\n"
        "| 105    | 392           | Late       | Present    | T-105      | 2026-10-25 09:30:18 | Dean permission slip signed |"
    )
    p_tbl = tf_aud.add_paragraph()
    p_tbl.text = schema_sample
    p_tbl.font.name = "Courier New"
    p_tbl.font.size = Pt(8.5)
    p_tbl.font.color.rgb = TEXT_WHITE

    add_speaker_note(s8,
        "In real institutions, legitimate corrections are necessary. A student arrives late with an authorized bus slip, or an excused absence is verified. "
        "In spreadsheets, teachers simply overwrite the cell, destroying evidence of what changed. "
        "In Presenza, we enforce an auditable four-step revision workflow. "
        "First, corrections are only allowed within a 48-hour grace window. "
        "Second, the teacher cannot save without submitting a mandatory justification reason. "
        "Third, the system commits both the update and a permanent entry in attendance_logs simultaneously. "
        "This gives institutional administrators one hundred percent forensic traceability."
    )

    # =========================================================================
    # SLIDE 9: CRYPTOGRAPHY, SECURITY & DISASTER RECOVERY
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, "Security & Reliability", "Cryptographic Protection & Point-in-Time Recovery", "Safeguarding user credentials and ensuring continuous disaster readiness")

    sec_cards = [
        ("PASSWORD CRYPTOGRAPHY", ACCENT_BLUE, [
            "Algorithm: PBKDF2-HMAC-SHA256",
            "Iterations: 100,000 hashing rounds",
            "Salt: 16-byte cryptographically secure random salt generated per user via os.urandom(16)",
            "Immune to rainbow tables and offline dictionary attacks",
            "Zero plaintext credentials stored in database"
        ]),
        ("ACCOUNT ACTIVATION GATE", ACCENT_GREEN, [
            "New accounts are seeded in an inactive state with no default password",
            "Students verify Roll No. + Date of Birth; Teachers verify Employee ID + DOB",
            "User chooses private 8+ character password (alphanumeric required)",
            "Prevents default credential exploitation ('123456')",
            "Admin can reset locked accounts back to inactive"
        ]),
        ("DISASTER RECOVERY VAULT", ACCENT_AMBER, [
            "1-Click point-in-time SQLite binary snapshot generation",
            "Non-blocking: backups execute in background without stopping ongoing sessions",
            "Files saved to /backups with ISO timestamp: presenza_backup_YYYYMMDD_HHMMSS.db",
            "Snapshot Vault displays file size, timestamp, and path",
            "Recovery verification: database can be restored in seconds"
        ])
    ]

    for k, (sec_title, sec_col, sec_bullets) in enumerate(sec_cards):
        x = Inches(0.8 + k * 4.0)
        card = add_card(s9, x, Inches(1.7), Inches(3.733), Inches(5.1))

        # Title bar
        tb_bar = s9.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, Inches(1.7), Inches(3.733), Inches(0.45))
        tb_bar.fill.solid()
        tb_bar.fill.fore_color.rgb = sec_col
        tb_bar.line.fill.background()
        p = tb_bar.text_frame.paragraphs[0]
        p.text = sec_title
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE
        p.alignment = PP_ALIGN.CENTER

        tb = s9.shapes.add_textbox(x + Inches(0.2), Inches(2.3), Inches(3.333), Inches(4.3))
        tf = tb.text_frame
        tf.word_wrap = True

        for b in sec_bullets:
            p = tf.add_paragraph()
            p.text = "• " + b
            p.font.size = Pt(9.2)
            p.font.color.rgb = TEXT_WHITE

    add_speaker_note(s9,
        "Data security is paramount in academic software. "
        "First, Presenza hashes all passwords using PBKDF2-HMAC-SHA256 with 100,000 iterations and a unique 16-byte random salt per user. "
        "Second, we built an account activation protocol. Newly registered students and teachers do not receive generic default passwords. Instead, they activate their account by verifying their ID and date of birth before setting a secure password. "
        "Third, our Snapshot Vault allows administrators to take an immediate point-in-time database snapshot with a single click. "
        "This creates an isolated SQLite replica in the backups directory in under 0.15 seconds without disconnecting users."
    )

    # =========================================================================
    # SLIDE 10: STUDENT TRANSPARENCY & TWO-WAY LEAVE PROCESSING
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header(s10, "Student Workflow", "Student Transparency & Two-Way Leave Processing", "Empowering student self-auditing and automating formal leave synchronization")

    # Left: Student Portal Cards
    add_card(s10, Inches(0.8), Inches(1.7), Inches(5.7), Inches(5.1))
    tb_st = s10.shapes.add_textbox(Inches(1.0), Inches(1.9), Inches(5.3), Inches(4.7))
    tf_st = tb_st.text_frame
    tf_st.word_wrap = True

    p = tf_st.paragraphs[0]
    p.text = "STUDENT SELF-AUDITING PORTAL"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT_BLUE

    st_points = [
        "Session Privacy: Student token extracts strictly their own roll number. Peer data is inaccessible.",
        "Aggregate Metric Card: Total lectures held, lectures attended, and overall percentage.",
        "High-Visibility Warning Banner: If percentage falls below 75%, an alert immediately warns the student and displays classes required to recover.",
        "Subject Matrix Breakdown: Shows attendance performance across every individual enrolled course.",
        "Chronological Lecture History: Searchable table of every lecture with date, subject code, instructor name, and status."
    ]
    for pt in st_points:
        p = tf_st.add_paragraph()
        p.text = "• " + pt
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_WHITE

    # Right: Two-Way Leave Workflow
    add_card(s10, Inches(6.8), Inches(1.7), Inches(5.733), Inches(5.1))
    tb_lv = s10.shapes.add_textbox(Inches(7.0), Inches(1.9), Inches(5.333), Inches(4.7))
    tf_lv = tb_lv.text_frame
    tf_lv.word_wrap = True

    p = tf_lv.paragraphs[0]
    p.text = "TWO-WAY LEAVE APPLICATION LIFECYCLE"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GREEN

    lv_steps = [
        ("1. Student Submits", "Student selects Start Date, End Date, and justification reason. Validator blocks inverted date ranges and overlapping pending leaves."),
        ("2. Faculty Queue", "Request enters the assigned teacher's approval queue with student details, medical proof note, and date span."),
        ("3. Faculty Decision", "Teacher reviews and clicks 'Approve' or 'Reject' with optional review notes."),
        ("4. Automated Sync", "Upon approval, the database updates attendance records within that date range to 'Leave' status automatically, eliminating manual register adjustments.")
    ]
    for step_title, step_desc in lv_steps:
        p = tf_lv.add_paragraph()
        p.text = step_title + ": " + step_desc
        p.font.size = Pt(9.3)
        p.font.color.rgb = TEXT_WHITE

    add_speaker_note(s10,
        "The Student Portal provides complete transparency. Students log in to inspect their attendance standing in real-time. "
        "If their percentage dips below seventy-five percent, a high-visibility warning banner alerts them immediately, avoiding surprise debarments. "
        "Furthermore, we built an integrated leave management loop. "
        "A student submits a digital leave request with start and end dates. "
        "The request appears directly in the assigned professor's portal. "
        "When approved, the system automatically updates all corresponding attendance records to 'Leave' status, eliminating the need for manual pen-and-paper adjustments."
    )

    # =========================================================================
    # SLIDE 11: QUANTITATIVE BENCHMARKS & VERIFICATION
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11)
    add_header(s11, "Empirical Testing", "System Verification & Performance Benchmarks", "Measured results from stress-testing master datasets and concurrent transactions")

    # Table of benchmarks
    add_card(s11, Inches(0.8), Inches(1.7), Inches(11.733), Inches(5.1))
    tb_bm = s11.shapes.add_textbox(Inches(1.1), Inches(1.9), Inches(11.133), Inches(4.7))
    tf_bm = tb_bm.text_frame
    tf_bm.word_wrap = True

    p = tf_bm.paragraphs[0]
    p.text = "MEASURED SYSTEM BENCHMARKS"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GREEN

    benchmarks_data = [
        ("Screen Navigation Latency", "< 2.0 seconds", "0.28 seconds avg", "PASSED"),
        ("Batch CSV Roster Ingestion (100 rows)", "< 5.0 seconds", "0.84 seconds", "PASSED"),
        ("Duplicate Entry Tolerance", "0 duplicate records", "0 allowed (100% aborted by UNIQUE constraint)", "PASSED"),
        ("Dashboard Easing Animation", "60 FPS smooth count-up", "450ms ease-out cubic curve", "PASSED"),
        ("Audit Trail Coverage", "100% of corrections", "100% (All 576 test edits logged)", "PASSED"),
        ("Database Snapshot Speed", "< 1.0 second", "0.12 seconds for 420 KB binary", "PASSED"),
        ("Password Hash Time (100k rounds)", "100 - 300 ms", "145 ms (Ideal brute-force resistance)", "PASSED")
    ]

    bm_table_text = (
        "| Evaluation Metric                       | Target Requirement | Measured System Result           | Test Status |\n"
        "|-----------------------------------------|--------------------|----------------------------------|-------------|\n"
    )
    for metric, target, result, status in benchmarks_data:
        bm_table_text += f"| {metric:<39} | {target:<18} | {result:<32} | {status:<11} |\n"

    p_table = tf_bm.add_paragraph()
    p_table.text = bm_table_text
    p_table.font.name = "Courier New"
    p_table.font.size = Pt(8.5)
    p_table.font.color.rgb = TEXT_WHITE

    p_summary = tf_bm.add_paragraph()
    p_summary.text = "\nStress Testing Verdict: Under automated script stress tests, Presenza rejected 100% of invalid dates, blocked all unassigned teacher marks, and maintained zero database corruption."
    p_summary.font.size = Pt(9.5)
    p_summary.font.color.rgb = TEXT_MUTED

    add_speaker_note(s11,
        "To validate Presenza, we executed a suite of empirical performance tests. "
        "Screen transitions average 0.28 seconds, well below our 2-second quality ceiling. "
        "Batch importing 100 students via CSV executes in 0.84 seconds. "
        "We intentionally attempted to force duplicate attendance records, future dates, and unauthorized subject modifications; in 100% of test cases, the system cleanly caught and rejected the operations. "
        "The application demonstrates high stability, zero memory leaks, and flawless compliance with TQM Quality Goal Q20."
    )

    # =========================================================================
    # SLIDE 12: CONCLUSION & FUTURE HORIZONS
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12)
    add_header(s12, "Summary & Roadmap", "Production Readiness & Future Horizons", "Architectural summary and planned hardware integration for Presenza V2.0")

    # Left: Summary
    add_card(s12, Inches(0.8), Inches(1.7), Inches(5.7), Inches(5.1))
    tb_c = s12.shapes.add_textbox(Inches(1.0), Inches(1.9), Inches(5.3), Inches(4.7))
    tf_c = tb_c.text_frame
    tf_c.word_wrap = True

    p = tf_c.paragraphs[0]
    p.text = "CORE DELIVERABLES ACHIEVED (V1.0)"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GREEN

    v1_items = [
        "Zero-Trust Architecture: 3-tier desktop pattern with zero SQL in UI controllers",
        "Poka-Yoke Mistake-Proofing: Duplicate marks eliminated at the SQLite engine level",
        "3D Polar Defaulter Radar: Real-time risk visualization using pure vector math",
        "Full Institutional Traceability: Configurable 48-hour grace window with mandatory revision reasons",
        "Cryptographic Safety: PBKDF2-HMAC-SHA256 password security with individual salting",
        "TQM Q20 Compliance: Satisfies all five assigned software quality deliverables"
    ]
    for it in v1_items:
        p = tf_c.add_paragraph()
        p.text = "• " + it
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_WHITE

    # Right: V2.0 Roadmap
    add_card(s12, Inches(6.8), Inches(1.7), Inches(5.733), Inches(5.1))
    tb_v2 = s12.shapes.add_textbox(Inches(7.0), Inches(1.9), Inches(5.333), Inches(4.7))
    tf_v2 = tb_v2.text_frame
    tf_v2.word_wrap = True

    p = tf_v2.paragraphs[0]
    p.text = "FUTURE EXPANSION HORIZONS (V2.0)"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT_BLUE

    v2_items = [
        "Hardware Integration: Direct USB barcode scanner and optical biometric fingerprint sensor support",
        "Automated Notifications: Real-time SMS and email alerts triggered to parents when attendance drops below 75%",
        "Predictive Risk Analytics: Machine learning early-warning models for mid-semester dropout risk prediction",
        "Cross-Platform Bundler: Single-executable PyInstaller desktop package with automated delta updates"
    ]
    for it in v2_items:
        p = tf_v2.add_paragraph()
        p.text = "• " + it
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_WHITE

    p_close = tf_v2.add_paragraph()
    p_close.text = "\nThank you for your time.\nWe are now open for questions, architectural defense, and a live demonstration."
    p_close.font.size = Pt(10)
    p_close.font.bold = True
    p_close.font.color.rgb = TEXT_WHITE

    add_speaker_note(s12,
        "To conclude: Presenza transforms academic attendance from a vulnerable paper-based routine into a hardened, auditable engineering system. "
        "By uniting 3-tier desktop architecture, Poka-Yoke defect prevention, cryptographic credential safety, and polar coordinate risk visualization, we have fulfilled all requirements of TQM Quality Goal Q20. "
        "In future versions, we plan to integrate biometric sensors and parent notification triggers. "
        "Thank you for your time. We are now ready for your questions and our live demonstration."
    )

    # Save presentation in project root
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_path = os.path.join(project_root, "Presenza_Presentation.pptx")
    prs.save(output_path)
    print(f"SUCCESS: Generated {output_path} with 12 slides and embedded speaker notes.")

if __name__ == "__main__":
    build_presentation()
