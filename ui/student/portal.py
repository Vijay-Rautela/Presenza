"""Student workspace for private attendance viewing and leave applications."""

from datetime import date
from tkinter import ttk

import customtkinter as ctk

from config import COLORS
from services import student_service


class StudentPortalView(ctk.CTkFrame):
    def __init__(self, master, user, on_logout):
        super().__init__(master, fg_color=COLORS["background"], corner_radius=0)
        self.user = user
        self.on_logout = on_logout
        self._shell(); self.show_page("Dashboard")

    def _shell(self):
        self.pack(fill="both", expand=True)
        side = ctk.CTkFrame(self, width=220, fg_color=COLORS.get("sidebar", "#0D2E1F"), corner_radius=0); side.pack(side="left", fill="y"); side.pack_propagate(False)
        ctk.CTkLabel(side, text="Presenza", font=("Georgia", 25, "bold"), text_color=COLORS["surface"]).pack(anchor="w", padx=27, pady=(30, 8))
        ctk.CTkLabel(side, text="STUDENT WORKSPACE", font=("Segoe UI", 11, "bold"), text_color="#A3E6C2").pack(anchor="w", padx=29, pady=(0, 28))
        for page in ("Dashboard", "My records", "Apply for leave"):
            ctk.CTkButton(side, text=page, anchor="w", command=lambda value=page: self.show_page(value), fg_color="transparent", hover_color=COLORS.get("sidebar_hover", "#174D34"), height=39).pack(fill="x", padx=14, pady=2)
        ctk.CTkButton(side, text="Sign out", command=self.on_logout, fg_color="transparent", hover_color=COLORS.get("sidebar_hover", "#174D34"), border_width=1, border_color="#1E5E3D").pack(side="bottom", fill="x", padx=18, pady=24)
        self.content = ctk.CTkFrame(self, fg_color=COLORS["background"], corner_radius=0); self.content.pack(side="left", fill="both", expand=True)

    def _clear(self):
        for child in self.content.winfo_children(): child.destroy()

    def _title(self, title, subtitle):
        ctk.CTkLabel(self.content, text=title, font=("Georgia", 27, "bold"), text_color=COLORS["text"]).pack(anchor="w", padx=34, pady=(28, 2))
        ctk.CTkLabel(self.content, text=subtitle, font=("Segoe UI", 13), text_color=COLORS["muted"]).pack(anchor="w", padx=34, pady=(0, 16))

    def show_page(self, page):
        if page == "Dashboard": self.show_dashboard()
        elif page == "My records": self.show_records()
        else: self.show_leave_form()

    def show_dashboard(self):
        self._clear(); self._title(f"Hello, {self.user.display_name}", "Your attendance overview is private to your account.")
        try: data = student_service.dashboard_data(self.user.id)
        except student_service.StudentServiceError as error: self._message(str(error), True); return
        cards = ctk.CTkFrame(self.content, fg_color="transparent"); cards.pack(fill="x", padx=34)
        for label, value in (("Overall attendance", f"{data['percentage']}%"), ("Classes attended", f"{data['present']} / {data['total']}"), ("Required minimum", f"{data['minimum']}%")):
            card = ctk.CTkFrame(cards, fg_color=COLORS["surface"], corner_radius=10, border_width=1, border_color=COLORS["border"]); card.pack(side="left", fill="x", expand=True, padx=5)
            ctk.CTkLabel(card, text=value, font=("Georgia", 25, "bold"), text_color=COLORS["primary"]).pack(anchor="w", padx=18, pady=(18, 3))
            ctk.CTkLabel(card, text=label, text_color=COLORS["muted"]).pack(anchor="w", padx=18, pady=(0, 18))
        if data["total"] and data["percentage"] < data["minimum"]:
            ctk.CTkLabel(self.content, text="Attendance warning: your overall percentage is below the required minimum.", text_color="#8B2D1A", font=("Segoe UI", 13, "bold")).pack(anchor="w", padx=39, pady=18)
        elif not data["total"]:
            ctk.CTkLabel(self.content, text="No attendance has been marked for you yet.", text_color=COLORS["muted"]).pack(anchor="w", padx=39, pady=18)
        self._subject_table(data["subjects"])

    def _subject_table(self, subjects):
        box = ctk.CTkFrame(self.content, fg_color=COLORS["surface"], corner_radius=10, border_width=1, border_color=COLORS["border"]); box.pack(fill="both", expand=True, padx=34, pady=(2, 24))
        ctk.CTkLabel(box, text="Subject-wise attendance", font=("Segoe UI", 16, "bold"), text_color=COLORS["text"]).pack(anchor="w", padx=20, pady=(16, 6))
        table = ttk.Treeview(box, columns=("code", "subject", "attended", "percentage"), show="headings")
        for col, label in zip(("code", "subject", "attended", "percentage"), ("Code", "Subject", "Attended", "Percentage")):
            table.heading(col, text=label); table.column(col, width=150)
        for item in subjects: table.insert("", "end", values=(item["code"], item["name"], f"{item['present']} / {item['total']}", f"{item['percentage']}%"))
        table.pack(fill="both", expand=True, padx=12, pady=(0, 14))

    def show_records(self):
        self._clear(); self._title("My attendance records", "Date-wise records for your account only.")
        box = ctk.CTkFrame(self.content, fg_color=COLORS["surface"], corner_radius=10); box.pack(fill="both", expand=True, padx=34, pady=8)
        table = ttk.Treeview(box, columns=("date", "code", "subject", "status"), show="headings")
        for col, label in zip(("date", "code", "subject", "status"), ("Date", "Subject code", "Subject", "Status")):
            table.heading(col, text=label); table.column(col, width=160)
        try:
            for record in student_service.attendance_records(self.user.id): table.insert("", "end", values=[record[col] for col in ("date", "code", "subject", "status")])
        except student_service.StudentServiceError as error: self._message(str(error), True)
        table.pack(fill="both", expand=True, padx=12, pady=12)

    def show_leave_form(self):
        self._clear(); self._title("Apply for leave", "Your request will remain Pending until a Teacher or Admin makes a decision.")
        form = ctk.CTkFrame(self.content, fg_color=COLORS["surface"], corner_radius=10, border_width=1, border_color=COLORS["border"]); form.pack(fill="x", padx=34, pady=8)
        ctk.CTkLabel(form, text="From date (YYYY-MM-DD)", text_color=COLORS["text"]).pack(anchor="w", padx=24, pady=(20, 4)); start = ctk.CTkEntry(form, width=250); start.insert(0, date.today().isoformat()); start.pack(anchor="w", padx=24, pady=(0, 10))
        ctk.CTkLabel(form, text="To date (YYYY-MM-DD)", text_color=COLORS["text"]).pack(anchor="w", padx=24, pady=(0, 4)); end = ctk.CTkEntry(form, width=250); end.insert(0, date.today().isoformat()); end.pack(anchor="w", padx=24, pady=(0, 10))
        ctk.CTkLabel(form, text="Reason", text_color=COLORS["text"]).pack(anchor="w", padx=24, pady=(0, 4)); reason = ctk.CTkTextbox(form, width=500, height=75); reason.pack(anchor="w", padx=24, pady=(0, 10))
        message = ctk.CTkLabel(form, text="", wraplength=540, justify="left"); message.pack(anchor="w", padx=24)
        def submit():
            try:
                student_service.apply_leave(self.user.id, start.get(), end.get(), reason.get("1.0", "end")); message.configure(text="Leave request submitted successfully.", text_color=COLORS["primary"]); self._leave_history()
            except student_service.StudentServiceError as error: message.configure(text=str(error), text_color="#8B2D1A")
        ctk.CTkButton(form, text="Submit leave request", command=submit, fg_color=COLORS["primary"], hover_color=COLORS["primary_dark"]).pack(anchor="w", padx=24, pady=(4, 22))
        self.history_box = ctk.CTkFrame(self.content, fg_color="transparent"); self.history_box.pack(fill="both", expand=True, padx=34, pady=12); self._leave_history()

    def _leave_history(self):
        if not hasattr(self, "history_box"): return
        for child in self.history_box.winfo_children(): child.destroy()
        ctk.CTkLabel(self.history_box, text="My leave request status", font=("Segoe UI", 16, "bold"), text_color=COLORS["text"]).pack(anchor="w")
        table = ttk.Treeview(self.history_box, columns=("from", "to", "reason", "status"), show="headings")
        for col, label in zip(("from", "to", "reason", "status"), ("From", "To", "Reason", "Status")):
            table.heading(col, text=label); table.column(col, width=150)
        try:
            for item in student_service.leave_history(self.user.id): table.insert("", "end", values=(item["from_date"], item["to_date"], item["reason"], item["status"]))
        except student_service.StudentServiceError as error: self._message(str(error), True)
        table.pack(fill="both", expand=True, pady=(6, 0))

    def _message(self, text, error=False):
        ctk.CTkLabel(self.content, text=text, text_color="#8B2D1A" if error else COLORS["primary"], wraplength=700).pack(anchor="w", padx=34, pady=12)
