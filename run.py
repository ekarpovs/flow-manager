from tkinter import *
from tkinter import font
from tkinter import ttk

from src import MainWindow

if __name__ == '__main__':
  root = Tk()

  root.title("Flow Manager")
  root.iconbitmap()
  # Creating a Font object of "TkDefaultFont"
  default_font = font.nametofont("TkDefaultFont")
  # Overriding default-font with custom settings
  default_font.configure(size=11)
  root.option_add('*TCombobox*Listbox.font', default_font)
  myapp = MainWindow(root)

  root.mainloop()