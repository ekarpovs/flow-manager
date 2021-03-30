from tkinter import *
from tkinter import ttk

class ContentFrame(Frame):
  def __init__(self, parent):
    super().__init__(parent) 
    self['bd'] = 2
    self['relief'] = RIDGE 

