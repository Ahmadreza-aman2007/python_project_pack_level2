import arabic_reshaper
from bidi.algorithm import get_display
import tkinter

def use_persian(text: str):
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)
def change_page(window:tkinter.Tk):
    pass