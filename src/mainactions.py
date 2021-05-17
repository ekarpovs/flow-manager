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

    self.stdout_textbox=ScrolledText(self, height=6, width=105,  wrap=WORD)
    self.stdout_textbox.grid(row=0, column=0, columnspan=2, padx=PADX, pady=PADY, sticky=W+S)

    self.stderr_textbox=ScrolledText(self, height=6, width=105,  wrap=WORD)
    self.stderr_textbox.grid(row=0, column=2, columnspan=2, padx=PADX, pady=PADY, sticky=W+S)

    bfr = Frame(self)
    bfr.grid(row=0, column=4, padx=PADX, pady=PADY, sticky=E)

    self.btn_clear = Button(bfr, text='Clear', width=BTNW, command=self.clear)
    self.btn_clear.grid(row=0, column=0, padx=PADX, pady=PADY, sticky=E)

    self.btn_exit = Button(bfr, text='Exit', width=BTNW)
    self.btn_exit.grid(row=1, column=0, padx=PADX, pady=PADY, sticky=E)

        
    sys.stdout.write = self.stdout_redirector
    sys.stderr.write = self.stderr_redirector


  def clear(self):
    self.stdout_textbox.delete(1.0, END)
    self.stderr_textbox.delete(1.0, END)

  def stdout_redirector(self, line):
    self.stdout_textbox.insert(END, line)
    self.stdout_textbox.yview(END)

  def stderr_redirector(self, line):
    self.stderr_textbox.insert(END, line)
    self.stderr_textbox.yview(END)
