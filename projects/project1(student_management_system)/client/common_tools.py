import tkinter

import arabic_reshaper
from bidi.algorithm import get_display


def use_persian(text: str):
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)


class PageChanger:
    def __init__(self, window: tkinter.Tk):
        self.page = None
        self.window = window

    def change(self, cls: object):
        if self.page is not None:
            self.page.frame.destroy()
        new_page = cls(self.window, self)
        self.page = new_page
