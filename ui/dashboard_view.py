"""Temporary role shells that enforce routing until each portal is built."""

import customtkinter as ctk

from config import COLORS


ROLE_MESSAGES = {
    "Admin": "The Admin workspace is reserved for Phase 3: master data, imports, assignments, and settings.",
    "Teacher": "The Teacher workspace is reserved for Phase 4: attendance marking, corrections, and leave approval.",
    "Student": "The Student workspace is reserved for Phase 5: personal attendance records and leave applications.",
}


class DashboardView(ctk.CTkFrame):
    def __init__(self, master, user, on_logout):
        super().__init__(master, fg_color=COLORS["background"], corner_radius=0)
        self.user = user
        self.on_logout = on_logout
        self._build()

    def _build(self):
        self.pack(fill="both", expand=True)
        header = ctk.CTkFrame(self, height=78, fg_color=COLORS["primary"], corner_radius=0)
        header.pack(fill="x")
        ctk.CTkLabel(header, text="Presenza", font=("Georgia", 25, "bold"), text_color=COLORS["surface"]).pack(side="left", padx=34, pady=20)
        ctk.CTkButton(header, text="Sign out", command=self.on_logout, width=100, fg_color="transparent", hover_color=COLORS["primary_dark"], border_width=1, border_color=COLORS["cove"]).pack(side="right", padx=30, pady=19)
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=52, pady=58)
        ctk.CTkLabel(content, text=f"Hello, {self.user.display_name}", font=("Georgia", 29, "bold"), text_color=COLORS["text"]).pack(anchor="w")
        ctk.CTkLabel(content, text=f"{self.user.role} portal", font=("Segoe UI", 14, "bold"), text_color=COLORS["accent"]).pack(anchor="w", pady=(6, 28))
        notice = ctk.CTkFrame(content, fg_color=COLORS["surface"], corner_radius=10, border_width=1, border_color=COLORS["border"])
        notice.pack(anchor="w", fill="x")
        ctk.CTkLabel(notice, text="Access verified", font=("Segoe UI", 17, "bold"), text_color=COLORS["primary"]).pack(anchor="w", padx=25, pady=(22, 6))
        ctk.CTkLabel(notice, text=ROLE_MESSAGES[self.user.role], justify="left", wraplength=700, font=("Segoe UI", 14), text_color=COLORS["muted"]).pack(anchor="w", padx=25, pady=(0, 22))
