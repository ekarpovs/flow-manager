from tkinter import *
from tkinter.scrolledtext import *

from tkinter import ttk
import sys
from .uiconst import *

class MainActions(Frame):
  def __init__(self, parent):
    super().__init__(parent)
    self.parent = parent 

    self["bg"] = "green"

    self.grid()
    self.columnconfigure(0, weight=1)
    self.columnconfigure(1, weight=1)
    self.columnconfigure(2, weight=1)
    self.columnconfigure(3, weight=1)
    self.columnconfigure(4, weight=1)

    stdout_textbox=ScrolledText(self, height=6, width=105,  wrap=WORD)
    stdout_textbox.grid(row=0, column=0, columnspan=2, padx=PADX, pady=PADY, sticky=W+S)

    stderr_textbox=ScrolledText(self, height=6, width=105,  wrap=WORD)
    stderr_textbox.grid(row=0, column=2, columnspan=2, padx=PADX, pady=PADY, sticky=W+S)

    self.btn_exit = Button(self, text='Exit', width=BTNW)
    self.btn_exit.grid(row=0, column=4, padx=PADX, pady=PADY, sticky=E)

    def stdout_redirector(line):
      stdout_textbox.insert(END, line)
      stdout_textbox.yview(END)

    def stderr_redirector(line):
      stderr_textbox.insert(END, line)
      stderr_textbox.yview(END)
        

    sys.stdout.write = stdout_redirector
    sys.stderr.write = stderr_redirector
