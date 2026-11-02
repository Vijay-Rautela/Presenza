"""Teacher attendance workspace with a modern, data-rich dashboard.

All database work stays in service modules. The UI only reads and
displays the data returned by attendance_service and report_service.
"""

from datetime import date, datetime
import tkinter as tk
from tkinter import ttk

import customtkinter as ctk

from config import COLORS


# Extended palette for the teacher portal. These supplement config.COLORS
# without touching global state, so other portals are unaffected.
_T = {
    "sidebar":       "#0D2E1F",
    "sidebar_hover": "#174D34",
    "sidebar_sel":   "#1B874B",
    "card":          "#FFFFFF",
    "card_border":   "#D5E2D9",
    "header_bg":     "#EBE7DC",
    "stat_green":    "#1B874B",
    "stat_amber":    "#C4881C",
    "stat_red":      "#DC3545",
    "stat_blue":     "#1E7E9E",
    "tag_green_bg":  "#E8F5EE",
    "tag_green_fg":  "#1B874B",
    "tag_amber_bg":  "#FFF3CD",
    "tag_amber_fg":  "#7A5A00",
    "tag_red_bg":    "#FDECEA",
    "tag_red_fg":    "#B02A37",
    "tag_blue_bg":   "#E3EFF7",
    "tag_blue_fg":   "#1F4E6E",
    "divider":       "#E2DDD5",
    "row_alt":       "#F8F6F2",
    "icon_muted":    "#8A9A90",
}

# Sidebar navigation items: (label, icon_char)
# Using Unicode geometric and misc symbols instead of emoji
_NAV_ITEMS = [
    ("Dashboard",       "\u25A3"),   # filled square with vert line
    ("Mark attendance",  "\u2713"),   # check mark
    ("Corrections",     "\u270E"),   # pencil
    ("Leave requests",  "\u2691"),   # flag
    ("Reports",         "\u2637"),   # trigram
]


class TeacherPortalView(ctk.CTkFrame):
    """A polished Teacher workspace with a data-rich dashboard and
    consistent card-based layouts across every page."""

    def __init__(self, master, user, on_logout):
        super().__init__(master, fg_color=COLORS["background"], corner_radius=0)
        self.user = user
        self.on_logout = on_logout
        self.assignments = []
        self.assignment_lookup = {}
        self.status_controls = []
        self.active_page = None
        self.nav_buttons = {}
        self.status_bar = None
        self._build_shell()
        self.show_page("Dashboard")

    # ------------------------------------------------------------------
    # Shell: sidebar + header + content area + status bar
    # ------------------------------------------------------------------

    def _build_shell(self):
        self.pack(fill="both", expand=True)

        # --- Sidebar ---
        side = ctk.CTkFrame(self, width=240, fg_color=_T["sidebar"], corner_radius=0)
        side.pack(side="left", fill="y")
        side.pack_propagate(False)

        # Brand block
        brand = ctk.CTkFrame(side, fg_color="transparent")
        brand.pack(fill="x", padx=22, pady=(28, 6))
        ctk.CTkLabel(
            brand, text="Presenza",
            font=("Georgia", 24, "bold"), text_color="#FFFFFF",
        ).pack(anchor="w")
        ctk.CTkLabel(
            brand, text="TEACHER",
            font=("Segoe UI", 10, "bold"), text_color="#8FA589",
        ).pack(anchor="w", pady=(2, 0))

        # Divider
        ctk.CTkFrame(side, height=1, fg_color="#3D5038", corner_radius=0).pack(
            fill="x", padx=18, pady=(18, 14)
        )

        # Navigation buttons
        for label, icon in _NAV_ITEMS:
            btn = ctk.CTkButton(
                side,
                text=f"  {icon}   {label}",
                anchor="w",
                font=("Segoe UI", 13),
                command=lambda p=label: self.show_page(p),
                fg_color="transparent",
                hover_color=_T["sidebar_hover"],
                text_color="#C5CFC2",
                height=42,
                corner_radius=8,
            )
            btn.pack(fill="x", padx=12, pady=2)
            self.nav_buttons[label] = btn

        # User card at bottom
        spacer = ctk.CTkFrame(side, fg_color="transparent")
        spacer.pack(fill="both", expand=True)

        user_card = ctk.CTkFrame(side, fg_color="#3D5038", corner_radius=10)
        user_card.pack(fill="x", padx=14, pady=(0, 12))
        # Avatar circle
        avatar = ctk.CTkFrame(user_card, width=36, height=36, fg_color="#5A7C53", corner_radius=18)
        avatar.pack(side="left", padx=(12, 10), pady=12)
        avatar.pack_propagate(False)
        initials = "".join(w[0].upper() for w in self.user.display_name.split()[:2])
        ctk.CTkLabel(
            avatar, text=initials, font=("Segoe UI", 12, "bold"), text_color="#FFFFFF",
        ).place(relx=0.5, rely=0.5, anchor="center")
        # Name and role
        info = ctk.CTkFrame(user_card, fg_color="transparent")
        info.pack(side="left", fill="x", expand=True, pady=10)
        ctk.CTkLabel(
            info, text=self.user.display_name,
            font=("Segoe UI", 12, "bold"), text_color="#E8E3DB",
            anchor="w",
        ).pack(anchor="w")
        ctk.CTkLabel(
            info, text=self.user.login_id,
            font=("Segoe UI", 10), text_color="#8FA589", anchor="w",
        ).pack(anchor="w")

        ctk.CTkButton(
            side, text="Sign out", command=self.on_logout,
            fg_color="transparent", hover_color=_T["sidebar_hover"],
            border_width=1, border_color="#5A7C53",
            text_color="#C5CFC2", height=38, corner_radius=8,
        ).pack(fill="x", padx=14, pady=(4, 18))

        # --- Main area (right side) ---
        main = ctk.CTkFrame(self, fg_color=COLORS["background"], corner_radius=0)
        main.pack(side="left", fill="both", expand=True)

        # Top header bar
        self.header = ctk.CTkFrame(main, height=60, fg_color=_T["header_bg"], corner_radius=0)
        self.header.pack(fill="x")
        self.header.pack_propagate(False)
        self.header_title = ctk.CTkLabel(
            self.header, text="Dashboard",
            font=("Georgia", 20, "bold"), text_color=COLORS["text"],
        )
        self.header_title.pack(side="left", padx=30, pady=14)

        today_str = datetime.now().strftime("%A, %d %B %Y")
        ctk.CTkLabel(
            self.header, text=today_str,
            font=("Segoe UI", 11), text_color=_T["icon_muted"],
        ).pack(side="right", padx=30)

        # Status banner (hidden by default)
        self.status_bar = ctk.CTkFrame(main, height=0, fg_color=_T["tag_green_bg"], corner_radius=0)
        self.status_bar.pack(fill="x")
        self.status_bar.pack_propagate(False)
        self.status_label = ctk.CTkLabel(
            self.status_bar, text="",
            font=("Segoe UI", 12), text_color=_T["tag_green_fg"],
        )
        self.status_label.pack(side="left", padx=30, pady=8)
        self.status_dismiss = ctk.CTkButton(
            self.status_bar, text="\u2715", width=30, height=24,
            fg_color="transparent", hover_color=_T["divider"],
            text_color=_T["icon_muted"],
            command=self._dismiss_status,
        )
        self.status_dismiss.pack(side="right", padx=16)

        # Content area
        self.content = ctk.CTkFrame(main, fg_color=COLORS["background"], corner_radius=0)
        self.content.pack(fill="both", expand=True)

    def _set_active_nav(self, page):
        """Visually highlight the active sidebar button."""
        for label, btn in self.nav_buttons.items():
            if label == page:
                btn.configure(fg_color=_T["sidebar_sel"], text_color="#FFFFFF")
            else:
                btn.configure(fg_color="transparent", text_color="#C5CFC2")

    def _show_status(self, text, is_error=False):
        """Show the floating status banner with success or error styling."""
        if is_error:
            self.status_bar.configure(fg_color=_T["tag_red_bg"])
            self.status_label.configure(text_color=_T["tag_red_fg"])
        else:
            self.status_bar.configure(fg_color=_T["tag_green_bg"])
            self.status_label.configure(text_color=_T["tag_green_fg"])
        self.status_label.configure(text=text)
        self.status_bar.configure(height=40)

    def _dismiss_status(self):
        self.status_bar.configure(height=0)

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def _clear(self):
        for child in self.content.winfo_children():
            child.destroy()
        self.status_controls = []
        self._dismiss_status()

    def show_page(self, page):
        self.active_page = page
        self._set_active_nav(page)
        self.header_title.configure(text=page)
        if page == "Dashboard":
            self.show_dashboard()
        elif page == "Mark attendance":
            self.show_marking()
        elif page == "Corrections":
            self.show_corrections()
        elif page == "Leave requests":
            self.show_leaves()
        else:
            self.show_reports()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _load_assignments(self):
        from services import attendance_service
        self.assignments = attendance_service.list_assignments(self.user.id)
        self.assignment_lookup = {
            self._assignment_label(row): row["id"] for row in self.assignments
        }
        return list(self.assignment_lookup)

    @staticmethod
    def _assignment_label(row):
        return f"{row['code']}  \u00B7  {row['subject']}  \u00B7  Sem {row['semester']}  \u00B7  Sec {row['section']}"

    def _assignment_picker(self, parent):
        values = self._load_assignments()
        variable = ctk.StringVar(
            value=values[0] if values else "No assignments available"
        )
        picker = ctk.CTkComboBox(
            parent,
            values=values or ["No assignments available"],
            variable=variable,
            width=460,
            height=38,
            fg_color=COLORS["surface"],
            border_color=_T["card_border"],
            button_color=COLORS["primary"],
            button_hover_color=COLORS["primary_dark"],
            dropdown_fg_color=COLORS["surface"],
            dropdown_hover_color=_T["header_bg"],
            dropdown_text_color=COLORS["text"],
            font=("Segoe UI", 12),
            state="readonly",
        )
        picker.pack(side="left", padx=(0, 10))
        return variable

    # ------------------------------------------------------------------
    # Card builders
    # ------------------------------------------------------------------

    def _stat_card(self, parent, value, label, color, tag_bg, tag_fg, row=0, col=0):
        """A single metric card with a coloured accent bar at top."""
        card = ctk.CTkFrame(
            parent, fg_color=_T["card"], corner_radius=12,
            border_width=1, border_color=_T["card_border"],
        )
        card.grid(row=row, column=col, sticky="nsew", padx=8, pady=8)

        # Accent bar
        accent = ctk.CTkFrame(card, height=4, fg_color=color, corner_radius=2)
        accent.pack(fill="x", padx=16, pady=(14, 0))

        ctk.CTkLabel(
            card, text=str(value),
            font=("Georgia", 32, "bold"), text_color=color,
        ).pack(anchor="w", padx=20, pady=(12, 2))

        ctk.CTkLabel(
            card, text=label,
            font=("Segoe UI", 12), text_color=_T["icon_muted"],
        ).pack(anchor="w", padx=20, pady=(0, 16))

        return card

    def _section_title(self, parent, text):
        ctk.CTkLabel(
            parent, text=text,
            font=("Georgia", 16, "bold"), text_color=COLORS["text"],
        ).pack(anchor="w", padx=4, pady=(18, 8))

    # ------------------------------------------------------------------
    # Status colour helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _status_colours(status: str) -> tuple[str, str]:
        """Return meaningful fg and hover colours for attendance status."""
        if status == "Absent":
            return _T["stat_red"], "#7F2E26"
        if status == "Late":
            return _T["stat_amber"], "#8E6B00"
        return _T["stat_green"], COLORS["primary_dark"]

    def _status_menu(self, parent, variable):
        """Create a status selector that changes colour with the value."""
        foreground, hover = self._status_colours(variable.get())
        menu = ctk.CTkOptionMenu(
            parent,
            values=["Present", "Absent", "Late"],
            variable=variable,
            width=120,
            height=32,
            fg_color=foreground,
            button_color=hover,
            corner_radius=6,
            font=("Segoe UI", 11, "bold"),
        )

        def recolour(selected):
            fg, hv = self._status_colours(selected)
            menu.configure(fg_color=fg, button_color=hv)

        menu.configure(command=recolour)
        return menu

    # ------------------------------------------------------------------
    # DASHBOARD (the hero page)
    # ------------------------------------------------------------------

    def show_dashboard(self):
        from services import attendance_service, report_service
        self._clear()

        scroll = ctk.CTkScrollableFrame(
            self.content, fg_color=COLORS["background"],
            corner_radius=0, scrollbar_button_color=_T["divider"],
        )
        scroll.pack(fill="both", expand=True, padx=0, pady=0)

        # --- Greeting banner ---
        greeting = ctk.CTkFrame(scroll, fg_color=_T["card"], corner_radius=14,
                                border_width=1, border_color=_T["card_border"])
        greeting.pack(fill="x", padx=28, pady=(20, 6))

        hour = datetime.now().hour
        if hour < 12:
            greet_text = "Good morning"
        elif hour < 17:
            greet_text = "Good afternoon"
        else:
            greet_text = "Good evening"

        g_left = ctk.CTkFrame(greeting, fg_color="transparent")
        g_left.pack(side="left", fill="x", expand=True, padx=24, pady=20)

        ctk.CTkLabel(
            g_left, text=f"{greet_text}, {self.user.display_name}",
            font=("Georgia", 22, "bold"), text_color=COLORS["text"],
        ).pack(anchor="w")
        ctk.CTkLabel(
            g_left,
            text="Your classes are ready. Here is a snapshot of today's attendance activity.",
            font=("Segoe UI", 12), text_color=_T["icon_muted"],
        ).pack(anchor="w", pady=(4, 0))

        # Quick action buttons on right
        g_right = ctk.CTkFrame(greeting, fg_color="transparent")
        g_right.pack(side="right", padx=24, pady=16)
        ctk.CTkButton(
            g_right, text="\u2713  Mark attendance",
            command=lambda: self.show_page("Mark attendance"),
            fg_color=COLORS["primary"], hover_color=COLORS["primary_dark"],
            height=38, corner_radius=8, font=("Segoe UI", 12, "bold"),
        ).pack(side="left", padx=4)
        ctk.CTkButton(
            g_right, text="\u270E  Corrections",
            command=lambda: self.show_page("Corrections"),
            fg_color="transparent", hover_color=_T["header_bg"],
            border_width=1, border_color=COLORS["primary"],
            text_color=COLORS["primary"],
            height=38, corner_radius=8, font=("Segoe UI", 12),
        ).pack(side="left", padx=4)

        # --- Load live data ---
        try:
            assignments = self._load_assignments()
        except attendance_service.AttendanceServiceError:
            assignments = []

        # Stats from the database
        try:
            student_rows = report_service.student_report("Teacher", self.user.id)
        except Exception:
            student_rows = []

        try:
            subject_rows = report_service.subject_report("Teacher", self.user.id)
        except Exception:
            subject_rows = []

        try:
            pending_leaves = attendance_service.pending_leave_requests(self.user.id)
        except Exception:
            pending_leaves = []

        # Derive dashboard numbers
        total_students = len(student_rows)
        overall_pct = (
            round(sum(r["percentage"] for r in student_rows) / len(student_rows), 1)
            if student_rows else 0
        )
        below_75 = sum(1 for r in student_rows if r["percentage"] < 75)
        pending_count = len(pending_leaves)

        # --- Metric cards row ---
        cards_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        cards_frame.pack(fill="x", padx=20, pady=(6, 0))
        for i in range(4):
            cards_frame.grid_columnconfigure(i, weight=1)

        self._stat_card(
            cards_frame, len(assignments), "Assigned classes",
            _T["stat_blue"], _T["tag_blue_bg"], _T["tag_blue_fg"],
            row=0, col=0,
        )
        self._stat_card(
            cards_frame, total_students, "Total students",
            _T["stat_green"], _T["tag_green_bg"], _T["tag_green_fg"],
            row=0, col=1,
        )
        self._stat_card(
            cards_frame, f"{overall_pct}%", "Average attendance",
            _T["stat_amber"] if overall_pct < 85 else _T["stat_green"],
            _T["tag_amber_bg"], _T["tag_amber_fg"],
            row=0, col=2,
        )
        self._stat_card(
            cards_frame, below_75, "Below threshold",
            _T["stat_red"] if below_75 > 0 else _T["stat_green"],
            _T["tag_red_bg"], _T["tag_red_fg"],
            row=0, col=3,
        )

        # --- Two-column middle section ---
        mid = ctk.CTkFrame(scroll, fg_color="transparent")
        mid.pack(fill="x", padx=28, pady=(12, 0))
        mid.grid_columnconfigure(0, weight=3)
        mid.grid_columnconfigure(1, weight=2)

        # Left: Subject-wise attendance breakdown
        subj_card = ctk.CTkFrame(
            mid, fg_color=_T["card"], corner_radius=12,
            border_width=1, border_color=_T["card_border"],
        )
        subj_card.grid(row=0, column=0, sticky="nsew", padx=(0, 8), pady=8)

        ctk.CTkLabel(
            subj_card, text="Subject-wise attendance",
            font=("Georgia", 15, "bold"), text_color=COLORS["text"],
        ).pack(anchor="w", padx=20, pady=(18, 12))

        if subject_rows:
            for i, row in enumerate(subject_rows):
                row_frame = ctk.CTkFrame(
                    subj_card,
                    fg_color=_T["row_alt"] if i % 2 == 0 else _T["card"],
                    corner_radius=6,
                )
                row_frame.pack(fill="x", padx=14, pady=2)

                ctk.CTkLabel(
                    row_frame,
                    text=f"{row['code']}  \u00B7  {row['subject']}",
                    font=("Segoe UI", 12), text_color=COLORS["text"],
                    anchor="w",
                ).pack(side="left", padx=12, pady=10)

                pct = row["percentage"]
                if pct >= 85:
                    tag_bg, tag_fg = _T["tag_green_bg"], _T["tag_green_fg"]
                elif pct >= 75:
                    tag_bg, tag_fg = _T["tag_amber_bg"], _T["tag_amber_fg"]
                else:
                    tag_bg, tag_fg = _T["tag_red_bg"], _T["tag_red_fg"]

                tag = ctk.CTkFrame(row_frame, fg_color=tag_bg, corner_radius=6)
                tag.pack(side="right", padx=12, pady=8)
                ctk.CTkLabel(
                    tag, text=f" {pct}% ",
                    font=("Segoe UI", 11, "bold"), text_color=tag_fg,
                ).pack(padx=6, pady=2)

                # Visual bar
                bar_bg = ctk.CTkFrame(row_frame, width=120, height=8,
                                      fg_color=_T["divider"], corner_radius=4)
                bar_bg.pack(side="right", padx=(0, 6), pady=10)
                bar_bg.pack_propagate(False)
                bar_fill = ctk.CTkFrame(
                    bar_bg, height=8,
                    fg_color=tag_fg, corner_radius=4,
                )
                bar_fill.place(x=0, y=0, relwidth=min(pct / 100, 1.0), relheight=1.0)
        else:
            ctk.CTkLabel(
                subj_card,
                text="No attendance data recorded yet.",
                font=("Segoe UI", 12), text_color=_T["icon_muted"],
            ).pack(anchor="w", padx=20, pady=(0, 18))

        # Add total row
        if subject_rows:
            total_attended = sum(r["attended"] for r in subject_rows)
            total_total = sum(r["total"] for r in subject_rows)
            total_pct = round((total_attended / total_total) * 100, 1) if total_total else 0

            total_frame = ctk.CTkFrame(subj_card, fg_color=_T["header_bg"], corner_radius=8)
            total_frame.pack(fill="x", padx=14, pady=(8, 16))
            ctk.CTkLabel(
                total_frame, text="Overall",
                font=("Segoe UI", 12, "bold"), text_color=COLORS["text"],
            ).pack(side="left", padx=12, pady=10)
            ctk.CTkLabel(
                total_frame,
                text=f"{total_attended} / {total_total} records  \u00B7  {total_pct}%",
                font=("Segoe UI", 12, "bold"), text_color=COLORS["primary"],
            ).pack(side="right", padx=12, pady=10)

        # Right: Pending leave requests + assignment list
        right_col = ctk.CTkFrame(mid, fg_color="transparent")
        right_col.grid(row=0, column=1, sticky="nsew", padx=(8, 0), pady=0)

        # Pending leaves card
        leave_card = ctk.CTkFrame(
            right_col, fg_color=_T["card"], corner_radius=12,
            border_width=1, border_color=_T["card_border"],
        )
        leave_card.pack(fill="x", pady=(8, 6))

        leave_header = ctk.CTkFrame(leave_card, fg_color="transparent")
        leave_header.pack(fill="x", padx=20, pady=(16, 10))
        ctk.CTkLabel(
            leave_header, text="Pending leave requests",
            font=("Georgia", 14, "bold"), text_color=COLORS["text"],
        ).pack(side="left")

        if pending_count > 0:
            count_badge = ctk.CTkFrame(leave_header, fg_color=_T["tag_red_bg"], corner_radius=10)
            count_badge.pack(side="right")
            ctk.CTkLabel(
                count_badge, text=f" {pending_count} ",
                font=("Segoe UI", 10, "bold"), text_color=_T["tag_red_fg"],
            ).pack(padx=6, pady=2)

        if pending_leaves:
            for leave in pending_leaves[:5]:
                l_row = ctk.CTkFrame(leave_card, fg_color="transparent")
                l_row.pack(fill="x", padx=16, pady=3)
                ctk.CTkLabel(
                    l_row,
                    text=f"{leave['roll_no']}  \u00B7  {leave['name']}",
                    font=("Segoe UI", 11), text_color=COLORS["text"],
                    anchor="w",
                ).pack(side="left", padx=4)
                ctk.CTkLabel(
                    l_row,
                    text=f"{leave['from_date']}",
                    font=("Segoe UI", 10), text_color=_T["icon_muted"],
                ).pack(side="right", padx=4)
            if pending_count > 5:
                ctk.CTkLabel(
                    leave_card,
                    text=f"+ {pending_count - 5} more requests",
                    font=("Segoe UI", 10), text_color=_T["icon_muted"],
                ).pack(anchor="w", padx=20, pady=(0, 4))
            ctk.CTkButton(
                leave_card, text="Review all requests",
                command=lambda: self.show_page("Leave requests"),
                fg_color="transparent", hover_color=_T["header_bg"],
                border_width=1, border_color=COLORS["primary"],
                text_color=COLORS["primary"], height=32, corner_radius=6,
                font=("Segoe UI", 11),
            ).pack(anchor="w", padx=20, pady=(6, 16))
        else:
            ctk.CTkLabel(
                leave_card,
                text="No pending requests right now.",
                font=("Segoe UI", 11), text_color=_T["icon_muted"],
            ).pack(anchor="w", padx=20, pady=(0, 16))

        # Assignments card
        assign_card = ctk.CTkFrame(
            right_col, fg_color=_T["card"], corner_radius=12,
            border_width=1, border_color=_T["card_border"],
        )
        assign_card.pack(fill="x", pady=(6, 8))

        ctk.CTkLabel(
            assign_card, text="Your assignments",
            font=("Georgia", 14, "bold"), text_color=COLORS["text"],
        ).pack(anchor="w", padx=20, pady=(16, 10))

        if assignments:
            for i, item in enumerate(assignments):
                a_row = ctk.CTkFrame(
                    assign_card,
                    fg_color=_T["row_alt"] if i % 2 == 0 else _T["card"],
                    corner_radius=6,
                )
                a_row.pack(fill="x", padx=14, pady=2)
                ctk.CTkLabel(
                    a_row, text=item,
                    font=("Segoe UI", 11), text_color=COLORS["text"],
                    anchor="w",
                ).pack(anchor="w", padx=10, pady=8)
        else:
            ctk.CTkLabel(
                assign_card,
                text="No assignments found for this account.",
                font=("Segoe UI", 11), text_color=_T["icon_muted"],
            ).pack(anchor="w", padx=20, pady=(0, 16))

        # Bottom spacer
        ctk.CTkFrame(assign_card, height=8, fg_color="transparent").pack()

        # --- Defaulter alert strip ---
        if below_75 > 0:
            alert = ctk.CTkFrame(
                scroll, fg_color=_T["tag_red_bg"], corner_radius=10,
                border_width=1, border_color="#E8B4AE",
            )
            alert.pack(fill="x", padx=28, pady=(12, 8))
            ctk.CTkLabel(
                alert,
                text=f"\u26A0  {below_75} student(s) are below the 75% attendance threshold and may be flagged as defaulters.",
                font=("Segoe UI", 12), text_color=_T["tag_red_fg"],
            ).pack(anchor="w", padx=20, pady=14)

    # ------------------------------------------------------------------
    # MARK ATTENDANCE
    # ------------------------------------------------------------------

    def show_marking(self):
        from services import attendance_service
        self._clear()

        # Controls bar
        controls = ctk.CTkFrame(
            self.content, fg_color=_T["card"], corner_radius=12,
            border_width=1, border_color=_T["card_border"],
        )
        controls.pack(fill="x", padx=28, pady=(20, 8))

        ctrl_inner = ctk.CTkFrame(controls, fg_color="transparent")
        ctrl_inner.pack(fill="x", padx=20, pady=16)

        ctk.CTkLabel(
            ctrl_inner, text="Class",
            font=("Segoe UI", 11, "bold"), text_color=_T["icon_muted"],
        ).pack(side="left", padx=(0, 8))
        assignment_var = self._assignment_picker(ctrl_inner)

        ctk.CTkLabel(
            ctrl_inner, text="Date",
            font=("Segoe UI", 11, "bold"), text_color=_T["icon_muted"],
        ).pack(side="left", padx=(16, 8))
        date_entry = ctk.CTkEntry(
            ctrl_inner, width=130, height=38,
            fg_color=COLORS["surface"], border_color=_T["card_border"],
            font=("Segoe UI", 12),
        )
        date_entry.insert(0, date.today().isoformat())
        date_entry.pack(side="left", padx=(0, 12))

        ctk.CTkButton(
            ctrl_inner, text="Load class",
            command=lambda: load(),
            fg_color=COLORS["primary"], hover_color=COLORS["primary_dark"],
            height=38, corner_radius=8, font=("Segoe UI", 12, "bold"),
        ).pack(side="left", padx=4)

        # Student list area
        list_frame = ctk.CTkScrollableFrame(
            self.content, fg_color=_T["card"], corner_radius=12,
            border_width=1, border_color=_T["card_border"],
            scrollbar_button_color=_T["divider"],
        )
        list_frame.pack(fill="both", expand=True, padx=28, pady=8)

        # Column headers
        header_row = ctk.CTkFrame(list_frame, fg_color=_T["header_bg"], corner_radius=6)
        header_row.pack(fill="x", padx=8, pady=(8, 4))
        ctk.CTkLabel(
            header_row, text="Roll No.  /  Student Name",
            font=("Segoe UI", 11, "bold"), text_color=_T["icon_muted"],
            anchor="w",
        ).pack(side="left", padx=12, pady=8)
        ctk.CTkLabel(
            header_row, text="Status",
            font=("Segoe UI", 11, "bold"), text_color=_T["icon_muted"],
        ).pack(side="right", padx=24, pady=8)

        # placeholder text
        placeholder = ctk.CTkLabel(
            list_frame,
            text="Select a class and click 'Load class' to begin marking attendance.",
            font=("Segoe UI", 12), text_color=_T["icon_muted"],
        )
        placeholder.pack(pady=40)

        # Actions bar
        actions = ctk.CTkFrame(self.content, fg_color="transparent")
        actions.pack(fill="x", padx=28, pady=(4, 16))
        ctk.CTkButton(
            actions, text="Mark all present",
            command=lambda: all_present(),
            fg_color="transparent", hover_color=_T["header_bg"],
            border_width=1, border_color=COLORS["primary"],
            text_color=COLORS["primary"],
            height=38, corner_radius=8, font=("Segoe UI", 12),
        ).pack(side="left")
        ctk.CTkButton(
            actions, text="Save attendance",
            command=lambda: save(),
            fg_color=COLORS["primary"], hover_color=COLORS["primary_dark"],
            height=38, corner_radius=8, font=("Segoe UI", 12, "bold"),
        ).pack(side="right")

        def load():
            for child in list_frame.winfo_children():
                child.destroy()
            self.status_controls = []
            try:
                assignment_id = self.assignment_lookup[assignment_var.get()]
                students = attendance_service.students_for_assignment(
                    self.user.id, assignment_id
                )
                # Re-add header
                h_row = ctk.CTkFrame(list_frame, fg_color=_T["header_bg"], corner_radius=6)
                h_row.pack(fill="x", padx=8, pady=(8, 4))
                ctk.CTkLabel(
                    h_row, text="Roll No.  /  Student Name",
                    font=("Segoe UI", 11, "bold"), text_color=_T["icon_muted"],
                    anchor="w",
                ).pack(side="left", padx=12, pady=8)
                ctk.CTkLabel(
                    h_row, text="Status",
                    font=("Segoe UI", 11, "bold"), text_color=_T["icon_muted"],
                ).pack(side="right", padx=24, pady=8)

                for i, student in enumerate(students):
                    row = ctk.CTkFrame(
                        list_frame,
                        fg_color=_T["row_alt"] if i % 2 == 0 else _T["card"],
                        corner_radius=6,
                    )
                    row.pack(fill="x", padx=8, pady=2)
                    ctk.CTkLabel(
                        row,
                        text=f"{student['roll_no']}    {student['name']}",
                        font=("Segoe UI", 12), text_color=COLORS["text"],
                        width=420, anchor="w",
                    ).pack(side="left", padx=12, pady=8)
                    status = ctk.StringVar(value="Present")
                    self._status_menu(row, status).pack(side="right", padx=12, pady=6)
                    self.status_controls.append((student["id"], status))
                self._show_status(f"{len(students)} students loaded. All start as Present.")
            except (KeyError, attendance_service.AttendanceServiceError) as error:
                self._show_status(str(error), is_error=True)

        def all_present():
            for _, control in self.status_controls:
                control.set("Present")

        def save():
            try:
                assignment_id = self.assignment_lookup[assignment_var.get()]
                total = attendance_service.mark_attendance(
                    self.user.id, assignment_id, date_entry.get(),
                    [(sid, ctrl.get()) for sid, ctrl in self.status_controls],
                )
                self._show_status(f"Attendance saved for {total} students.")
            except (KeyError, attendance_service.AttendanceServiceError) as error:
                self._show_status(str(error), is_error=True)

    # ------------------------------------------------------------------
    # CORRECTIONS
    # ------------------------------------------------------------------

    def show_corrections(self):
        from services import attendance_service
        self._clear()

        # Controls card
        controls = ctk.CTkFrame(
            self.content, fg_color=_T["card"], corner_radius=12,
            border_width=1, border_color=_T["card_border"],
        )
        controls.pack(fill="x", padx=28, pady=(20, 8))

        ctrl_inner = ctk.CTkFrame(controls, fg_color="transparent")
        ctrl_inner.pack(fill="x", padx=20, pady=16)

        ctk.CTkLabel(
            ctrl_inner, text="Class",
            font=("Segoe UI", 11, "bold"), text_color=_T["icon_muted"],
        ).pack(side="left", padx=(0, 8))
        assignment_var = self._assignment_picker(ctrl_inner)

        ctk.CTkLabel(
            ctrl_inner, text="Date",
            font=("Segoe UI", 11, "bold"), text_color=_T["icon_muted"],
        ).pack(side="left", padx=(16, 8))
        date_entry = ctk.CTkEntry(
            ctrl_inner, width=130, height=38,
            fg_color=COLORS["surface"], border_color=_T["card_border"],
            font=("Segoe UI", 12),
        )
        date_entry.insert(0, date.today().isoformat())
        date_entry.pack(side="left", padx=(0, 12))

        ctk.CTkButton(
            ctrl_inner, text="Load existing records",
            command=lambda: load(),
            fg_color=COLORS["primary"], hover_color=COLORS["primary_dark"],
            height=38, corner_radius=8, font=("Segoe UI", 12, "bold"),
        ).pack(side="left", padx=4)

        # Records area
        records_box = ctk.CTkScrollableFrame(
            self.content, fg_color=_T["card"], corner_radius=12,
            border_width=1, border_color=_T["card_border"],
            scrollbar_button_color=_T["divider"],
        )
        records_box.pack(fill="both", expand=True, padx=28, pady=8)

        placeholder = ctk.CTkLabel(
            records_box,
            text="Load existing attendance records to make corrections.",
            font=("Segoe UI", 12), text_color=_T["icon_muted"],
        )
        placeholder.pack(pady=40)

        # Reason + save
        bottom = ctk.CTkFrame(self.content, fg_color="transparent")
        bottom.pack(fill="x", padx=28, pady=(4, 16))

        reason = ctk.CTkEntry(
            bottom,
            placeholder_text="Reason for corrections (mandatory)",
            width=480, height=38,
            fg_color=COLORS["surface"], border_color=_T["card_border"],
            font=("Segoe UI", 12),
        )
        reason.pack(side="left")
        ctk.CTkButton(
            bottom, text="Save corrections",
            command=lambda: save(),
            fg_color=COLORS["primary"], hover_color=COLORS["primary_dark"],
            height=38, corner_radius=8, font=("Segoe UI", 12, "bold"),
        ).pack(side="right")

        def load():
            for child in records_box.winfo_children():
                child.destroy()
            self.status_controls = []
            try:
                records = attendance_service.existing_attendance(
                    self.user.id,
                    self.assignment_lookup[assignment_var.get()],
                    date_entry.get(),
                )

                # Header
                h_row = ctk.CTkFrame(records_box, fg_color=_T["header_bg"], corner_radius=6)
                h_row.pack(fill="x", padx=8, pady=(8, 4))
                ctk.CTkLabel(
                    h_row, text="Roll No.  /  Student Name",
                    font=("Segoe UI", 11, "bold"), text_color=_T["icon_muted"],
                    anchor="w",
                ).pack(side="left", padx=12, pady=8)
                ctk.CTkLabel(
                    h_row, text="Current Status",
                    font=("Segoe UI", 11, "bold"), text_color=_T["icon_muted"],
                ).pack(side="right", padx=24, pady=8)

                for i, record in enumerate(records):
                    row = ctk.CTkFrame(
                        records_box,
                        fg_color=_T["row_alt"] if i % 2 == 0 else _T["card"],
                        corner_radius=6,
                    )
                    row.pack(fill="x", padx=8, pady=2)
                    ctk.CTkLabel(
                        row,
                        text=f"{record['roll_no']}    {record['name']}",
                        font=("Segoe UI", 12), text_color=COLORS["text"],
                        width=400, anchor="w",
                    ).pack(side="left", padx=12, pady=8)
                    control = ctk.StringVar(value=record["status"])
                    self._status_menu(row, control).pack(side="right", padx=12, pady=6)
                    self.status_controls.append((record["id"], record["status"], control))

                self._show_status(f"{len(records)} existing records loaded.")
            except (KeyError, attendance_service.AttendanceServiceError) as error:
                self._show_status(str(error), is_error=True)

        def save():
            try:
                changed = 0
                for record_id, original, control in self.status_controls:
                    if control.get() != original:
                        attendance_service.edit_attendance(
                            self.user.id, record_id, control.get(), reason.get()
                        )
                        changed += 1
                if not changed:
                    raise attendance_service.AttendanceServiceError(
                        "Choose at least one changed status before saving."
                    )
                self._show_status(f"{changed} correction(s) saved in the audit log.")
            except attendance_service.AttendanceServiceError as error:
                self._show_status(str(error), is_error=True)

    # ------------------------------------------------------------------
    # LEAVE REQUESTS
    # ------------------------------------------------------------------

    def show_leaves(self):
        from services import attendance_service
        self._clear()

        # Wrapper card
        card = ctk.CTkFrame(
            self.content, fg_color=_T["card"], corner_radius=12,
            border_width=1, border_color=_T["card_border"],
        )
        card.pack(fill="both", expand=True, padx=28, pady=(20, 8))

        # Card header
        card_header = ctk.CTkFrame(card, fg_color="transparent")
        card_header.pack(fill="x", padx=20, pady=(18, 12))
        ctk.CTkLabel(
            card_header,
            text="Pending leave requests from your classes",
            font=("Georgia", 16, "bold"), text_color=COLORS["text"],
        ).pack(side="left")

        # Configure ttk style for the treeview
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Teacher.Treeview",
            background=_T["card"],
            foreground=COLORS["text"],
            fieldbackground=_T["card"],
            rowheight=36,
            font=("Segoe UI", 11),
            borderwidth=0,
        )
        style.configure(
            "Teacher.Treeview.Heading",
            background=_T["header_bg"],
            foreground=COLORS["text"],
            font=("Segoe UI", 11, "bold"),
            borderwidth=0,
            relief="flat",
        )
        style.map(
            "Teacher.Treeview",
            background=[("selected", "#D4E6D9")],
            foreground=[("selected", COLORS["text"])],
        )
        style.map(
            "Teacher.Treeview.Heading",
            background=[("active", _T["divider"])],
        )

        columns = ("id", "roll_no", "name", "from_date", "to_date", "reason")
        table = ttk.Treeview(
            card, columns=columns, show="headings",
            selectmode="browse", style="Teacher.Treeview",
        )
        for column, label, width in zip(
            columns,
            ("ID", "Roll No.", "Student", "From", "To", "Reason"),
            (50, 100, 180, 110, 110, 240),
        ):
            table.heading(column, text=label)
            table.column(column, width=width, anchor="w")

        # Alternating row colours via tags
        table.tag_configure("odd", background=_T["row_alt"])
        table.tag_configure("even", background=_T["card"])

        scroll = ttk.Scrollbar(card, orient="vertical", command=table.yview)
        table.configure(yscrollcommand=scroll.set)
        table.pack(side="left", fill="both", expand=True, padx=(14, 0), pady=(0, 14))
        scroll.pack(side="right", fill="y", padx=(0, 14), pady=(0, 14))

        try:
            for i, leave in enumerate(attendance_service.pending_leave_requests(self.user.id)):
                tag = "odd" if i % 2 == 0 else "even"
                table.insert(
                    "", "end",
                    values=[leave[col] for col in columns],
                    tags=(tag,),
                )
        except attendance_service.AttendanceServiceError as error:
            self._show_status(str(error), is_error=True)

        # Actions
        actions = ctk.CTkFrame(self.content, fg_color="transparent")
        actions.pack(fill="x", padx=28, pady=(4, 16))

        ctk.CTkButton(
            actions, text="Reject",
            command=lambda: decide("Rejected"),
            fg_color="transparent", hover_color=_T["tag_red_bg"],
            border_width=1, border_color=_T["stat_red"],
            text_color=_T["stat_red"],
            height=38, corner_radius=8, font=("Segoe UI", 12),
        ).pack(side="right", padx=(8, 0))
        ctk.CTkButton(
            actions, text="Approve",
            command=lambda: decide("Approved"),
            fg_color=COLORS["primary"], hover_color=COLORS["primary_dark"],
            height=38, corner_radius=8, font=("Segoe UI", 12, "bold"),
        ).pack(side="right")

        def decide(decision):
            selected = table.selection()
            if not selected:
                self._show_status("Select one leave request first.", is_error=True)
                return
            try:
                leave_id = int(table.item(selected[0], "values")[0])
                attendance_service.decide_leave_request(self.user.id, leave_id, decision)
                self._show_status(f"Leave request {decision.lower()}.")
                self.show_leaves()
            except attendance_service.AttendanceServiceError as error:
                self._show_status(str(error), is_error=True)

    # ------------------------------------------------------------------
    # REPORTS
    # ------------------------------------------------------------------

    def show_reports(self):
        from ui.report_window import open_report_window
        open_report_window(self, self.user)
