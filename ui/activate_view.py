"""One-time account activation screen."""

import customtkinter as ctk

from config import COLORS
from services.auth_service import AuthenticationError, activate_account


class ActivateView(ctk.CTkFrame):
    def __init__(self, master, on_back):
        super().__init__(master, fg_color=COLORS["background"], corner_radius=0)
        self.on_back = on_back
        self._build()

    def _build(self):
        self.pack(fill="both", expand=True)
        card = ctk.CTkFrame(self, width=460, fg_color=COLORS["surface"], corner_radius=12, border_width=1, border_color=COLORS["border"])
        card.place(relx=0.5, rely=0.5, anchor="center")
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(padx=42, pady=38)
        ctk.CTkLabel(content, text="Activate your account", font=("Georgia", 25, "bold"), text_color=COLORS["text"]).pack(anchor="w")
        ctk.CTkLabel(content, text="For teachers and students. Use the date of birth saved by the admin.", wraplength=360, justify="left", text_color=COLORS["muted"]).pack(anchor="w", pady=(6, 20))
        self.entries = {}
        for label, key, secret in (("Login ID", "login_id", False), ("Date of birth (YYYY-MM-DD)", "dob", False), ("New password", "password", True), ("Confirm password", "confirm", True)):
            ctk.CTkLabel(content, text=label, text_color=COLORS["text"]).pack(anchor="w")
            entry = ctk.CTkEntry(content, width=360, height=39, show="•" if secret else "", fg_color=COLORS["background"], border_color=COLORS["border"])
            entry.pack(pady=(5, 12))
            self.entries[key] = entry
        self.message = ctk.CTkLabel(content, text="", width=360, wraplength=360, justify="left")
        self.message.pack(anchor="w", pady=(0, 10))
        ctk.CTkButton(content, text="Activate account", command=self._activate, width=360, height=42, fg_color=COLORS["primary"], hover_color=COLORS["primary_dark"]).pack()
        ctk.CTkButton(content, text="Back to sign in", command=self.on_back, width=360, height=38, fg_color="transparent", hover_color=COLORS["cove"], text_color=COLORS["primary"]).pack(pady=(8, 0))
        self.entries["login_id"].focus()

    def _activate(self):
        try:
            activate_account(*(self.entries[key].get() for key in ("login_id", "dob", "password", "confirm")))
            self.message.configure(text="Account activated. You can now sign in.", text_color=COLORS["primary"])
        except AuthenticationError as error:
            self.message.configure(text=str(error), text_color="#8B2D1A")
