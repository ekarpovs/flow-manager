from tkinter import *
from tkinter import ttk

from src import MainWindow

if __name__ == '__main__':
  root = Tk()
  root.title("Flow Manager")
  # root.state('zoomed')
  sw = root.winfo_screenwidth ()
  sh = root.winfo_screenheight()
  root.geometry("{}x{}+{}+{}".format(sw-10, sh-70, 0,0))
  root.resizable(0, 0) 

  myapp = MainWindow(root)

  root.mainloop()