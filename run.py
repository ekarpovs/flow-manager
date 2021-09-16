from tkinter import *
from tkinter import font
from tkinter import ttk

from src import MainWindow

if __name__ == '__main__':
  root = Tk()

  # # Creating a Font object of "TkDefaultFont"
  # root.defaultFont = font.nametofont("TkDefaultFont")
  # # Overriding default-font with custom settings
  # # i.e changing font-family, size and weight
  # root.defaultFont.configure(size=12)

  root.title("Flow Manager")
  root.iconbitmap()
  # root.state('zoomed')
  sw = root.winfo_screenwidth ()
  sh = root.winfo_screenheight()
  root.geometry("{}x{}+{}+{}".format(sw-10, sh-70, 0,0))
  root.resizable(0, 0) 
  default_font = font.nametofont("TkDefaultFont")
  default_font.configure(size=11)
  root.option_add('*TCombobox*Listbox.font', default_font)
  myapp = MainWindow(root)

  root.mainloop()