import customtkinter, tkinter
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

import common_tools


class RegistrationPage:
    def __init__(self, window: tkinter.Tk):
        self.window = window
        self.window.title("registration")
        self.frame = tkinter.Frame(self.window, bg="#c4c4c4")
        self.frame.pack(fill="both", expand=True)
        self.create_widgets()

    def create_label(
        self,
        master: tkinter.Frame | customtkinter.CTkFrame,
        color: str,
        font_size: int,
        text: str,
        row: int,
        column: int,
    ):
        tkinter.Label(
            master,
            text=common_tools.use_persian(text),
            anchor="e",
            bg="#ffffff",
            fg=color,
            font=("DejaVu Sans", font_size),
        ).grid(row=row, column=column, sticky="ns", pady=10)

    def create_entry(
        self,
        master: tkinter.Frame | customtkinter.CTkFrame,
        color: str,
        text: str,
        row: int,
        column: int,
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
        entry.grid(row=row, column=column, pady=10)
        return entry

    def create_widgets(self):
        center_frame = customtkinter.CTkFrame(
            self.frame, fg_color="#ffffff", corner_radius=20
        )
        center_frame.place(
            relx=0.5, rely=0.5, relwidth=0.5, relheight=0.5, anchor="center"
        )
        container = tkinter.Frame(center_frame, bg="#ffffff")
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=1)
        container.pack(fill="x", padx=20, pady=(60, 30))
        self.create_label(container, "#220a46", 16, "نام", 0, 1)
        firstname_entry = self.create_entry(container, "#220a46", "نام", 0, 0)
        self.create_label(container, "#220a46", 16, "نام خانوادگی", 1, 1)
        lastname_entry=self.create_entry(container,"#220a46","نام خانوادگی",1,0)
        self.create_label(container, "#220a46", 16, "کدملی", 2, 1)
        national_code_entry =self.create_entry(container,"#220a46","کدملی",2,0)
        submit_button = customtkinter.CTkButton(
            center_frame,
            height=60,
            corner_radius=10,
            text=common_tools.use_persian("ثبت درخواست"),
            font=("DejaVu Sans", 16),
            fg_color="#603cff",
        )
        submit_button.pack(anchor="center", pady=(60, 10))



if __name__ == "__main__":
    window = tkinter.Tk()
    window.attributes("-zoomed",True)
    window.minsize(1000,750)
    registration_page=RegistrationPage(window)
    window.mainloop()

