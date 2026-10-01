import tkinter

import common_tools
from pages import login


def main():
    window = tkinter.Tk()
    window.minsize(1000, 750)
    window.attributes("-zoomed", True)
    pg_changer = common_tools.PageChanger(window=window)
    pg_changer.change(login.LoginPage)
    window.mainloop()


if __name__ == "__main__":
    main()
