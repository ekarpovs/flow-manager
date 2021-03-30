from tkinter import *
from .buttonsframe import ButtonsFrame
from .contentframe import ContentFrame

class MainWindow():
  def __init__(self, root):
    self.root = root

    # root.rowconfigure(0, weight=1)
    # root.rowconfigure(1, weight=1)

    self.content_frame = ContentFrame(self.root)
    self.content_frame['height'] = 1100
    self.content_frame.grid(row=0, column=0, padx=10, pady=10, sticky=E+W+N+S)

    self.buttons_frame = ButtonsFrame(self.root)
    self.buttons_frame.grid(row=1, column=0, padx=10, pady=10, sticky=E+W+S)

