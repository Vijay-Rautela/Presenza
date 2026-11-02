"""Login screen matching the modern Attendance System design with rich emerald palette."""

from pathlib import Path
from tkinter import messagebox

import customtkinter as ctk
from PIL import Image

from config import APP_NAME, COLORS, PROJECT_ROOT
from services.auth_service import AuthenticationError, login

REMEMBER_FILE = PROJECT_ROOT / "database" / ".remember_me"


def _load_remembered_id() -> str:
    try:
        if REMEMBER_FILE.exists():
            return REMEMBER_FILE.read_text(encoding="utf-8").strip()
    except Exception:
        pass
    return ""


def _save_remembered_id(login_id: str, remember: bool) -> None:
    try:
        if remember and login_id.strip():
            REMEMBER_FILE.parent.mkdir(parents=True, exist_ok=True)
            REMEMBER_FILE.write_text(login_id.strip(), encoding="utf-8")
        elif REMEMBER_FILE.exists():
            REMEMBER_FILE.unlink(missing_ok=True)
    except Exception:
        pass


class LoginView(ctk.CTkFrame):
    def __init__(self, master, on_login, on_activate):
        super().__init__(master, fg_color=COLORS.get("background", "#F7F5EA"), corner_radius=0)
        self.on_login = on_login
        self.on_activate = on_activate

        saved_id = _load_remembered_id()
        self.login_id = ctk.StringVar(value=saved_id)
        self.password = ctk.StringVar()
        self.remember_var = ctk.BooleanVar(value=bool(saved_id))
        self.show_password = False

        self._build()

    def _build(self):
        self.pack(fill="both", expand=True)

        # -------------------------------------------------------------
        # LEFT PANEL: Deep Tech Emerald Brand Showcase
        # -------------------------------------------------------------
        brand_bg = "#0F3526"
        brand = ctk.CTkFrame(self, width=440, fg_color=brand_bg, corner_radius=0)
        brand.pack(side="left", fill="y")
        brand.pack_propagate(False)

        # Subtle luminous neon green vertical divider on right edge
        glow_divider = ctk.CTkFrame(self, width=2, fg_color="#2ECC71", corner_radius=0)
        glow_divider.pack(side="left", fill="y")

        # Brand Logo Header: Green box with "PZ" in orange-beige + "Presenza"
        logo_frame = ctk.CTkFrame(brand, fg_color="transparent")
        logo_frame.pack(anchor="w", padx=46, pady=(45, 18))

        logo_path = PROJECT_ROOT / "ui" / "pz_box_logo.png"
        if logo_path.exists():
            try:
                pz_pil = Image.open(logo_path)
                self.pz_logo_img = ctk.CTkImage(light_image=pz_pil, dark_image=pz_pil, size=(46, 46))
                ctk.CTkLabel(logo_frame, image=self.pz_logo_img, text="").pack(side="left", padx=(0, 14))
            except Exception:
                self._fallback_pz_box(logo_frame)
        else:
            self._fallback_pz_box(logo_frame)

        text_col = ctk.CTkFrame(logo_frame, fg_color="transparent")
        text_col.pack(side="left", fill="y")

        ctk.CTkLabel(
            text_col,
            text="Presenza",
            font=("Segoe UI", 24, "bold"),
            text_color="#FFFFFF",
        ).pack(anchor="w")

        ctk.CTkLabel(
            text_col,
            text="SECURE ACCESS",
            font=("Segoe UI", 10, "bold"),
            text_color="#A3E6C2",
        ).pack(anchor="w")

        # Headline
        ctk.CTkLabel(
            brand,
            text="WELCOME BACK",
            font=("Segoe UI", 27, "bold"),
            text_color="#FFFFFF",
        ).pack(anchor="w", padx=46, pady=(10, 8))

        # Subtitle
        ctk.CTkLabel(
            brand,
            text="Please log in to your account to manage attendance, track performance, and streamline records.",
            justify="left",
            wraplength=340,
            font=("Segoe UI", 13),
            text_color="#B6DCBE",
        ).pack(anchor="w", padx=46, pady=(0, 16))

        # Bottom Team Collaboration Artwork
        art_path = PROJECT_ROOT / "ui" / "login_team_art_clean.png"
        if art_path.exists():
            try:
                art_pil = Image.open(art_path)
                self.art_img = ctk.CTkImage(light_image=art_pil, dark_image=art_pil, size=(380, 320))
                art_lbl = ctk.CTkLabel(brand, image=self.art_img, text="")
                art_lbl.pack(side="bottom", anchor="s", fill="x", pady=(0, 34))
            except Exception:
                pass

        # -------------------------------------------------------------
        # RIGHT PANEL: Elegant Off-White Login Container
        # -------------------------------------------------------------
        panel_bg = COLORS.get("background", "#F7F5EA")
        panel = ctk.CTkFrame(self, fg_color=panel_bg, corner_radius=0)
        panel.pack(side="left", fill="both", expand=True)

        # Center Card Container
        center_wrap = ctk.CTkFrame(panel, fg_color="transparent")
        center_wrap.place(relx=0.5, rely=0.5, anchor="center")

        # Portal Title (design spec ~24pt)
        ctk.CTkLabel(
            center_wrap,
            text="LOGIN PORTAL",
            font=("Segoe UI", 24, "bold"),
            text_color="#103825",
        ).pack(anchor="center")

        # Subtitle (design spec ~14pt)
        ctk.CTkLabel(
            center_wrap,
            text="Attendance Management System",
            font=("Segoe UI", 13),
            text_color="#5D7364",
        ).pack(anchor="center", pady=(3, 20))

        # Floating Card
        card = ctk.CTkFrame(
            center_wrap,
            fg_color="#FFFFFF",
            corner_radius=14,
            border_width=1,
            border_color="#D5E2D9",
            width=390,
        )
        card.pack(anchor="center")

        card_content = ctk.CTkFrame(card, fg_color="transparent", width=330)
        card_content.pack(padx=32, pady=28)

        # Field 1: Staff ID / Email
        row1 = ctk.CTkFrame(card_content, fg_color="transparent")
        row1.pack(fill="x", pady=(0, 6))

        # Circle Badge "1"
        ctk.CTkLabel(
            row1,
            text="1",
            width=20,
            height=20,
            corner_radius=10,
            fg_color="#103825",
            text_color="#FFFFFF",
            font=("Segoe UI", 10, "bold"),
        ).pack(side="left", padx=(0, 8))

        ctk.CTkLabel(
            row1,
            text="Staff ID / Email",
            font=("Segoe UI", 12, "bold"),
            text_color="#14281E",
        ).pack(side="left")

        # Input Box 1 (Direct CTkEntry with solid complete 4-sided rounded border)
        self.id_entry = ctk.CTkEntry(
            card_content,
            textvariable=self.login_id,
            placeholder_text="👤  e.g., emp12345",
            width=320,
            height=44,
            corner_radius=8,
            border_width=1.5,
            border_color="#1B874B",
            fg_color="#FFFFFF",
            font=("Segoe UI", 13),
            text_color="#14281E",
        )
        self.id_entry.pack(fill="x", pady=(0, 16))

        # Field 2: Password
        row2 = ctk.CTkFrame(card_content, fg_color="transparent")
        row2.pack(fill="x", pady=(0, 6))

        # Circle Badge "2"
        ctk.CTkLabel(
            row2,
            text="2",
            width=20,
            height=20,
            corner_radius=10,
            fg_color="#103825",
            text_color="#FFFFFF",
            font=("Segoe UI", 10, "bold"),
        ).pack(side="left", padx=(0, 8))

        ctk.CTkLabel(
            row2,
            text="Password",
            font=("Segoe UI", 12, "bold"),
            text_color="#14281E",
        ).pack(side="left")

        # Password Entry Row with Eye Toggle Button
        pw_row = ctk.CTkFrame(card_content, fg_color="transparent")
        pw_row.pack(fill="x", pady=(0, 16))

        self.password_entry = ctk.CTkEntry(
            pw_row,
            textvariable=self.password,
            placeholder_text="🔒  Enter Password",
            show="•",
            width=274,
            height=44,
            corner_radius=8,
            border_width=1.5,
            border_color="#CFDDD3",
            fg_color="#FFFFFF",
            font=("Segoe UI", 13),
            text_color="#14281E",
        )
        self.password_entry.pack(side="left", padx=(0, 6))

        self.eye_btn = ctk.CTkButton(
            pw_row,
            text="👁",
            width=40,
            height=44,
            corner_radius=8,
            border_width=1.5,
            border_color="#CFDDD3",
            fg_color="#FFFFFF",
            hover_color="#E8F5EE",
            text_color="#1B874B",
            font=("Segoe UI Emoji", 13),
            command=self._toggle_password,
        )
        self.eye_btn.pack(side="left")

        # Dynamic focus border transitions
        self.id_entry.bind("<FocusIn>", lambda _e: self.id_entry.configure(border_color="#1B874B"))
        self.id_entry.bind("<FocusOut>", lambda _e: self.id_entry.configure(border_color="#CFDDD3"))
        self.password_entry.bind(
            "<FocusIn>",
            lambda _e: (
                self.password_entry.configure(border_color="#1B874B"),
                self.eye_btn.configure(border_color="#1B874B"),
            ),
        )
        self.password_entry.bind(
            "<FocusOut>",
            lambda _e: (
                self.password_entry.configure(border_color="#CFDDD3"),
                self.eye_btn.configure(border_color="#CFDDD3"),
            ),
        )

        # Options Row: Remember Me (Left) & Forgot Password? (Right)
        options_row = ctk.CTkFrame(card_content, fg_color="transparent")
        options_row.pack(fill="x", pady=(0, 16))

        ctk.CTkCheckBox(
            options_row,
            text="Remember Me",
            variable=self.remember_var,
            fg_color="#1B874B",
            hover_color="#136A3B",
            text_color="#33473B",
            font=("Segoe UI", 11),
            checkbox_width=18,
            checkbox_height=18,
            corner_radius=4,
        ).pack(side="left")

        ctk.CTkButton(
            options_row,
            text="Forgot Password?",
            fg_color="transparent",
            hover_color="#F4FAF6",
            text_color="#103825",
            font=("Segoe UI", 11, "underline"),
            command=self.on_activate,
            height=24,
            width=100,
        ).pack(side="right")

        # Submit Action Button (Rich Vivid Emerald Green)
        ctk.CTkButton(
            card_content,
            text="SIGN IN\nSecure Login",
            command=self._submit,
            height=48,
            corner_radius=8,
            font=("Segoe UI", 13, "bold"),
            fg_color="#1B874B",
            hover_color="#136A3B",
        ).pack(fill="x", pady=(0, 8))

        # Error Notice
        self.error_label = ctk.CTkLabel(
            card_content,
            text="",
            wraplength=320,
            justify="center",
            text_color="#DC3545",
            font=("Segoe UI", 11, "bold"),
        )
        self.error_label.pack(fill="x", pady=(0, 6))

        # Bottom Link: Activate Account
        ctk.CTkButton(
            card_content,
            text="First time user? Activate Account",
            fg_color="transparent",
            hover_color="#F4FAF6",
            text_color="#1B874B",
            font=("Segoe UI", 11, "underline"),
            command=self.on_activate,
            height=24,
        ).pack(anchor="center")

        # Keyboard shortcuts
        self.id_entry.focus()
        self.id_entry.bind("<Return>", lambda _event: self._submit())
        self.password_entry.bind("<Return>", lambda _event: self._submit())

    def _fallback_pz_box(self, parent):
        box = ctk.CTkFrame(
            parent,
            width=46,
            height=46,
            corner_radius=10,
            fg_color="#1B874B",
            border_width=1.5,
            border_color="#2ECC71",
        )
        box.pack(side="left", padx=(0, 14))
        box.pack_propagate(False)
        ctk.CTkLabel(
            box,
            text="PZ",
            font=("Segoe UI", 18, "bold"),
            text_color="#FFD3AB",
        ).place(relx=0.5, rely=0.5, anchor="center")

    def _toggle_password(self):
        self.show_password = not self.show_password
        if self.show_password:
            self.password_entry.configure(show="")
            self.eye_btn.configure(text="👁‍🗨")
        else:
            self.password_entry.configure(show="•")
            self.eye_btn.configure(text="👁")

    def _contact_hr(self):
        messagebox.showinfo(
            "HR & System Administration Support",
            "Staff & Student Accounts are provisioned by the Administrator.\n\n"
            "• Helpline: +1 234 567 890\n"
            "• Support Email: support@ams.com\n"
            "• Office: Administrative Block, Presenza Campus\n\n"
            "Note: Newly enrolled teachers and students can activate their accounts "
            "directly using their Staff/Student ID and Date of Birth via 'Activate Account'.",
        )

    def _submit(self):
        self.error_label.configure(text="")
        staff_id = self.login_id.get().strip()
        pwd = self.password.get()

        if not staff_id or not pwd:
            self.error_label.configure(text="Please enter both your Staff ID/Email and Password.")
            return

        try:
            user = login(staff_id, pwd)
            _save_remembered_id(staff_id, self.remember_var.get())
            self.on_login(user)
        except AuthenticationError as error:
            self.error_label.configure(text=str(error))

