"""Shared report window for Admin and Teacher scopes."""

from tkinter import filedialog, ttk

import customtkinter as ctk

from config import COLORS
from reports.charts import subject_attendance_chart
from services import report_service


def open_report_window(parent, user):
    window = ctk.CTkToplevel(parent); window.title("Presenza reports"); window.geometry("900x620"); window.configure(fg_color=COLORS["background"])
    ctk.CTkLabel(window, text="Attendance reports", font=("Georgia", 25, "bold"), text_color=COLORS["text"]).pack(anchor="w", padx=28, pady=(24, 2))
    ctk.CTkLabel(window, text="Reports are limited to your permitted data scope.", text_color=COLORS["muted"]).pack(anchor="w", padx=28, pady=(0, 14))
    controls = ctk.CTkFrame(window, fg_color="transparent"); controls.pack(fill="x", padx=28)
    selection = ctk.StringVar(value="Student-wise")
    ctk.CTkOptionMenu(controls, values=["Student-wise", "Subject-wise", "Monthly", "Defaulters"], variable=selection, width=180, fg_color=COLORS["primary"]).pack(side="left")
    message = ctk.CTkLabel(window, text="", wraplength=800, justify="left"); message.pack(anchor="w", padx=28, pady=(8, 0))
    table_box = ctk.CTkFrame(window, fg_color=COLORS["surface"], corner_radius=9); table_box.pack(fill="both", expand=True, padx=28, pady=8)
    table = ttk.Treeview(table_box, show="headings"); table.pack(fill="both", expand=True, padx=10, pady=10)
    current_rows = []
    def render():
        nonlocal current_rows
        try:
            report_type = selection.get()
            functions = {"Student-wise": report_service.student_report, "Subject-wise": report_service.subject_report, "Monthly": report_service.monthly_report, "Defaulters": report_service.defaulter_report}
            current_rows = functions[report_type](user.role, user.id)
            columns = list(current_rows[0]) if current_rows else ["message"]
            table.configure(columns=columns)
            for column in columns: table.heading(column, text=column.replace("_", " ").title()); table.column(column, width=130)
            table.delete(*table.get_children())
            for row in current_rows: table.insert("", "end", values=[row[column] for column in columns])
            message.configure(text=f"{len(current_rows)} row(s) loaded.", text_color=COLORS["primary"])
        except report_service.ReportServiceError as error: message.configure(text=str(error), text_color="#8B2D1A")
    def export():
        if not current_rows: message.configure(text="Load a report before exporting.", text_color="#8B2D1A"); return
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
        if not path: return
        try: message.configure(text=f"Saved CSV: {report_service.export_csv(current_rows, path)}", text_color=COLORS["primary"])
        except report_service.ReportServiceError as error: message.configure(text=str(error), text_color="#8B2D1A")
    def chart():
        try:
            rows = report_service.subject_report(user.role, user.id)
            message.configure(text=f"Chart created: {subject_attendance_chart(rows)}", text_color=COLORS["primary"])
        except (report_service.ReportServiceError, ValueError, ImportError) as error: message.configure(text=f"Could not create chart: {error}", text_color="#8B2D1A")
    ctk.CTkButton(controls, text="Load report", command=render, fg_color=COLORS["primary"]).pack(side="left", padx=8)
    ctk.CTkButton(controls, text="Export CSV", command=export, fg_color="transparent", border_width=1, border_color=COLORS["primary"], text_color=COLORS["primary"]).pack(side="left")
    ctk.CTkButton(controls, text="Subject chart", command=chart, fg_color="transparent", border_width=1, border_color=COLORS["primary"], text_color=COLORS["primary"]).pack(side="left", padx=8)
