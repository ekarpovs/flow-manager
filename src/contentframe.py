from tkinter import *
from tkinter import ttk

class ContentFrame(LabelFrame):
  def __init__(self, parent):
    super().__init__(parent) 
    self['text'] = 'Content'

