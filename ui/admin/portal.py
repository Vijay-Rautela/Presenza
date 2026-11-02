"""Futuristic Command Center - Presenza Admin Portal.

Styled in Presenza's signature Forest Green and Warm Beige palette.
Equipped with 3D perspective tactical radar, live telemetry waveform,
animated metric tickers, smooth spectrum expansion, breathing beacons,
and complete administrative master data operations.
"""

from datetime import datetime
import math
import os
from pathlib import Path
import time
import tkinter as tk
from tkinter import filedialog, ttk

import customtkinter as ctk

from config import BACKUP_DIR, COLORS, DATABASE_PATH
from services import admin_service
from services.import_service import import_file


# Presenza Forest Green & Warm Beige Architectural Palette
_THEME = {
    # Base background (Warm Cream / Beige)
    "bg_base": "#F7F5EA",
    "bg_alt": "#ECE8DC",

    # Sidebar (Deep Forest Green)
    "sidebar": "#0D2E1F",
    "sidebar_hover": "#174D34",
    "sidebar_active": "#1B874B",
    "sidebar_text": "#F4FAF6",
    "sidebar_muted": "#8EA696",
    "sidebar_border": "#16432D",

    # Cards & Containers (Beige & Warm Surface)
    "card": "#FFFFFF",
    "card_alt": "#F8F6F2",
    "card_border": "#D5E2D9",
    "card_border_glow": "#1B874B",
    "card_highlight": "#FAF8F5",

    # Tactical Monitor Sub-Panels (for Radar & Oscilloscope Screen)
    # Deep tactical olive/forest cockpit screen
    "monitor_bg": "#0B2418",
    "monitor_border": "#16432D",
    "monitor_grid": "#123523",
    "monitor_accent": "#22C55E",

    # Primary Forest Greens
    "primary": "#1B874B",
    "primary_dark": "#136A3B",
    "primary_light": "#22C55E",
    "primary_dim": "#E8F5EE",

    # Semantic Status Accents
    "emerald": "#1B874B",         # Present / Optimal
    "emerald_light": "#22C55E",   # Radar sweep line / wave
    "emerald_dim": "#E8F5EE",     # Badge background
    "emerald_border": "#A3DBB7",

    "amber": "#C77612",           # Late / Attention
    "amber_dim": "#FEF5E7",
    "amber_border": "#F3CE9B",

    "crimson": "#DC3545",         # Defaulter / Danger
    "crimson_dim": "#FDF0ED",
    "crimson_border": "#EEA9A1",

    "sand": "#D5CCA6",            # Sand tone
    "cove": "#D4DFD7",            # Neutral cove

    # Typography
    "text_dark": "#11261B",       # Deep Forest / Black
    "text_body": "#2D3F34",       # Primary readable body
    "text_muted": "#5A7263",      # Subtitles / labels
    "text_dim": "#9AA496",        # Dividers
    "text_white": "#FFFFFF",

    # Inputs
    "input_bg": "#FFFFFF",
    "input_border": "#D5E2D9",
    "input_focus": "#1B874B",
}

RECORD_CONFIG = {
    "Students": {
        "columns": [
            ("id", "ID", 50),
            ("roll_no", "Roll Number", 110),
            ("name", "Student Name", 160),
            ("course", "Course", 110),
            ("semester", "Sem", 50),
            ("section", "Sec", 50),
            ("email", "Email", 170),
            ("dob", "DOB", 95),
            ("is_active", "Active", 60),
        ],
        "fields": [
            ("roll_no", "Roll Number"),
            ("name", "Full Name"),
            ("dob", "Date of Birth (YYYY-MM-DD)"),
            ("course_id", "Course Program"),
            ("semester", "Semester (1-8)"),
            ("section", "Section (A, B, C...)"),
            ("email", "Institutional Email"),
        ],
        "list": admin_service.list_students,
        "save": admin_service.save_student,
        "delete": admin_service.delete_student,
    },
    "Teachers": {
        "columns": [
            ("id", "ID", 50),
            ("emp_id", "Employee ID", 110),
            ("name", "Faculty Name", 160),
            ("department", "Department", 140),
            ("email", "Email", 180),
            ("dob", "DOB", 95),
            ("is_active", "Active", 60),
        ],
        "fields": [
            ("emp_id", "Employee ID"),
            ("name", "Faculty Name"),
            ("dob", "Date of Birth (YYYY-MM-DD)"),
            ("department", "Department"),
            ("email", "Institutional Email"),
        ],
        "list": admin_service.list_teachers,
        "save": admin_service.save_teacher,
        "delete": admin_service.delete_teacher,
    },
    "Courses": {
        "columns": [
            ("id", "ID", 60),
            ("name", "Course Title", 240),
            ("duration_years", "Duration (Years)", 120),
        ],
        "fields": [
            ("name", "Course Name"),
            ("duration_years", "Duration in Years"),
        ],
        "list": admin_service.list_courses,
        "save": admin_service.save_course,
        "delete": admin_service.delete_course,
    },
    "Subjects": {
        "columns": [
            ("id", "ID", 60),
            ("code", "Code", 90),
            ("name", "Subject Title", 200),
            ("course", "Course", 120),
            ("semester", "Semester", 80),
        ],
        "fields": [
            ("code", "Subject Code"),
            ("name", "Subject Name"),
            ("course_id", "Course Program"),
            ("semester", "Semester"),
        ],
        "list": admin_service.list_subjects,
        "save": admin_service.save_subject,
        "delete": admin_service.delete_subject,
    },
}

_NAV_MENU = [
    ("// OPERATIONS", [
        ("Dashboard", "◈", "Operations telemetry and KPI radar"),
        ("Students", "⬢", "Student records and enrollment"),
        ("Teachers", "⬡", "Faculty roster and credentials"),
        ("Courses", "⊞", "Academic degree programs"),
        ("Subjects", "⎈", "Course curriculum catalog"),
        ("Assignments", "⚡", "Faculty subject allocations"),
    ]),
    ("// INTELLIGENCE & DATA", [
        ("Import", "↑", "Batch CSV and Excel ingest"),
        ("Audit Logs", "⟁", "Security and attendance logs"),
        ("Reports", "☷", "Attendance analytics and export"),
    ]),
    ("// SYSTEM", [
        ("Backup", "💾", "SQLite database snapshots"),
        ("Settings", "⚙", "Thresholds and compliance policy"),
    ]),
]


# ======================================================================
# MOTION GRAPHIC 1: 3D Perspective Tactical Radar Widget (Cockpit Screen)
# ======================================================================
class TacticalRadarCanvas(tk.Canvas):
    """Real-time animated 3D perspective radar sweep with plotted student risk blips."""

    def __init__(self, master, defaulters=None, **kwargs):
        super().__init__(master, bg=_THEME["monitor_bg"], highlightthickness=0, **kwargs)
        self.angle = 0
        self.defaulters = defaulters or []
        self._animating = True
        self.cx = 115
        self.cy = 95
        self.rx = 85
        self.ry = 55
        self.pulse_phase = 0.0
        self._schedule_sweep()

    def update_defaulters(self, defaulters):
        self.defaulters = defaulters

    def _schedule_sweep(self):
        if not self.winfo_exists() or not self._animating:
            return
        self._draw_frame()
        self.after(35, self._schedule_sweep)

    def _draw_frame(self):
        self.delete("all")
        w = self.winfo_width()
        h = self.winfo_height()
        if w > 20 and h > 20:
            self.cx = w / 2.0
            self.cy = h / 2.0
            self.rx = min(w * 0.42, 85)
            self.ry = min(h * 0.32, 55)

        self.angle = (self.angle + 3.5) % 360
        self.pulse_phase += 0.15

        # 1. Perspective Grid & Range Ellipses
        # Outer Ring (100% boundary)
        self.create_oval(self.cx - self.rx, self.cy - self.ry, self.cx + self.rx, self.cy + self.ry, outline="#243422", width=1)
        # Middle Ring (75% threshold ring)
        r75_x, r75_y = self.rx * 0.75, self.ry * 0.75
        self.create_oval(self.cx - r75_x, self.cy - r75_y, self.cx + r75_x, self.cy + r75_y, outline="#334B30", width=1)
        # Core Danger Ring (35% ring)
        r35_x, r35_y = self.rx * 0.35, self.ry * 0.35
        self.create_oval(self.cx - r35_x, self.cy - r35_y, self.cx + r35_x, self.cy + r35_y, outline="#4A2622", width=1)

        # Crosshairs
        self.create_line(self.cx - self.rx, self.cy, self.cx + self.rx, self.cy, fill="#1F2E1E", width=1)
        self.create_line(self.cx, self.cy - self.ry, self.cx, self.cy + self.ry, fill="#1F2E1E", width=1)

        # 2. Sweep Trail (Fading phosphor sectors in forest sage)
        for offset, color, width in [(12, "#1E3320", 1), (6, "#2B4C2E", 1.5), (0, _THEME["emerald_light"], 2)]:
            trail_angle = (self.angle - offset) % 360
            rad = math.radians(trail_angle)
            sx = self.cx + self.rx * math.cos(rad)
            sy = self.cy + self.ry * math.sin(rad)
            self.create_line(self.cx, self.cy, sx, sy, fill=color, width=width)

        # 3. Outer Compliant Blips (Emerald markers plotted around outer rings)
        compliant_blips = [(35, 0.88), (75, 0.92), (130, 0.85), (185, 0.95), (230, 0.82), (280, 0.90), (320, 0.86)]
        for b_deg, b_scale in compliant_blips:
            brad = math.radians(b_deg)
            bx = self.cx + (self.rx * b_scale) * math.cos(brad)
            by = self.cy + (self.ry * b_scale) * math.sin(brad)
            self.create_oval(bx - 2, by - 2, bx + 2, by + 2, fill=_THEME["emerald_light"], outline="")

        # 4. Critical Defaulter Risk Blips (Pulsing crimson beacons)
        pulse_r = 3 + 2 * math.sin(self.pulse_phase)
        defaulter_angles = [65, 155, 250, 310]
        for i, student in enumerate(self.defaulters[:4]):
            deg = defaulter_angles[i % len(defaulter_angles)]
            scale = max(0.18, min(0.45, student.get("percentage", 10.0) / 100.0 * 0.7))
            brad = math.radians(deg)
            bx = self.cx + (self.rx * scale) * math.cos(brad)
            by = self.cy + (self.ry * scale) * math.sin(brad)

            # Pulsing ring
            self.create_oval(bx - pulse_r - 2, by - pulse_r - 2, bx + pulse_r + 2, by + pulse_r + 2, outline=_THEME["crimson"], width=1)
            # Center blip
            self.create_oval(bx - 2.5, by - 2.5, bx + 2.5, by + 2.5, fill=_THEME["crimson"], outline="")

        # Center core marker
        self.create_oval(self.cx - 2, self.cy - 2, self.cx + 2, self.cy + 2, fill=_THEME["emerald_light"], outline="")

        # Tactical HUD Legend
        self.create_text(8, 12, text="RADAR SCAN // 32 Hz", font=("Consolas", 8, "bold"), fill=_THEME["emerald_light"], anchor="w")
        h = self.winfo_height() if self.winfo_height() > 30 else 190
        self.create_text(8, h - 10, text="RANGE: 100% • THRESHOLD: 75%", font=("Consolas", 7), fill="#8FA589", anchor="w")

    def stop(self):
        self._animating = False


# ======================================================================
# MOTION GRAPHIC 2: Real-time Oscilloscope Telemetry Waveform
# ======================================================================
class TelemetryWaveformCanvas(tk.Canvas):
    """Animated cyber oscilloscope showing a real-time oscillating heartbeat waveform."""

    def __init__(self, master, **kwargs):
        super().__init__(master, bg=_THEME["monitor_bg"], highlightthickness=0, **kwargs)
        self.phase = 0.0
        self._animating = True
        self._schedule_wave()

    def _schedule_wave(self):
        if not self.winfo_exists() or not self._animating:
            return
        self._draw_wave()
        self.after(40, self._schedule_wave)

    def _draw_wave(self):
        self.delete("all")
        width = self.winfo_width() or 240
        height = self.winfo_height() or 38
        mid_y = height / 2.0
        self.phase += 0.18

        # Subtle background grid lines
        for gx in range(0, width, 30):
            self.create_line(gx, 0, gx, height, fill="#202D1E", width=1)
        self.create_line(0, mid_y, width, mid_y, fill="#243422", width=1)

        pts = []
        for x in range(0, width, 3):
            wave1 = math.sin(x * 0.05 + self.phase)
            wave2 = 0.5 * math.sin(x * 0.12 - self.phase * 1.5)
            center_dist = abs(x - (width * 0.45))
            spike = math.exp(-(center_dist**2) / 120.0) * math.sin(self.phase * 3.0) * 11.0
            y = mid_y + (wave1 + wave2) * 5.5 + spike
            pts.extend([x, y])

        if len(pts) >= 4:
            self.create_line(*pts, fill=_THEME["emerald_light"], width=1.5)

        self.create_text(width - 6, 8, text="SYS TELEMETRY: 128 kb/s", font=("Consolas", 7), fill=_THEME["emerald_light"], anchor="e")

    def stop(self):
        self._animating = False


# ======================================================================
# MOTION GRAPHIC 3: Eased Segmented Spectrum Expansion
# ======================================================================
class AnimatedSpectrumBar(tk.Canvas):
    """Canvas-based segmented attendance spectrum with smooth glide expansion."""

    def __init__(self, master, present_pct=78.6, late_pct=13.2, absent_pct=8.2, **kwargs):
        super().__init__(master, height=20, bg=_THEME["card_alt"], highlightthickness=0, **kwargs)
        self.p_target = present_pct
        self.l_target = late_pct
        self.a_target = absent_pct
        self.anim_progress = 0.0
        self._animating = True
        self._start_time = time.time()
        self.bind("<Configure>", lambda _e: self._step())
        self._step()

    def update_targets(self, p, l, a):
        self.p_target, self.l_target, self.a_target = p, l, a
        self.anim_progress = 0.0
        self._start_time = time.time()
        self._step()

    def _step(self):
        if not self.winfo_exists():
            return
        elapsed = (time.time() - self._start_time) * 1000
        self.anim_progress = min(1.0, elapsed / 500.0)
        eased = 1.0 - (1.0 - self.anim_progress) ** 3

        width = self.winfo_width()
        if width > 10:
            self.delete("all")
            cur_p_w = int(width * (self.p_target / 100.0) * eased)
            cur_l_w = int(width * (self.l_target / 100.0) * eased)
            cur_a_w = int(width * (self.a_target / 100.0) * eased)

            x = 0
            if cur_p_w > 0:
                self.create_rectangle(x, 0, x + cur_p_w, 20, fill=_THEME["emerald"], outline="")
                x += cur_p_w
            if cur_l_w > 0:
                self.create_rectangle(x, 0, x + cur_l_w, 20, fill=_THEME["amber"], outline="")
                x += cur_l_w
            if cur_a_w > 0:
                self.create_rectangle(x, 0, width, 20, fill=_THEME["crimson"], outline="")

            # Subtle top highlight edge
            self.create_line(0, 0, width, 0, fill="#FFFFFF", width=1)

        if self.anim_progress < 1.0:
            self.after(20, self._step)


# ======================================================================
# Main View: Futuristic Nexus Admin Portal (Forest Green & Beige)
# ======================================================================
class AdminPortalView(ctk.CTkFrame):
    """Futuristic Admin Control Console with live telemetry, radar, and warm beige styling."""

    def __init__(self, master, user, on_logout):
        super().__init__(master, fg_color=_THEME["bg_base"], corner_radius=0)
        self.user = user
        self.on_logout = on_logout
        self.current_page = "Dashboard"
        self.nav_buttons = {}
        self.table = None
        self.current_rows = {}
        self.toast_frame = None
        self.toast_label = None
        self.clock_label = None
        self.beacon_label = None
        self.filter_entry = None
        self.radar_widget = None
        self.waveform_widget = None
        self.spectrum_widget = None
        self._beacon_phase = 0.0

        self._configure_tree_theme()
        self._build_shell()
        self.show_dashboard()
        self._start_clock()
        self._start_beacon_pulse()

    def _configure_tree_theme(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Presenza.Treeview",
            background=_THEME["card"],
            foreground=_THEME["text_dark"],
            rowheight=34,
            fieldbackground=_THEME["card"],
            bordercolor=_THEME["card_border"],
            borderwidth=0,
            font=("Segoe UI", 10),
        )
        style.configure(
            "Presenza.Treeview.Heading",
            background=_THEME["sidebar"],
            foreground=_THEME["sidebar_text"],
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            padding=(10, 8),
            bordercolor=_THEME["sidebar_border"],
            borderwidth=1,
        )
        style.map(
            "Presenza.Treeview",
            background=[("selected", _THEME["primary"])],
            foreground=[("selected", "#FFFFFF")],
        )

    # ------------------------------------------------------------------
    # Shell Layout
    # ------------------------------------------------------------------
    def _build_shell(self):
        self.pack(fill="both", expand=True)

        # Deep Forest Green Sidebar
        sidebar = ctk.CTkFrame(self, width=255, fg_color=_THEME["sidebar"], corner_radius=0)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # Brand Banner
        brand_box = ctk.CTkFrame(sidebar, fg_color="transparent")
        brand_box.pack(fill="x", padx=20, pady=(24, 6))

        logo_row = ctk.CTkFrame(brand_box, fg_color="transparent")
        logo_row.pack(fill="x")
        ctk.CTkLabel(logo_row, text="⬢", font=("Segoe UI", 20, "bold"), text_color=_THEME["sand"]).pack(side="left", padx=(0, 8))
        ctk.CTkLabel(logo_row, text="PRESENZA", font=("Georgia", 19, "bold"), text_color=_THEME["sidebar_text"]).pack(side="left")

        sub_row = ctk.CTkFrame(brand_box, fg_color="transparent")
        sub_row.pack(fill="x", pady=(4, 0))
        ctk.CTkLabel(sub_row, text="ADMIN COMMAND", font=("Consolas", 10, "bold"), text_color=_THEME["sand"]).pack(side="left")
        ctk.CTkLabel(sub_row, text="• v3.0", font=("Consolas", 10), text_color=_THEME["sidebar_muted"]).pack(side="left", padx=4)

        # Breathing Engine Beacon
        status_chip = ctk.CTkFrame(sidebar, fg_color="#182116", corner_radius=6, height=26, border_width=1, border_color="#273824")
        status_chip.pack(fill="x", padx=18, pady=(10, 16))
        status_chip.pack_propagate(False)
        self.beacon_label = ctk.CTkLabel(
            status_chip, text="● SYSTEM ONLINE", font=("Consolas", 9, "bold"), text_color=_THEME["emerald_light"]
        )
        self.beacon_label.place(relx=0.5, rely=0.5, anchor="center")

        # Scrollable Navigation
        nav_scroll = ctk.CTkScrollableFrame(sidebar, fg_color="transparent")
        nav_scroll.pack(fill="both", expand=True, padx=8, pady=0)

        for category, items in _NAV_MENU:
            ctk.CTkLabel(
                nav_scroll, text=category, font=("Consolas", 9, "bold"), text_color=_THEME["sidebar_muted"]
            ).pack(anchor="w", padx=12, pady=(14, 4))

            for page_name, icon, _desc in items:
                btn = ctk.CTkButton(
                    nav_scroll,
                    text=f"  {icon}   {page_name}",
                    anchor="w",
                    height=38,
                    corner_radius=7,
                    font=("Segoe UI", 12, "bold" if page_name == "Dashboard" else "normal"),
                    fg_color="transparent",
                    text_color=_THEME["sidebar_text"],
                    hover_color=_THEME["sidebar_hover"],
                    command=lambda p=page_name: self.show_page(p),
                )
                btn.pack(fill="x", padx=4, pady=1)
                self.nav_buttons[page_name] = btn

        # Admin User Card
        user_card = ctk.CTkFrame(sidebar, fg_color="#1A2418", corner_radius=10, border_width=1, border_color="#2D3B2A")
        user_card.pack(fill="x", padx=14, pady=(10, 14))

        u_row = ctk.CTkFrame(user_card, fg_color="transparent")
        u_row.pack(fill="x", padx=10, pady=10)

        avatar = ctk.CTkFrame(u_row, width=34, height=34, fg_color=_THEME["primary"], corner_radius=17)
        avatar.pack(side="left", padx=(0, 10))
        avatar.pack_propagate(False)
        ctk.CTkLabel(
            avatar, text="AD", font=("Consolas", 11, "bold"), text_color="#FFFFFF"
        ).place(relx=0.5, rely=0.5, anchor="center")

        u_info = ctk.CTkFrame(u_row, fg_color="transparent")
        u_info.pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(
            u_info, text=self.user.display_name or "Administrator", font=("Segoe UI", 11, "bold"), text_color=_THEME["sidebar_text"], anchor="w"
        ).pack(anchor="w")
        ctk.CTkLabel(
            u_info, text="Superuser", font=("Consolas", 9), text_color=_THEME["sand"], anchor="w"
        ).pack(anchor="w")

        ctk.CTkButton(
            user_card,
            text="Sign Out",
            height=28,
            font=("Segoe UI", 11),
            fg_color="transparent",
            hover_color=_THEME["sidebar_hover"],
            text_color=_THEME["sand"],
            border_width=1,
            border_color=_THEME["sidebar_border"],
            command=self.on_logout,
        ).pack(fill="x", padx=10, pady=(0, 10))

        # Main Dynamic Content Area (Warm Beige Canvas)
        self.content = ctk.CTkFrame(self, fg_color=_THEME["bg_base"], corner_radius=0)
        self.content.pack(side="left", fill="both", expand=True)

    # ------------------------------------------------------------------
    # Breathing Pulse & Digital Clock
    # ------------------------------------------------------------------
    def _start_clock(self):
        def tick():
            if self.clock_label and self.clock_label.winfo_exists():
                now = datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
                self.clock_label.configure(text=f"SYS TIME: {now}")
                self.after(1000, tick)

        self.after(1000, tick)

    def _start_beacon_pulse(self):
        def pulse():
            if self.beacon_label and self.beacon_label.winfo_exists():
                self._beacon_phase += 0.2
                val = int(180 + 70 * math.sin(self._beacon_phase))
                hex_col = f"#{int(val*0.35):02x}{val:02x}{int(val*0.5):02x}"
                self.beacon_label.configure(text_color=hex_col)
                self.after(80, pulse)

        self.after(80, pulse)

    # ------------------------------------------------------------------
    # Number Ticker Animation (Smooth Numeric Easing)
    # ------------------------------------------------------------------
    def _animate_number(self, label, target, duration_ms=450, prefix="", suffix="", is_float=False):
        start_time = time.time()

        def step():
            if not label.winfo_exists():
                return
            elapsed = (time.time() - start_time) * 1000
            progress = min(1.0, elapsed / duration_ms)
            eased = 1.0 - (1.0 - progress) ** 3
            current = target * eased

            if is_float:
                text = f"{prefix}{current:.1f}{suffix}"
            else:
                text = f"{prefix}{int(current)}{suffix}"

            label.configure(text=text)
            if progress < 1.0:
                label.after(16, step)
            else:
                final_val = f"{prefix}{target:.1f}{suffix}" if is_float else f"{prefix}{int(target)}{suffix}"
                label.configure(text=final_val)

        step()

    def _update_nav_highlight(self, active_page):
        for name, btn in self.nav_buttons.items():
            if name == active_page:
                btn.configure(
                    fg_color=_THEME["sidebar_active"],
                    text_color=_THEME["sand"],
                    font=("Segoe UI", 12, "bold"),
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    text_color=_THEME["sidebar_text"],
                    font=("Segoe UI", 12, "normal"),
                )

    def _clear_content(self):
        if self.radar_widget:
            self.radar_widget.stop()
            self.radar_widget = None
        if self.waveform_widget:
            self.waveform_widget.stop()
            self.waveform_widget = None
        self.spectrum_widget = None

        for child in self.content.winfo_children():
            child.destroy()
        self.table = None
        self.current_rows = {}
        self.toast_frame = None
        self.toast_label = None

    # ------------------------------------------------------------------
    # Header & Notification Toast
    # ------------------------------------------------------------------
    def _header(self, title, subtitle, show_refresh=False):
        header_frame = ctk.CTkFrame(self.content, fg_color="transparent")
        header_frame.pack(fill="x", padx=32, pady=(24, 14))

        left = ctk.CTkFrame(header_frame, fg_color="transparent")
        left.pack(side="left")

        title_row = ctk.CTkFrame(left, fg_color="transparent")
        title_row.pack(anchor="w")
        ctk.CTkLabel(
            title_row, text=title, font=("Georgia", 24, "bold"), text_color=_THEME["text_dark"]
        ).pack(side="left")

        ctk.CTkLabel(
            left, text=subtitle, font=("Segoe UI", 12), text_color=_THEME["text_muted"]
        ).pack(anchor="w", pady=(2, 0))

        right = ctk.CTkFrame(header_frame, fg_color="transparent")
        right.pack(side="right", anchor="e")

        telemetry_box = ctk.CTkFrame(right, fg_color=_THEME["card"], corner_radius=8, border_width=1, border_color=_THEME["card_border"])
        telemetry_box.pack(side="left", padx=(0, 10))

        self.clock_label = ctk.CTkLabel(
            telemetry_box,
            text=f"SYS TIME: {datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}",
            font=("Consolas", 10, "bold"),
            text_color=_THEME["primary"],
        )
        self.clock_label.pack(padx=14, pady=7)

        if show_refresh:
            ctk.CTkButton(
                right,
                text="⟳ Sync Telemetry",
                width=120,
                height=32,
                font=("Segoe UI", 11, "bold"),
                fg_color=_THEME["card"],
                hover_color=_THEME["card_alt"],
                text_color=_THEME["primary"],
                border_width=1,
                border_color=_THEME["card_border"],
                command=self.show_dashboard,
            ).pack(side="left")

        # Notification Toast Row
        self.toast_frame = ctk.CTkFrame(self.content, fg_color=_THEME["card"], corner_radius=8, border_width=1, border_color=_THEME["card_border"])
        self.toast_frame.pack(fill="x", padx=32, pady=(0, 14))
        self.toast_label = ctk.CTkLabel(
            self.toast_frame, text="● System operational. Master data telemetry synchronized.", font=("Segoe UI", 11), text_color=_THEME["emerald"], anchor="w"
        )
        self.toast_label.pack(fill="x", padx=16, pady=8)

    def _toast(self, message, error=False, warning=False):
        if not self.toast_label or not self.toast_frame:
            return
        if error:
            color = _THEME["crimson"]
            bg = _THEME["crimson_dim"]
            border = _THEME["crimson_border"]
            prefix = "✕ ERROR: "
        elif warning:
            color = _THEME["amber"]
            bg = _THEME["amber_dim"]
            border = _THEME["amber_border"]
            prefix = "⚠ WARNING: "
        else:
            color = _THEME["emerald"]
            bg = _THEME["emerald_dim"]
            border = _THEME["emerald_border"]
            prefix = "✓ SUCCESS: "

        self.toast_frame.configure(fg_color=bg, border_color=border)
        self.toast_label.configure(text=f"{prefix}{message}", text_color=color)

    # ------------------------------------------------------------------
    # Routing
    # ------------------------------------------------------------------
    def show_page(self, page):
        self.current_page = page
        self._update_nav_highlight(page)
        if page == "Dashboard":
            self.show_dashboard()
        elif page in RECORD_CONFIG:
            self.show_records(page)
        elif page == "Assignments":
            self.show_assignments()
        elif page == "Import":
            self.show_import()
        elif page == "Audit Logs":
            self.show_audit_logs()
        elif page == "Reports":
            self.show_reports()
        elif page == "Backup":
            self.show_backup()
        else:
            self.show_settings()

    # ------------------------------------------------------------------
    # Master Dashboard
    # ------------------------------------------------------------------
    def show_dashboard(self):
        self._clear_content()
        self._update_nav_highlight("Dashboard")
        self._header("COMMAND TELEMETRY // OVERVIEW", "Real-time institutional attendance status, risk radar, and operations.", show_refresh=True)

        try:
            telemetry = admin_service.dashboard_telemetry(self.user.role)
        except Exception as error:
            self._toast(f"Failed to load telemetry: {error}", error=True)
            return

        counts = telemetry["counts"]
        breakdown = telemetry["breakdown"]
        defaulters = telemetry["defaulters"]
        recent_logs = telemetry["recent_logs"]
        recent_leaves = telemetry["recent_leaves"]
        threshold = telemetry["threshold"]

        dash_scroll = ctk.CTkScrollableFrame(self.content, fg_color="transparent")
        dash_scroll.pack(fill="both", expand=True, padx=32, pady=(0, 20))

        # --------------------------------------------------------------
        # SECTION 1: Responsive Executive HUD Metric Grid
        # --------------------------------------------------------------
        kpi_container = ctk.CTkFrame(dash_scroll, fg_color="transparent")
        kpi_container.pack(fill="x", pady=(0, 16))

        kpis = [
            ("TOTAL STUDENTS", counts["students"], f"◈ {counts['students']} Enrolled", _THEME["primary"], lambda: self.show_page("Students"), False, ""),
            ("FACULTY CADRE", counts["teachers"], "⬡ Verified Staff", _THEME["emerald"], lambda: self.show_page("Teachers"), False, ""),
            ("CURRICULUM", counts["subjects"], f"⎈ {counts['assignments']} Allocations", _THEME["sand"], lambda: self.show_page("Subjects"), False, ""),
            ("ATTENDANCE RATE", breakdown["overall_pct"], f"Target ≥ {threshold}%", _THEME["emerald"] if breakdown["overall_pct"] >= threshold else _THEME["amber"], lambda: self.show_page("Reports"), True, "%"),
            ("RISK RADAR", len(defaulters), f"< {threshold}% Critical", _THEME["crimson"] if defaulters else _THEME["emerald"], None, False, " Alerts"),
            ("SYSTEM EVENTS", counts["total_attendance"], f"{counts['today_attendance']} Logged Today", _THEME["primary_dark"], lambda: self.show_page("Audit Logs"), False, ""),
        ]

        card_widgets = []
        for label, num_val, sub, accent, action, is_float, suffix in kpis:
            card = ctk.CTkFrame(kpi_container, fg_color=_THEME["card"], corner_radius=10, border_width=1, border_color=_THEME["card_border"])
            ctk.CTkFrame(card, height=4, fg_color=accent, corner_radius=2).pack(fill="x", padx=12, pady=(10, 8))

            ctk.CTkLabel(card, text=label, font=("Consolas", 10, "bold"), text_color=_THEME["text_muted"]).pack(anchor="w", padx=14)

            val_label = ctk.CTkLabel(card, text="0", font=("Georgia", 25, "bold"), text_color=_THEME["text_dark"])
            val_label.pack(anchor="w", padx=14, pady=(2, 0))
            self._animate_number(val_label, num_val, duration_ms=450, is_float=is_float, suffix=suffix)

            sub_frame = ctk.CTkFrame(card, fg_color="transparent")
            sub_frame.pack(fill="x", padx=14, pady=(4, 12))
            ctk.CTkLabel(sub_frame, text=sub, font=("Segoe UI", 10, "bold"), text_color=accent).pack(side="left")

            if action:
                card.bind("<Button-1>", lambda _e, act=action: act())
            card_widgets.append(card)

        last_kpi_cols = [0]
        def layout_kpis(event=None):
            if not kpi_container.winfo_exists():
                return
            w = kpi_container.winfo_width()
            cols = 6 if w >= 1260 else (3 if w >= 700 else 2)
            if cols == last_kpi_cols[0]:
                return
            last_kpi_cols[0] = cols
            for c in range(6):
                kpi_container.grid_columnconfigure(c, weight=1 if c < cols else 0, uniform="kpi" if c < cols else "")
            for i, c_widget in enumerate(card_widgets):
                row = i // cols
                col = i % cols
                c_widget.grid(row=row, column=col, sticky="nsew", padx=4, pady=4)

        kpi_container.bind("<Configure>", layout_kpis)
        layout_kpis()

        # --------------------------------------------------------------
        # SECTION 2: Responsive Attendance Spectrum & Rapid Actions
        # --------------------------------------------------------------
        mid_container = ctk.CTkFrame(dash_scroll, fg_color="transparent")
        mid_container.pack(fill="x", pady=(0, 16))

        # Left Card: Attendance Spectrum & Status Breakdown
        spectrum_card = ctk.CTkFrame(mid_container, fg_color=_THEME["card"], corner_radius=12, border_width=1, border_color=_THEME["card_border"])

        s_header = ctk.CTkFrame(spectrum_card, fg_color="transparent")
        s_header.pack(fill="x", padx=20, pady=(16, 10))
        ctk.CTkLabel(s_header, text="ATTENDANCE SPECTRUM // DISTRIBUTION", font=("Georgia", 13, "bold"), text_color=_THEME["text_dark"]).pack(side="left")
        ctk.CTkLabel(s_header, text=f"TOTAL LOGS: {breakdown['total']}", font=("Consolas", 10, "bold"), text_color=_THEME["primary"]).pack(side="right")

        # Animated Segmented Spectrum Bar Canvas
        self.spectrum_widget = AnimatedSpectrumBar(
            spectrum_card,
            present_pct=breakdown["present_pct"],
            late_pct=breakdown["late_pct"],
            absent_pct=breakdown["absent_pct"],
        )
        self.spectrum_widget.pack(fill="x", padx=20, pady=(0, 14))

        # Status Chips Grid
        chips_row = ctk.CTkFrame(spectrum_card, fg_color="transparent")
        chips_row.pack(fill="x", padx=20, pady=(0, 16))

        stats = [
            ("PRESENT", f"{breakdown['present']} logs", f"{breakdown['present_pct']}%", _THEME["emerald"], _THEME["emerald_dim"], _THEME["emerald_border"]),
            ("LATE", f"{breakdown['late']} logs", f"{breakdown['late_pct']}%", _THEME["amber"], _THEME["amber_dim"], _THEME["amber_border"]),
            ("ABSENT", f"{breakdown['absent']} logs", f"{breakdown['absent_pct']}%", _THEME["crimson"], _THEME["crimson_dim"], _THEME["crimson_border"]),
        ]
        for title, count_text, pct_text, fg_color, bg_color, b_color in stats:
            chip = ctk.CTkFrame(chips_row, fg_color=bg_color, corner_radius=8, border_width=1, border_color=b_color)
            chip.pack(side="left", fill="x", expand=True, padx=4)
            ctk.CTkLabel(chip, text=title, font=("Consolas", 10, "bold"), text_color=fg_color).pack(anchor="w", padx=12, pady=(8, 0))
            val_box = ctk.CTkFrame(chip, fg_color="transparent")
            val_box.pack(fill="x", padx=12, pady=(2, 8))
            ctk.CTkLabel(val_box, text=count_text, font=("Segoe UI", 12, "bold"), text_color=_THEME["text_dark"]).pack(side="left")
            ctk.CTkLabel(val_box, text=f" ({pct_text})", font=("Consolas", 10), text_color=fg_color).pack(side="left")

        # Telemetry footer
        t_foot = ctk.CTkFrame(spectrum_card, fg_color=_THEME["card_alt"], corner_radius=6)
        t_foot.pack(fill="x", padx=20, pady=(0, 16))
        ctk.CTkLabel(
            t_foot,
            text=f"• Database Engine: SQLite v{telemetry['sqlite_version']}  |  Database Size: {telemetry['db_size_kb']} KB  |  Audit Revisions: {len(recent_logs)}",
            font=("Consolas", 9),
            text_color=_THEME["text_muted"],
        ).pack(fill="x", padx=12, pady=8)

        # Right Card: Rapid Action Command Station
        action_card = ctk.CTkFrame(mid_container, fg_color=_THEME["card"], corner_radius=12, border_width=1, border_color=_THEME["card_border"])

        a_header = ctk.CTkFrame(action_card, fg_color="transparent")
        a_header.pack(fill="x", padx=20, pady=(16, 10))
        ctk.CTkLabel(a_header, text="OPERATIONS // COMMAND SHORTCUTS", font=("Georgia", 13, "bold"), text_color=_THEME["text_dark"]).pack(side="left")
        ctk.CTkLabel(a_header, text="RAPID ACTIONS", font=("Consolas", 10, "bold"), text_color=_THEME["emerald"]).pack(side="right")

        grid_frame = ctk.CTkFrame(action_card, fg_color="transparent")
        grid_frame.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        actions = [
            ("◈  Enroll Student", "Register new student record", lambda: self._record_dialog("Students", RECORD_CONFIG["Students"])),
            ("⬡  Appoint Faculty", "Onboard new teacher credential", lambda: self._record_dialog("Teachers", RECORD_CONFIG["Teachers"])),
            ("⚡  Map Assignment", "Link faculty to subject & section", self._assignment_dialog),
            ("↑  Bulk CSV Ingest", "Batch import students or staff", lambda: self.show_page("Import")),
            ("💾  DB Snapshot", "Create timestamped backup now", self._quick_backup),
            ("⚙  Threshold Policy", "Configure minimum attendance rule", lambda: self.show_page("Settings")),
        ]

        for i, (btn_title, btn_desc, cmd) in enumerate(actions):
            row = i // 2
            col = i % 2
            btn_box = ctk.CTkFrame(grid_frame, fg_color=_THEME["card_alt"], corner_radius=8, border_width=1, border_color=_THEME["card_border"])
            btn_box.grid(row=row, column=col, sticky="nsew", padx=4, pady=4)
            grid_frame.grid_columnconfigure(col, weight=1)
            grid_frame.grid_rowconfigure(row, weight=1)

            btn = ctk.CTkButton(
                btn_box,
                text=btn_title,
                font=("Segoe UI", 11, "bold"),
                anchor="w",
                fg_color="transparent",
                hover_color=_THEME["bg_base"],
                text_color=_THEME["primary"],
                command=cmd,
                height=26,
            )
            btn.pack(fill="x", padx=10, pady=(8, 0))

            desc_lbl = ctk.CTkLabel(
                btn_box, text=btn_desc, font=("Segoe UI", 9), text_color=_THEME["text_muted"], anchor="w"
            )
            desc_lbl.pack(fill="x", padx=12, pady=(0, 8))

        last_mid_mode = [None]
        def layout_mid(event=None):
            if not mid_container.winfo_exists():
                return
            w = mid_container.winfo_width()
            mode = "side" if w >= 880 else "stack"
            if mode == last_mid_mode[0]:
                return
            last_mid_mode[0] = mode
            if mode == "side":
                mid_container.grid_columnconfigure(0, weight=1, uniform="mid")
                mid_container.grid_columnconfigure(1, weight=1, uniform="mid")
                spectrum_card.grid(row=0, column=0, sticky="nsew", padx=(0, 6), pady=0)
                action_card.grid(row=0, column=1, sticky="nsew", padx=(6, 0), pady=0)
            else:
                mid_container.grid_columnconfigure(0, weight=1, uniform="")
                mid_container.grid_columnconfigure(1, weight=0, uniform="")
                spectrum_card.grid(row=0, column=0, sticky="nsew", padx=0, pady=(0, 12))
                action_card.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)

        mid_container.bind("<Configure>", layout_mid)
        layout_mid()

        # --------------------------------------------------------------
        # SECTION 3: Responsive 3D Tactical Radar & Security Audit Feed
        # --------------------------------------------------------------
        bot_container = ctk.CTkFrame(dash_scroll, fg_color="transparent")
        bot_container.pack(fill="x", pady=(0, 10))

        # Left Radar: Tactical Radar HUD with Motion Graphics Sweep
        radar_card = ctk.CTkFrame(bot_container, fg_color=_THEME["card"], corner_radius=12, border_width=1, border_color=_THEME["card_border"])

        r_header = ctk.CTkFrame(radar_card, fg_color="transparent")
        r_header.pack(fill="x", padx=20, pady=(16, 8))
        ctk.CTkLabel(r_header, text="DEFAULTER RADAR // 3D TACTICAL SCAN", font=("Georgia", 13, "bold"), text_color=_THEME["text_dark"]).pack(side="left")
        ctk.CTkLabel(r_header, text=f"THRESHOLD: {threshold}%", font=("Consolas", 10, "bold"), text_color=_THEME["crimson"]).pack(side="right")

        r_content = ctk.CTkFrame(radar_card, fg_color="transparent")
        r_content.pack(fill="both", expand=True, padx=16, pady=(0, 14))

        # Tactical Monitor Screen
        self.radar_widget = TacticalRadarCanvas(r_content, defaulters=defaulters, width=190, height=175)
        self.radar_widget.pack(side="left", padx=(0, 10))

        # Defaulter List
        def_panel = ctk.CTkFrame(r_content, fg_color=_THEME["card_alt"], corner_radius=8, border_width=1, border_color=_THEME["card_border"])
        def_panel.pack(side="left", fill="both", expand=True)

        if not defaulters:
            ctk.CTkLabel(
                def_panel,
                text="✓ ALL STUDENTS COMPLIANT\nNO CRITICAL DEFAULTERS DETECTED",
                font=("Segoe UI", 11, "bold"),
                text_color=_THEME["emerald"],
                justify="center",
            ).place(relx=0.5, rely=0.5, anchor="center")
        else:
            ctk.CTkLabel(
                def_panel, text="CRITICAL INTERVENTION LIST", font=("Consolas", 9, "bold"), text_color=_THEME["crimson"]
            ).pack(anchor="w", padx=12, pady=(10, 4))

            for student in defaulters[:5]:
                item = ctk.CTkFrame(def_panel, fg_color="transparent")
                item.pack(fill="x", padx=10, pady=3)

                badge = ctk.CTkFrame(item, fg_color=_THEME["crimson_dim"], corner_radius=4, border_width=1, border_color=_THEME["crimson_border"])
                badge.pack(side="left", padx=(0, 8))
                ctk.CTkLabel(
                    badge, text=f" {student['percentage']}% ", font=("Consolas", 8, "bold"), text_color=_THEME["crimson"]
                ).pack(padx=2, pady=1)

                ctk.CTkLabel(
                    item, text=f"{student['roll_no']} • {student['name']}", font=("Segoe UI", 10, "bold"), text_color=_THEME["text_dark"]
                ).pack(side="left")

                ctk.CTkLabel(
                    item, text=f"{student['attended']}/{student['total']} logs", font=("Consolas", 9), text_color=_THEME["amber"]
                ).pack(side="right")

        # Right Radar: Security Audit & Oscilloscope Telemetry
        audit_card = ctk.CTkFrame(bot_container, fg_color=_THEME["card"], corner_radius=12, border_width=1, border_color=_THEME["card_border"])

        au_header = ctk.CTkFrame(audit_card, fg_color="transparent")
        au_header.pack(fill="x", padx=20, pady=(16, 6))
        ctk.CTkLabel(au_header, text="AUDIT TELEMETRY // SECURITY & ACTIVITY", font=("Georgia", 13, "bold"), text_color=_THEME["text_dark"]).pack(side="left")

        ctk.CTkButton(
            au_header,
            text="View Full Log →",
            font=("Segoe UI", 10, "bold"),
            fg_color="transparent",
            text_color=_THEME["primary"],
            hover_color=_THEME["card_alt"],
            height=24,
            command=lambda: self.show_page("Audit Logs"),
        ).pack(side="right")

        # Live Real-time Oscilloscope Telemetry Canvas
        self.waveform_widget = TelemetryWaveformCanvas(audit_card, height=36)
        self.waveform_widget.pack(fill="x", padx=16, pady=(0, 8))

        feed_frame = ctk.CTkFrame(audit_card, fg_color=_THEME["card_alt"], corner_radius=8, border_width=1, border_color=_THEME["card_border"])
        feed_frame.pack(fill="both", expand=True, padx=16, pady=(0, 14))

        events = []
        for log in recent_logs[:3]:
            events.append((
                "LOG REVISION",
                f"Att #{log['attendance_id']}: {log['old_status']} → {log['new_status']} by {log['changed_by_user'] or 'User'} ({log['reason']})",
                log["changed_at"],
                _THEME["amber"],
                _THEME["amber_dim"],
            ))
        for leave in recent_leaves[:2]:
            events.append((
                "LEAVE REQUEST",
                f"{leave['roll_no']} ({leave['student_name']}): {leave['from_date']} to {leave['to_date']} [{leave['status']}]",
                leave["from_date"],
                _THEME["sand"],
                _THEME["card"],
            ))

        if not events:
            ctk.CTkLabel(
                feed_frame, text="No recent audit events recorded.", font=("Segoe UI", 11), text_color=_THEME["text_muted"]
            ).pack(pady=20)
        else:
            for tag, desc, timestamp, tag_color, tag_bg in events[:4]:
                event_row = ctk.CTkFrame(feed_frame, fg_color="transparent")
                event_row.pack(fill="x", padx=12, pady=4)

                tag_badge = ctk.CTkFrame(event_row, fg_color=tag_bg, corner_radius=4, border_width=1, border_color=tag_color)
                tag_badge.pack(side="left", padx=(0, 8))
                ctk.CTkLabel(
                    tag_badge, text=f" {tag} ", font=("Consolas", 8, "bold"), text_color=tag_color
                ).pack(padx=2, pady=1)

                ctk.CTkLabel(
                    event_row, text=desc, font=("Segoe UI", 10), text_color=_THEME["text_dark"], anchor="w"
                ).pack(side="left", fill="x", expand=True)

                ctk.CTkLabel(
                    event_row, text=timestamp, font=("Consolas", 9), text_color=_THEME["text_muted"]
                ).pack(side="right")

        last_bot_mode = [None]
        def layout_bot(event=None):
            if not bot_container.winfo_exists():
                return
            w = bot_container.winfo_width()
            mode = "side" if w >= 940 else "stack"
            if mode == last_bot_mode[0]:
                return
            last_bot_mode[0] = mode
            if mode == "side":
                bot_container.grid_columnconfigure(0, weight=1, uniform="bot")
                bot_container.grid_columnconfigure(1, weight=1, uniform="bot")
                radar_card.grid(row=0, column=0, sticky="nsew", padx=(0, 6), pady=0)
                audit_card.grid(row=0, column=1, sticky="nsew", padx=(6, 0), pady=0)
            else:
                bot_container.grid_columnconfigure(0, weight=1, uniform="")
                bot_container.grid_columnconfigure(1, weight=0, uniform="")
                radar_card.grid(row=0, column=0, sticky="nsew", padx=0, pady=(0, 12))
                audit_card.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)

        bot_container.bind("<Configure>", layout_bot)
        layout_bot()

    def _quick_backup(self):
        try:
            from utils.backup import create_database_backup
            path = create_database_backup(self.user.role)
            self._toast(f"Database snapshot secured: {Path(path).name}")
        except Exception as error:
            self._toast(f"Backup failed: {error}", error=True)

    # ------------------------------------------------------------------
    # Universal Treeview Factory (Warm Surface & Forest Heading)
    # ------------------------------------------------------------------
    def _tree(self, columns, rows, on_double_click=None):
        wrapper = ctk.CTkFrame(self.content, fg_color=_THEME["card"], corner_radius=10, border_width=1, border_color=_THEME["card_border"])
        wrapper.pack(fill="both", expand=True, padx=32, pady=(0, 24))

        col_keys = [key for key, _, _ in columns]
        tree = ttk.Treeview(wrapper, columns=col_keys, show="headings", selectmode="browse", style="Presenza.Treeview")

        for key, heading, width in columns:
            tree.heading(key, text=heading)
            tree.column(key, width=width, anchor="w")

        for row in rows:
            r_dict = dict(row)
            values = [r_dict.get(key, "") for key, _, _ in columns]
            tree.insert("", "end", values=values)

        if on_double_click:
            tree.bind("<Double-1>", lambda _event: on_double_click())

        scrollbar = ttk.Scrollbar(wrapper, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        scrollbar.pack(side="right", fill="y", padx=(0, 10), pady=10)
        self.table = tree

    def _selected_id(self):
        selected = self.table.selection() if self.table else ()
        if not selected:
            raise admin_service.AdminServiceError("Select a record row first.")
        return int(self.table.item(selected[0], "values")[0])

    # ------------------------------------------------------------------
    # Master Records Management (Students, Teachers, Courses, Subjects)
    # ------------------------------------------------------------------
    def show_records(self, kind):
        self._clear_content()
        self._update_nav_highlight(kind)
        config = RECORD_CONFIG[kind]
        rows = config["list"](self.user.role)
        self.current_rows = {int(row["id"]): dict(row) for row in rows}

        self._header(f"{kind.upper()} // DIRECTORY", f"Active registry: {len(rows)} total {kind.lower()} records configured.")

        # Toolbar & Search Filter
        toolbar = ctk.CTkFrame(self.content, fg_color="transparent")
        toolbar.pack(fill="x", padx=32, pady=(0, 12))

        # Left Actions
        ctk.CTkButton(
            toolbar,
            text=f"+ Add {kind[:-1]}",
            font=("Segoe UI", 11, "bold"),
            fg_color=_THEME["primary"],
            hover_color=_THEME["primary_dark"],
            text_color="#FFFFFF",
            command=lambda: self._record_dialog(kind, config),
            height=34,
        ).pack(side="left", padx=(0, 8))

        ctk.CTkButton(
            toolbar,
            text="✎ Edit Selected",
            font=("Segoe UI", 11),
            fg_color=_THEME["card"],
            text_color=_THEME["primary"],
            border_width=1,
            border_color=_THEME["primary"],
            hover_color=_THEME["card_alt"],
            command=lambda: self._edit_record(kind, config),
            height=34,
        ).pack(side="left", padx=(0, 8))

        ctk.CTkButton(
            toolbar,
            text="✕ Delete Selected",
            font=("Segoe UI", 11),
            fg_color=_THEME["card"],
            text_color=_THEME["crimson"],
            border_width=1,
            border_color=_THEME["crimson_border"],
            hover_color=_THEME["crimson_dim"],
            command=lambda: self._delete_selected(config["delete"]),
            height=34,
        ).pack(side="left", padx=(0, 8))

        if kind in {"Teachers", "Students"}:
            ctk.CTkButton(
                toolbar,
                text="↺ Reset Password & State",
                font=("Segoe UI", 11),
                fg_color=_THEME["card"],
                text_color=_THEME["amber"],
                border_width=1,
                border_color=_THEME["amber_border"],
                hover_color=_THEME["amber_dim"],
                command=self._reset_selected,
                height=34,
            ).pack(side="left", padx=(0, 8))

        # Live Search box on Right
        search_box = ctk.CTkFrame(toolbar, fg_color=_THEME["card"], corner_radius=6, border_width=1, border_color=_THEME["card_border"])
        search_box.pack(side="right")

        ctk.CTkLabel(search_box, text="🔍", font=("Segoe UI", 10), text_color=_THEME["text_muted"]).pack(side="left", padx=(8, 4))
        self.filter_entry = ctk.CTkEntry(
            search_box,
            placeholder_text=f"Search {kind.lower()}...",
            width=220,
            height=30,
            fg_color="transparent",
            border_width=0,
            text_color=_THEME["text_dark"],
        )
        self.filter_entry.pack(side="left", padx=(0, 6))
        self.filter_entry.bind("<KeyRelease>", lambda _e: self._filter_table(config["columns"], rows))

        self._tree(config["columns"], rows, lambda: self._edit_record(kind, config))

    def _filter_table(self, columns, all_rows):
        query = self.filter_entry.get().strip().lower() if self.filter_entry else ""
        if not self.table:
            return
        for item in self.table.get_children():
            self.table.delete(item)

        for row in all_rows:
            row_dict = dict(row)
            row_text = " ".join(str(val) for val in row_dict.values()).lower()
            if not query or query in row_text:
                values = [row_dict.get(key, "") for key, _, _ in columns]
                self.table.insert("", "end", values=values)

    def _course_choices(self):
        rows = admin_service.list_courses(self.user.role)
        mapping = {row["name"]: str(row["id"]) for row in rows}
        return list(mapping), mapping

    # ------------------------------------------------------------------
    # Dialogs: Add / Edit Records
    # ------------------------------------------------------------------
    def _record_dialog(self, kind, config, values=None, record_id=None):
        dialog = ctk.CTkToplevel(self)
        dialog.title(f"{'Edit' if record_id else 'New'} {kind[:-1]} | Presenza Admin")
        dialog.geometry("490x640")
        dialog.grab_set()
        dialog.configure(fg_color=_THEME["bg_base"])

        body = ctk.CTkScrollableFrame(dialog, fg_color=_THEME["card"], corner_radius=12, border_width=1, border_color=_THEME["card_border"])
        body.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(
            body,
            text=f"{'Edit' if record_id else 'Add'} {kind[:-1]} Record",
            font=("Georgia", 20, "bold"),
            text_color=_THEME["text_dark"],
        ).pack(anchor="w", padx=20, pady=(18, 4))

        ctk.CTkLabel(
            body,
            text="Ensure data compliance before submitting.",
            font=("Segoe UI", 11),
            text_color=_THEME["text_muted"],
        ).pack(anchor="w", padx=20, pady=(0, 16))

        inputs, course_map = {}, {}
        for key, label in config["fields"]:
            ctk.CTkLabel(body, text=label, font=("Segoe UI", 11, "bold"), text_color=_THEME["text_dark"]).pack(anchor="w", padx=20, pady=(4, 2))

            if key == "course_id":
                choices, course_map = self._course_choices()
                selected = values.get("course", "") if values else (choices[0] if choices else "")
                widget = ctk.CTkComboBox(
                    body,
                    values=choices or ["No programs available"],
                    width=410,
                    height=36,
                    fg_color=_THEME["card"],
                    border_color=_THEME["card_border"],
                    button_color=_THEME["primary"],
                    dropdown_fg_color=_THEME["card"],
                    text_color=_THEME["text_dark"],
                    state="readonly",
                )
                if selected:
                    widget.set(selected)
            else:
                widget = ctk.CTkEntry(
                    body,
                    width=410,
                    height=36,
                    fg_color=_THEME["card"],
                    border_color=_THEME["card_border"],
                    text_color=_THEME["text_dark"],
                )
                widget.insert(0, "" if values is None else str(values.get(key, "")))

            widget.pack(padx=20, pady=(0, 10))
            inputs[key] = widget

        feedback = ctk.CTkLabel(body, text="", font=("Segoe UI", 11), wraplength=410, justify="left")
        feedback.pack(anchor="w", padx=20, pady=(0, 10))

        def save():
            try:
                arguments = []
                for key, _label in config["fields"]:
                    value = inputs[key].get().strip()
                    if key == "course_id":
                        value = course_map.get(value, "")
                    arguments.append(value)

                if record_id is None:
                    config["save"](self.user.role, *arguments)
                    self._toast(f"New {kind[:-1]} registered successfully.")
                else:
                    config["save"](self.user.role, *arguments, record_id)
                    self._toast(f"{kind[:-1]} record #{record_id} updated.")

                dialog.destroy()
                self.show_records(kind)
            except admin_service.AdminServiceError as error:
                feedback.configure(text=f"✕ {error}", text_color=_THEME["crimson"])

        ctk.CTkButton(
            body,
            text=f"Save {kind[:-1]} Record",
            command=save,
            width=410,
            height=40,
            font=("Segoe UI", 12, "bold"),
            fg_color=_THEME["primary"],
            hover_color=_THEME["primary_dark"],
            text_color="#FFFFFF",
        ).pack(padx=20, pady=(6, 24))

    def _edit_record(self, kind, config):
        try:
            record_id = self._selected_id()
            self._record_dialog(kind, config, self.current_rows[record_id], record_id)
        except (admin_service.AdminServiceError, KeyError) as error:
            self._toast(str(error), error=True)

    def _delete_selected(self, delete_fn):
        try:
            record_id = self._selected_id()
            delete_fn(self.user.role, record_id)
            self._toast(f"Record #{record_id} removed.")
            self.show_page(self.current_page)
        except admin_service.AdminServiceError as error:
            self._toast(str(error), error=True)

    def _reset_selected(self):
        try:
            record = self.current_rows[self._selected_id()]
            identifier = record.get("emp_id") or record.get("roll_no")
            admin_service.reset_account(self.user.role, identifier)
            self._toast(f"Account for {identifier} reset. User can now activate anew.")
        except (admin_service.AdminServiceError, KeyError) as error:
            self._toast(str(error), error=True)

    # ------------------------------------------------------------------
    # Teaching Assignments Matrix
    # ------------------------------------------------------------------
    def show_assignments(self):
        self._clear_content()
        self._update_nav_highlight("Assignments")
        rows = admin_service.list_assignments(self.user.role)
        self.current_rows = {int(row["id"]): dict(row) for row in rows}

        self._header("TEACHING MATRIX // ALLOCATIONS", f"Active faculty assignments: {len(rows)} subject courses mapped.")

        toolbar = ctk.CTkFrame(self.content, fg_color="transparent")
        toolbar.pack(fill="x", padx=32, pady=(0, 12))

        ctk.CTkButton(
            toolbar,
            text="+ Add Assignment",
            font=("Segoe UI", 11, "bold"),
            fg_color=_THEME["primary"],
            hover_color=_THEME["primary_dark"],
            text_color="#FFFFFF",
            command=self._assignment_dialog,
            height=34,
        ).pack(side="left", padx=(0, 8))

        ctk.CTkButton(
            toolbar,
            text="✕ Revoke Assignment",
            font=("Segoe UI", 11),
            fg_color=_THEME["card"],
            text_color=_THEME["crimson"],
            border_width=1,
            border_color=_THEME["crimson_border"],
            hover_color=_THEME["crimson_dim"],
            command=lambda: self._delete_selected(admin_service.delete_assignment),
            height=34,
        ).pack(side="left", padx=(0, 8))

        columns = [
            ("id", "ID", 50),
            ("emp_id", "Employee ID", 110),
            ("teacher", "Faculty Name", 160),
            ("code", "Subject Code", 95),
            ("subject", "Subject Name", 180),
            ("course", "Course Program", 110),
            ("semester", "Sem", 50),
            ("section", "Sec", 50),
        ]
        self._tree(columns, rows)

    def _assignment_dialog(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Map Teaching Assignment | Presenza Admin")
        dialog.geometry("510x620")
        dialog.grab_set()
        dialog.configure(fg_color=_THEME["bg_base"])

        body = ctk.CTkFrame(dialog, fg_color=_THEME["card"], corner_radius=12, border_width=1, border_color=_THEME["card_border"])
        body.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(
            body, text="Allocate Teaching Assignment", font=("Georgia", 20, "bold"), text_color=_THEME["text_dark"]
        ).pack(anchor="w", padx=24, pady=(20, 4))
        ctk.CTkLabel(
            body, text="Connect a verified teacher to a subject, course, semester, and section.", font=("Segoe UI", 11), text_color=_THEME["text_muted"]
        ).pack(anchor="w", padx=24, pady=(0, 16))

        teachers = admin_service.list_teachers(self.user.role)
        subjects = admin_service.list_subjects(self.user.role)
        courses = admin_service.list_courses(self.user.role)

        teacher_map = {f"{row['emp_id']} - {row['name']}": str(row["id"]) for row in teachers}
        subject_map = {f"{row['code']} - {row['name']}": str(row["id"]) for row in subjects}
        course_map = {row["name"]: str(row["id"]) for row in courses}

        controls = {}
        for label, key, options in (
            ("Faculty Personnel", "teacher", list(teacher_map)),
            ("Curriculum Subject", "subject", list(subject_map)),
            ("Course Program", "course", list(course_map)),
        ):
            ctk.CTkLabel(body, text=label, font=("Segoe UI", 11, "bold"), text_color=_THEME["text_dark"]).pack(anchor="w", padx=24, pady=(4, 2))
            control = ctk.CTkComboBox(
                body,
                values=options or ["No options available"],
                width=420,
                height=36,
                fg_color=_THEME["card"],
                border_color=_THEME["card_border"],
                button_color=_THEME["primary"],
                dropdown_fg_color=_THEME["card"],
                text_color=_THEME["text_dark"],
                state="readonly",
            )
            if options:
                control.set(options[0])
            control.pack(padx=24, pady=(0, 10))
            controls[key] = control

        sem_sec_row = ctk.CTkFrame(body, fg_color="transparent")
        sem_sec_row.pack(fill="x", padx=24, pady=(2, 10))

        sem_box = ctk.CTkFrame(sem_sec_row, fg_color="transparent")
        sem_box.pack(side="left", fill="x", expand=True, padx=(0, 6))
        ctk.CTkLabel(sem_box, text="Semester", font=("Segoe UI", 11, "bold"), text_color=_THEME["text_dark"]).pack(anchor="w")
        semester = ctk.CTkComboBox(
            sem_box,
            values=[str(number) for number in range(1, 9)],
            height=36,
            fg_color=_THEME["card"],
            border_color=_THEME["card_border"],
            button_color=_THEME["primary"],
            dropdown_fg_color=_THEME["card"],
            text_color=_THEME["text_dark"],
            state="readonly",
        )
        semester.set("1")
        semester.pack(fill="x", pady=(2, 0))

        sec_box = ctk.CTkFrame(sem_sec_row, fg_color="transparent")
        sec_box.pack(side="left", fill="x", expand=True, padx=(6, 0))
        ctk.CTkLabel(sec_box, text="Section", font=("Segoe UI", 11, "bold"), text_color=_THEME["text_dark"]).pack(anchor="w")
        section = ctk.CTkComboBox(
            sec_box,
            values=["A", "B", "C", "D", "E"],
            height=36,
            fg_color=_THEME["card"],
            border_color=_THEME["card_border"],
            button_color=_THEME["primary"],
            dropdown_fg_color=_THEME["card"],
            text_color=_THEME["text_dark"],
            state="readonly",
        )
        section.set("A")
        section.pack(fill="x", pady=(2, 0))

        feedback = ctk.CTkLabel(body, text="", font=("Segoe UI", 11), wraplength=420, justify="left")
        feedback.pack(anchor="w", padx=24, pady=(0, 8))

        def save():
            try:
                admin_service.save_assignment(
                    self.user.role,
                    teacher_map.get(controls["teacher"].get(), ""),
                    subject_map.get(controls["subject"].get(), ""),
                    course_map.get(controls["course"].get(), ""),
                    semester.get(),
                    section.get(),
                )
                self._toast("Teaching assignment committed.")
                dialog.destroy()
                self.show_assignments()
            except admin_service.AdminServiceError as error:
                feedback.configure(text=f"✕ {error}", text_color=_THEME["crimson"])

        ctk.CTkButton(
            body,
            text="Commit Teaching Assignment",
            command=save,
            width=420,
            height=40,
            font=("Segoe UI", 12, "bold"),
            fg_color=_THEME["primary"],
            hover_color=_THEME["primary_dark"],
            text_color="#FFFFFF",
        ).pack(padx=24, pady=(8, 20))

    # ------------------------------------------------------------------
    # Bulk Data Ingestion Center
    # ------------------------------------------------------------------
    def show_import(self):
        self._clear_content()
        self._update_nav_highlight("Import")
        self._header("BULK INGESTION // DATA IMPORT", "Batch import student or faculty records from CSV / Excel spreadsheets.")

        container = ctk.CTkFrame(self.content, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=32, pady=(0, 24))

        row = ctk.CTkFrame(container, fg_color="transparent")
        row.pack(fill="x", pady=(0, 16))

        for title, record_type, icon, desc, template_cols, color in (
            ("Student Roster Ingest", "students", "⬢", "Batch register student accounts with roll numbers, names, DOB, and semester assignments.", "Required columns: roll_no, name, dob, course, semester, section, email", _THEME["primary"]),
            ("Faculty Personnel Ingest", "teachers", "⬡", "Batch register faculty members with employee IDs, departments, DOB, and emails.", "Required columns: emp_id, name, dob, department, email", _THEME["emerald"]),
        ):
            box = ctk.CTkFrame(row, fg_color=_THEME["card"], corner_radius=12, border_width=1, border_color=_THEME["card_border"])
            box.pack(side="left", fill="both", expand=True, padx=6)

            ctk.CTkFrame(box, height=4, fg_color=color, corner_radius=2).pack(fill="x", padx=16, pady=(12, 10))

            h_row = ctk.CTkFrame(box, fg_color="transparent")
            h_row.pack(fill="x", padx=18)
            ctk.CTkLabel(h_row, text=icon, font=("Segoe UI", 18, "bold"), text_color=color).pack(side="left", padx=(0, 8))
            ctk.CTkLabel(h_row, text=title, font=("Georgia", 15, "bold"), text_color=_THEME["text_dark"]).pack(side="left")

            ctk.CTkLabel(
                box, text=desc, font=("Segoe UI", 11), text_color=_THEME["text_body"], wraplength=380, justify="left"
            ).pack(anchor="w", padx=18, pady=(8, 6))

            t_box = ctk.CTkFrame(box, fg_color=_THEME["card_alt"], corner_radius=6, border_width=1, border_color=_THEME["card_border"])
            t_box.pack(fill="x", padx=18, pady=(6, 16))
            ctk.CTkLabel(
                t_box, text=template_cols, font=("Consolas", 9), text_color=_THEME["text_muted"], wraplength=360, justify="left"
            ).pack(fill="x", padx=10, pady=8)

            def do_import(rtype=record_type):
                path = filedialog.askopenfilename(filetypes=[("Spreadsheet files", "*.csv *.xlsx *.xls")])
                if not path:
                    return
                try:
                    res = import_file(self.user.role, path, rtype)
                    err_msg = ("\n" + "\n".join(res.errors[:4])) if res.errors else ""
                    self._toast(f"Ingest complete: {res.added} records committed, {res.skipped} skipped.{err_msg}")
                except Exception as error:
                    self._toast(str(error), error=True)

            ctk.CTkButton(
                box,
                text=f"Select & Ingest {record_type.capitalize()} File",
                command=do_import,
                height=38,
                font=("Segoe UI", 11, "bold"),
                fg_color=color,
                hover_color=_THEME["primary_dark"],
                text_color="#FFFFFF",
            ).pack(fill="x", padx=18, pady=(0, 18))

    # ------------------------------------------------------------------
    # Security & Audit Logs Viewer
    # ------------------------------------------------------------------
    def show_audit_logs(self):
        self._clear_content()
        self._update_nav_highlight("Audit Logs")
        logs = admin_service.list_audit_logs(self.user.role, limit=100)
        self._header("AUDIT RADAR // SECURITY & REVISION LOGS", f"Tracking immutable attendance corrections and security state ({len(logs)} events).")

        columns = [
            ("id", "Log ID", 65),
            ("attendance_id", "Attendance #", 100),
            ("old_status", "Old Status", 100),
            ("new_status", "New Status", 100),
            ("reason", "Revision Reason", 220),
            ("changed_by_user", "Modified By", 110),
            ("changed_at", "Timestamp", 160),
        ]
        self._tree(columns, [dict(r) for r in logs])

    # ------------------------------------------------------------------
    # Reports & Analytics Hub
    # ------------------------------------------------------------------
    def show_reports(self):
        from ui.report_window import open_report_window
        open_report_window(self, self.user)

    # ------------------------------------------------------------------
    # Database Backup & Snapshots
    # ------------------------------------------------------------------
    def show_backup(self):
        self._clear_content()
        self._update_nav_highlight("Backup")
        self._header("SNAPSHOTS // DATABASE BACKUP & RESTORE", "Create point-in-time snapshots of the Presenza SQLite engine.")

        box = ctk.CTkFrame(self.content, fg_color=_THEME["card"], corner_radius=12, border_width=1, border_color=_THEME["card_border"])
        box.pack(fill="x", padx=32, pady=(0, 16))

        h_row = ctk.CTkFrame(box, fg_color="transparent")
        h_row.pack(fill="x", padx=22, pady=(20, 4))
        ctk.CTkLabel(h_row, text="💾 Instant Live Snapshot", font=("Georgia", 16, "bold"), text_color=_THEME["text_dark"]).pack(side="left")

        ctk.CTkLabel(
            box,
            text="Generates an isolated timestamped copy of the live database in the /backups directory without downtime.",
            font=("Segoe UI", 11),
            text_color=_THEME["text_body"],
        ).pack(anchor="w", padx=22, pady=(0, 14))

        def take_backup():
            try:
                from utils.backup import create_database_backup
                path = create_database_backup(self.user.role)
                self._toast(f"Snapshot secured: {Path(path).name}")
                self.show_backup()
            except Exception as error:
                self._toast(f"Backup failed: {error}", error=True)

        ctk.CTkButton(
            box,
            text="Create Point-in-Time Database Backup",
            font=("Segoe UI", 11, "bold"),
            fg_color=_THEME["primary"],
            hover_color=_THEME["primary_dark"],
            text_color="#FFFFFF",
            height=38,
            command=take_backup,
        ).pack(anchor="w", padx=22, pady=(0, 20))

        # Backup History Table
        backups = admin_service.list_backups_info(self.user.role)
        ctk.CTkLabel(self.content, text="SNAPSHOT VAULT // RECENT BACKUPS", font=("Consolas", 11, "bold"), text_color=_THEME["primary"]).pack(anchor="w", padx=32, pady=(4, 8))

        columns = [
            ("name", "Snapshot File", 300),
            ("size_kb", "Size (KB)", 90),
            ("modified", "Creation Timestamp", 180),
            ("path", "Absolute Path", 380),
        ]
        self._tree(columns, backups)

    # ------------------------------------------------------------------
    # System Policy & Governance Settings
    # ------------------------------------------------------------------
    def show_settings(self):
        self._clear_content()
        self._update_nav_highlight("Settings")
        self._header("GOVERNANCE // POLICY CONFIGURATION", "Institutional rules governing attendance calculation, grace windows, and defaulter radar.")

        try:
            settings = admin_service.get_settings(self.user.role)
            current_threshold = settings.get("min_attendance", "75")
        except admin_service.AdminServiceError as error:
            self._toast(str(error), error=True)
            return

        box = ctk.CTkFrame(self.content, fg_color=_THEME["card"], corner_radius=12, border_width=1, border_color=_THEME["card_border"])
        box.pack(anchor="w", padx=32, pady=(0, 16))

        ctk.CTkLabel(
            box, text="Institutional Attendance Minimum Threshold", font=("Georgia", 15, "bold"), text_color=_THEME["text_dark"]
        ).pack(anchor="w", padx=24, pady=(22, 4))

        ctk.CTkLabel(
            box,
            text="Students whose attendance rate falls below this threshold are flagged on the Defaulter Radar.",
            font=("Segoe UI", 11),
            text_color=_THEME["text_muted"],
        ).pack(anchor="w", padx=24, pady=(0, 14))

        entry_row = ctk.CTkFrame(box, fg_color="transparent")
        entry_row.pack(anchor="w", padx=24, pady=(0, 18))

        entry = ctk.CTkEntry(
            entry_row,
            width=180,
            height=38,
            font=("Consolas", 13, "bold"),
            fg_color=_THEME["card"],
            border_color=_THEME["card_border"],
            text_color=_THEME["text_dark"],
        )
        entry.insert(0, current_threshold)
        entry.pack(side="left", padx=(0, 10))

        ctk.CTkLabel(entry_row, text="%", font=("Consolas", 14, "bold"), text_color=_THEME["primary"]).pack(side="left")

        def save_policy():
            try:
                admin_service.save_minimum_attendance(self.user.role, entry.get())
                self._toast("Institutional threshold policy committed.")
            except admin_service.AdminServiceError as error:
                self._toast(str(error), error=True)

        ctk.CTkButton(
            box,
            text="Commit Policy Change",
            font=("Segoe UI", 11, "bold"),
            fg_color=_THEME["primary"],
            hover_color=_THEME["primary_dark"],
            text_color="#FFFFFF",
            height=38,
            command=save_policy,
        ).pack(anchor="w", padx=24, pady=(0, 22))
