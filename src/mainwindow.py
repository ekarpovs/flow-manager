from tkinter import *
from .buttonsframe import ButtonsFrame
from .contentframe import ContentFrame

class MainWindow():
  def __init__(self, root):
    self.root = root
    self.PADX = 10
    self.PADY = 10
    
    # create all of the main containers
    self.buttons_frame = ButtonsFrame(self.root)

    # Calculate as reminder
    content_height = self.calculate_content_frame_height()

    self.content_frame = ContentFrame(self.root)
    self.content_frame['height'] = content_height

    root.update()
    print("CH", self.content_frame.winfo_reqheight())


    # layout all of the main container
    root.rowconfigure(1, weight=1)
    root.columnconfigure(0, weight=1)

    self.content_frame.grid(row=0, column=0, padx=self.PADX, pady=self.PADY, sticky=E+W)
    self.buttons_frame.grid(row=1, column=0, padx=self.PADX, pady=self.PADY, sticky=E+W)


  def calculate_content_frame_height(self):
    self.root.update()
    root_height = self.root.winfo_height()
    buttons_height = self.buttons_frame.winfo_reqheight()
    return root_height - buttons_height - self.PADY*4


