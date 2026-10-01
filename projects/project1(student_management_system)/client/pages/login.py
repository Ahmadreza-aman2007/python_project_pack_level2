import sys
import tkinter
from pathlib import Path
import customtkinter


sys.path.append(str(Path(__file__).parent.parent))
import common_tools
import services.auth


class LoginPage:
    def __init__(self, window: tkinter.Tk, pg_changer: common_tools.PageChanger):
        self.window = window
        self.frame = tkinter.Frame(window, bg="#c4c4c4")
        self.frame.pack(fill="both", expand=True)
        self.create_widgets()
        self.page_changer = pg_changer


    def create_label(
        self,
        master: tkinter.Frame | customtkinter.CTkFrame,
        color: str,
        font_size: int,
        text: str,
    ):
        tkinter.Label(
            master,
            text=common_tools.use_persian(text),
            anchor="e",
            bg="#ffffff",
            fg=color,
            font=("DejaVu Sans", font_size),
        ).pack(padx=10, pady=10)

    def create_entry(
        self,
        master: tkinter.Frame | customtkinter.CTkFrame,
        color: str,
        text: str,
    ) -> customtkinter.CTkEntry:
        entry = customtkinter.CTkEntry(
            master,
            text_color=color,
            corner_radius=10,
            fg_color="#c4c4c4",
            width=300,
            placeholder_text=common_tools.use_persian(text),
            border_color="#603cff",
            border_width=2,
            height=40,
            justify="right",
        )
        entry.pack(padx=20, pady=20)
        return entry

    def create_widgets(self):
        center_frame = customtkinter.CTkFrame(
            self.frame, fg_color="#ffffff", corner_radius=20
        )
        center_frame.place(
            relx=0.5, rely=0.5, relheight=0.5, relwidth=0.5, anchor="center"
        )
        self.create_label(center_frame, "#220a46", 16, "نام کاربری")
        username_entry = self.create_entry(center_frame, "#220a46", "نام کاربری")
        self.create_label(center_frame, "#220a46", 16, "رمز عبور")
        password_entry = self.create_entry(center_frame, "#220a46", "رمز عبور")
        button_container = customtkinter.CTkFrame(center_frame, fg_color="#ffffff")
        button_container.grid_columnconfigure(0, weight=1)
        button_container.grid_columnconfigure(1, weight=1)
        button_container.pack(pady=(60, 10), fill="x", padx=20)
        login_button = customtkinter.CTkButton(
            button_container,
            text=common_tools.use_persian("ورود"),
            font=("DejaVu Sans", 15),
            height=50,
            fg_color="#603cff",
            command=lambda: self.send_login_request(
                username_entry.get(), password_entry.get()
            ),
        )
        login_button.grid(row=0, column=0, sticky="ns")
        register_button = customtkinter.CTkButton(
            button_container,
            text=common_tools.use_persian("ثبت نام"),
            font=("DejaVu Sans", 15),
            height=50,
            fg_color="#603cff",
            command=self.go_to_registration,
        )
        register_button.grid(row=0, column=1, sticky="ns")
    def go_to_registration(self):
        from pages.registration import RegistrationPage
        self.page_changer.change(RegistrationPage)
    def send_login_request(self, username: str, password: str):
        services.auth.login(username=username, password=password)
