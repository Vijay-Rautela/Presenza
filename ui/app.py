"""Application coordinator: it switches screens without mixing in SQL rules."""

import customtkinter as ctk

from config import APP_NAME, COLORS
from services.auth_service import AuthenticatedUser
from ui.activate_view import ActivateView
from ui.dashboard_view import DashboardView
from ui.login_view import LoginView


class PresenzaApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("green")
        self.title(APP_NAME + " | Attendance Management")
        self.geometry("1080x680")
        self.minsize(900, 600)
        self.configure(fg_color=COLORS["background"])
        self.current_view = None
        self.show_login()

    def _replace_view(self, view):
        if self.current_view is not None:
            self.current_view.destroy()
        self.current_view = view

    def show_login(self):
        self._replace_view(LoginView(self, self.route_after_login, self.show_activation))

    def show_activation(self):
        self._replace_view(ActivateView(self, self.show_login))

    def route_after_login(self, user: AuthenticatedUser):
        if user.must_change_password:
            self.show_password_change(user)
            return
        if user.role == "Admin":
            from ui.admin.portal import AdminPortalView
            self._replace_view(AdminPortalView(self, user, self.show_login))
            return
        if user.role == "Teacher":
            from ui.teacher.portal import TeacherPortalView
            self._replace_view(TeacherPortalView(self, user, self.show_login))
            return
        if user.role == "Student":
            from ui.student.portal import StudentPortalView
            self._replace_view(StudentPortalView(self, user, self.show_login))
            return
        self._replace_view(DashboardView(self, user, self.show_login))

    def show_password_change(self, user: AuthenticatedUser):
        from services.auth_service import AuthenticationError, change_password

        frame = ctk.CTkFrame(self, fg_color=COLORS["background"], corner_radius=0)
        self._replace_view(frame)
        frame.pack(fill="both", expand=True)
        card = ctk.CTkFrame(frame, width=430, fg_color=COLORS["surface"], corner_radius=12, border_width=1, border_color=COLORS["border"])
        card.place(relx=0.5, rely=0.5, anchor="center")
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(padx=38, pady=38)
        ctk.CTkLabel(content, text="Create a new admin password", font=("Georgia", 23, "bold"), text_color=COLORS["text"]).pack(anchor="w")
        ctk.CTkLabel(content, text="Your default password must be replaced before continuing.", wraplength=330, justify="left", text_color=COLORS["muted"]).pack(anchor="w", pady=(6, 20))
        password = ctk.CTkEntry(content, show="•", width=350, height=40, placeholder_text="New password")
        password.pack(pady=(0, 12))
        confirm = ctk.CTkEntry(content, show="•", width=350, height=40, placeholder_text="Confirm new password")
        confirm.pack(pady=(0, 12))
        message = ctk.CTkLabel(content, text="", width=350, wraplength=350, justify="left")
        message.pack(anchor="w", pady=(0, 10))

        def save_password():
            try:
                change_password(user.id, password.get(), confirm.get())
                user_after_change = AuthenticatedUser(user.id, user.login_id, user.role, user.display_name, False)
                self.route_after_login(user_after_change)
            except AuthenticationError as error:
                message.configure(text=str(error), text_color="#8B2D1A")

        ctk.CTkButton(content, text="Save password", command=save_password, width=350, height=42, fg_color=COLORS["primary"], hover_color=COLORS["primary_dark"]).pack()
